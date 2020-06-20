from gtag import *

"""
An exemple of using another set of tags
(here based on materialize.css)
Just to show how to build its own gui !
"""

class Div(GTag):
    def build(self):
        return Tag.div(*self._args,**self._kargs)

class Text(GTag):
    def build(self):
        return Tag.p(*self._args,**self._kargs)

class Button(GTag):
    def build(self):
        return Tag.button(*self._args,**self._kargs,klass="waves-effect waves-light btn")

class Nav(GTag):
    def init(self,title,menus={}):
        self.title=title
        self.menus=menus
    def build(self):
        ul=Tag.ul(klass="right")
        for k in self.menus.keys():
            ul.add( Tag.li( Tag.A(k,onclick=self.bind.select(k)) ))

        return Tag.nav( Tag.div(
                            Tag.A(self.title,klass="brand-logo left"),
                            ul,
                            klass="nav-wrapper"
                    ),
                    klass="navbar-fixed",
        )
    def select(self,k):
        self.menus[k]()

class Modal(GTag):
    def init(self,obj):
        self.obj=obj
    def build(self):
        if self.obj:
            self("""M.Modal.init(tag, {onCloseEnd:function() {%s}}).open()""" % self.bind.close())
            return Tag.div(self.obj,klass="modal")

    @render.local
    def close(self):
        self.obj=None

class Toaster(GTag):
    def init(self,content):
        self.content=content

    def build(self):
        try:
            if self.content:
                self("""M.toast({html: "%s"})""" % self.content)
                return ""
        finally:
            self.content=None # clear content ! (so gtag object is possible)


class Datepicker(GTag):
    def init(self,obj):
        self.obj=obj
    def build(self):
        self("""M.Datepicker.init(tag);""")
        return Tag.input(self.obj,type="text",klass="datepicker")

class Timepicker(GTag):
    def init(self,obj):
        self.obj=obj
    def build(self):
        self("""M.Timepicker.init(tag);""")
        return Tag.input(self.obj,type="text",klass="timepicker")


class _Selector(GTag):
    def init(self,value, choices:list, disabled=False, onchange=None):
        assert value in choices
        self.value=value
        self.choices=choices
        self.disabled=disabled
        self.onchange=onchange


    def select(self,idx):
        self.value=self.choices[int(idx)]
        if self.onchange: self.onchange( value(self.value) )

class RadioButtons(_Selector):
    def build(self):
        o=Tag.div(klass="control")
        for idx,i in enumerate(self.choices):
            o.add( Tag.p(
                Tag.label(
                Tag.input(
                    type="radio",
                    name="r%s"%id(self),
                    onclick=self.bind.select(idx),
                    checked=(self.value==i),
                    disabled=bool(self.disabled)
                    ),
                Tag.span(i),
                klass="radio"
            )))
        return o


class Select(_Selector):
    def build(self):
        self("""M.FormSelect.init(tag)""")
        s=Tag.select( onchange=self.bind.select(b"this.value"), style="width:100%",disabled=bool(self.disabled) )
        for idx,i in enumerate(self.choices):
            s.add( Tag.option(i,value=idx,selected=(self.value==i)))
        return s

class Tabs(_Selector): #TODO: implement disabled
    def build(self):
        self("""M.Tabs.init(tag)""")
        u=Tag.ul(klass="tabs")
        for idx,i in enumerate(self.choices):
            isActive="active" if self.value==i else None
            u.add( Tag.li( Tag.A(i,onclick=self.bind.select(idx),klass=isActive), klass="tab col s3" ) )
        return u


class Checkbox(GTag):
    def init(self,value:bool,title:str, disabled=False, onchange=None):
        self.value=value
        self.title=title
        self.disabled=disabled
        self.onchange=onchange

    def build(self):
        return Tag.label(
            Tag.input(
                checked=bool(self.value),
                type="checkbox",
                onclick=self.bind.switch(),
                disabled=bool(self.disabled)
            ),
            Tag.span(self.title),
        )

    def switch(self):
        self.value = not self.value
        if self.onchange: self.onchange( value(self.value) )


class AnotherGUI(GTag):
    size=(800,600)
    css="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css"  # can be a list of str too
    js="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js"     # can be a list of str too

    def init(self):
        self._mbox=None
        self._toast=None
        self.rb=1
        self.cb=False

    def build(self):
        return Div(
            Nav("Hello", {"Print":lambda: self.mbox("yolo") }),
            Tag.div(
                Text("hello"),Datepicker(None),Timepicker(None),
                Checkbox(self.cb,"disabled"),
                RadioButtons(self.rb,[1,2,3],disabled=self.cb),
                Select(self.rb,[1,2,3],disabled=self.cb),
                Tabs(self.rb,[1,2,3],disabled=self.cb),
                Button("Button",onclick=self.bind.mbox("42")),
                Button("Toast js",onclick="M.toast({html:'koko'})"),
                Button("Toast",onclick=self.bind.toast('yooooo')),
                Div( Div(klass="indeterminate"), klass="progress"),
                klass="container"
            ),
            Modal( self._mbox ),
            Toaster( self._toast ),
        )

    def mbox(self,obj):
        self._mbox=obj

    def toast(self,m):
        self._toast=m

t=AnotherGUI()
t.run()


