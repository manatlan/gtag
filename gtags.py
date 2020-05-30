from gtag import GTag, bind
import gtag.gui as t
"""
An exemple of GTags

the kind of library, you should construct before using "gtag"
"""
class MyBox(GTag):
    def init(self,content):
        self.content=content

    @bind
    def build(self):
        if self.content!=None:
            o = t.Div(klass="modal is-active")
            o.add( t.Div(klass="modal-background",onclick=self.bind.close()) )
            o.add( t.Div( t.Box(self.content),klass="modal-content") )
            o.add( t.Div(klass="modal-close is-large",aria_label="close",onclick=self.bind.close()) )
            return o

    def close(self):
        self.content=None

class MyInput(GTag):

    def init(self,txt,type="text"):
        self.v=txt
        self.type=type

    def build(self):
        return t.Input(type=self.type,value=self.v,onchange=self.bind.onchange("this.value"))

    def onchange(self,txt):
        self.v = txt


class MyNav(GTag):
    def init(self,title,entries:dict={}):
        self.title=title
        self.entries=entries

    @bind
    def build(self): # DYNAMIC RENDERING HERE !
        divBrand=t.Div( klass="navbar-brand" )
        divBrand.add( t.A("<b>"+self.title+"</b>",klass="navbar-item",href="/") )
        divBrand.add( t.A('<span aria-hidden="true"></span><span aria-hidden="true"></span><span aria-hidden="true"></span>',
                        role="button",
                        klass="navbar-burger burger",
                        aria_label="menu",
                        aria_expanded="false",
                        data_target="navbarBasicExample",
                        onclick="this.classList.toggle('is-active');document.querySelector('.navbar-menu').classList.toggle('is-active')") )

        menu=t.Div(klass="navbar-start")
        for k,v in self.entries.items():
            menu.add( t.A(k, klass="navbar-item", onclick=self.bind.evtSelectEntry("'%s'"%k)))

        divMenu=t.Div( menu, klass="navbar-menu" )

        return t.Nav( divBrand, divMenu, role="navigation",aria_label="main navigation")

    def evtSelectEntry(self,name):
        callback=self.entries[name]
        callback()


class MyTabs(GTag):

    def init(self,value, choices:list):
        assert value in choices
        self.value=value
        self.choices=choices

    @bind
    def renderUL(self):
        u=t.Ul()
        for idx,name in enumerate(self.choices):
            isActive="is-active" if self.value==name else None
            u.add( t.Li(t.A(name,onclick=self.bind.select(idx)), klass=isActive ) )
        return u

    def build(self): # dynamic rendering !
        return t.Tabs( self.renderUL() )

    def select(self,idx):
        self.value=self.choices[idx]

class MyRadioButtons(GTag):

    def init(self,value, choices:list):
        assert value in choices
        self.value=value
        self.choices=choices


    @bind
    def build(self):
        o=t.Div(klass="control")
        for idx,i in enumerate(self.choices):
            o.add('<label class="radio">',
                t.Input(
                    type="radio",
                    klass="radio", # override
                    name="r%s"%id(self),
                    onclick=self.bind.onchange(idx),
                    checked=(self.value==i) and "true" or "",
                    ),
                i,
                "</label>"
            )
        return o

    def onchange(self,idx):
        self.value = self.choices[idx]

class MySelect(GTag):

    def init(self,value, choices:list):
        assert value in choices
        self.value=value
        self.choices=choices

    @bind
    def build(self):
        s=t.Select( onclick=self.bind.onchange("this.value"),style="width:100%" )
        for idx,i in enumerate(self.choices):
            s.add( t.Option(i,value=idx,selected=(self.value==i) and "true" or ""))
        return t.Div(s,klass="select")

    def onchange(self,idx):
        self.value = self.choices[int(idx)]