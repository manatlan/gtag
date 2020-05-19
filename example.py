#!/usr/bin/env python3
from gtag import GTag
import gtag.gui as g

class Starred(GTag):
    def __init__(self, v=0):
        self.value = v
        super().__init__()

    def build(self):
        return g.HBox(
            g.Button( "-", onclick=self.bind.addValue(-1) ),
            g.Text( self.bind.value, style="text-align:center" ),
            g.Button( "+", onclick=self.bind.addValue(1) ),
        )

    def addValue(self, v):
        self.value += v


class App(GTag):
    size=(400,150)

    def __init__(self):
        self.cpt1 = 12
        self.cpt2 = 7
        super().__init__()

    def build(self):
        return g.VBox(
            g.HBox( g.Text("Value1:"), Starred( self.bind.cpt1 )),
            g.HBox( g.Text("Value2:"), Starred( self.bind.cpt2 )),
        )

app=App()
app.run()