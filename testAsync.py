#!/usr/bin/python3 -u
from gtag import GTag
from gtags import *
import time


import asyncio
async def longProcess(time=2):
    await asyncio.sleep(time)
    return time

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
        await longProcess()
        self.cpt+=1


app=App()
app.run()