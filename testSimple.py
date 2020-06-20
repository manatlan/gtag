#!/usr/bin/python3 -u
from gtag import GTag,Tag

class App(GTag):
    size=(400,150)

    def init(self):
        self.cpt = 0

    def build(self):
        return Tag.span(
            self.cpt,
            Tag.Button("++",onclick=self.bind.add()),
            style="background:yellow;padding:10px"
        )

    def add(self):
        self.cpt+=1


app=App()
app.run()
