#!/usr/bin/python3 -u
from gtag import GTag
from gtag.gtags import *
import time,asyncio

class App(GTag):
    size=(400,150)

    def init(self):
        self.cpt = 0

    def build(self):
        return VBox(
            self.bind.cpt,
            Button("t1",onclick=self.bind.t1()),
            Button("t2",onclick=self.bind.t2()),
        )

    def t1(self):
        self.cpt+=1

    async def t2(self):
        await asyncio.sleep(2)
        self.cpt+=1

app=App()
app.run()
