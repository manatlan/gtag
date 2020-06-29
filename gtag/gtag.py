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

import guy,sys,asyncio,hashlib,html,inspect,types
import typing as T


isAsyncGenerator=lambda x: "async_generator" in str(type(x)) #TODO: howto better ?
fixBacktip=lambda x: x.replace("`",r"\`")

value=lambda x: x.getValue() if isinstance(x,ReactiveProp) else x

def jjs(obj): #TODO: not optimal ... do better than str's pattern subst ;-)
    """ json dumps (js is b'' (bytes)) """
    def my(obj):
        if isinstance(obj,bytes):
            return "<:<:%s:>:>" % obj.decode()
        else:
            return guy.serialize(obj)
    return guy.json.dumps(obj, default=my).replace('"<:<:',"").replace(':>:>"',"")

def log(*a):
    # print(*a)
    pass


class MyMetaclass(type):
    def __getattr__(self,name:str):
        def _(*a,**k) -> Tag:
            t=Tag(*a,**k)
            t.tag=name
            return t
        return _

class Tag(metaclass=MyMetaclass):
    """ This is a helper to produce a "HTML TAG" """
    tag="div" # default one
    klass=None

    def __init__(self,*contents,**attrs):
        #~ assert "id" not in attrs.keys()
        self.id=None
        self.__contents=list(contents)
        self.__dict__.update(attrs)

    def add(self,*elt):
        self.__contents.extend(elt)

    def __str__(self):
        attrs={k:v for k,v in self.__dict__.items() if not k.startswith("_")} # clone the dict (important)!
        klass= attrs.get("klass") or self.klass
        if "klass" in attrs: del attrs["klass"]
        if klass: attrs["class"]=klass
        if self.id: attrs["id"]=self.id
        rattrs=[]
        for k,v in attrs.items():
            if v is not None and k not in ["tag"]:
                if isinstance(v,bool):
                    if v: rattrs.append(k)
                else:
                    rattrs.append( '%s="%s"'%(k.replace("_","-") if k!="klass" else "class",html.escape( str(v) )) )

        return """<%(tag)s%(attrs)s>%(content)s</%(tag)s>""" % dict(
            tag=self.tag.replace("_","-"),
            attrs=" ".join([""]+rattrs) if rattrs else "",
            content=" ".join([str(i) for i in self.__contents if i is not None and not isinstance(i,bool)]),
        )
    def __repr__(self):
        return "<%s>" % self.__class__.__name__

class NONE: pass
class ReactiveProp:
    def __init__(self,dico:dict,attribut:str,value=NONE):
        assert not isinstance(dico,ReactiveProp)
        assert not isinstance(attribut,ReactiveProp)
        assert not isinstance(value,ReactiveProp)
        self._instance=dico
        self._attribut=attribut
        if value!=NONE:
            self.setValue(value)
    def setValue(self,v):
        assert not isinstance(v,ReactiveProp)
        self._instance[self._attribut]=v
    def getValue(self):
        return self._instance[self._attribut]


    def __eq__(self, v):
        return self.getValue() == value(v)

    def __ne__(self, v):
        return self.getValue() != value(v)

    def __lt__(self, v):
        return self.getValue() < value(v)

    def __le__(self, v):
        return self.getValue() <= value(v)

    def __ge__(self, v):
        return self.getValue() >= value(v)

    def __gt__(self, v):
        return self.getValue() > value(v)

    def __add__(self,v):
        return self.getValue() + value(v)
    def __sub__(self,v):
        return self.getValue() - value(v)
    def __mul__(self,v):
        return self.getValue() * value(v)
    def __truediv__(self,v):
        return self.getValue() / value(v)
    def __floordiv__(self,v):
        return self.getValue() // value(v)
    def __mod__(self,v):
        return self.getValue() % value(v)

    def __iadd__(self,v):
        return self.getValue() + value(v)
    def __isub__(self,v):
        return self.getValue() - value(v)
    def __imul__(self,v):
        return self.getValue() * value(v)
    def __itruediv__(self,v):
        return self.getValue() / value(v)
    def __ifloordiv__(self,v):
        return self.getValue() // value(v)


    def __radd__(self, v):
        return value(v) + self.getValue()
    def __rsub__(self, v):
        return value(v) - self.getValue()
    def __rmul__(self, v):
        return value(v) * self.getValue()
    def __rtruediv__(self, v):
        return value(v) / self.getValue()
    def __rfloordiv__(self, v):
        return value(v) // self.getValue()
    def __rmod__(self,v):
        return value(v) % self.getValue()

    def __and__(self,v):
        return self.getValue() & value(v)
    def __or__(self,v):
        return self.getValue() | value(v)
    def __xor__(self,v):
        return self.getValue() ^ value(v)

    def __rand__(self,v):
        return value(v) & self.getValue()
    def __ror__(self,v):
        return value(v) | self.getValue()
    def __rxor__(self,v):
        return value(v) ^ self.getValue()


    def __getitem__(self,k):
        return self.getValue()[k]
    def __setitem__(self,k,v):
        self.getValue()[k]=value(v)
    def __delitem__(self,k):
        del self.getValue()[ value(k) ]

    def __float__(self):
        return float(self.getValue())
    def __int__(self):
        return int(self.getValue())
    def __bool__(self):
        return bool(self.getValue())
    def __str__(self):
        return str(self.getValue())

    def __repr__(self):
        iid=self._instance.id if hasattr(self._instance,"id") else str(self._instance)
        return "<ReactiveProp:%s attr=%s of instance=%s>" % (self.__class__.__name__,self._attribut,iid)


    @property
    def __class__(self):
        return type(self.getValue())

    def __hash__(self):
        return hash(self.getValue())

    def __iter__(self):
        return iter(self.getValue())

    def __next__(self):
        return next(self.getValue())

    def __contains__(self,x):
        return value(x) in self.getValue()



    def __getattr__(self,k):
        return getattr(self.getValue(),k)
    def __setattr__(self,k,v):
        if k.startswith("_"):
            super().__setattr__(k, v)
        else:
            setattr(self.getValue(),k,value(v))

    def __len__(self):
        return len(self.getValue())

    def __call__(self,*a,**k):
        return self.getValue()(*a,**k)
    #TODO: add a lot of __slot__ ;-)


class render:

    # POST build
    @staticmethod
    def local( method ): # gtag.event decorator
        """ Make the method renders only this component (and its childs)"""
        Capacity(method).set(inspect.getouterframes(inspect.currentframe())[0].function)
        return method

    @staticmethod
    def parent( method ): # gtag.event decorator
        """ Make the method renders only its parent (and its childs) """
        Capacity(method).set(inspect.getouterframes(inspect.currentframe())[0].function)
        return method

    @staticmethod
    def none( method ): # gtag.event decorator
        """ Make the method renders nothing """
        Capacity(method).set(inspect.getouterframes(inspect.currentframe())[0].function)
        return method


class Capacity:
    def __init__(self,method:callable):
        self.__method=method
    def has( self, f:callable ):
        if hasattr(self.__method,"capacities"):
            return f.__name__ in self.__method.capacities
    def set( self, capacity ):
        if not hasattr(self.__method,"capacities"):
            self.__method.capacities=[]
        self.__method.capacities.append(capacity)


class Binder:
    def __init__(self,instance):
        self.__instance=instance
    def __getattr__(self,name:str):
        m=hasattr(self.__instance,name) and getattr(self.__instance,name)
        if m and callable( m ):   # bind a self.method    -> return a js/string for a guy's call in js side

            #/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
            # resolve all declaredJsVars from all childs
            pool={}
            for id,o in self.__instance._getChilds().items():
                pool.update( {o.__class__.__name__:o._declaredJsInputs} )
            #/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\

            def _(*args,**kargs):
                if args or kargs:
                    args=[value(i) for i in args]
                    kargs={k:value(v) for k,v in kargs.items()}

                return "self.bindUpdate('%s',GID,'%s',%s,%s,%s)" % (self.__instance.id,name,jjs(args),jjs(kargs),jjs(pool))
            return _
        else:
            raise Exception("Unknown method '%s' in '%s'"%(name,self.__instance.__class__.__name__))


class GTag:
    """
    The magic thing ;-)
    """
    size=None
    _call=None # first event to call at start !
    _parent=None

    """ size of the windowed runned gtag (tuple (width,height) or guy.FULLSCREEN or None) """

    # implicit parent version (don't need to pass self(=parent) when creating a gtag)
    def __init__(self,*a,**k):
        self._data={}
        self._id="%s_%s" % (self.__class__.__name__,hex(id(self))[2:])
        self._tag=NONE
        self._scripts=[]

        if "parent" in k.keys(): # clonage (only main tags, so parent is None)
            #(but could be used to reparent a gtag manually)
            parent=k["parent"]
            del k["parent"]
        else:
            # guess parent
            lvl=0
            while True:
                lvl+=1
                frame = sys._getframe(lvl)
                arguments = frame.f_code.co_argcount
                if arguments == 0:
                    parent=None
                    break
                else:
                    caller_calls_self = frame.f_code.co_varnames[0]
                    parent=frame.f_locals[caller_calls_self]
                    if isinstance(parent,GTag):
                        break

        self._childs=[]     #<- this is cleared at each rendering
        self._args=a
        self._kargs=k
        self._parent=parent

        log("INIT",repr(self))

        #/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
        signature = inspect.signature( self.init )
        self._declaredJsInputs={k: v.default for k, v in signature.parameters.items() if type(v.default)==bytes}
        #/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\

        self.init(*self._args,**self._kargs)
        self._childs=[]     #<- clear innerchilds (creating during child phase), to avoid to appears in child

        self._scriptsInInit=self._scripts[:]
        # self._tag = self.build()    #TODO: remove this build !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        # Store the instance in the parent._childs
        if self._parent:
            self._parent._childs.append(self)

    def _tree(self):
        def _gc(g,lvl=0) -> list:
            ll=["+" + ("   "*lvl) + repr(g)]
            for obj in g._ichilds:
                inners=_gc(obj,lvl+1)
                ll.extend( [i+' (INNER)' for i in inners] )
            for obj in g._childs:
                ll.extend( _gc(obj,lvl+1) )
            return ll
        return "\n".join(_gc(self,0))


    @property
    def _ichilds(self):
        ll= [v for k,v in self._data.items() if isinstance(v,GTag)]
        return ll

    def _getChilds(self) -> dict:

        def _gc(g) -> dict:
            d={g.id:g}
            for obj in g._ichilds:
                d.update( _gc(obj) )
            for obj in g._childs:
                d.update( _gc(obj) )
            return d

        return _gc(self)

    def _getRef(self,id): # -> GTag
        childs=self._getChilds()
        try:
            return childs[id]
        except KeyError:
            raise Exception("ERROR: Unknown child '%s' in '%s'"%(id,self.id))


    @property
    def id(self):
        return self._id


    @property
    def parent(self): # -> T.Union[GTag,None]:
        """ return the parent instance (None if gtag is the main) """
        if self._parent is None:
            return None
        else:
            return self._parent


    @property
    def main(self): # -> GTag:
        """ return the main instance """
        x=self
        while x._parent is not None:
            x=x._parent
        return x



    @property
    def bind(self):
        """ to bind method ! and return its js repr"""
        return Binder(self)


    def _clone(self): #TODO: not clear here ... need redone (the rebuild() needed ?! why ?! (because storage in "_tag")
        assert self._parent==None,"Can't clone a gtag which is not the main one"
        props={k:v for k,v in self.__dict__.items() if k[0]!="_" or k=="_call" or k=="_data"}
        gtag = self.__class__(*self._args,**self._kargs,parent=None) # parent=None, will avoid guess parent ! (it makes sense, because you can clone only mains)
        gtag.__dict__.update(props)
        gtag._scripts=[]
        gtag.init(*self._args,**self._kargs)
        gtag._rebuild()
        log("^^^ CLONED ^^^",repr(self),"-->",repr(gtag))
        return gtag


    def _guessHeaders(self):
        """ try to found the headers, based of declarations of each gtag, and return the html elements to include in header
        """
        assert self._parent is None,"You are not on the main instance, you can't get a child"

        mklist=lambda x: x if isinstance(x,list) else [x]

        md5= lambda x: hashlib.md5(x.encode('utf-8')).hexdigest()

        lmd5=[]
        ll=[]
        for g in GTag.__subclasses__():
            if hasattr(g,"headers"):
                for i in mklist(getattr(g,"headers")):
                    m5=md5(str(i))
                    if m5 not in lmd5:
                        lmd5.append(m5)
                        ll.append( i )
        return ll


    def init(self,*a,**k):
        """ Override to make inits (replace the __init__(), but same role)"""
        pass

    def build(self) -> T.Union[Tag,None]:
        """ Override for static build
            SHOULD RETURN a "Tag" (not a GTag)
        """
        raise Exception("Should be implemented")

    async def _start(self):
        #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- call statement (old autostart system)
        if self._call:  # there is an event to call at start !
            if asyncio.iscoroutine(self._call):
                await self._call
            elif isAsyncGenerator(self._call):
                async for _ in self._call:
                    assert _ is None, "wtf?"
                    yield
            else:
                raise Exception("Not implemented (calling a sync/start function)")
        #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

    def exit(self,v=None): pass # overriden by run/runcef/serve

    def _clearScripts(self):
        self._scripts=self._scriptsInInit[:]

    def _rebuild(self,clearScripts=True):
        if clearScripts: self._clearScripts()
        self._childs=[]
        self._tag=self.build( )

    def __str__(self):
        log("___rendering",repr(self))

        if self._tag == NONE:
            self._tag=self.build()

        o= self._tag

        if o is None:
            return ""
        else:
            for i in self._ichilds:
                i._rebuild()

            if isinstance(o,Tag):
                o.id=self.id
            elif isinstance(o,GTag):
                o=Tag.div(o) # auto div'ify
                o.id=self.id
            else:
                o=Tag.span(o) # auto span'ify
                o.id=self.id
            return str(o)

    def __repr__(self):
        return "<GTag: %s [parent:%s] (innerchilds=%s)>" % (
            self._id,
            self._parent.id if self._parent else "None",
            [i._id for i in self._ichilds]
        )

    def __setattr__(self,k,v):
        if k.startswith("_"):
            # print("REAL SET",k,repr(v))
            super().__setattr__(k,v)
        else:
            o=self._data.get(k)

            if isinstance(o,ReactiveProp):
                # print("SET EXISTING REACTIVE",k,repr(v))

                if isinstance(v,ReactiveProp):
                    # v is RP
                    self._data[k]=v
                    super().__setattr__(k,v)
                else:
                    # v is real
                    o.setValue( v )

            else:
                # print("CREATE REACTIVE",k,repr(v))

                if isinstance(v,ReactiveProp):
                    # v is RP
                    self._data[k]=v            #(put RP in RP !!!!!!!!!!!!!!!!!!!!!!)
                    super().__setattr__(k,v)
                else:
                    # v is real
                    self._data[k]=v
                    super().__setattr__(k,ReactiveProp(self._data,k,v))


    @property
    def scripts(self):
        return ";".join(self._scripts)

    def __call__(self,js):
        self._scripts.append(js)

    def _getScripts(self) -> str:
        ll=[]
        for g in self._getChilds().values():
            js=g.scripts
            if js:
                ll.append( "(function(tag){%s})(document.getElementById('%s'))" % (str(js),g.id) )
        return ";".join(ll)


    def _update(self) -> dict:
        h=str(self)
        s=self._getScripts()
        log(">>>UPDATE:",repr(self))
        log(self._tree())

        return dict( script="""
(function (id,content) {
    let o=document.querySelector(id);
    if(o) o.outerHTML=content;
    else document.body.innerHTML=content;
})("#%s",`%s`); %s
        """ % (self.id, fixBacktip(h),s))

    def run(self,*a,start=None,**k) -> any:
        """ Run as Guy App (using Chrome) """
        self._call=start
        g=GTagApp(self,False)
        g._name=self.__class__.__name__
        return g.run(*a,**k)

    def runCef(self,*a,start=None,**k) -> any:
        """ Run as Guy App (using Cef) """
        self._call=start
        g=GTagApp(self,False)
        g._name=self.__class__.__name__
        return GTagApp.runCef(*a,**k)

    def serve(self,*a,start=None,**k) -> any:
        """ Run as Guy Server App """
        self._call=start
        g=GTagApp(self,True)
        g._name=self.__class__.__name__
        return g.serve(*a,**k)



class GTagApp(guy.Guy):
    """ The main guy instance app, which can run a gtag inside """

    def __init__(self,gtag,isMultipleSessionPossible=False):
        assert isinstance(gtag,GTag)
        self._originalGTag=gtag

        self.size=gtag.size

        if isMultipleSessionPossible:
            self._ses={}
        else:
            self._ses=None
        super().__init__()

    def render(self,path=None):
        hh=self._originalGTag._guessHeaders()

        return """<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <script>
            if(!sessionStorage["gtag"]) sessionStorage["gtag"]=Math.random().toString(36).substring(2);
            var GID=sessionStorage["gtag"];
            async function getSessionId() {return GID}
        </script>
        %s
    </head>
    <body>
            <script src="guy.js"></script>
    </body>
</html>""" % "\n".join([str(h) for h in hh])

    async def init(self):
        if self._ses is not None: # web mode
            gid=await self.js.getSessionId()
            log("CREATE SESSION:",gid)
            gtag = self._ses.get(gid)
            if gtag is None:
                gtag = self._originalGTag._clone()
                self._ses[gid] = gtag
        else: # app mode
            gtag = self._originalGTag

        gtag.exit = self.exit #plug the exit()

        log(">>>SERVE",repr(gtag))
        log(gtag._tree())

        await self.js.eval( gtag.bind._start()+";"+gtag._getScripts() )


    async def bindUpdate(self,id:str,gid:str,method:str,args,kargs,jsArgs={}):
        """ inner (js exposed) guy method, called by gtag.bind.<method>(*args) """

        async def forceUpdate(g):
            g._rebuild(clearScripts=False)
            log(">>>Force UPDATE:",repr(g))
            await self.js.eval( g._update()["script"] )

        if self._ses is None:
            gtag=self._originalGTag
        else:
            gtag=self._ses[gid]

        #////////////////////////////////////////////////////////////////// THE MAGIC TODO: move to gtag
        obj=gtag._getRef(id)

        log("BINDUPDATE on",repr(gtag),"----->",repr(obj),"%s(%s %s)"% (method,args,kargs))
        proc=getattr(obj,method)

        #/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
        # dispatch jsArgs in gtag childs
        #/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
        for o in gtag._getChilds().values():
            defs=jsArgs.get( o.__class__.__name__,{})
            if defs:
                for jsk in o._declaredJsInputs.keys():
                    if jsk in defs:
                        setattr(o,jsk,defs[jsk])
        #/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\

        if Capacity(proc).has(render.local):
            toRender=obj
        elif Capacity(proc).has(render.parent):
            toRender=obj._parent if obj._parent else obj
        elif Capacity(proc).has(render.none):
            toRender=None
        else:
            toRender=gtag

        if toRender: toRender._clearScripts()

        if asyncio.iscoroutinefunction( proc ):
            rep=await proc(*args,**kargs)
        else:
            rep=proc(*args,**kargs)

        if rep:
            if isAsyncGenerator(rep):
                async for _ in rep: # could use yielded thing to update all or local ?!
                    assert _ is None, "wtf (event returns something)?"
                    if toRender:
                        await forceUpdate(toRender)
            else:
                raise Exception("wtf (event returns something)?")

        if toRender:
            toRender._rebuild(clearScripts=False)
            return toRender._update()
        #////////////////////////////////////////////////////////////////// THE MAGIC

