from gtag import GTag,bind
from gtag.gui import A,Box,Button,Div,HBox,Input,Li,Nav,Section,Tabs,Text,Ul,VBox
import gtags as g

"""
the most advanced gtag example, in the world ;-)
(mainly used for manual tests)
"""

class MyInc(GTag):
    def init(self,v=0):
        self.cpt=v

    def build(self):
        return HBox(
                Button("-",onclick=self.bind.addV(-1) ),         #<- bind GuyCompo event
                Text(self.bind.cpt,style="text-align:center"),
                Button("+",onclick=self.bind.addV(1) ),          #<- bind GuyCompo event
            )

    def addV(self,v):
        self.cpt+=v




class Page1(GTag):

    def init(self,nb,txt):
        self.nb=nb
        self.txt=txt

    @bind
    def compute(self):
        b=Div()
        for i in range( int(self.nb) ):
            b.add( "⭐" )
        return b

    def build(self):
        return VBox(
            HBox(g.MyInput(self.bind.txt ),Text(self.bind.txt)),
            MyInc(self.bind.nb),
            MyInc(self.bind.nb),
            Box(self.bind.nb, self.compute()),
            Button("Show mbox",onclick=self.bind.aff()) #TODO: find better !!!
        )

    def aff(self):
        self.main.setMBox( MyInc(42) )

class Page2(GTag):

    def init(self,b):
        self.nb=b

    def build(self):
        return Div(
            Box("A test page, with a binding value:", self.bind.nb),
            MyInc(self.bind.nb),
            Button("show",onclick=self.bind.kik())
        )
    def kik(self):
        self.main.setMBox("yo")

class Page3(GTag):

    def init(self,sel,rb,so,sb):
        self.selected=sel
        self.rb=rb
        self.so=so
        self.sb=sb

    def build(self):
        t=g.MyTabs(self.bind.selected,["tab1","tab2","tab3"])

        return Div(t,Box(self.renderContent()),
            HBox(
                Text("You selected",self.bind.rb),
                g.MyRadioButtons(self.bind.rb,["apple","pear","banana"]),
            ),
            HBox(
                Text("You selected",self.bind.so),
                g.MySelect(self.bind.so,["apple","pear","banana"]),
            ),
            HBox(
                Text("You selected",self.bind.sb),
                g.MySelectButtons(self.bind.sb,["apple","pear","banana"]),
            )
        )

    @bind
    def renderContent(self):
        return "Content %s" % self.selected


class TestApp(GTag):
    size=(500,400)

    def init(self):
        self.txt="yolo"
        self.n=12
        self.nb=12
        self.msg=None
        self.page=1
        self.selectedTab="tab1"
        self.rb="banana"
        self.sb="banana"
        self.so="banana"


    @bind
    def build(self): # DYNAMIC RENDERING HERE !
        nav= g.MyNav("gtag-demo",{
            "Page1":lambda: self.setPage(1),
            "Page2 (%s)"% int(self.nb):lambda: self.setPage(2),
            "Page3":lambda: self.setPage(3),
            "exit":lambda: self.exit(-1),
        })

        if self.page==1:
            page=Page1(self.bind.n,self.bind.txt)
        elif self.page==2:
            page=Page2(self.bind.nb)
        elif self.page==3:
            page=Page3(self.bind.selectedTab,self.bind.rb,self.bind.so,self.bind.sb)
        else:
            page="no"

        return Div(
            nav,
            Section( Div( "<br>", page, klass="container") ),
            g.MyBox( self.bind.msg )
        )

    def setPage(self,n):
        self.page=n

    def setMBox(self,txt):
        self.msg=txt


if __name__=="__main__":
    app=TestApp( )
    # app=Page3("tab2","banana","banana")
    print( app.run(log=False) )
    # print( app.serve(log=False) )