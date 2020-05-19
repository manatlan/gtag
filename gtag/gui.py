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
from .tag import Tag

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
