## Interact with js, in your binded events

```python
from gtag import GTag,Tag

class InputText(GTag):
    def init(self,value):
        self.value=value

    def build(self):
        return Tag.input(
            type="text",
            value=self.value,
            onchange=self.bind.select( b"this.value" )
        )

    def select(self,value):
        self.value = value

class App(GTag):
    size=(200,200)
    def init(self,txt):
        self.txt=txt
    def build(self):
        return Tag.div(
            InputText(self.txt) ,
            self.txt,
        )

app=App("hello")
app.run()
```

!!! note
    - You can interact (your events) with JS side, by surrounding your js statement with `b"<js>"` :
    put a `b` fefore your strings (in py3: it means bytestring, but in **GTag** : it means "bind" ;-) ). 
    Thus, the value of the html input element will be send to the python event/method.


## Interact more !

For power users only (js addicts). The **gtag**'s instance can render javascript code to be executed. When setted, the content
will be executed on JS side, when rendering. It can be very practice to initialize some things in the frontend !

Exemple:
```python
class App(GTag):
    def init(self):
        self.cpt = 0
        self("alert(1)")

    def build(self):
        self("alert(2)")
        return VBox(
            self.cpt,
            Button("++",onclick=self.bind.add())
        )

    def add(self):
        self.cpt+=1
        self("alert(3)")
```

Each call of `self("<js>")` will append the javascript code in the rendering process, and execute them in the frontend, according the order : init > (event) > build.

- when component is rendered, it will call `alert(1)` and `alert(2)` in the frontend.
- when you will click on [++], it will call `alert(1)`, `alert(3)` and `alert(2)` : calling event's `add()` will ends with the `self.build()` !

All script contents will be executed, after rendering (one time at the end), in a [IIFE](https://developer.mozilla.org/fr/docs/Glossaire/IIFE) statement,
with the parameter `tag` valued with the current `domElement` of the gtag.

!!! note
    Understand that everything that is created in this context will be lost after execution.


