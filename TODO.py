#!/usr/bin/python3 -u
from gtag import GTag,Tag,local

#TODO: write a UT for that !!!!!

class Comp(GTag):
    def init(self,value):
        self.value=value
    def build(self):
        return Tag.div(
            Tag.div( "hello", self.value ),
            Tag.div( "hello", self.bind.value ),
            Tag.button( "Click me", onclick=self.bind.clickMe(1) ),
        )
    # @local                        # <- here is the trick
    def clickMe(self,inc):
        self.value+=inc

class App(GTag):
    size=(200,200)
    def init(self):
        self.c2=Comp(42)
    def build(self): # build will rebuild innerchilds too (without that : trouble !!!)
        return Tag.div( self.c2,self.c2.value )

app=App()
app.run()