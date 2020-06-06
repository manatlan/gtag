from gtag import GTag,Tag
import pytest

import asyncio

async def fetch():
    await asyncio.sleep(1)
    return 42

def test_it():
    class App(GTag):

        def init(self):
            self.v=None

        def build(self):
            o=Tag.div( self.v,
                Tag.button("reload1",onclick=self.bind.evtReload()),
                Tag.button("reload2",onclick=self.bind.evtReload2()),
            )
            return o

        async def evtReload(self):  # better approach !
            self.v = None
            yield                           # <- make an intermediate update/render
            self.v = await fetch()

        async def evtReload2(self):
            self.v = await fetch()

    a=App()
    a._id="myid" #override random one, just for test
    assert a.bind.evtReload()=="self.bindUpdate('myid',GID,'evtReload')"
    assert a.bind.evtReload2()=="self.bindUpdate('myid',GID,'evtReload2')"

    assert a.v==None
    asyncio.run( a.evtReload2() )   # test normal coro
    assert a.v==42

    async def eat_ag(coro):
        async for _ in coro:
            assert a.v == None
        assert a.v == 42

    asyncio.run( eat_ag( a.evtReload()) )   # test coro with async generator

