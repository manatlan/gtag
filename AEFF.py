from gtag import *
import datetime
class My(GTag):
    size=(100,100)
    def build(self):
        return Tag.div("hello",Tag.button("w",onclick=self.bind.evt(False,b"window.innerWidth",None,0,datetime.datetime.now(),p=32,t="hello") ))
    async def evt(self,*a,**k):
        print(a,k)
        self.exit()


m=My()
m.run()
