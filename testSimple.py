#!/usr/bin/python3 -u
from gtag import GTag,Tag
# from gtag.gtags import *

class App(GTag):
    size=(400,150)

    def init(self):
        self.cpt = 0

    def build(self):
        return Tag.div(
            self.cpt,
            Tag.Button("++",onclick=self.bind.add())
            # Button("++",onclick=self.bind.add())
        )

    def add(self):
        self.cpt+=1

# class Btn(GTag):
#     def init(self,v):
#         self.v=v
#     def build(self):
#         return Tag.div(
#             self.v,
#             Tag.button("++",onclick=self.bind.add()),
#             style="border:2px solid red"
#         )
#     def add(self):
#         self.v+=1


app=App()
# app=Btn(0)
app.run()
