#!/usr/bin/env python3
from gtag import GTag
import gtag.gui as g

class Btn(GTag):
    def build(self):
        return g.VBox(
            g.Button("++",onclick=self.bind.add())
        )
    def add(self):
        self.parent.cpt+=1


class App(GTag):
    size=(400,150)

    def init(self):
        self.cpt = 0

    def build(self):
        return g.VBox(
            self.bind.cpt,
            Btn(self)
        )



app=App()
app.run(log=True)