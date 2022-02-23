# The simplest gtag app could look like this

```python
from gtag import GTag, Tag

class Comp(GTag):
    size=(200,100)
    def build(self):
        return Tag.span("hello world")

app=Comp()
app.run()
```
Will produce (on Ubuntu 20.04) 

<p align="center"> 
  <img src="https://cdn.glitch.com/a8ab5bc9-a841-4e27-886a-cd261970d57d%2FCapture%20d%E2%80%99%C3%A9cran%20du%202020-06-05%2018-21-39.png?v=1591374151655">
</p>


!!! important

    - Here ... the build() method return a [Tag](tag.md). (but it exactly the same rendering that the previous example)
    - the build() method is called at each rendering time.
