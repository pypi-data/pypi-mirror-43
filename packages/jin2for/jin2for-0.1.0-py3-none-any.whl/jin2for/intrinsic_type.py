# This file is part of the jin2for project
# (c) 2019 Francesc Verdugo <fverdugo@cimne.upc.edu>

default_kind = -1

class IntrinsicType:

    def __init__(self,name,kind,short_name):
        self.name = name
        self.kind = kind
        self.short_name = short_name

    @property
    def alias(self):
        if isinstance(self.kind,int):
            if self.kind == default_kind:
                return self.short_name
            else:
                return '{}{}'.format(self.short_name,self.kind)

        else:
            assert isinstance(self.kind,string)
            return self.kind

    @property
    def decl(self):
        if self.kind == default_kind:
            return self.name
        else:
            return '{}({})'.format(self.name,self.kind)

