from gtag import GTag,ReactiveProp,bind,Tag
from gtag.gui import A,Body,Box,Button,Div,HBox,Input,Li,Nav,Section,Tabs,Text,Ul,VBox
import types

class Star(Tag): # a Star tag for the tests bellow
    tag="Star"
    def __init__(self,v):
        super().__init__("*(%s)"%v)
        self.id="%s" % hex(id(self))[2:]

class StaticComputed(GTag): # GOOD PRATICE !!
    """ A gtag component with a property bind'ed and a method binded (computed) """
    def __init__(self,n):
        self.n=n
        super().__init__()

    @bind # -> ReactiveMethod
    def stars(self):
        return Text( *[Star(i) for i in range(int(self.n))] )

    @bind
    def nnn(self,c):
        return c * self.n

    def build(self):
        return Text(self.nnn("X"), self.stars() )

t=StaticComputed(2)
print(t)
t.run()


# from gtag import GTag,bind,ReactiveMethod
# from gtag.tags import Div,Tag
# import pytest

# class My(GTag):
#     size=(100,100)
#     def init(self):
#         self.exit(42)
#     def build(self):
#         return Div("hello")

# m=My()
# assert m.run(log=True)==42
