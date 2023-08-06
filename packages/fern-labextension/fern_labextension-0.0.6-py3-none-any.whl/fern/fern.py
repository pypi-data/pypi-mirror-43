import ast
import inspect
import logging
import os
import symtable
import sys
import time
import types
import uuid
import zlib

import numpy as np
import pandas as pd
from ipykernel.comm import Comm
from IPython.core.magic import Magics, line_magic, magics_class

import amieci

# default to info logging, even tho it's maybe too chatty
# extensions are pretty magic my themselves
LOG_LEVEL = os.environ.get("FERN_LOGLEVEL", "INFO")
LOG_MSG_FORMAT = "amieci %(levelname)s: %(message)s"
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(LOG_LEVEL)


class OutputCapture(object):
    def __init__(self, **kwargs):
        self.attachments = []

    def __call__(self, msg, **kwargs):
        # The structure of msg is a dict with keys {header, msg_id, msg_type,
        # parent_header, content, metadata} see
        # https://jupyter-client.readthedocs.io/en/stable/messaging.html
        # At present, this only capture pngs, which matplotlib outputs inline
        try:
            self.attachments.append(msg["content"]["data"]["image/png"])
        except:
            pass

        return msg


class ExecutionLog():
    def __init__(self, ip, garden, tree):
        self.shell = ip
        self.leaves = {}
        self.currentLeaf = None
        self.currentHook = None
        self.garden = garden
        self.externalDependencies = set()
        self.tree = tree

    def pre_run_cell(self, info):
        code = info.raw_cell
        # Always generate a new uuid
        leaf_id = str(uuid.uuid4())

        # As we parse the AST, this will fail for syntax errors
        try:
            # Parse code block for inputs, outputs and imports
            variables = CellExecution(code)

            leaf = Leaf(leaf_id)
            self.leaves[leaf_id] = leaf

            # Set currentLeaf, for access after execution
            self.currentLeaf = leaf.id

            leaf.update_leaf_inputs(variables, self.shell.user_ns, self.leaves)

            self.attachRichDisplayCaptureHook()
        except:
            # Error, Jupyter will provide the traceback
            pass

        sys.settrace(self.traceClosure)

    def post_run_cell(self, result):
        sys.settrace(None)
        if result.error_before_exec or result.error_in_exec:
            pass
        else:
            if self.currentLeaf is not None:
                leaf = self.leaves[self.currentLeaf]
                if leaf.code == "":
                    pass
                else:
                    leaf.update_leaf_outputs(self.shell.user_ns)
                    # Add attachments that may have been output from this
                    # cell execution
                    leaf.add_attachments(self.currentHook.attachments)
                    # Add external dependencies, typically these are
                    # imported files (csv, etc)
                    leaf.add_dependencies(self.externalDependencies)
                    # The execution count matches the label on the Jupyter
                    # cell
                    leaf.input_number = result.execution_count
                    # Publish leaf to amie
                    if self.garden is not None:
                        leaf.publish(self.garden, self.tree, self.leaves)
            else:
                # The current leaf has not been set
                pass

            # The cell run cycle is over, unset current leaf
            self.currentLeaf = None
            self.detachRichDisplayCaptureHook()

        # Reset dependencies
        self.externalDependencies = set()

    def attachRichDisplayCaptureHook(self):
        # Create and attach hooks to capture output msg Note that this ONLY
        # captures SOME rich display items. The other output
        # streams are harder to catch, see here for where to find them
        # https://github.com/ipython/ipykernel/issues/113#issuecomment-200897928
        self.currentHook = OutputCapture()
        self.shell.display_pub.register_hook(self.currentHook)

    def detachRichDisplayCaptureHook(self):
        # Unregister output capture hooks
        self.shell.display_pub.unregister_hook(self.currentHook)
        # Unset hook
        self.currentHook = None

    def traceClosure(self, frame, event, arg):
        def tracefunc(frame, event, arg):
            # Supported extensions
            extensions = [
                ".csv", ".txt", ".npz", ".npy", ".png", ".pdf", ".svg"
            ]

            # Capture loaded files
            if 'mode' in frame.f_locals:
                for (k, v) in frame.f_locals.items():
                    if 'path' in k:
                        self.externalDependencies.update(
                            {v
                             for exts in extensions if exts in v})

            return tracefunc

        return tracefunc


@magics_class
class FernMagics(Magics):
    def __init__(self, shell):
        super(FernMagics, self).__init__(shell)
        self.tracking = None
        self.comm_init_tracker = Comm(target_name="init_tracker")
        self.comm_update = Comm(target_name="update_state")
        self.comm_init_tracker.on_msg(self.start_tracking)
        self.garden = None
        self.log = None
        self.comm_update.send(data={
            "extensionLoaded": True,
            "amieConnected": False,
            "tracking": False
        })
        self.comm_update.on_msg(self.heartbeat)

    def heartbeat(self, msg):
        self.comm_update.send(data={
            "extensionLoaded": True,
            "amieConnected": True,
            "tracking": True
        })

    def start_tracking(self, msg):
        ## todo: https://ipywidgets.readthedocs.io/en/stable/examples/Output%20Widget.html
        ## log errors with the above trick
        try:
            self.tracking = msg['content']['data']
            notebookUUID = self.tracking["uuid"]
            notebookName = self.tracking["nb_name"]
            trees = self.garden.trees
            if notebookUUID in trees:
                LOGGER.info("Connected to existing tree in amie")
                # This notebook has a corresponding tree, load it
                self.tree = trees[notebookUUID]
                self.tree.leafHashes = {}
                for (leaf_id, leaf) in self.tree.leaves.items():
                    kvHash = hash(str(leaf.kvs.to_json()))
                    self.tree.leafHashes[kvHash] = leaf_id
            else:
                LOGGER.info(
                    "This notebook has not been tracked by amie yet, creating a new tree with uuid %s",
                    notebookUUID)
                # This is a new notebook, create a new tree
                self.tree = self.garden.new_tree(tree_id=notebookUUID)
                self.tree.set_title(notebookName)
                # The uuids are stored in the description
                self.tree.set_description(notebookUUID)
                self.tree.save()

                # Create an empty mother leaf to ensure that all subbranches
                # are connected to something
                root = self.tree._new_leaf(parent=None)
                root.set_title(notebookName)
                root.set_description("The root of all leaves for notebook " +
                                     notebookName)
                root.save()
            self.log = ExecutionLog(self.shell, self.garden, self.tree)
            self.shell.events.register('pre_run_cell', self.log.pre_run_cell)
            self.shell.events.register('post_run_cell', self.log.post_run_cell)
            self.comm_update.send(data={
                "extensionLoaded": True,
                "amieConnected": True,
                "tracking": True
            })
        except Exception as e:
            self.comm_update.send(data={
                "extensionLoaded": True,
                "amieConnected": False,
                "tracking": True
            })

    # turn on self.tracking to true

    # Note: %track on and %track off must be specified in independent cells for
    # things to work as expected
    @line_magic
    def track(self, parameter_s=''):
        """
        track this(?) notebook using fern and amie
        """
        args = parameter_s.split(sep=" ")
        try:
            command = args[0]
        except IndexError:
            LOGGER.error(
                "use %track on  or %track off to turn on or off automatic tracking"
            )
        if command == 'off' and self.tracking is not None:
            self.tracking = None
            # This should be a different event
            self.comm_update.send(data={
                "extensionLoaded": True,
                "amieConnected": True,
                "tracking": False
            })
            self.shell.events.unregister('pre_run_cell', self.log.pre_run_cell)
            self.shell.events.unregister('post_run_cell',
                                         self.log.post_run_cell)
            return
        # parse rest of arguments for track on
        try:
            key = args[1].strip('"')
        except IndexError:
            LOGGER.error(
                "First argument must be your api key: get one at https://amie.ai/#/graph/user"
            )
        try:
            url = args[2].strip('"')
        except IndexError:
            url = None
        if command == 'on':
            self.comm_init_tracker.send(data={})
            if url is not None:
                self.garden = amieci.Garden(key=key, url=url)
            else:
                self.garden = amieci.Garden(key=key)


def load_ipython_extension(ip):
    """Load the extension in IPython."""
    magics = FernMagics(ip)
    ip.register_magics(magics)


class ReferenceFinder(ast.NodeVisitor):
    def __init__(self):
        self.locals = set()
        self.inputs = set()
        self.imports = set()

    def visit_Assign(self, node):
        # we need to visit "value" before "targets"
        self.visit(node.value)
        for target in node.targets:
            self.visit(target)
            # Handle and catch output for mutations on the form
            # df['newcol'] = 123
            if (type(target) is ast.Subscript):
                if type(target.ctx) in {ast.Store, ast.Param}:
                    self.locals.add(target.value.id)
                elif type(target.ctx) is ast.Load:
                    if target.value.id not in self.locals:
                        self.inputs.add(node.id)

    def generic_comp(self, node):
        # we need to visit generators before elt
        for generator in node.generators:
            self.visit(generator)
        self.visit(node.elt)

    def visit_ListComp(self, node):
        return self.generic_comp(node)

    def visit_SetComp(self, node):
        return self.generic_comp(node)

    def visit_GeneratorExp(self, node):
        return self.generic_comp(node)

    def visit_DictComp(self, node):
        # we need to visit generators before key/value
        for generator in node.generators:
            self.visit(generator)
        self.visit(node.value)
        self.visit(node.key)

    def visit_FunctionDef(self, node):
        self.locals.add(node.name)
        self.generic_visit(node)

    def visit_arg(self, node):
        self.locals.add(node.arg)

    def visit_AugAssign(self, node):
        target = node.target
        while (type(target) is ast.Subscript):
            target = target.value
        if target.id not in self.locals:
            self.inputs.add(target.id)
        self.generic_visit(node)

    def visit_Name(self, node):
        if type(node.ctx) in {ast.Store, ast.Param}:
            self.locals.add(node.id)
        elif type(node.ctx) is ast.Load:
            if node.id not in self.locals:
                self.inputs.add(node.id)

    def visit_alias(self, node):
        self.imports.add(node.name)
        if node.asname is not None:
            self.locals.add(node.asname)
        else:
            self.locals.add(node.name)


class CellExecution(object):
    def __init__(self, code):

        self.code = code

        tree = ast.parse(self.code)
        rf = ReferenceFinder()
        rf.visit(tree)

        symbolTable = symtable.symtable(code, "?", 'exec')
        # Top level identifiers are in global scope
        globalScope = symbolTable.get_identifiers()

        self.inputs = {x: None for x in rf.inputs}
        # Use symtable to filter outputs outside of global scope
        self.outputs = {x: None for x in rf.locals if x in globalScope}
        self.imports = rf.imports


class Leaf(object):
    def __init__(self, name):
        self.id = name
        self.inputs = {}
        self.outputs = {}
        self.imports = set()
        self.code = ''
        self.ancestors = {}
        self.attachments = []
        self.externalDependencies = set()
        self.input_number = None
        self.time = time.time()

    def update_leaf_inputs(self, variables, user_ns, leaves):
        """
        Parse a block of python code for its inputs and assign to this node
        """
        self.code = variables.code

        # TODO: We shouldn't need to hash here, simply look up by key?
        self.inputs = {x: Value(user_ns.get(x)) for x in variables.inputs}
        self.outputs = variables.outputs
        self.imports = variables.imports

        # Sort vars by time so if two leaves have the same var and value, we
        # attach to the most recent
        varsByLeaf = [(k, v.outputs) for (k, v) in sorted(
            list(leaves.items()), key=lambda x: x[1].time, reverse=True)]

        # Iterate over all inputs
        for (var, value) in self.inputs.items():
            # Iterate over all leaf outputs nt is a proxy time ordered index
            for (nt, (leafId, outputs)) in enumerate(varsByLeaf):
                inheritedValue = outputs.get(var)
                # If an input is found as an output to a previous leaf, add it
                # as an ancestor
                if inheritedValue is not None and (
                        # The hashes match, all is well
                        inheritedValue.hash == value.hash
                        # For "unhashable" types we just pass through on most
                        # recent appearace
                        or inheritedValue.hash is None):
                    # Set the time ordered index so we can grab the most recent
                    # place where it appeared as an ouput
                    self.ancestors[leafId] = nt
                    # Once an ancestor has been found for this var break out of
                    # the inner loop
                    break

    def update_leaf_outputs(self, user_ns):

        mutated_inputs = {}
        # Check for possible mutation of input variables
        for (ik, iv) in self.inputs.items():
            thisInput = Value(user_ns.get(ik))
            # Input has mutated if the hashes don't match and the variable is
            # not already found in the outputs. In the case the hash is None we
            # assume mutation by default
            if (iv.hash != thisInput.hash
                    or iv.hash is None) and (ik not in self.outputs):
                mutated_inputs[ik] = thisInput
        self.outputs = {
            k: Value(user_ns.get(k))
            for (k, v) in self.outputs.items()
        }

        self.outputs.update(mutated_inputs)

    def add_attachments(self, attachments):
        self.attachments = attachments

    def add_dependencies(self, dependencies):
        self.externalDependencies = dependencies

    def publish(self, garden, tree, leaves):
        if len(self.ancestors) == 0:
            # This leaf doesn't inherit from anywhere, but is a child of the
            # root leaf which defines the tree
            amieLeaf = tree._new_leaf(leaf_id=self.id, parent=tree.first)
        else:
            first = True
            # Sort ancestors by the number of references to them
            for ancestor in sorted(
                    self.ancestors, key=self.ancestors.get, reverse=False):
                # The first ancestor is the one with the most references,
                # create a new leaf with this ancestor as the parent
                if first is True:
                    parentLeaf = tree.leaves[ancestor]
                    amieLeaf = tree._new_leaf(
                        parent=parentLeaf, leaf_id=self.id)
                    first = False
                # Other ancestors are added as references
                else:
                    amieLeaf._add_reference(garden, ancestor)

        # Use Jupyter input number as the title.
        # TODO: if the user has updated title this will just overwrite
        # it on every execution
        if self.input_number is not None:
            amieLeaf.set_title(f"In [{self.input_number}]:")
        else:
            amieLeaf.set_title("")
        # Add code highlighting markup
        amieLeaf.set_description("```py\n" + self.code + "\n```")
        for (k, v) in self.outputs.items():
            # Only send "displayable" variables to amie
            if v.type == "displayable":
                amieLeaf.kvs.add(k, v.value)

        # TODO: only handles image/png attachments for the moment (ie mainly
        # matplotlib)
        for a in self.attachments:
            attachment = amieci.highlevel.DataAttachment(
                "attachment.png", a, "", 'image/png')
            amieLeaf.data.update({attachment.fileID: attachment})

        for dependencyName in list(self.externalDependencies):
            with open(dependencyName, mode='rb') as file:
                fileContent = file.read()
                amieLeaf.add_data(dependencyName, fileContent)

        kvHash = hash(str(amieLeaf.kvs.to_json()))
        if kvHash in tree.leafHashes:
            # This cell has been run before yielding the same outputs, we will
            # skip updating amie

            # Update the internal dict with the key that matches amie
            leaves[tree.leafHashes[kvHash]] = leaves[amieLeaf.leaf_id]
            del leaves[amieLeaf.leaf_id]

            # Discard the leaf from amieci
            tree.discard_leaf(amieLeaf.leaf_id)
        else:
            amieLeaf.save()
            tree.leafHashes[kvHash] = self.id


# Compute adler32 checksum of arbitrary python objects
def hash(obj):
    if obj is None:
        return 0
    elif isinstance(obj, str):
        return zlib.adler32(obj.encode())
    elif isinstance(obj, bytes):
        return zlib.adler32(obj)
    # TODO: better handling of tuple and list
    elif isinstance(obj, (int, float, bool, tuple, list)):
        return zlib.adler32(str(obj).encode())
    # For np arrays, convert to bytes
    elif isinstance(obj, (np.ndarray, np.generic)):
        return zlib.adler32(obj.tobytes())
    # Pandas dataframe
    elif isinstance(obj, pd.DataFrame):
        return zlib.adler32(obj.to_records(index=False).tobytes())
    # Pandas series
    elif isinstance(obj, pd.Series):
        return zlib.adler32(obj.values.tobytes())
    # For modules, hash the repr
    elif isinstance(obj, types.ModuleType):
        return zlib.adler32(obj.__repr__().encode())
    elif inspect.isclass(obj):
        return zlib.adler32(str(obj).encode())
    else:
        # We assume all other types are unhashable. This includes but is not
        # limited to functions, etc.
        return None


class Value(object):
    def __init__(self, value):
        # WARNING: the value is likely to mutate if the underlying object
        # changes
        self.value = value
        self.hash = hash(value)

        # Determine the "type" of the value, this is largely to prevent
        # displaying modules and uninstantiated classes as variables (we still
        # use them for graph construction though)
        if inspect.ismodule(value):
            self.type = "module"
        elif inspect.isclass(value):
            self.type = "class"
        elif inspect.isfunction(value):
            self.type = "function"
        elif value is None:
            self.type = "none"
        else:
            self.type = "displayable"
