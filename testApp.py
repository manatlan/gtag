from gtag import GTag,bind
import gtag.gui as t
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
        return t.HBox(
                t.Button("-",onclick=self.bind.addV(-1) ),
                t.Text(self.bind.cpt,style="text-align:center"),
                t.Button("+",onclick=self.bind.addV(1) ),
            )

    def addV(self,v):
        self.cpt+=v



class Page1(GTag):

    def init(self,nb,txt):
        self.nb=nb
        self.txt=txt

    @bind
    def compute(self):
        b=t.Div()
        for i in range( int(self.nb) ):
            b.add( "⭐" )
        return b

    def build(self):
        return t.VBox(
            t.HBox(g.MyInput(self.bind.txt ),t.Text(self.bind.txt)),
            MyInc(self.bind.nb),
            MyInc(self.bind.nb),
            t.Box(self.bind.nb, self.compute()),
            t.Button("Show mbox",onclick=self.bind.aff())
        )

    def aff(self):
        # self.main.setMBox( MyInc(42) )    #TODO: permit this !
        self.main.setMBox( "help" )

class Page2(GTag):

    def init(self,b):
        self.nb=b

    def build(self):
        return t.Div(
            t.Box("A test page, with a binding value:", self.bind.nb),
            MyInc(self.bind.nb),
            t.Button("show",onclick=self.bind.kik()),
            t.Button("show T",onclick=self.bind.kik2()),
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
        tabs=g.MyTabs(self.bind.selected,["tab1","tab2","tab3"])

        return t.Div(tabs,t.Box(self.renderContent()),
            MyCheckbox(self.cb, "disable all (vv)"),
            t.HBox(
                t.Text("You selected",self.bind.rb),
                g.MyRadioButtons(self.bind.rb,["apple","pear","banana"],disabled=self.bind.cb,onchange=self.realCallback),
            ),
            t.HBox(
                t.Text("You selected",self.bind.so),
                g.MySelect(self.bind.so,["apple","pear","banana"],disabled=self.bind.cb),
            ),
            t.HBox(
                t.Text("You selected",self.bind.sb),
                g.MySelectButtons(self.bind.sb,["apple","pear","banana"],disabled=self.bind.cb),
            )
        )

    def realCallback(self,x):
        self.main.setToast("Changed to %s"%x)

    @bind
    def renderContent(self):
        if self.selected=="tab2":
            rows=[[1,2,3,4],[1,2,3,4],[1,2,3,4]]
            return t.Table(rows,["Col1","Col2","Col3","Col4"])
        else:
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

        return t.Div(
            nav,
            t.Section( t.Div( "<br>", page, klass="container") ),
            t.Button("test toast",onclick=self.bind.setToast(42)),
            t.Button("test mm",onclick=self.bind.setMBox(42)),
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