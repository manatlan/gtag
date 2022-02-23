# A most complex gtag app (re-use the component) could look like this

```python
from gtag import GTag,Tag

class Comp(GTag):
    def init(self,value):
        self.value=value
    def build(self):
        return Tag.div(
            Tag.span( "hello", self.value ),
            Tag.button( "Click me", onclick=self.bind.clickMe(1) ),
        )
    def clickMe(self,inc):
        self.value+=inc

class App(GTag):
    size=(200,200)
    def init(self,v1,v2,v3):
        self.v1=v1
        self.v2=v2
        self.v3=v3
    def build(self):
        return Tag.div( Comp(self.v1), Comp(self.v2), Comp(self.v3) )

app=App(1,2,3)
app.run()
```

