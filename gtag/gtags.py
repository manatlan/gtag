from gtag import GTag, bind, Tag

"""
An exemple of GTags

the kind of library, you should construct before using "gtag"
"""

class VBox(GTag):
    css="""
div.vbox {display: flex;flex-flow: column nowrap;}
div.vbox > * {flex: 1 1 50%;margin:1px}
    """
    def build(self):
        return Tag.div(*self._args,**self._kargs,klass="vbox")

class HBox(GTag):
    css="""
div.hbox {display: flex;flex-flow: row nowrap;align-items:center}
div.hbox > * {flex: 1 1 50%;margin:1px}
    """
    def build(self):
        return Tag.div(*self._args,**self._kargs,klass="hbox")
# class HBox(Tag):
#     tag="div"
#     klass="columns is-mobile"
#     def __init__(self,*contents,**attrs):
#         super().__init__(**attrs)
#         self.contents=[Div(i,klass="column") for i in list(contents)]
#     def add(self,o):
#         self.contents.append( Div(o,klass="column"))

class Button(GTag):
    css="https://cdn.jsdelivr.net/npm/bulma@0.8.2/css/bulma.min.css"

    def build(self):
        if "klass" not in self._kargs:
            self._kargs["klass"]="button is-light"
        return Tag.button(*self._args,**self._kargs)

class Input(GTag):
    def build(self):
        if "klass" not in self._kargs:
            self._kargs["klass"]="input"
        return Tag.input(*self._args,**self._kargs)

class A(GTag):
    def build(self):
        if "klass" not in self._kargs:
            self._kargs["klass"]="a"
        return Tag.a(*self._args,**self._kargs)
class Box(GTag):
    def build(self):
        return Tag.div(*self._args,**self._kargs,klass="box")

class Text(GTag):
    def build(self):
        return Tag.p(*self._args,**self._kargs,klass="p")

class Section(GTag):
    def build(self):
        return Tag.section(*self._args,**self._kargs,klass="section")


class Table(GTag):
    def init(self,rows:list,cols:list=None):
        self.rows=rows
        self.cols=cols
    def build(self):
        if self.cols:
            h=Tag.thead(*[Tag.th(col) for col in self.cols])
        else:
            h=None
        ll=[]
        for row in self.rows:
            row=row if hasattr(row,"__iter__") else [row]
            ll.append( Tag.tr( *[Tag.td(col) for col in row] ))
        return Tag.table(h,Tag.tbody(*ll),klass="table is-bordered is-striped is-narrow is-hoverable is-fullwidth")

class GBox(GTag):
    def init(self,content):
        self.content=content

    def build(self):
        o = Tag.div()
        if self.content:
            o.klass="modal is-active"
            o.add( Tag.div(klass="modal-background",onclick=self.bind.close()) )
            o.add( Tag.div( Box(self.content),klass="modal-content") )
            o.add( Tag.div(klass="modal-close is-large",aria_label="close",onclick=self.bind.close()) )
        return o

    def close(self):
        self.content=None

class GToaster(GTag):
    def init(self,content):
        self.content=content

    def build(self):
        o=Tag.div()
        if bool(self.content):
            o.style="position:fixed;left:0px;right:0px;bottom:0px;z-index:1000"
            o.klass="notification is-primary"
            o.add( Button(klass='delete',onclick="window.hideToast()") )
            o.add( str(self.content) ) # force to render now !
            self.content=None # clear content ! (so gtag object is possible)
        return o

    def script(self):
        return """
        window.hideToast=function() {if(tag && tag.parentNode) tag.parentNode.removeChild(tag)}
        setTimeout(window.hideToast,2000)
        """

    def close(self):
        self.content=None


class GInput(GTag):

    def init(self,value,type="text",disabled=False,onchange=None):
        self.value=value
        self.type=type
        self.disabled=disabled
        self.onchange=onchange

    @bind
    def build(self):
        return Input(type=self.type,value=self.value,onchange=self.bind.select("this.value"),disabled=bool(self.disabled))

    def select(self,value):
        self.value = value
        if self.onchange: self.onchange(self.value)



class GTextArea(GTag):

    def init(self,value,disabled=False,onchange=None):
        self.value=value
        self.disabled=disabled
        self.onchange=onchange

    @bind
    def build(self):
        return Tag.textarea(self.value,onchange=self.bind.select("this.value"),disabled=bool(self.disabled))

    def select(self,value):
        self.value = value
        if self.onchange: self.onchange(self.value)


class GNav(GTag):
    def init(self,title,entries:dict={}):
        self.title=title
        self.entries=entries

    @bind
    def build(self): # DYNAMIC RENDERING HERE !
        divBrand=Tag.div( klass="navbar-brand" )
        divBrand.add( A("<b>"+self.title+"</b>",klass="navbar-item",href="/") )
        divBrand.add( A('<span aria-hidden="true"></span><span aria-hidden="true"></span><span aria-hidden="true"></span>',
                        role="button",
                        klass="navbar-burger burger",
                        aria_label="menu",
                        aria_expanded="false",
                        data_target="navbarBasicExample",
                        onclick="this.classList.toggle('is-active');document.querySelector('.navbar-menu').classList.toggle('is-active')") )

        menu=Tag.div(klass="navbar-start")
        for k,v in self.entries.items():
            menu.add( A(k, klass="navbar-item", onclick=self.bind.evtSelectEntry("'%s'"%k)))

        divMenu=Tag.div( menu, klass="navbar-menu" )

        return Tag.nav( divBrand, divMenu, role="navigation",aria_label="main navigation",klass="navbar is-fixed-top is-black")

    def evtSelectEntry(self,name):
        callback=self.entries[name]
        callback()


class _Selector(GTag):
    def init(self,value, choices:list, disabled=False, onchange=None):
        assert value in choices
        self.value=value
        self.choices=choices
        self.disabled=disabled
        self.onchange=onchange


    def select(self,idx):
        self.value=self.choices[int(idx)]
        if self.onchange: self.onchange(self.value)

class GTabs(_Selector): #TODO: implement disabled
    @bind
    def build(self):
        u=Tag.ul()
        for idx,i in enumerate(self.choices):
            isActive="is-active" if self.value==i else None
            u.add( Tag.li( A(i,onclick=self.bind.select(idx)), klass=isActive ) )
        return Tag.div( u , klass="tabs is-centered")


class GRadioButtons(_Selector):
    @bind
    def build(self):
        o=Tag.div(klass="control")
        for idx,i in enumerate(self.choices):
            o.add('<label class="radio">',
                Input(
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


class GSelect(_Selector):
    @bind
    def build(self):
        s=Tag.select( onclick=self.bind.select("this.value"),style="width:100%",disabled=bool(self.disabled) )
        for idx,i in enumerate(self.choices):
            s.add( Tag.option(i,value=idx,selected=(self.value==i)))
        return Tag.div(s,klass="select")

class GSelectButtons(_Selector):    #TODO: add disabled
    @bind
    def build(self):
        u=Tag.ul()
        for idx,i in enumerate(self.choices):
            isActive="is-active" if self.value==i else None
            u.add( Tag.li(A(i,onclick=self.bind.select(idx)), klass=isActive ) )
        return Tag.div( u , klass="tabs is-toggle")


class GCheckbox(GTag):
    def init(self,value:bool,title:str, disabled=False, onchange=None):
        self.value=value
        self.title=title
        self.disabled=disabled
        self.onchange=onchange

    @bind
    def build(self):
        o=Tag.div(klass="control")
        o.add('<label class="checkbox">',
            Input(
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
            tt=t.Table([[1,2,3,4],[1,2,3,4]],cols=list("abcd"))
            return Div(tt,
                GCheckbox(self.bind.v,"ok ?"),
                GRadioButtons(1,[1,2,3],self.bind.v),
                GInput("hekk",disabled=self.bind.v),
                GTextArea("hekk",disabled=self.bind.v),
                self.bind.v,
            )

    app=M()
    app.run()
