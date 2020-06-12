#!/usr/bin/python3 -u
from gtag import GTag,Tag
from gtag.gtags import *

class App(GTag):
    size=(400,150)

    def init(self):
        self.cpt = 0
        self("alert(1)")

    def build(self):
        self("alert(2)")
        return VBox(
            self.cpt,
            Button("++",onclick=self.bind.add())
        )

    def add(self):
        self.cpt+=1
        self("alert(3)")


app=App()
print(app.scripts)
app2=app._clone()
app2=app._clone()
app2=app._clone()
print(app.scripts)
print(app2.scripts)
app.run()
# app.add()
# print(app.scripts)

