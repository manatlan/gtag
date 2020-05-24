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

import guy,sys
from .tag import Tag
import typing as T


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

    def __init__(self,**defaults):
        self.__d=defaults

    def __setattr__(self,k,v):
        if k.startswith("_"):
            super().__setattr__(k, v)
        else:
            raise Exception("can't")
    def __getattr__(self,k):
        if k in self.__d.keys():
            return ReactiveProp(self.__d,k)
        else:
            raise Exception("can't")

    def _clone(self): #NEW
        return self.__class__(**self.__d)


    def __repr__(self):
        return "<STATE:%s (id:%s)>" % (self.__class__.__name__,id(self))

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

    def _getInstance(self,id):
        return GTag._tags[id]          # TODO: make more intelligent here

    # implicit parent version (don't need to pass self(=parent) when creating a gtag)
    def __init__(self,parent_or_state=None,*a,**k):
        self.id="%s_%s" % (self.__class__.__name__,hex(id(self))[2:])
        GTag._tags[self.id]=self       # TODO: make more intelligent here

        self._args=list(a)
        self._kargs=k

        # guess parent
        frame = sys._getframe(1)
        arguments = frame.f_code.co_argcount
        if arguments == 0:
            parent=None
        else:
            caller_calls_self = frame.f_code.co_varnames[0]
            parent=frame.f_locals[caller_calls_self]
            assert isinstance(parent,GTag)
            if parent.__class__ == self.__class__: parent=None

        self._state=None
        if parent_or_state is not None:
            if isinstance(parent_or_state,State):
                self.parent=None                             # main gtag
                self._state=parent_or_state
                print("**STATE INIT**",repr(self._state))
            elif isinstance(parent_or_state,GTag):
                self.parent=parent_or_state                  #explicit re-parent
            else:
                self._args.insert(0,parent_or_state)
                self.parent=parent
        else:
            self.parent=parent

        print("INIT",repr(self))
        self.init(*self._args,**self._kargs)
        self._tag = self.build()

    def _getMain(self):
        x=self
        while x.parent is not None:
            x=x.parent
        return x

    @property
    def state(self):
        x=self._getMain()
        return x._state

    def _setState(self,s):  # rebind the state on the main parent of this gtag
        if s is not None:
            assert isinstance(s,State)
        x=self._getMain()
        x._state=s


    """
        def __init__(self,parent=None,*a,**k):
            self.id="%s_%s" % (self.__class__.__name__,hex(id(self))[2:])
            self._args=a
            self._kargs=k
            GTag._tags[self.id]=self       # TODO: make more intelligent here

            if parent is None: # main gtag instance with no state
                self.parent=None
                self.state=None
            elif isinstance(parent,State): # main gtag instance with state
                self.parent=None
                self.state=parent   #<- the trick
            else:
                assert isinstance(parent,GTag)
                self.parent=parent
                self.state=self.parent.state

            self.init(*self._args,**self._kargs)
            self._tag = self.build()
    """
    def _clone(self):
        props={k:v for k,v in self.__dict__.items() if k not in ['id', 'parent', '_tag',"_state"]}
        state=self.state._clone() if self.state else None
        gtag = self.__class__(state,*self._args,**self._kargs)
        gtag.__dict__.update(props)
        assert isinstance(gtag,GTag)
        print("^^^ CLONED ^^^",repr(self),"-->",repr(gtag))
        return gtag


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
        return "<GTAG:%s %s (parent:%s) (state:%s)>" % (self.__class__.__name__, self.id,self.parent.id if self.parent else "no",id(self.state) if self.state else "no")

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
        print(">>>>>>>>>>>>>>>>>> UPDATE:",repr(self))
        return dict(script="""document.querySelector("#%s").innerHTML=`%s`;""" % (
            self.id, self
        ))

    def run(self,*a,**k) -> any:
        """ Run as Guy App """
        return GTagApp(self,False).run(*a,**k)

    def serve(self,*a,**k) -> any:    # serve will be available when state will depend on session !
        """ Run as Guy Server App """
        return GTagApp(self,True).serve(*a,**k)



class GTagApp(guy.Guy):
    """ The main guy instance app, which cn run a gtag inside """

    def __init__(self,gtag,isMultipleSessionPossible=False):
        assert isinstance(gtag,GTag)
        self._originalGTag=gtag

        self.size=gtag.size

        if isMultipleSessionPossible:
            self._ses={}
        else:
            self._ses=None
        super().__init__()


    async def init(self):
        if self._ses is not None:
            gid=await self.js.getSessionId()
            print("CREATE SESSION:",gid)
            gtag = self._ses.get(gid)
            if gtag is None:
                gtag = self._originalGTag._clone()
                self._ses[gid] = gtag
        else:
            gtag = self._originalGTag

        gtag.exit = self.exit

        print("SERVE",repr(gtag))
        css,js=gtag._guessCssJs()
        await self.js._render( str(gtag),css,js )

    def render(self,path=None):
        return """<!DOCTYPE html>
        <html>
            <head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1">

                <script>
                    if(!sessionStorage["gid"]) sessionStorage["gid"]=Math.random().toString(36).substring(2);
                    var GID=sessionStorage["gid"];

                    async function getSessionId() {return GID}
                    async function _render(html,css,js) {
                        document.body.style="visibility:hidden";
                        document.body.innerHTML=html;

                        function show() {
                            document.body.style="visibility:visible";
                        }

                        for(var f of css) {
                            var t = document.createElement("link");
                            t.type = "text/css";
                            t.rel = "stylesheet";
                            t.href = f;
                            t.onload=show
                            document.getElementsByTagName("head")[0].appendChild(t);
                        }

                        for(var f of js) {
                            var t = document.createElement("script");
                            t.type = "text/javascript";
                            t.src = f;
                            t.onload=show
                            document.getElementsByTagName("head")[0].appendChild(t);
                        }
                        if(css.length==0 && js.length==0) show()
                    }
                </script>

                <script src="guy.js"></script>

                <style>
                div.hbox {display: flex;flex-flow: row nowrap;align-items:center}
                div.vbox {display: flex;flex-flow: column nowrap;}
                div.hbox > *,div.vbox > * {flex: 1 1 50%;margin:1px}
                </style>
            </head>
            <body></body>
        </html>
        """

    def bindUpdate(self,id:str,gid:str,method:str,*args):
        """ inner (js exposed) guy method, called by gtag.bind.<method>(*args) """
        if self._ses is None:
            gtag=self._originalGTag
        else:
            gtag=self._ses[gid]

        obj=gtag._getInstance(id)    # TODO: make more intelligent here
        obj._setState(gtag._state)   # <--- PATH (NOT GREAT) TODO: fix that
        print("BINDUPDATE on",repr(gtag),"---obj-->",repr(obj))
        r=getattr(obj,method)(*args)
        return gtag.update()
