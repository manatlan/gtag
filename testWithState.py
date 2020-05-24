from gtag import GTag,bind
from gtag.gui import Div,Button



class ShareState(GTag):

    def build(self):
        return Div( "hello",
            self.main.a,        # <-- the shared state is the main instance !
        )

class Page2(GTag):
    size=(200,100)

    def init(self):
        self.a=12

    def build(self):
        return Div(
            ShareState() , self.bind.a,
            Button("++",onclick=self.bind.changeState()),
            Button("QUIT",onclick=self.bind.quit()+";window.close()"),
        )

    def changeState(self):
        self.a+=1

    def quit(self):
        self.exit()

###############################################################################

app=Page2( )
GTag._tags={} #<- good try : delete all created object, to be sure to loose them
app.serve(log=False)

