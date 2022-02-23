# Understand the lifecycle

At this step, you know 90% of the **GTag**'s features ! 

But you must understand how it works ...

Consider this basic component :
```python
class Comp(GTag):
    def init(self,value,cpt):
        self.value=value
    def build(self):
        return Tag.button( self.value, onclick=self.bind.inc() )
    def inc(self):
        self.value+=1
```

You can use it like this (dynamic approach):
```python
class App(GTag):

    def init(self):
        self.v=0

    def build(self):
        return Tag.div(
            Comp(self.v),
            self.v,
        )
```
!!! note
    The component is (re)created at each app's rendering. Because, it is declared in the app's `build()` method. 

Or like that (static approach):
```python
class App(GTag):

    def init(self):
        self.c=Comp(0)

    def build(self):
        return Tag.div(
            self.c,
            self.c.value,
        )
```

!!! note
    The component is created in the app's `init()` (just one time). And it's just (re)rendered at each app's rendering. 
    In this case, it holds the value (but it could be binded from the parent too)
    
Visually : **the result will be exactly the same** ! But under the hood : there are a lot of differences !

There aren't good pratice, it will mainly depend on your needs/habits. But you will need to familiarize with this two ways
of doing things.

Dynamic approach is less error proof. Static approach is speeder (?!), but can give headaches and strange results
if bad used (ex: bad used in a dynamic approach)


**TODO: COMPLETE **

