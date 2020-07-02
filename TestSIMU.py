
from gtag import GTag,Tag,render,GSimu



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


s=GSimu( A(0),True)

s.start()

for r in s.event(s.get("C"),"evt"):
    print(r)
assert '<div id="C">1</div>' in r["content"]
