# Optimize your rendering

Sometimes, if your component doesn't need to refresh all the app : it can re-render itself only.
In this case, put the `@render.local` on your method/event, like this :

```python
from gtag import GTag,Tag,render

class Comp(GTag):
    def init(self,value):
        self.value=value
    def build(self):
        return Tag.div(
            Tag.span( "hello", self.value ),
            Tag.button( "Click me", onclick=self.bind.clickMe(1) ),
        )
    @render.local                        # <- here is the trick
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

!!! note
    In this case, it makes a lot of sense : because `Comp` doesn't have any interactions with others.
    
**TODO: there is `render.parent` & `render.none` too !!!!!!!!!!!!!!! **