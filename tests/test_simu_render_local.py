if __name__=="__main__":
    import sys,os
    sys.path.insert(0,os.path.dirname(os.path.dirname(__file__)))


from gtag import GTag,Tag,render,GSimu
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
            self.c=C(self.v)

        def build(self):
            return Tag.div( self.c, self.v )

    s=GSimu( A(0),False)
    s.start()
    rr=s.event(s.get("C"),"evt")
    assert '<div id="A"><div id="C">1</div> 1</div>' in rr[-1]["content"]





def test_redraw_local():
    class C(GTag):
        def init(self,v):
            self.v=v
            self._id="C" #override id, for the test

        def build(self):
            return Tag.div( self.v )

        @render.local
        def evt(self):
            self.v+=1

    class A(GTag):
        def init(self,v):
            self._id="A" #override id, for the test
            self.v=v
            self.c=C(self.v)

        def build(self):
            return Tag.div( self.c, self.v )


    s=GSimu( A(0),False)
    s.start()
    rr=s.event(s.get("C"),"evt")
    assert '<div id="C">1</div>' in rr[-1]["content"]


def test_redraw_none():
    class C(GTag):
        def init(self,v):
            self.v=v
            self._id="C" #override id, for the test

        def build(self):
            return Tag.div( self.v )

        @render.none
        def evt(self):
            self.v+=1

    class A(GTag):
        def init(self,v):
            self._id="A" #override id, for the test
            self.v=v
            self.c=C(self.v)

        def build(self):
            return Tag.div( self.c, self.v )


    s=GSimu( A(0),False)
    s.start()
    rr=s.event(s.get("C"),"evt")
    assert rr[-1] is None


def test_redraw_parent():
    class C(GTag):
        def init(self,v):
            self.v=v
            self._id="C" #override id, for the test

        def build(self):
            return Tag.div( self.v )

        @render.parent
        def evt(self):
            self.v+=1

    class A(GTag):
        def init(self,v):
            self._id="A" #override id, for the test
            self.v=v
            self.c=C(self.v)

        def build(self):
            return Tag.div( self.c, self.v )

    s=GSimu( A(0),False)
    s.start()
    rr=s.event(s.get("C"),"evt")
    assert '<div id="A"><div id="C">1</div> 1</div>' in rr[-1]["content"]
