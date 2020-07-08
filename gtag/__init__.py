#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# #############################################################################
#    Apache2 2020 - manatlan manatlan[at]gmail(dot)com
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#        http://www.apache.org/licenses/LICENSE-2.0
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
#
#    more: https://github.com/manatlan/guy
# #############################################################################

__version__="0.0.41"

from .gtag import GTag, Tag, value, render

__all__ = [ 'GTag', 'Tag', 'value', 'render' ]

from .gtag import GTagApp

import asyncio,json

class GSResponse(dict):
    def __init__(self,type,dico):
        self.type=type
        super().__init__( dico)
    def __repr__(self):
        return "----------"+self.type+"-----------"+json.dumps(self,indent=4)

class GSimu:
    """ New (Guy/GTag) Simulator """
    def __init__(self, gtag, webMode=False, start=None):
        gtag._call=start
        self.gapp = GTagApp(gtag, webMode)
        self.gapp._callMe = self._mockCallMe  # guy override!
        assert self.gapp.render()

    def start(self):
        """ do the init and run the 1st event '_start' """
        self._iter = []
        r = asyncio.run(self.gapp.init())
        assert not r #ensure init() returns nothinf

        # ensure that the scripts part starts the event "_start"
        assert len(self._iter) == 1
        assert "callEvent(" in self._iter[0]["scripts"],self._iter[0]["scripts"]
        assert "'_start',[],{}," in self._iter[0]["scripts"]

        ll=[]
        for i in self._iter:
            ll.append( GSResponse("INIT", i) )

        for e in self.event(self.main, "_start"):
            ll.append(e)
        return ll

    def event(self, gobject, eventMethod, *a, **k):
        assert isinstance(gobject, GTag)
        self._iter = []
        r = asyncio.run( self.gapp.bindUpdate(gobject.id, "fake", eventMethod, a,k))  # GID is None
        ll=[]
        for i in self._iter:
            ll.append( GSResponse("%s yield" % eventMethod, i) )

        ll.append( None if r is None else GSResponse( "%s end" % eventMethod, r ) )
        return ll

    @property
    def main(self):
        if self.gapp._ses is None:
            return self.gapp._originalGTag
        else:
            return self.gapp._ses["fake"]

    @property
    def childs(self):
        return self.main._childs

    @property
    def ichilds(self):
        return self.main._ichilds

    def get(self, name):
        objects = self.main._getChilds()
        founds = [i for i in objects.keys() if i.startswith(name)]
        if len(founds) == 1:
            return objects[founds[0]]
        else:
            raise Exception("FOUND %s" % founds)

    async def _mockCallMe(self, jsmethod, *a):

        def myexec(id,content,scripts,exchange):
            self._iter.append( dict(id=id,content=content,scripts=scripts,exchange=exchange))
            return {}

        cbjs = dict(execute=myexec, getSessionId=lambda: "fake")

        assert jsmethod in cbjs, "Undefined js-callback '%s'" % jsmethod
        return cbjs[jsmethod](*a)


###################################################################
from gtag import GTag, Tag


class App(GTag):
    size = (400, 150)

    # def init(self):
    def init(self,yo=b"JJJJJJJJJ()"):
        self.cpt = 0
        self("CCCCCCCCCCCCCCCCCCCC()")

    def build(self):
        return Tag.span(
            self.cpt,
            Tag.Button("++", onclick=self.bind.add()),
            style="background:yellow;padding:10px")

    def add(self):
        self.cpt += 1
        yield


###################################################################
if __name__=="__main__":
    # App().run()

    s = GSimu( App() , False)
    for typ,r in s.start():
        print("====",typ,"=" * 70)
        print(json.dumps(r, indent=2))
    for typ,r in s.event( s.main, "add"):
        print("====",typ,"=" * 70)
        print(json.dumps(r, indent=2))

