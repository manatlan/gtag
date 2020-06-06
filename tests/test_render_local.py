if __name__=="__main__":
    import sys,os
    sys.path.insert(0,os.path.dirname(os.path.dirname(__file__)))


from gtag import GTag,Tag,local
import pytest

def test_redraw_global():
    class C(GTag):
        def init(self,v):
            self.v=v
            self._id="C" #override id, for the test

        def build(self):
            return Tag.div( self.v )

        def evt(self):
            self.v+=1

    class A(GTag):
        def init(self,v):
            self._id="A" #override id, for the test
            self.v=v
            self.c=C(self.bind.v)

        def build(self):
            return Tag.div( self.c, self.bind.v )


    a=A(0)
    assert str(a)=='<div id="A"><div id="C">0</div> 0</div>'
    a.c.evt()
    assert str(a)=='<div id="A"><div id="C">1</div> 1</div>' # the str() rebuild all
    assert a.v==1
    assert a.c.v==1


def test_redraw_local():
    class C(GTag):
        def init(self,v):
            self.v=v
            self._id="C" #override id, for the test

        def build(self):
            return Tag.div( self.v )

        @local #<- THE ONLY CHANGE ^^
        def evt(self):
            self.v+=1

    class A(GTag):
        def init(self,v):
            self._id="A" #override id, for the test
            self.v=v
            self.c=C(self.bind.v)

        def build(self):
            return Tag.div( self.c, self.bind.v )


    a=A(0)
    assert str(a)=='<div id="A"><div id="C">0</div> 0</div>'
    a.c.evt()
    assert str(a)=='<div id="A"><div id="C">1</div> 1</div>'    # the str() rebuild all
    # but on the screen it should be <div id="A"><div id="C">1</div> 0</div>
    assert a.v==1
    assert a.c.v==1

