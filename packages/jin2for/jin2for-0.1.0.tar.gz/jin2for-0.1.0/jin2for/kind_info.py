# This file is part of the jin2for project
# (c) 2019 Francesc Verdugo <fverdugo@cimne.upc.edu>

import json
import tempfile
import subprocess
import pkg_resources
import os
import shlex

integer_key = 'integer'
real_key = 'real'
character_key = 'character'
logical_key = 'logical'
keys = [integer_key, real_key, character_key, logical_key]

class KindInfo:

    def __init__(self):

        default_data = {}
        default_data[integer_key] = [-1,]
        default_data[real_key] = [-1,]
        default_data[character_key] = [-1,]
        default_data[logical_key] = [-1,]
        self._set_data(default_data)

    @property
    def has_data(self):
        return hasattr(self,'_data')

    @property
    def integer_kinds(self):
        return self._data[integer_key]

    @property
    def real_kinds(self):
        return self._data[real_key]

    @property
    def character_kinds(self):
        return self._data[character_key]

    @property
    def logical_kinds(self):
        return self._data[logical_key]

    def generate(self,compiler):

        kindsf90 = pkg_resources.resource_filename(
            'jin2for','data/kinds.f90')

        with tempfile.TemporaryDirectory() as tmpdir:

            exefile = os.path.join(tmpdir,'kinds.exe')

            cmd = '{} -o {}  {}'.format(compiler,exefile,kindsf90)
            r = subprocess.run(shlex.split(cmd),cwd=tmpdir)
            assert r.returncode == 0

            r = subprocess.run(exefile,cwd=tmpdir,stdout=subprocess.PIPE)
            assert r.returncode == 0

            data = json.loads(r.stdout.decode('utf-8'))

            self._set_data(data)

    def _set_data(self,data):

        self._data = {}
        for key in keys:
          assert isinstance(data[key],list)
          self._data[key] = data[key]

    def load(self,filename):

        with open(filename,'r') as f:
            data = json.load(f)

        self._set_data(data)


    def dump(self,filename):

        assert hasattr(self,'_data')

        with open(filename,'w') as f:
            data = json.dump(self._data,f)

