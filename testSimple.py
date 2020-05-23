#!/usr/bin/env python3
from gtag import GTag
import gtag.gui as g


class App(GTag):
    size=(400,150)

    def init(self):
        self.cpt = 0

    def build(self):
        return g.VBox(
            self.bind.cpt,
            g.Button("++",onclick=self.bind.add())
        )

    def add(self):
        self.cpt+=1


app=App()
app.run(log=True)