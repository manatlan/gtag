#!/usr/bin/env python3
from gtag import GTag, bind
import gtag.gui as g

"""
A basic simple example
With all main features:
    - dynamic compute with @bind
    - nested gtag (reusable component)
    - bind/call a method
    - reactive prop (share the same state)
    - sized main window
"""

class Starred(GTag):
    def init(self, v=0):
        self.value = v

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

    def init(self):
        self.cpt1 = 12
        self.cpt2 = 7

    @bind
    def compute(self):
        return self.cpt1 * self.cpt2

    def build(self):
        return g.VBox(
            g.HBox( g.Text("Value1:"), Starred( self, self.bind.cpt1 )),
            g.HBox( g.Text("Value2:"), Starred( self, self.bind.cpt2 )),
            g.Text("Value1 x Value2=",self.compute(),style="text-align:center")
        )

app=App()
app.run(log=False)