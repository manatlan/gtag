from gtag import GTag,Tag

# def test_GTagApp_run():
#     class My(GTag):
#         size=(100,100)
#         def build(self):
#             return Div("hello")
#         def script(self): # just present to close the app after run
#             return self.bind.evtExit(42) # produce js (bindUpdate)
#         def evtExit(self,p):
#             self.exit(p)


#     m=My()
#     assert isinstance(m._tag,Tag)
#     assert ">hello<" in str(m)
#     assert m.run()==42

# def test_GTagApp_serve():
#     class My(GTag):
#         size=(100,100)
#         def build(self):
#             return Div("hello")
#         def script(self): # just present to close the app after run
#             return self.bind.evtExit(42) # produce js (bindUpdate)
#         def evtExit(self,p):
#             self.exit(p)

#     m=My()
#     assert isinstance(m._tag,Tag)
#     assert ">hello<" in str(m)
#     assert m.serve()==42


