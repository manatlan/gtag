# The simplest gtag app could look like this

```python
from gtag import GTag

class Comp(GTag):
    size=(200,100)
    def build(self):
        return "hello world"

app=Comp()
app.run()
```
Will produce (on Windows 10) 

<p align="center"> 
  <img src="https://cdn.glitch.com/a8ab5bc9-a841-4e27-886a-cd261970d57d%2FCapture.PNG?v=1590561806946">
</p>


!!! important

    - the build() method is called at each rendering time.
