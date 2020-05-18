from gtag import GTag,bind
from gtag.tags import A,Body,Box,Button,Div,HBox,Input,Li,Nav,Section,Tabs,Text,Ul,VBox

class Inc(GTag):
    def __init__(self,v=0):
        self.cpt=v
        super().__init__()

    def build(self):    # called at __init__()
        return HBox(
                Button("-",onclick=self.bind.addV(-1) ),         #<- bind GuyCompo event
                Text(self.bind.cpt,style="text-align:center"),
                Button("+",onclick=self.bind.addV(1) ),          #<- bind GuyCompo event
            )

    def addV(self,v):
        self.cpt+=v


class MyInput(GTag):

    def __init__(self,txt):
        self.v=txt
        super().__init__()

    def build(self):
        return Input(type="text",value=self.v,onchange=self.bind.onchange("this.value"))

    def onchange(self,txt):
        self.v = txt



class MyTabs(GTag):

    def __init__(self,selected:int,tabs:list):
        self.selected=selected
        self.tabs=tabs
        super().__init__()

    @bind
    def build(self): # dynamic rendering !
        o = Tabs( )
        for idx,t in enumerate(self.tabs):
            o.addTab( self.selected==idx+1, t, onclick=self.bind.select(idx+1) )
        return o

    def select(self,idx):
        self.selected=idx


class DynCreate(GTag):

    def __init__(self,n):
        self.n=n
        super().__init__()

    @bind
    def build(self):
        b=Box()
        for i in range( int(self.n) ):
            b.add(Inc(i))
        return b

class Page1(GTag):

    def __init__(self):
        self.nb=12
        self.txt="yolo"
        self.selected=2
        super().__init__()

    def build(self):    # called at __init__()
        return VBox(
            MyInput( self.bind.txt ),
            Text(self.bind.txt,self.bind.selected),
            Inc(self.bind.nb),
            Inc(self.bind.nb),
            Inc(self.nb),
            Inc(13),
            Box(self.bind.nb),
            DynCreate(self.bind.nb),
            MyTabs(self.bind.selected,["johan","jim"]),
        )

class Page2(GTag):

    def __init__(self):
        self.nb=12
        super().__init__()

    def build(self):    # called at __init__()
        return VBox(
            Box("A test page, with a binding value:", self.bind.nb),
            Inc(self.bind.nb),
        )

class TestApp(GTag):
    size=(400,300)

    def __init__(self):
        self.obj=Page1()
        super().__init__()

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

        divMenu=Div( klass="navbar-menu" )
        menu=Div(klass="navbar-start")
        menu.add( A("Page1", klass="navbar-item",onclick=self.bind.setPage1() ))
        menu.add( A("Page2", klass="navbar-item",onclick=self.bind.setPage2() ))
        menu.add( A("Exit", klass="navbar-item", onclick=self.bind.doExit() ) )
        divMenu.add( menu )

        return Body(
            Nav( divBrand, divMenu, role="navigation",aria_label="main navigation"),
            Section( Div( "<br>", self.obj, klass="container") ),
        )

    def doExit(self):
        self.exit(-1)

    def setPage1(self):
        self.obj=Page1()

    def setPage2(self):
        self.obj=Page2()

if __name__=="__main__":
    # tag=Multi()
    tag=TestApp()

    print( tag.run() )
