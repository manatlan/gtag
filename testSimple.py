#!/usr/bin/python3 -u
from gtag import GTag,Tag
from gtags import *

class App(GTag):
    size=(400,150)
    css="https://cdn.jsdelivr.net/npm/bulma@0.8.2/css/bulma.min.css"

    def init(self):
        self.cpt = 0

    def build(self):
        return VBox(
            self.bind.cpt,
            Button("++",onclick=self.bind.add())
        )

    def add(self):
        self.cpt+=1


app=App()
app.run()
