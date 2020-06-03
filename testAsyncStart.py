#!/usr/bin/python3 -u
from gtag import GTag,start
from gtag.gtags import *
import random,asyncio


class App(GTag):
    size=(500,400)

    def init(self):
        self.rows = None

    def build(self):
        o=Tag.div( Tag.button("b",onclick=self.bind.evtLoad()) )
        if self.rows:
            o.add( Table(self.rows))
        else:
            o.add( "Loading",Tag.progress(klass="progress") )
        return o

    # def script(self):
    #     return self.bind.evtLoad()

    async def evtLoad(self):
        if self.rows==None:
            self.rows = [[random.randint(1,999) for j in range(10)] for i in range(10)]

        # if self.rows==None:
        #     await asyncio.sleep(3)
        #     self.rows = [[random.randint(1,999) for j in range(10)] for i in range(10)]
        #     return True # force local update
        # else:
        #     return False # do nothing

app=App()
app.run()