#!/usr/bin/python3 -u
from gtag import GTag
from gtag.gtags import *

class Btn(GTag):
    def build(self):
        return VBox(
            self.parent.cpt,
            Button("++",onclick=self.bind.add())
        )
    def add(self):
        self.parent.cpt+=1


class App(GTag):
    size=(400,150)

    def init(self):
        self.cpt = 0

    def build(self):
        return VBox(
            self.cpt,
            Btn()
        )

app=App()
app.run(log=False)
