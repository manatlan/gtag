from gtag import GTag,Tag
from gtag.gui import Div

# def test_GTagApp():
#     class My(GTag):
#         size=(100,100)
#         def init(self):     #<- this works only for the main gtag TODO: should do something for others (liflecycle events)
#             self.exit(42)
#         def build(self):
#             return Div("hello")

#     m=My(None)
#     assert isinstance(m._tag,Tag)
#     assert ">hello<" in str(m)
#     assert m.run()==42

# def test_GTagAppBad():
#     class My(GTag):
#         size=(100,100)
#         def init(self):     #<- this works only for the main gtag TODO: should do something for others (liflecycle events)
#             self.exit(42)
#         def build(self):
#             return None

#     m=My(None)  # no css included (in guy win)
#     assert str(m)==""
#     assert m.run()==42

