from gtag import GTag,bind
from gtag.gui import A,Box,Button,Div,HBox,Input,Li,Nav,Section,Tabs,Text,Ul,VBox
import gtags as g
from gtags import MyCheckbox

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

    @bind
    def build(self):
        return VBox(
            HBox(g.MyInput(self.bind.txt ),Text(self.bind.txt)),
            MyInc(self.bind.nb),
            MyInc(self.bind.nb),
            Box(self.bind.nb, self.compute()),
            Button("Show mbox",onclick=self.bind.aff())
        )

    def aff(self):
        # self.main.setMBox( self.XXX )
        self.main.setMBox( "helllllllo" )

class Page2(GTag):

    def init(self,b):
        self.nb=b

    def build(self):
        return Div(
            Box("A test page, with a binding value:", self.bind.nb),
            MyInc(self.bind.nb),
            Button("show",onclick=self.bind.kik()),
            Button("show T",onclick=self.bind.kik2()),
        )
    def kik(self):
        self.main.setMBox("yom")
    def kik2(self):
        self.main.setToast("yot")

class Page3(GTag):

    def init(self,sel,rb,so,sb,cb):
        self.selected=sel
        self.rb=rb
        self.so=so
        self.sb=sb
        self.cb=cb

    def build(self):
        t=g.MyTabs(self.bind.selected,["tab1","tab2","tab3"])

        return Div(t,Box(self.renderContent()),
            MyCheckbox(self.cb, "disable all (vv)"),
            HBox(
                Text("You selected",self.bind.rb),
                g.MyRadioButtons(self.bind.rb,["apple","pear","banana"],disabled=self.bind.cb),
            ),
            HBox(
                Text("You selected",self.bind.so),
                g.MySelect(self.bind.so,["apple","pear","banana"],disabled=self.bind.cb),
            ),
            HBox(
                Text("You selected",self.bind.sb),
                g.MySelectButtons(self.bind.sb,["apple","pear","banana"],disabled=self.bind.cb),
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
        self.msg=None #mbox
        self.toast=None #toast
        self.page=1
        self.selectedTab="tab1"
        self.rb="banana"
        self.sb="banana"
        self.so="banana"
        self.cb=False


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
            page=Page3(self.bind.selectedTab,self.bind.rb,self.bind.so,self.bind.sb,self.bind.cb)
        else:
            page="no"

        return Div(
            nav,
            Section( Div( "<br>", page, klass="container") ),
            Button("test toast",onclick=self.bind.setToast(42)),
            Button("test mm",onclick=self.bind.setMBox(42)),
            g.MyBox( self.bind.msg ),
            g.MyToaster( self.bind.toast ),
        )

    def setPage(self,n):
        self.page=n

    def setMBox(self,obj):
        print(">>",obj)
        self.msg=obj
    def setToast(self,obj):
        print(">>>",obj)
        self.toast=obj


if __name__=="__main__":
    app=TestApp( )
    # app=Page3("tab2","banana","banana")
    print( app.run(log=False) )
    # print( app.serve(log=False) )