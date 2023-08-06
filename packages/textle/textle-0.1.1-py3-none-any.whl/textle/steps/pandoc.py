from ..pipeline import Step
from ..fileref import FileRef, FileUse, to_fref

TAG_LOOKUP = {
    "md": "markdown",
    "pdf": "pdflatex",
    "tex": "latex",
    "rst": "rst"
}

INV_TAG_LOOKUP = {v: k for k, v in TAG_LOOKUP.items()}

OUT_LOOKUP = {k: k for k in TAG_LOOKUP.values()}
OUT_LOOKUP.update({
    "pdflatex": "latex"
})

class PandocStep(Step):
    """
    Generic pandoc step.

    Options beginning with - are passed to pandoc verbatim, if they are boolean type it is passed as a flag, if it's a string it is passed with <option>=<value>
    If you want {} {} formatting, prefix the thing with an underscore

    Because this is rather cumbersome, I plan to add some better aliases to these later
    Subtype is the input type, although this can be inferred from the input file

    Since pandoc can sometimes take multiple inputs, it's helpful use the requires tag (notimplemented yet)

    Current options:
        standalone: default is true
        bib_source: none/biblatex/natbib/bib_file.<json/bib/yaml>
            - biblatex uses latex
            - natbib use natbib
            - others are used as --bibliograpghy arguments
        bib_csl:
            - bib csl for pandoc
        variable:
            - list of parameters after variables
        template:
            - path to template file, added as dependency
    """

    name = "pandoc"

    def handles_extra_type(self, et):
        return super().handles_extra_type(et)

    def __init__(self, files, subtype, options, extras):
        super().__init__(files, subtype, options, extras)

        if subtype:
            self.in_type = subtype
        else:
            self.in_type = None

        self.out_type = None
        self.extra_args = []
        for option, value in options.items():
            if not option.startswith("-") or option.startswith("_-"): continue
            
            if type(value) is bool and value:
                self.extra_args.append(option)
            elif option.startswith("-"):
                self.extra_args.append("{}={}".format(option, str(value)))
            else:
                self.extra_args.extend([option[1:], value])
        
        if self.input:
            if self.input.tag in TAG_LOOKUP and not self.in_type:
                self.in_type = TAG_LOOKUP[self.input.tag]

        self.opt = {
            "standalone": True,
            "bib_source": "none",
            "variable": []
        }

        self.opt.update(options)

    def set_next(self, nx):
        super().set_next(nx)

        for i in nx.get_input_types_valid():
            if i not in TAG_LOOKUP:
                continue
            else:
                self.out_type = TAG_LOOKUP[i]
                break

    def solve_inout(self):
        if self.out_type is None or self.in_type is None:
            raise ValueError("Pandoc step has no output type nor input type")

    def get_products(self):
        return super().get_products()

    def get_output_type(self):
        return INV_TAG_LOOKUP[self.out_type]

    def get_input_types_valid(self):
        return list(TAG_LOOKUP.keys())

    def get_dependencies_for(self, output):
        normal_depends = super().get_dependencies_for(output)
        if self.opt["bib_source"] not in ["natbib", "biblatex", "none"]:
            normal_depends.append(to_fref(self.opt["bib_source"], FileUse.INPUT))
            if "bib_csl" in self.opt:
                normal_depends.append(to_fref(self.opt["bib_csl"], FileUse.INPUT))
        if "template" in self.opt:
            normal_depends.append(to_fref(self.opt["template"], FileUse.INPUT))

        return normal_depends
        
    def get_command_for(self, product):
        base_command = ["pandoc", "--from", OUT_LOOKUP[self.in_type], "--to", OUT_LOOKUP[self.out_type], "-i", self.input, "-o", self.output,
                *self.extra_args]

        if self.opt["standalone"]:
            base_command.append("-s")
        if self.opt["bib_source"] == "biblatex":
            base_command.append("--biblatex")
        elif self.opt["bib_source"] == "natbib":
            base_command.append("--natbib")
        elif self.opt["bib_source"] != "none":
            base_command.extend(["--bibliography", to_fref(self.opt["bib_source"], FileUse.INPUT)])
            if "bib_csl" in self.opt:
                base_command.extend(["--csl", to_fref(self.opt["bib_csl"], FileUse.INPUT)])

        if "template" in self.opt:
            base_command.extend(["--template", to_fref(self.opt["template"], FileUse.INPUT)])

        return (base_command,)
