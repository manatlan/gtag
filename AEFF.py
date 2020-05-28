from gtag import GTag,bind
import gtag.gui as t

class Comp(GTag):
    def init(self,value):
        self.value=value
    def build(self):
        return t.Div(
            t.Text( "hello ", self.bind.value ),
            t.Button( "Click me", onclick=self.bind.clickMe() ),
        )
    def clickMe(self):
        self.value+=1

class App(GTag):
    size=(200,200)

    def build(self):
        return t.Div( Comp(1), Comp(2), Comp(3) )

app=App()
app.run()