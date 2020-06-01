#!/usr/bin/python3 -u
from gtag import GTag
import gtag.gui as g
import time
# IN PROGRESS
# IN PROGRESS
# IN PROGRESS
# IN PROGRESS
# IN PROGRESS

import asyncio
async def longProcess(time=2):
    await asyncio.sleep(time)
    return time

class App(GTag):
    size=(400,150)

    def init(self):
        self.cpt = 0

    def build(self):
        return g.VBox(
            self.bind.cpt,
            g.Button("t1",onclick=self.bind.t1()),
            g.Button("t2",onclick=self.bind.t2()),
        )

    def t1(self):
        self.cpt+=1

    async def t2(self):
        await longProcess()
        self.cpt+=1


app=App()
app.run()