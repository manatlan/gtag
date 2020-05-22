from gtag import State,GTag,bind
from gtag.gui import Div,Button


class MyState(State):
    def inc(self):
        self.a.set(self.a.get()+1)


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
        return Div(
            ShareState() ,
            Button("++",onclick=self.bind.change()),
            Button("QUIT",onclick=self.bind.quit()+";window.close()"),
        )

    def change(self):
        self.state.inc()

    def quit(self):
        self.exit()


app=Page2( MyState(a=12) )
app.serve()
