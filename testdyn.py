from gtag import GTag
from gtag.tags import A,Body,Box,Button,Div,HBox,Input,Li,Nav,Section,Tabs,Text,Ul,VBox



class STag(GTag):
    def __init__(self,n):
        self.n=n
        super().__init__()
    def build(self):
        stars="*" * self.bind.n.get()
        return Text(self.bind.n,stars)

class DTag(GTag):
    def __init__(self,n):
        self.n=n
        super().__init__()
    def render(self):
        stars="*" * self.bind.n.get()
        return Text(self.bind.n,stars)

class SSTag(GTag):
    def __init__(self,n):
        self.n=n
        super().__init__()

    def compute(self):
        class R:
            def __str__(zelf):
                return "*" * self.n
        return R()

    def build(self):

        return Text(self.bind.n,self.compute())



tags=[STag(3),DTag(3),SSTag(3)]
for t in tags:
    print(t)
for t in tags:
    t.n=42
    print(t)

