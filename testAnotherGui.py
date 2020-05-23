from gtag import GTag,ReactiveProp,bind,Tag

"""
An exemple of using another set of tags
(here based on materialize.css)
Just to show how to build its own gui !
"""

class MaterializeTag(Tag):
    css="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css"  # can be a list of str too
    js="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js"     # can be a list of str too

###################################################################################################
## here are Materialize specific tags
###################################################################################################
class Div(MaterializeTag):
    tag="div"

class Text(MaterializeTag):
    tag="p"

class Button(MaterializeTag):
    tag="button"
    klass="waves-effect waves-light btn"

####################################################################################################
####################################################################################################
####################################################################################################

class AnotherGUI(GTag):
    size=(200,200)

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


