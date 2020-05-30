#!/usr/bin/python3 -u
from gtag import GTag,bind
import gtag.gui as g

class Btn(GTag):
    def build(self):
        return g.VBox(
            self.parent.cpt,
            g.Button("++",onclick=self.bind.add())
        )
    def add(self):
        self.parent.cpt+=1


class App(GTag):
    size=(400,150)

    def init(self):
        self.cpt = 0

    @bind
    def build(self):
        return g.VBox(
            self.bind.cpt,
            Btn()
        )

app=App()
app.serve(log=False)