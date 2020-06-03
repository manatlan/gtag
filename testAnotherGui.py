from gtag import GTag,Tag

"""
An exemple of using another set of tags
(here based on materialize.css)
Just to show how to build its own gui !
"""

class Div(GTag):
    def build(self):
        return Tag.div(*self._args,**self._kargs)

class Text(GTag):
    def build(self):
        return Tag.p(*self._args,**self._kargs)

class Button(GTag):
    def build(self):
        return Tag.button(*self._args,**self._kargs,klass="waves-effect waves-light btn")


class AnotherGUI(GTag):
    size=(200,200)
    css="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css"  # can be a list of str too
    js="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js"     # can be a list of str too

    # ^^^ here, it's downloaded from the internet
    # but you can imagine putting files in the "static" folder of guy
    # (see https://guy-docs.glitch.me/server/#static-content)

    def build(self):
        return Div(
                Text("hello"),
                Button("Button",onclick=self.bind.print()),
                Div( Div(klass="indeterminate"), klass="progress")
        )

    def print(self):
        print("hello")


t=AnotherGUI(None)
t.run()


