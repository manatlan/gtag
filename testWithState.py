from gtag import GTag,bind,Tag
from gtags import *

class ShareState(GTag):

    def build(self):
        return Tag.div( "hello",
            self.main.a,        # <-- the shared state is the main instance !
        )

class Page2(GTag):
    size=(200,100)

    def init(self):
        self.a=12

    def build(self):
        return Tag.div(
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
app.serve(log=False)

