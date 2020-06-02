#!/usr/bin/python3 -u
from gtag import GTag,bind
from gtag.gtags import *

class Btn(GTag):
    def build(self):
        return VBox(
            self.parent.cpt,self.main.id,
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
            self.bind.cpt,
            Btn()
        )

app=App()
app.serve(log=False)
