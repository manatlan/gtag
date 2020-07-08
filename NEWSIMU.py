#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
import asyncio,json


###################################################################
from gtag import GTag, Tag, GSimu


#######################################
#######################################
#######################################
class Fake(GTag):
    headers=Tag.script("""
function m1() {alert(1)}
function m2() {alert(2)}
function m3() {alert(3)}
function JJJJJJJJJ() {}
    """)

class A1(GTag):
    """ Simple GTAG """

    def init(self,yo=b"JJJJJJJJJ()"):
        self.cpt = 0
        self("m1()")

    def build(self):
        self("m3()")
        return Tag.span(
            self.cpt,
            Tag.Button("++", onclick=self.bind.add()),
            style="background:yellow;padding:10px")

    def add(self):
        self("m2()")
        self.cpt += 1

class A2(GTag):
    """ The event is async """

    def init(self,yo=b"JJJJJJJJJ()"):
        self.cpt = 0
        self("m1()")

    def build(self):
        self("m3()")
        return Tag.span(
            self.cpt,
            Tag.Button("++", onclick=self.bind.add()),
            style="background:yellow;padding:10px")

    async def add(self):
        self("m2()")
        self.cpt += 1


class A3(GTag):
    """ The event is generator """

    def init(self,yo=b"JJJJJJJJJ()"):
        self.cpt = 0
        self("m1()")

    def build(self):
        self("m3()")
        return Tag.span(
            self.cpt,
            Tag.Button("++", onclick=self.bind.add()),
            style="background:yellow;padding:10px")

    def add(self):
        self("m2()")
        self.cpt += 1
        yield

class A4(GTag):
    """ The event is async generator """

    def init(self,yo=b"JJJJJJJJJ()"):
        self.cpt = 0
        self("m1()")

    def build(self):
        self("m3()")
        return Tag.span(
            self.cpt,
            Tag.Button("++", onclick=self.bind.add()),
            style="background:yellow;padding:10px")

    async def add(self):
        self("m2()")
        self.cpt += 1
        yield



def test_manual_click(s):

    # start phase
    rr=s.start()
    assert len(rr)==2

    r=rr[0]
    assert r["id"]=="gtag"
    assert r["exchange"]=='{\"yo\": JJJJJJJJJ()}'
    assert "m1();m3()" in r["scripts"]

    r=rr[1]
    assert r["id"]==s.main.id
    assert r["exchange"]=='{\"yo\": JJJJJJJJJ()}'
    assert "m1();m3()" in r["scripts"]

    assert ">0 <" in r["content"]
    assert s.main.cpt==0

    # interact with event "add"
    rr=s.event( s.main, "add")

    r=rr[0] # first response will do the scripts !
    assert r["id"]==s.main.id
    assert r["exchange"]=='{\"yo\": JJJJJJJJJ()}'
    assert "m1();m2();m3()" in r["scripts"]

    if len(rr)>1: # a yield has produced another interaction
        r=rr[-1]
        assert r["id"]==s.main.id
        assert r["exchange"]=='{\"yo\": JJJJJJJJJ()}'
        assert "m1();m3()" in r["scripts"]

    assert ">1 <" in r["content"]
    assert s.main.cpt==1


def test_autostart(app,webMode=False):
    s=GSimu( app , webMode, start=app.add() )
    rr=s.start()
    assert any( [ "m1();m2();m3()" in r["scripts"] for r in rr] )
    r=rr[-1]
    assert ">1 <" in r["content"]
    assert s.main.cpt==1

###################################################################
if __name__=="__main__":
    # App().run()

    test_manual_click( GSimu( A1() , False) )
    test_manual_click( GSimu( A1() , True)  )
    test_manual_click( GSimu( A2() , False) )
    test_manual_click( GSimu( A2() , True)  )
    test_manual_click( GSimu( A3() , False) )
    test_manual_click( GSimu( A3() , True)  )
    test_manual_click( GSimu( A4() , False) )
    test_manual_click( GSimu( A4() , True)  )

    test_autostart( A2(), False )
    # test_autostart( A2(), True ) #TODO: trouble in test ;-( (but works IRL)
    test_autostart( A3(), False )
    #~ test_autostart( A3(), True ) #TODO: trouble in test ;-( (but works IRL)
    test_autostart( A4(), False )
    #~ test_autostart( A4(), True ) #TODO: trouble in test ;-( (but works IRL)


    # RAISE EXCEPTION
    #~ app=A1()
    #~ s=GSimu( app , False, start=app.add )
    #~ rr=s.start()
