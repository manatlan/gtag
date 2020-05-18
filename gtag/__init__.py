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

import guy
from .tags import Tag

__version__="0.0.1"

_gg=lambda x: x.get() if isinstance(x,ReactiveProp) else x

class ReactiveProp:
    def __init__(self,instance,attribut:str):
        # assert attribut in instance.__dict__.keys()
        self.__instance=instance
        self.__attribut=attribut
    def set(self,v):
        self.__instance.__dict__[self.__attribut]=v
    def get(self):
        return self.__instance.__dict__[self.__attribut]


    def __eq__(self, v):
        return self.get() == _gg(v)

    def __ne__(self, v):
        return self.get() != _gg(v)

    def __lt__(self, v):
        return self.get() < _gg(v)

    def __le__(self, v):
        return self.get() <= _gg(v)

    def __ge__(self, v):
        return self.get() >= _gg(v)

    def __gt__(self, v):
        return self.get() > _gg(v)


    def __int__(self):
        return int(self.get())

    def __add__(self,v): # add in place
        vv=self.get() + _gg(v)
        self.set( vv )
        return self

    def __str__(self):
        return str(self.get())

    def __repr__(self):
        iid=self.__instance.id if hasattr(self.__instance,"id") else str(self.__instance)
        return "<%s instance=%s attr=%s>" % (self.__class__.__name__,iid,self.__attribut)
    #TODO: add a lot of __slot__ ;-)



class ReactiveTag:
    """ like ReactiveProp, but for gtag.method wchich can return binded tag
        (object created by @bind decorator)
    """
    def __init__(self,instance,method):
        self.__instance=instance
        self.__method=method

    def getTag(self):
        x=self.__method(self.__instance)
        if x:
            assert isinstance(x,Tag)
            return x

    def __str__(self) -> str:
        return str(self.getTag()) or ''


def bind( method ): # gtag.method decorator -> ReactiveTag
    """ Decorator to make a gtag.method() able to return a "Reactive Tag" !
        (like 'computed vars' in vuejs)
    """
    def _(gtagInstance):
        assert isinstance(gtagInstance,GTag)
        return ReactiveTag(gtagInstance,method)
    return _


class GTagApp(guy.Guy):
    """ The main guy instance app, which cn run a gtag inside """

    def __init__(self,gtag):
        super().__init__()
        self._gtag=gtag

    def render(self,path=None):
        return """<!DOCTYPE html>
        <html>
            <head>
                <script>
                if(!sessionStorage["gid"]) sessionStorage["gid"]=Math.random().toString(36).substring(2);
                var GID=sessionStorage["gid"];

                async function launchApp() {    // NOT USED YET !!
                    await self.startApp(GID);
                }
                </script>

                <script src="guy.js"></script>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.8.2/css/bulma.min.css">

                <style>
                div.hbox {display: flex;flex-flow: row nowrap;align-items:center }
                div.vbox {display: flex;flex-flow: column nowrap;}
                div.hbox > *,div.vbox > * {flex: 1 1 50%%;margin:1px}
                </style>
            </head>
            <body>%s</body>
        </html>
        """ % self._gtag

    def bindUpdate(self,id:str,method:str,*args):
        """ inner (js exposed) guy method, called by gtag.bind.<method>(*args) """
        obj=self._gtag._getInstance(id)
        r=getattr(obj,method)(*args)
        return self.update()    # currently it update all ;-(

    def update(self):
        """ inner (js exposed) guy method, which returns the JS to update the content of the gtag !"""
        return self._gtag.update()





class GTag:
    """
    The magic thing ;-)
    """
    _tags={}

    size=None
    """ size of the windowed runned gtag (tuple (width,height) or guy.FULLSCREEN or None) """

    def __init__(self):
        self.id="%s_%s" % (self.__class__.__name__,id(self))
        GTag._tags[self.id]=self       # maj une liste des dynamic created

        self._tag = self.build()

    def __del__(self):
        del GTag._tags[self.id]

    def build(self) -> Tag:
        """ Override for static build
            SHOULD RETURN a "Tag" (not a GTag)
        """
        pass

    def __str__(self):
        o= self._tag
        assert o is not None, "no build ?!"
        if isinstance(o,ReactiveTag):
            o=o.getTag()
        assert not isinstance(o,GTag), "'%s' produce a GTag, wtf?!" % self.__class__.__name__ # because it's a non-sense that a GTag return a GTag .. that's all!
        o.id=self.id
        return str(o)


    def _getInstance(self,id):
        return GTag._tags[id]

    def __setattr__(self,k,v):
        # current="%s_%s" % (self.__class__.__name__,id(self))
        o=self.__dict__.get(k)
        if isinstance(o,ReactiveProp):
            # print("Maj %s ReactProp %s <- %s" % (current,k,repr(v)))
            if isinstance(v,ReactiveProp):
                self.__dict__[k]=v
            else:
                o.set(v)
        else:
            # print("Maj %s Prop %s <- %s" % (current,k,repr(v)))
            super().__setattr__(k,v)

    @property
    def bind(self):
        """ to bind attribute or method !"""
        class Binder:
            def __getattr__(sself,name):
                if name in self.__dict__.keys(): # bind a data attribut  -> return a ReactiveProp
                    o=self.__dict__[name]
                    if isinstance(o,ReactiveProp):
                        return o
                    else:
                        return ReactiveProp(self,name)
                elif name in dir(self):   # bind a self.method    -> return a js/string for a guy's call in js side
                    def _(*args):
                        if args:
                            return "self.bindUpdate('%s','%s',%s)" % (self.id,name,",".join([str(i) for i in args]) ) #TODO: escaping here ! (and the render/str ?) json here !
                        else:
                            return "self.bindUpdate('%s','%s')" % (self.id,name)
                    return _
                else:
                    raise Exception("Unknown method/attribut '%s' in '%s'"%(name,self.__class__.__name__))
        return Binder()

    def update(self):
        #print("update:"+self.id)
        return dict(script="""document.querySelector("#%s").innerHTML=`%s`;""" % (
            self.id, self
        ))

    def run(self,*a,**k):
        """ Run as Guy App """
        app=GTagApp(self)
        app.size=self.size
        self.exit=app.exit
        return app.run(*a,**k)

    def serve(self,*a,**k):
        """ Run as Guy Server App """
        app=GTagApp(self)
        self.exit=app.exit
        return app.serve(*a,**k)


