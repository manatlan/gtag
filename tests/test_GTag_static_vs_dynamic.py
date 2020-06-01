from gtag import GTag,bind,Tag
from gtag.gtag import ReactiveProp


import types



class Star(Tag): # a Star tag for the tests bellow
    tag="Star"
    def __init__(self,v):
        super().__init__("*(%s)"%v)
        self.id="%s" % hex(id(self))[2:]


#############################################################

class Static(GTag):
    """ A full static gtag component without any 'bind' """
    def __init__(self,n):
        self.n=n
        super().__init__(None)

    def stars(self):
        return [Star(i) for i in range( int(self.n) )]

    def build(self):
        return Tag.text(self.n, *self.stars())

class StaticBinded(GTag):
    """ A gtag component with its property bind'ed ! """
    def __init__(self,n):
        self.n=n
        super().__init__(None)

    def stars(self):
        return [Star(i) for i in range(int(self.n))]

    def build(self):
        return Tag.text(self.bind.n, *self.stars())


class StaticComputed(GTag): # GOOD PRATICE !!
    """ A gtag component with a property bind'ed and a method binded (computed) """
    def __init__(self,n):
        self.n=n
        super().__init__(None)

    @bind
    def stars(self):
        return Tag.text( *[Star(i) for i in range(int(self.n))] )

    def build(self):
        return Tag.text(self.bind.n, self.stars() )


class StaticBuildBinded(GTag): # BAD PRACTICE
    """ the build is binded !!!!"""
    def __init__(self,n):
        self.n=n
        super().__init__(None)

    @bind
    def build(self):
        ll=[Star(i) for i in range(int(self.n))]
        return Tag.text(self.n, *ll )



def check(tag,nb,nbstar):
    t=str(tag)
    print("CHECK nb=%s and stars=%s:"%(nb,nbstar),t)
    assert ">%s"%nb in str(t)
    assert str(t).count("<Star") == nbstar


def test_simple():
    """ by default (initial value), all rendered good"""
    iv=2

    tags=[
        Static(iv),
        StaticBinded(iv),
        StaticComputed(iv),
        StaticBuildBinded(iv),
    ]

    for t in tags:
        check(t,iv,iv)

def test_change():
    """ initial value changed between rendered"""
    iv=2
    cv=3

    tags=[
        Static(iv),
        StaticBinded(iv),
        StaticComputed(iv),
        StaticBuildBinded(iv),
    ]

    for t in tags:
        t.n=cv

    check(tags[0],iv,iv)
    check(tags[1],cv,iv)
    check(tags[2],cv,cv) # good
    check(tags[3],cv,cv) # good


def test_rp():
    """ initial value is a reative prop, all is good """
    iv=2

    p=dict(a=iv)
    a=ReactiveProp(p,"a")

    tags=[
        Static(a),
        StaticBinded(a),
        StaticComputed(a),
        StaticBuildBinded(a),
    ]

    check(tags[0],iv,iv)
    check(tags[1],iv,iv)
    check(tags[2],iv,iv)
    check(tags[3],iv,iv)

    p["a"]=3 # change RP to 3

    check(tags[0],3,iv) # really bad !
    check(tags[1],3,iv)
    check(tags[2],3,3) # good
    check(tags[3],3,3) # good



def test_DANGEROUS():
    class StaticComputed(GTag): # GOOD PRATICE !!
        """ A gtag component with a property bind'ed and a method binded (computed) """
        def __init__(self,n):
            self.n=n
            super().__init__(None)

        @bind # -> Str'Able
        def stars(self):
            return Tag.text( *[Star(i) for i in range(int(self.n))] )

        def build(self):
            return Tag.text("-%s-" % self.bind.n, self.stars() ) # <---- DANGEROUS the binded is str'ised at build !!!!

    t=StaticComputed(2)
    assert "-2-" in str(t)

    t.n=3
    assert "-2-" in str(t) # ARGGHHH should be 3 ... but ^^ ... see workarounds vv

def test_DANGEROUS_workaround1():
    class StaticComputed(GTag): # GOOD PRATICE !!
        """ A gtag component with a property bind'ed and a method binded (computed) """
        def __init__(self,n):
            self.n=n
            super().__init__(None)

        @bind # -> Str'Able
        def stars(self):
            return Tag.text( *[Star(i) for i in range(int(self.n))] )

        @bind
        def compute(self):
            return Tag.text("-%s-" % self.n)

        def build(self):
            return Tag.text( self.compute(), self.stars() ) # <---- DANGEROUS the binded is str'ised at build !!!!

    t=StaticComputed(2)
    assert "-2-" in str(t)

    t.n=3
    assert "-3-" in str(t) # good!



def test_DANGEROUS_workaround2():
    class StaticBuildBinded(GTag): # BAD PRACTICE

        def __init__(self,n):
            self.n=n
            super().__init__(None)

        @bind
        def build(self):
            ll=[Star(i) for i in range(int(self.n))]
            return Tag.text("-%s-"%self.n, *ll )

    t=StaticBuildBinded(2)
    assert "-2-" in str(t)

    t.n=3
    assert "-3-" in str(t) # good!
