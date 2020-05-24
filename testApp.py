from gtag import GTag,bind
from gtag.gui import A,Box,Button,Div,HBox,Input,Li,Nav,Section,Tabs,Text,Ul,VBox

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


class MyBox(GTag):
    def init(self,content):
        self.content=content

    @bind
    def build(self):
        if self.content!=None:
            o = Div(klass="modal is-active")
            o.add( Div(klass="modal-background",onclick=self.bind.close()) )
            o.add( Div( Box(self.content),klass="modal-content") )
            o.add( Div(klass="modal-close is-large",aria_label="close",onclick=self.bind.close()) )
            return o

    def close(self):
        self.content=None


class MyTabs(GTag):
    def init(self,selected:int):
        self.selected=selected
        self.tabs=[]

    def addTab(self,title):
        self.tabs.append(title)

    @bind
    def renderUL(self):
        u=Ul()
        for idx,title in enumerate(self.tabs):
            isActive="is-active" if self.selected==idx+1 else None
            u.add( Li(A(title,onclick=self.bind.select(idx+1)), klass=isActive ) )
        return u

    def build(self): # dynamic rendering !
        return Tabs( self.renderUL() )

    def select(self,idx):
        self.selected=idx


class MyInput(GTag):

    def init(self,txt):
        self.v=txt

    def build(self):
        return Input(type="text",value=self.v,onchange=self.bind.onchange("this.value"))

    def onchange(self,txt):
        self.v = txt

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
            HBox(MyInput(self.bind.txt ),Text(self.bind.txt)),
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

    def init(self,sel):
        self.selected=sel

    def build(self):
        t=MyTabs(self.bind.selected)
        t.addTab("tab1")
        t.addTab("tab2")
        t.addTab("tab3")
        return Div(t,Box(self.renderContent()))

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
        self.selectedTab=1


    @bind
    def build(self): # DYNAMIC RENDERING HERE !
        divBrand=Div( klass="navbar-brand" )
        divBrand.add( A("<b>GTag Test App</b>",klass="navbar-item") )
        divBrand.add( A('<span aria-hidden="true"></span><span aria-hidden="true"></span><span aria-hidden="true"></span>',
                        role="button",
                        klass="navbar-burger burger",
                        aria_label="menu",
                        aria_expanded="false",
                        data_target="navbarBasicExample",
                        onclick="this.classList.toggle('is-active');document.querySelector('.navbar-menu').classList.toggle('is-active')") )

        menu=Div(klass="navbar-start")
        menu.add( A("Page1", klass="navbar-item", onclick=self.bind.setPage(1)))
        menu.add( A("Page2 (%s)"% int(self.nb), klass="navbar-item", onclick=self.bind.setPage(2)))
        menu.add( A("Page3", klass="navbar-item", onclick=self.bind.setPage(3)))
        menu.add( A("Exit", klass="navbar-item", onclick=self.bind.doExit() ) )

        divMenu=Div( menu, klass="navbar-menu" )

        if self.page==1:
            page=Page1(self.bind.n,self.bind.txt)
        elif self.page==2:
            page=Page2(self.bind.nb)
        elif self.page==3:
            page=Page3(self.bind.selectedTab)
        else:
            page="no"

        return Div(
            Nav( divBrand, divMenu, role="navigation",aria_label="main navigation"),
            Section( Div( "<br>", page, klass="container") ),
            MyBox( self.bind.msg )
        )

    def doExit(self):
        self.exit(-1)

    def setPage(self,n):
        self.page=n

    def setMBox(self,txt):
        self.msg=txt


if __name__=="__main__":
    app=TestApp( )
    print( app.run(log=False) )
    # print( app.serve(log=False) )