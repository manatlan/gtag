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

    def init(self,value,type="text",disabled=False,onchange=None):
        self.value=value
        self.type=type
        self.disabled=disabled
        self.onchange=onchange

    def build(self):
        return t.Input(type=self.type,value=self.value,onchange=self.bind.select("this.value"),disabled=bool(self.disabled))

    def select(self,value):
        self.value = value
        if self.onchange: self.onchange(self.value)


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


class Selector(GTag):
    def init(self,value, choices:list, disabled=False, onchange=None):
        assert value in choices
        self.value=value
        self.choices=choices
        self.disabled=disabled
        self.onchange=onchange


    def select(self,idx):
        self.value=self.choices[int(idx)]
        if self.onchange: self.onchange(self.value)

class MyTabs(Selector): #TODO: implement disabled
    @bind
    def build(self):
        u=t.Ul()
        for idx,i in enumerate(self.choices):
            isActive="is-active" if self.value==i else None
            u.add( t.Li(t.A(i,onclick=self.bind.select(idx)), klass=isActive ) )
        return t.Tabs( u )


class MyRadioButtons(Selector):
    @bind
    def build(self):
        o=t.Div(klass="control")
        for idx,i in enumerate(self.choices):
            o.add('<label class="radio">',
                t.Input(
                    type="radio",
                    klass="radio", # override
                    name="r%s"%id(self),
                    onclick=self.bind.select(idx),
                    checked=(self.value==i),
                    disabled=bool(self.disabled)
                    ),
                i,
                "</label>"
            )
        return o


class MySelect(Selector):
    @bind
    def build(self):
        s=t.Select( onclick=self.bind.select("this.value"),style="width:100%",disabled=bool(self.disabled) )
        for idx,i in enumerate(self.choices):
            s.add( t.Option(i,value=idx,selected=(self.value==i)))
        return t.Div(s,klass="select")

class MySelectButtons(Selector):
    @bind
    def build(self):
        h=t.HBox()
        for idx,i in enumerate(self.choices):
            isActive="button " + "is-active" if self.value==i else None
            h.add( t.Button(i,onclick=self.bind.select(idx), klass=isActive,disabled=bool(self.disabled) ) )
        return h


class MyCheckbox(GTag):
    def init(self,value:bool,title:str, disabled=False, onchange=None):
        self.value=value
        self.title=title
        self.disabled=disabled
        self.onchange=onchange

    @bind
    def build(self):
        o=t.Div(klass="control")
        o.add('<label class="checkbox">',
            t.Input(
                checked=bool(self.value),
                type="checkbox",
                klass="checkbox", # override
                onclick=self.bind.switch(),
                disabled=bool(self.disabled)
                ),
            self.title,
            "</label>"
        )
        return o

    def switch(self):
        self.value = not self.value
        if self.onchange: self.onchange(self.value)

if __name__=="__main__":

    class M(GTag):
        size=(100,100)
        def init(self):
            self.v=False
        def build(self):
            return t.Div(
                MyCheckbox(self.bind.v,"ok ?"),
                MyRadioButtons(1,[1,2,3],self.bind.v),
                self.bind.v
            )

    app=M()
    app.run()