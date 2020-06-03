#!/usr/bin/python3 -u
from gtag import GTag,local,start
from gtag.gtags import *
import random,asyncio


async def fetch():
    await asyncio.sleep(1)
    return [[random.randint(1,999) for j in range(10)] for i in range(10)]

class App(GTag):
    size=(500,400)

    def init(self):
        self.rows = None

    def build(self):
        o=Tag.div(Tag.button("reload",onclick=self.bind.evtReload()))
        if self.rows:
            o.add( Table(self.rows) )
        else:
            o.add( "Loading",Tag.progress(klass="progress") )
        return o

    async def evtReload(self):
        self.rows = None
        yield
        self.rows = await fetch()



app=App()
app.run()
