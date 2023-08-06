#! /usr/bin/env python3
"""

"""


import pdb
import traceback as tb

from ast import *
from os.path import exists
import re
import sys

from .omp import OMP
from .resolvers import Resolver


class AttribProxy:
    """Generate access via attributes"""

    # TODO: move to utils

    def __init__(self, data):
        self._data = data
        # self._func = func
        # self._args = args
        # self._kwds = kwds
        return

    def __getattr__(self, attr):
        data = self._data
        if isinstance(data, dict):
            return data[attr]
        if callable(data):
            return data(attr)
        raise AttributeError("Unable to process {attr}")


class Neulang:
    def __init__(self, debug):
        self._debug = debug
        ns = {}
        self._ns = ns
        self._resolver = ns["RESOLVER"] = Resolver(debug)
        self._ast = None
        self._src = None
        self._latest = None
        self._org_path = None
        return

    def load_astir(self, af=""):
        ns = {}
        if not exists(af):
            return
        am = self.load(af)
        am = compile(am, af, "exec")
        exec(am, ns)
        ap = AttribProxy(ns)
        return ap

    def load(self, path):
        if "core" in self._debug:
            pdb.set_trace()
        if not exists(path):
            raise OSError(f"{path} not found")
        success = None

        with open(path) as po:
            mod = po.read()

            try:
                success = self.loads(mod, path)

            except Exception as e:
                tb.print_exc()
                sys.exit(1)
        return success

    def loads(self, text, sf="<module>"):
        """Convert org text to AST object"""
        ompo = OMP()
        ompo.loads(text, self._org_path)
        self._ast = self._resolver.resolve(ompo.tree)
        self._src = sf
        self._latest = False
        return True

    def eval(self):
        if self._latest:
            return
        exec(compile(self._ast, self._src, "exec"), self._ns)
        self._latest = True
        return

    def reset(self):
        self._ast = self._ns = None
        self._latest = True
        return

    def org_path(self, op):
        if not op or not isinstance(op, list):
            return False
        self._org_path = op
        return True

    @property
    def ns(self):
        return self._ns


if __name__ == "__main__":
    main()
