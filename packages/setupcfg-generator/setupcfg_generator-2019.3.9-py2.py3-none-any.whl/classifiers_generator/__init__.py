#!/usr/bin/env python
import os
import public
import requests


@public.add
class Requirements:
    """`requirements` class"""
    requirements = []

    def __init__(self, requirements=None):
        if requirements is None:
            if os.path.exists("requirements.txt"):
                self.load("requirements.txt")
        else:
            self.load(requirements)

    def load(self, path=None):
        """load requirements from file"""
        if not path:
            path = "requirements.txt"
        self.requirements = []
        for line in open(path).read().splitlines():
            r = line.split("#")[0].strip()
            if r:
                self.requirements.append(r)
        return self

    def classifiers(self):
        """get requirements classifiers from pypi.org"""
        pyversions = []
        for req in self.requirements:
            url = "https://pypi.org/pypi/%s/json" % req
            if "==" in req:
                url = "https://pypi.org/pypi/%s/%s/json" % tuple(req.split("=="))
            r = requests.get(url)
            r.raise_for_status()
            classifiers = r.json()["info"]["classifiers"]
            _pyversions = list(filter(lambda l: 'Python ::' in l, classifiers))
            if not pyversions:
                pyversions = _pyversions
            else:
                pyversions = list(set(pyversions) & set(_pyversions))
        if "Programming Language :: Python" in str(pyversions):
            pyversions.append('Programming Language :: Python')
        return list(sorted(set(pyversions)))
