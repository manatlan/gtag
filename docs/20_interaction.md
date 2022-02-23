# A most complex gtag app (with interaction) could look like this

```python
from gtag import GTag, Tag

class Comp(GTag):
    size=(200,100)
    def build(self):
        return Tag.div(
            Tag.span( "hello world" ),
            Tag.button( "Click me", onclick=self.bind.clickMe() ),
        )
    def clickMe(self):
        print("You have clicked")
        
app=Comp()
app.run()
```

!!! important

    - `self.bind.clickMe()` is the way to bind the interaction with the `self.clickMe()`. (It will produce a
      js statement for the onclick event)
    - `self.clickMe()` is an event. At each call, it will update the rendering.
    - the build() method is called at each rendering time.
