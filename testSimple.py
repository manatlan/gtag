#!/usr/bin/python3 -u
from gtag import GTag,Tag
from gtag.gtags import *

class App(GTag):
    size=(400,150)

    def init(self):
        self.cpt = 0

    def build(self):
        return VBox(
            self.cpt,
            Button("++",onclick=self.bind.add())
        )

    def add(self):
        self.cpt+=1


app=App()
app.run()
