from gtag import GTag,Tag
import pytest


# def test_it():
#     class App(GTag):
#         def build(self):
#             return "hello"
#     a=App()
#     assert a.script==None


# def test_inBuild_with_clone():
#     class App(GTag):
#         def build(self):
#             self.script="api(%s)" % self.id
#             return "hello"
#     a=App()
#     assert a.script=="api(%s)"%a.id    #build() is called at init !
#     b=a._clone()
#     assert b.script!="api(%s)"%a.id
#     assert b.script=="api(%s)"%b.id

# def test_inInit_with_clone():
#     class App(GTag):
#         def init(self,v):
#             self.v=v
#             self.script="api(%s)" % self.id
#         def build(self):
#             return "hello"
#     a=App(1)
#     assert a.script=="api(%s)"%a.id    #build() is called at init !
#     assert a.v==1

#     b=a._clone()
#     assert b.script!="api(%s)"%a.id
#     assert b.script=="api(%s)"%b.id
#     assert b.v==1

def test_scripts():

    class App(GTag):

        def init(self):
            self.cpt = 0
            self("alert(1)")

        def build(self):
            self("alert(2)")
            return Tag.div(
                self.cpt,
                Tag.button("++",onclick=self.bind.add())
            )

        def add(self):
            self.cpt+=1
            self("alert(3)")


    app=App()
    assert app._scriptsInInit == ['alert(1)']
    assert app._scripts==['alert(1)']

    app=App()
    app._rebuild()
    app._rebuild()
    app._rebuild()
    assert app._scripts==['alert(1)', 'alert(2)']

    app2=app._clone()
    assert app2._scriptsInInit == ['alert(1)']
    assert app2._scripts==['alert(1)', 'alert(2)']

    assert app._scripts==['alert(1)', 'alert(2)']
