from lark import Lark, Tree
from ..pipeline import steps, Pipeline, Extra
from ..fileref import FileRef, FileUse, to_fref
from ..steps import aliases
import os

pipeline_raw = """
FNAME: /[^\[\]\\s'"@]+/

pipeline: a_step ("->" a_step)+

a_step: step ("+" step)*
step: name_options [":" fileref ("," fileref)*]

fileref: FNAME -> fname
       | "@" FNAME -> placeholder

name_options: CNAME ["." CNAME]
"""

l = Lark("""
%import common.WS
%ignore WS

%import common.ESCAPED_STRING
%import common.CNAME
%import common.LETTER""" + pipeline_raw, start="pipeline")

def string_to_pipeline(string, options={}):
    return tree_to_pipeline(l.parse(string), options)

def _construct_params(s_obj_tree, options):
    name_options = s_obj_tree.children[0]
    if len(name_options.children) == 1:
        name = name_options.children[0].value
        if name in aliases:
            subtype = aliases[name][1]
            name = aliases[name][0]
        else:
            subtype = ""
    else:
        name = name_options.children[0].value
        subtype = name_options.children[1].value

    if len(s_obj_tree.children) > 1:
        frefs = s_obj_tree.children[1:]
        files = []

        for fref in frefs:
            if fref.data == "placeholder":
                raise NotImplementedError("placeholder")
            fname = fref.children[0].value
            if os.path.isabs(fname):
                raise ValueError("Absolute path specified for input, if you want this behavior use the externals key on the pipeline to copy this file.")
            files.append(to_fref(fname, FileUse.INPUT))
    else:
        files = []

    if name in options:
        option = options[name]
    else:
        option = {}

    return name, files, subtype, option

def _construct(name, *args):
    try:
        cls = (x for x in steps if x.name == name).__next__()
        return cls(*args)
    except StopIteration:
        raise ValueError("Invalid step/sink type {}".format(name))

def tree_to_pipeline(tree: Tree, options=None):
    """
    Options is a dict: 
    {
        "pandoc": {
            <options>
        }
    }
    """
    if options is None:
        options = {}

    # Generate steps
    step_objs = []
    for step in tree.children:
        s_obj, *extras = step.children

        extras = [
            Extra(*_construct_params(x, options)) for x in extras
        ]

        step_objs.append(_construct(*(_construct_params(s_obj, options) + (extras,))))
    
    return Pipeline(step_objs)
