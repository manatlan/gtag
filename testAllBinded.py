#!/usr/bin/python3 -u
from gtag import GTag,Tag


class C(GTag):
    def build(self):
        return "hi"

class MTag(GTag):
    def init(self):
        self.c1=C()
    def build(self):
        self.c2=C()
        return C()

p=MTag()
print("GOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
print(len(p._getChilds()))
quit()

class Btn(GTag):
    def init(self,v):
        self.v=v
    def build(self):
        return Tag.div(
            self.v,
            Tag.button("++",onclick=self.bind.add()),
            style="border:2px solid red"
        )
    def add(self):
        self.v+=1


class App(GTag):
    size=(400,150)

    def init(self):
        self.cpt = 0
        self.ccc=Btn(12)

    def build(self):
        return Tag.div(
            self.cpt,
            Btn(self.cpt),
        )

from pprint import pprint
app=App()
pprint(app._ichilds)
pprint(app._childs)
pprint(app._getChilds())
# print(app._tree())
# app.run()
