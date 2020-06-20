from gtag import GTag,Tag,render
from gtag.gtags import *

"""
the most advanced gtag example, in the world ;-)
(mainly used for manual tests)
"""

class MyInc(GTag):
    def init(self,v=0):
        self.cpt=v

    def build(self):
        return HBox(
            Button("-",onclick=self.bind.addV(-1),klass="button is-light" ),
            Text(self.cpt,style="text-align:center"),
            Button("+",onclick=self.bind.addV(1),klass="button is-light" ),
        )

    def addV(self,v):
        self.cpt+=v


class Login(GTag):
  def init(self,callback):
    self.passwd=""
    self.callback=callback

  def build(self):
    return VBox(
      HBox( Text("Password"), InputText(self.passwd,type="password") ),
      Button("OK",onclick=self.bind.check())
    )

  def check(self):
    self.callback(self.passwd)


class Page1(GTag):

    def init(self,nb,txt):
        self.nb=nb
        self.txt=txt


    def build(self):
        return VBox(
            HBox(InputText(self.txt ),Text(self.txt)),
            MyInc(self.nb),
            MyInc(self.nb),
            Box(self.nb, Tag.div( "⭐" * int(self.nb) )),
            Button("Show mbox",onclick=self.bind.aff())
        )

    def aff(self):
        self.main.setMBox( MyInc(self.nb) )  #<-- auto-innerChild !

class Page2(GTag):

    def init(self,b):
        self.nb=b

    def build(self):
        return Tag.div(
            Box("A test page, with a binding value:", self.nb),
            MyInc(self.nb),
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
        tabs=Tabs(self.selected,["tab1","tab2","tab3"])

        return Tag.div(tabs,Box(self.renderContent()),
            Checkbox(self.cb, "disable all (vv)"),
            HBox(
                Text("You selected",self.rb),
                RadioButtons(self.rb,["apple","pear","banana"],disabled=self.cb,onchange=self.realCallback),
            ),
            HBox(
                Text("You selected",self.so),
                Select(self.so,["apple","pear","banana"],disabled=self.cb),
            ),
            HBox(
                Text("You selected",self.sb),
                SelectButtons(self.sb,["apple","pear","banana"],disabled=self.cb),
            )
        )

    def realCallback(self,x):
        self.main.setToast("Changed to %s"%x)

    def renderContent(self):
        if self.selected=="tab2":
            rows=[[1,2,3,4],[1,2,3,4],[1,2,3,4]]
            return Table(rows,["Col1","Col2","Col3","Col4"])
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


    def build(self): # DYNAMIC RENDERING HERE !
        nav= Nav("gtag-demo",{
            "Page1":lambda: self.setPage(1),
            "Page2 (%s)"% int(self.nb):lambda: self.setPage(2),
            "Page3":lambda: self.setPage(3),
            "Login":lambda: self.doLogin(),
        },{
            "exit":lambda: self.exit(-1),
        })

        if self.page==1:
            page=Page1(self.n,self.txt)
        elif self.page==2:
            page=Page2(self.nb)
        elif self.page==3:
            page=Page3(self.selectedTab,self.rb,self.so,self.sb,self.cb)
        else:
            page="no"
        return Tag.div(
            nav,
            Section( Tag.div( "<br>", page, klass="container") ),
            Button("test mbox",onclick=self.bind.setMBox(42)),
            Button("test toast",onclick=self.bind.setToast(42)),
            MBox( self.msg ),
            Toaster( self.toast ),
        )

    def setPage(self,n):
        self.page=n

    def setMBox(self,obj):
        self.msg=obj
    def setToast(self,obj):
        self.toast=obj

    def doLogin(self):
        self.setMBox( Login( self.check ) )

    def check(self,p):
        print("====>",p)
        self.setMBox( None )

if __name__=="__main__":
    app=TestApp( )
    # app=Page1(1,"kkk")
    print( app.run(log=False) )
    # print( app.serve(log=False) )
