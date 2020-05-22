from gtag import State,GTag
from gtag.gui import Div


class MyState(State):
    def __init__(self):
        super().__init__( a=12 )

    def change(self,nv):
        self.a.set(nv)


class ShareState(GTag):

    def build(self):
        return Div( "hello",
            self.state.a
        )


class Page2(GTag):

    def __init__(self,s):
        self.state=s        # <- self.state will be shared will all gtag (kind of mixins)
        super().__init__()

    def build(self):
        return Div( ShareState() )

app=Page2( MyState() )
app.serve()
