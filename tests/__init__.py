import pytest
from gtag.gtag import GTagApp
import asyncio

class GSimu:
    def __init__(self,gtag,webMode=False,callbacks={}):
        self.__callbacks=callbacks
        self.gapp=GTagApp(gtag,webMode)
        self.gapp._callMe=self._mockCallMe
        assert self.gapp.render()
        asyncio.run(self.gapp.init())

    @property
    def main(self):
        if self.gapp._ses is None:
            return self.gapp._originalGTag
        else:
            return self.gapp._ses[None] # GID is None

    @property
    def childs(self):
        return self.main._childs
    @property
    def innerchilds(self):
        return self.main.innerChilds


    def get(self,name):
        objects=self.main._getChilds()
        founds=[i for i in objects.keys() if i.startswith(name)]
        if len(founds)==1:
            return objects[ founds[0] ]
        else:
            raise Exception("FOUND %s"%founds)

    def callEvent(self,gobject,eventMethod,*a,**k):
        return asyncio.run(self.gapp.bindUpdate(gobject, None ,eventMethod,a,k)) # GID is None

    async def _mockCallMe(self,method,*a):
        assert method in self.__callbacks, "Undefined callback '%s'" % method
        return self.__callbacks[method](*a)