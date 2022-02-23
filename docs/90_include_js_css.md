# Customize your components

It's the main goal, but waited the end to present you ;-)

Til here, we worked with pure html/js components. But you can use any css/js libraries found on internet to help you to
build marvelous frontend GUI (bulma, tailwind, materialize, etc ...).

Here is an example using the marvelous [materializecss](https://materializecss.com/) :

```python
from gtag import GTag,Tag

class Div(GTag):
    def build(self):
        return Tag.div(*self._args,**self._kargs)

class Text(GTag):
    def build(self):
        return Tag.p(*self._args,**self._kargs)

class Button(GTag):
    def build(self):
        return Tag.button(*self._args,**self._kargs,klass="waves-effect waves-light btn")

class MaterializeApp(GTag):
    size=(200,200)
    headers=[
        Tag.script(src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js"),
        Tag.link(href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css",type="text/css",rel="stylesheet"),
    ]
    
    def build(self):
        return Div(
            Text( "hello" ),
            Button( "Button", onclick=self.bind.print() ),
            Div( Div(klass="indeterminate"), klass="progress" )
        )

    def print(self):
        print("hello")


t=MaterializeApp(None)
t.run()
```

In fact, each **gtag** components can declare `js` or `css` as static properties. There can
be string or list of strings, referencing 'http ressources' or declarative content.

When starting the app, all **gtag**'s js/css will be included in the html/headers, available for all the app/components.

!!! note
    In this example: the http ressources are downloaded from the internet, in frontend side.
    But as a **gtag app** is an advanced **[guy](https://guy-docs.glitch.me/) app** (which embbed its own http server) ;
    you can imagine putting files in the ["static" folder of guy](https://guy-docs.glitch.me/server/#static-content).
    So if your freeze it to a windows/exe, package as a pypi's app or build an apk : it will be automatically embedded in your app.
    **TODO: perhaps a new page for the embedded content with guy's static folder ?!**
  




