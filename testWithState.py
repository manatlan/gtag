from gtag import State,GTag
from gtag.gui import Div


class MyState(State):
    def __init__(self):
        super().__init__( a=12 )

    def change(self,nv):
        self.a.set(nv)

GTag.setState( MyState( ) )


class Page2(GTag):

    def build(self):
        return Div( "hello",
            self.state.a
        )

app=Page2()
app.run()
