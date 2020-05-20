from gtag import State


class MyState(State):
    def __init__(self,d):
        super().__init__(**d)

    def change(self,nv):
        self.a.set(nv)

s=MyState( dict(a=12) )

print( type(s.a), s.a)
s.change(42)
print( type(s.a), s.a)

