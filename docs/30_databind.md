# A most complex gtag app (the interaction changes the value) could look like this

```python
from gtag import GTag,Tag

class Comp(GTag):
    size=(200,100)
    def init(self,value):
        self.value=value
    def build(self):
        return Tag.div(
            Tag.span( "hello", self.value ),
            Tag.button( "Click me", onclick=self.bind.clickMe(1) ),
        )
    def clickMe(self,inc):
        self.value+=inc

app=Comp(0)
app.run()
```
!!! important

    - the `init()` method is called at constructor time, to initialize your component ;-) 
      (see it like a classical `__init__()`, the real `__init__` is reserved by the framework, to make the magic)
    - the build() method is called at each rendering time, so the value will be incremented visually.

