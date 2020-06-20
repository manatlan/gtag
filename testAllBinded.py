#!/usr/bin/python3 -u
from gtag import GTag,Tag,value

class Checkbox(GTag):
    def init(self,value:bool,title:str, disabled=False, onchange=None):
        self.value=value
        self.title=title
        self.disabled=disabled
        self.onchange=onchange

    def build(self):
        o=Tag.div(klass="control")
        o.add('<label class="checkbox">',
            Tag.input(
                checked=value(self.value),
                type="checkbox",
                klass="checkbox", # override
                onclick=self.bind.switch(),
                disabled=bool(self.disabled)
                ),
            self.title,self.value,
            "</label>"
        )
        return o

    def switch(self):
        print("----AV",self.value)
        self.value = not self.value
        print("----AP",self.value)
        if self.onchange: self.onchange( value(self.value) )

class XSelect(GTag):
    def init(self,value, choices:list, disabled=False, onchange=None):
        assert value in choices
        self.value=value
        self.choices=choices
        self.disabled=disabled
        self.onchange=onchange

    def build(self):
        s=Tag.select( onchange=self.bind.select(b"this.value"),style="width:100%",disabled=bool(self.disabled) )
        for idx,i in enumerate(self.choices):
            s.add( Tag.option(i,value=idx,selected=(self.value==i)))
        return Tag.div(s,klass="select")

    def select(self,idx):
        self.value=self.choices[int(idx)]
        if self.onchange: self.onchange( value(self.value) )


class Btn(GTag):
    def init(self,v):
        self.v=v
    def build(self):
        return Tag.div(
            self.v,
            Tag.button("++",onclick=self.bind.add()),
            style="border:2px solid red"
        )
    def add(self):
        self.v+=1


class App(GTag):
    size=(400,150)

    def init(self):
        self.cpt = 0
        self.v="1"
        self.cb=False

    def build(self):
        return Tag.div(
            self.cpt,
            Btn(self.cpt),
            XSelect(self.v,list("123")),
            Checkbox(self.cb,"yoo"),self.cb,
            Tag.button("EXIT",onclick=self.bind.exxx())
        )
    def exxx(self):
        self.exit(4)
        
app=App()
# print(type(app.v))
app.run(log=False)
