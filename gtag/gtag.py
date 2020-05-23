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
from .tag import Tag
import typing as T

__version__="0.0.2"

_gg=lambda x: x.get() if isinstance(x,ReactiveProp) else x

class ReactiveProp:
    def __init__(self,dico:dict,attribut:str):
        self.__instance=dico
        self.__attribut=attribut
    def set(self,v):
        self.__instance[self.__attribut]=v
    def get(self):
        return self.__instance[self.__attribut]


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

    def __iadd__(self,v):
        vv=self.get() + _gg(v)
        self.set( vv )
        return self

    def __str__(self):
        return str(self.get())

    def __repr__(self):
        iid=self.__instance.id if hasattr(self.__instance,"id") else str(self.__instance)
        return "<%s instance=%s attr=%s>" % (self.__class__.__name__,iid,self.__attribut)
    #TODO: add a lot of __slot__ ;-)

class State:
    """ Just the beginning of vuex-like (a instance of react'props)
        (it's important that props are reactiveprop ... to be able to be passed to a gtag)
    """
    _sessions={}
    _id=None

    def __init__(self,**defaults):
        self.__d=defaults

    def __setattr__(self,k,v):
        if k.startswith("_"):
            super().__setattr__(k, v)
        else:
            raise Exception("can't")
    def __getattr__(self,k):
        if k.startswith("_"):
            return super().__getattr__(k)
        else:
            if k in self.__d.keys():
                return ReactiveProp(self.__d,k)
            else:
                raise Exception("can't")

    def _initSession(self,sessName):
        import json
        clone=json.loads(json.dumps(self.__d)) #TODO: not needed (but to be sure, before removing)
        State._sessions[sessName] = self.__class__(**clone)
        State._sessions[sessName]._id=sessName

    @classmethod
    def _get(cls,sessName):
        return State._sessions[sessName]

    def __repr__(self):
        return "<STATE:%s %s>" % (self.__class__.__name__, self._id)

class ReactiveMethod:
    """ like ReactiveProp, but for gtag.method wchich can return binded tag
        (object created by @bind decorator)
    """
    def __init__(self,instance,method,args,kargs):
        self.__instance=instance
        self.__method=method
        self.__a=args
        self.__k=kargs

    def __call__(self):
        return self.__method(self.__instance,*self.__a,**self.__k)

    def __str__(self) -> str:
        return str(self())


def bind( method ): # gtag.method decorator -> ReactiveMethod
    """ Decorator to make a gtag.method() able to return a "Reactive Tag" !
        (like 'computed vars' in vuejs)
    """
    def _(gtagInstance,*a,**k):
        assert isinstance(gtagInstance,GTag)
        return ReactiveMethod(gtagInstance,method,a,k)
    return _


class GTagApp(guy.Guy):
    """ The main guy instance app, which cn run a gtag inside """

    def __init__(self,gtag,isMultipleSessionPossible=False):
        super().__init__()
        assert isinstance(gtag,GTag)
        self._gtag=gtag
        self._isSession=isMultipleSessionPossible

    async def init(self):
        if self._isSession:
            gid=await self.js.getSessionId()
            self._gtag.state._initSession(gid)
            print("WEB SESSION:",gid)
        self._gtag.init()

    def render(self,path=None):
        css,js=self._gtag._guessCssJs()
        return """<!DOCTYPE html>
        <html>
            <head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1">

                <script>
                    if(!sessionStorage["gid"]) sessionStorage["gid"]=Math.random().toString(36).substring(2);
                    var GID=sessionStorage["gid"];

                    async function getSessionId() {return GID}
                </script>

                <script src="guy.js"></script>
%s
%s
                <style>
                div.hbox {display: flex;flex-flow: row nowrap;align-items:center }
                div.vbox {display: flex;flex-flow: column nowrap;}
                div.hbox > *,div.vbox > * {flex: 1 1 50%%;margin:1px}
                </style>
            </head>
            <body>%s</body>
        </html>
        """ % (
            "\n".join(['<link rel="stylesheet" href="%s">'%i for i in css]),
            "\n".join(['<script src="%s"></script>'%i for i in js]),
            self._gtag
        )

    def bindUpdate(self,id:str,gid:str,method:str,*args):
        """ inner (js exposed) guy method, called by gtag.bind.<method>(*args) """
        print(">>>>",gid,"event",id,method,args)
        obj=self._gtag._getInstance(id)
        # if self._isSession:
        #     obj.state=State._get(gid)   # TODO: not optimal here
        r=getattr(obj,method)(*args)
        return self.update()    # currently it update all ;-(

    def update(self):
        """ inner (js exposed) guy method, which returns the JS to update the content of the gtag !"""
        return self._gtag.update()



import sys



class GTag:
    """
    The magic thing ;-)
    """
    _tags={}
    state=None
    parent=None
    # _tag=None
    size=None
    """ size of the windowed runned gtag (tuple (width,height) or guy.FULLSCREEN or None) """

    def __init__(self,parent,*a,**k):
        self.id="%s_%s" % (self.__class__.__name__,id(self))
        GTag._tags[self.id]=self       # maj une liste des dynamic created

        self.parent=parent
        if self.parent is not None:
            self.state=self.parent.state
            assert isinstance(self.parent,GTag)
        print("INIT",self.__class__.__name__, "parent=",repr(self.parent), "state:", self.state)

        self.init(*a,**k)
        self._tag = self.build()

    def __del__(self):
        del GTag._tags[self.id]

    def _guessCssJs(self):
        """ try to found the main tag used by the gtag component, and return its css/js (as a list)
            (downside: importing css/js will depends only on first tag returned by the gtag)
            (downside: as tag can be produce by a reactivemethod, we need to execute it)
        """
        js=[]
        css=[]
        if self._tag:
            tag=self._tag
            if isinstance(tag,ReactiveMethod): tag=tag()    # <- dangerous
            if hasattr(tag,"css"):
                css=getattr(tag,"css")
                css= [css] if isinstance(css,str) else css
            if hasattr(tag,"js"):
                js=getattr(tag,"js")
                js= [js] if isinstance(js,str) else js
        return (css,js)

    def init(self,*a,**k):                     
        """ Override to make inits """
        pass

    def build(self) -> T.Union[Tag,None]:
        """ Override for static build
            SHOULD RETURN a "Tag" (not a GTag)
        """
        pass

    def __str__(self):
        o= self._tag
        if isinstance(o,ReactiveMethod): o=o()
        if o is None:
            return ""
        else:
            assert isinstance(o,Tag), "'%s' doesn't produce a Tag, wtf?!" % self.__class__.__name__ # can't produce a gtag (non-sense !)
            o.id=self.id # set an id for js interactions (cf update()/bindUpdate())
            return str(o)

    def __repr__(self):
        return "<GTAG:%s %s>" % (self.__class__.__name__, self.id)


    def _getInstance(self,id):
        return GTag._tags[id]

    # def __getattr__(self,k):
    #     print("============",k)
    #     if k=="state":
    #         print("ooooooooooooooooooooooooooooooooo")
    #     else:
    #         return super().__getattr__(k)

    def __setattr__(self,k,v):
        # current="%s_%s" % (self.__class__.__name__,id(self))
        if k=="state":
            # assert GTag.state is None,"State is already setted, you can't change that"
            assert v==None or isinstance(v,State),"setting state with 'non State instance' is not possible!"
            super().__setattr__("state",v)
        else:
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
    def bind(self) -> any:
        """ to bind attribute or method !"""
        class Binder:
            def __getattr__(this,name:str):
                if name in self.__dict__.keys(): # bind a data attribut  -> return a ReactiveProp
                    o=self.__dict__[name]
                    if isinstance(o,ReactiveProp):
                        return o
                    else:
                        return ReactiveProp(self.__dict__,name)
                elif name in dir(self):   # bind a self.method    -> return a js/string for a guy's call in js side
                    def _(*args):
                        if args:
                            return "self.bindUpdate('%s',GID,'%s',%s)" % (self.id,name,",".join([str(i) for i in args]) ) #TODO: escaping here ! (and the render/str ?) json here !
                        else:
                            return "self.bindUpdate('%s',GID,'%s')" % (self.id,name)
                    return _
                else:
                    raise Exception("Unknown method/attribut '%s' in '%s'"%(name,self.__class__.__name__))
        return Binder()


    def update(self) -> dict:
        #print("update:"+self.id)
        return dict(script="""document.querySelector("#%s").innerHTML=`%s`;""" % (
            self.id, self
        ))

    def run(self,*a,**k) -> any:
        """ Run as Guy App """
        app=GTagApp(self,False)
        app.size=self.size
        self.exit=app.exit
        return app.run(*a,**k)

    def serve(self,*a,**k) -> any:    # serve will be available when state will depend on session !
        """ Run as Guy Server App """
        app=GTagApp(self,True)
        self.exit=app.exit
        return app.serve(*a,**k)


