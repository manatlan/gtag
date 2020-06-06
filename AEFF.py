from gtag import *
class My(GTag):
    size=(100,100)
    def build(self):
        return Tag.div("hello",Tag.button("w",onclick=self.bind.evt(False,None,0,32,"'hello'") ))
    async def evt(self,*a,**k):
        print(a,k)
        self.exit()


m=My()
m.run()
