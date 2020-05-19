#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# #############################################################################
#    Apache2 2020 - manatlan manatlan[at]gmail(dot)com
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#        http://www.apache.org/licenses/LICENSE-2.0
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
#
#    more: https://github.com/manatlan/guy
# #############################################################################
import html

class Tag:
    """
        This is a helper to produce "HTML TAG"
        This is completly css agnostic
    """
    tag="div" # default one
    klass=None

    def __init__(self,*contents,**attrs):
        assert "id" not in attrs.keys()
        self.id=None
        self.__tag=self.__class__.tag
        self.__contents=list(contents)
        self.__attrs=dict(attrs)

    def add(self,*elt):
        self.__contents.extend(elt)

    def __str__(self):
        attrs=self.__attrs
        klass= attrs.get("klass") or self.klass
        if "klass" in attrs: del attrs["klass"]
        if klass: attrs["class"]=klass
        if self.id: attrs["id"]=self.id
        attrs=['%s="%s"'%(k.replace("_","-") if k!="klass" else "class",html.escape( str(v) )) for k,v in attrs.items() if v]
        return """<%(tag)s%(attrs)s>%(content)s</%(tag)s>""" % dict(
            tag=self.__tag,
            attrs=" ".join([""]+attrs) if attrs else "",
            content=" ".join([str(i) for i in self.__contents]),
        )

    def __repr__(self):
        return "<%s>" % self.__class__.__name__

