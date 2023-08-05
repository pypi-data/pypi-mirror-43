# This file is part of the jin2for project
# (c) 2019 Francesc Verdugo <fverdugo@cimne.upc.edu>

import sys
import os
import argparse as ap
import jinja2 as ji

class App:

    def __init__(self,cml):
        self._cml = cml

    def run(self):

        self._setup_cml_parser()

        self._parse_args()

        self._setup_jinja2_loaders()

        self._setup_jinja2_env()

        self._setup_kinds()

        self._render_files()

    def _setup_cml_parser(self):

        m = 'Builds FORTRAN source files from jinja2 templates'
        parser = ap.ArgumentParser(
            description = m,
            formatter_class=ap.ArgumentDefaultsHelpFormatter)

        h = 'Adds the given directory to the search path \
            in order to look for included template files. \
            It can be used several times to add several directories.'

        parser.add_argument('-I','--include-dir',action='append',help=h)

        h = 'Output directory, where generated FORTRAN files are to be written to.'

        parser.add_argument('-O','--output-dir',help=h,default='./')

        h = 'Extension for the output files'

        parser.add_argument('-e','--output-extension',help=h, default='.f90')

        h = 'Generate intrinsic types for the given compiler'

        parser.add_argument('-g','--generate-for',help=h)

        h = 'Generate intrinsic types from the given file'

        parser.add_argument('-f','--generate-from',help=h)

        h = 'Name of the template file to be processed. \
            It is also possible to give \
            a lists of files to be processed. Unless fully \
            qualified file names are given,\
            the given templates \
            are searched either in the current folder or the paths \
            given by the -I option. For each given template name, \
            a corresponding FORTRAN source file is generated.'

        parser.add_argument('TEMPLATE',nargs='+',help=h)

        self._parser = parser

    def _parse_args(self):

        self._args = self._parser.parse_args(self._cml)

    def _setup_jinja2_loaders(self):

        loaders = [SingleFileLoader(fn) for fn in self._args.TEMPLATE]

        paths = ['./',]
        if self._args.include_dir is not None:
            paths += list(self._args.include_dir)
        abspaths = set([ os.path.abspath(path) for path in paths ])

        loaders += [ji.FileSystemLoader(list(abspaths)),]

        self._loader = ji.ChoiceLoader(loaders)

    def _setup_jinja2_env(self):

        env = ji.Environment(
            loader=self._loader, keep_trailing_newline=True)
        env.globals.update(zip=zip)
        self._env = env

    def _setup_kinds(self):

        from jin2for.kind_info import KindInfo
        from jin2for.intrinsic_type import IntrinsicType

        ki = KindInfo()

        if not self._args.generate_from is None:

            ki.load(self._args.generate_from)

        elif not self._args.generate_for is None:

            ki.generate(self._args.generate_for)


        ips = ki.integer_kinds
        rps = ki.real_kinds
        cps = ki.character_kinds
        lps = ki.logical_kinds

        integers = [ IntrinsicType('integer',k,'i') for k in ips  ]
        reals = [ IntrinsicType('real',k,'r') for k in rps ]
        characters = [ IntrinsicType('character',k,'c') for k in cps ]
        logicals = [ IntrinsicType('logical',k,'l') for k in lps ]

        numericals = integers + reals
        intrinsics = numericals + logicals + characters

        self._types = {
            'integer_types' : integers,
            'real_types' : reals,
            'character_types' : characters,
            'logical_types' : logicals,
            'numerical_types' : numericals,
            'intrinsic_types' : intrinsics }

    def _render_files(self):

        for fn in self._args.TEMPLATE:
            root, ext = os.path.splitext(os.path.basename(fn))
            fn_out = root + self._args.output_extension
            fn_out = os.path.join(self._args.output_dir,fn_out)
            template = self._env.get_template(fn)
            template.stream(**self._types).dump(fn_out)

class SingleFileLoader(ji.BaseLoader):

    def __init__(self, filepath):
        if not os.path.exists(filepath):
            raise FileNotFoundError("file: {}".format(filepath))
        self._filepath = os.path.abspath(filepath)

    def get_source(self, environment, template):
        filepath = os.path.abspath(template)
        if not os.path.exists(filepath):
            raise ji.TemplateNotFound(template)
        if not os.path.samefile(self._filepath,filepath):
            raise ji.TemplateNotFound(template)
        if not os.path.exists(filepath):
            raise ji.TemplateNotFound(template)
        mtime = os.path.getmtime(filepath)
        with open(filepath,'r') as f:
            source = f.read()
        return source, filepath, lambda: mtime == os.path.getmtime(filepath)

def main():

    app = App(sys.argv[1:])
    app.run()

if __name__ == '__main__':
    main()
