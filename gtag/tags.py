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

        klass= attrs.get("klass") or self.klass
        if "klass" in attrs: del attrs["klass"]

        self.__attrs=attrs
        if klass: self.__attrs["class"]=klass

    def add(self,*elt):
        self.__contents.extend(elt)

    def __str__(self):
        attrs=self.__attrs
        if self.id: attrs["id"]=self.id
        attrs=['%s="%s"'%(k.replace("_","-") if k!="klass" else "class",html.escape( str(v) )) for k,v in attrs.items() if v]
        return """<%(tag)s%(attrs)s>%(content)s</%(tag)s>""" % dict(
            tag=self.__tag,
            attrs=" ".join([""]+attrs) if attrs else "",
            content=" ".join([str(i) for i in self.__contents]),
        )

    def __repr__(self):
        return "<%s>" % self.__class__.__name__


###################################################################################################
## here are Bulma specific tags
###################################################################################################
class Body(Tag):
    tag="body"
    klass="body"

class Input(Tag):
    tag="input"
    klass="input"

class A(Tag):
    tag="a"
    klass="a"

class Box(Tag):
    tag="div"
    klass="box"

class Div(Tag):
    tag="div"
    klass="div"

class VBox(Tag):
    tag="div"
    klass="vbox"

class HBox(Tag):
    tag="div"
    klass="hbox"
# class HBox(Tag):
#     tag="div"
#     klass="columns is-mobile"
#     def __init__(self,*contents,**attrs):
#         super().__init__(**attrs)
#         self.contents=[Div(i,klass="column") for i in list(contents)]
#     def add(self,o):
#         self.contents.append( Div(o,klass="column"))

class Section(Tag):
    tag="section"
    klass="section"

class Nav(Tag):
    tag="nav"
    klass="navbar is-fixed-top is-black"

class Tabs(Tag):
    tag="div"
    klass="tabs is-centered"
    def __init__(self,**attrs):
        super().__init__(*attrs)
        self.ul=Ul()
        self.add( self.ul )
    def addTab(self,selected,title,onclick=None):
        if selected:
            self.ul.add( Li(A(title,onclick=onclick), klass="is-active" ) )
        else:
            self.ul.add( Li(A(title,onclick=onclick)) )

class Text(Tag):
    tag="p"
    klass="p"

class Button(Tag):
    tag="button"
    klass="button is-light"

class Ul(Tag):
    tag="ul"
    klass="ul"

class Li(Tag):
    tag="li"
    klass="li"
