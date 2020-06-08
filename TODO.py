#!/usr/bin/python3 -u
from gtag import GTag,Tag,local

#TODO: write a UT for that !!!!!

class Comp1(GTag):
    def init(self,value):
        self.value=value
        self.main.cpt1["init"]+=1
    def build(self):
        self.main.cpt1["build"]+=1
        return Tag.div(
            Tag.div( "self=", self.value ),
            Tag.button( "++", onclick=self.bind.clickMe(1) ),
        )
    def clickMe(self,inc):
        self.value+=inc

class Comp2(GTag):
    def init(self,value):
        self.value=value
        self.main.cpt2["init"]+=1
    def build(self):
        self.main.cpt2["build"]+=1
        return Tag.div(
            Tag.div( "self=", self.value ),
            Tag.button( "++", onclick=self.bind.clickMe(1) ),
        )
    def clickMe(self,inc):
        self.value+=inc

class App(GTag):
    size=(200,200)
    def init(self):
        self.cpt1=dict(init=0,build=0)
        self.cpt2=dict(init=0,build=0)

        self.v1=42
        self.c2=Comp2(42)
    def build(self): # build will rebuild innerchilds too (without that : trouble !!!)
        return Tag.div(
            Comp1(self.bind.v1),"exported=",self.v1,              # real child
            self.cpt1,
            "<hr>",
            self.c2,"exported=",self.c2.value,                   # innerchild
            self.cpt2,
        )

app=App()
app.run()