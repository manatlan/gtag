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

    def build(self):
        return Div(
            ShareState(self) ,
            Button("++",onclick=self.bind.change()),
            Button("QUIT",onclick=self.bind.quit()+";window.close()"),
        )

    def change(self):
        print(self.state._id,self.state.a)
        self.state.inc()

    def quit(self):
        self.exit()


app=Page2( MyState(a=12) )
print(app)
# app42=Page2( MyState(a=42) )
# print(app42)
# app.serve()
