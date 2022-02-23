# Tag

See **Tag** as an helper to help you to build your HTML elements : that's all. 

## Build your own Tags

Admit that you want to produce a `textarea` html element. You should do something like that :


Now, you can produce `textarea` html elements:
```python
Tag.textarea( )  
    #-> "<textarea></textarea>"
    
Tag.textarea( "content" )  
    #-> "<textarea>content</textarea>"
    
Tag.textarea( "content1", "content2", checked=True, data_info="mine", onclick="alert(42)" ) 
    #-> "<textarea checked data-info='mine' onclick='alert(42)'>content1 content2</textarea>"

Tag.textarea( klass="me" )  
    #-> "<textarea class='me'></textarea>"
```

!!! note
    - As `class` is python reserved keyword, you must use "klass"

!!! important
    The only html attribut you can't set is `id`. Because it is set by **GTag** when rendering the **Tag**.
    But if you need to set it, you can, on the **Tag** instance.(Keep in mind, that if the Tag is the main
    **Tag** produced by the GTag's build method, it may be overrided)

Be aware, that **Tag** is a metaclass, it can produce all what you want :

```python
Tag.My_Reach_Mega_Tag( "content1", klass="yo" ) 
    #-> "<My-Reach-Mega-Tag class="yo">content1</My-Reach-Mega-Tag>"
```


## You can add `content` to a Tag

`content` can be anything, from string to `GTag`, or another `Tag`, anything that is string'able ;-)

```python
t=MyFormTag(name='myform',onsubmit='post(this)')
t.add( MyInputTag(name='login',value='') )
t.add( MyInputTag(name='password', type='password', value='') )
t.add( "ps: the password is 'foo' ;-) ")
```

## You can change/set properties of a Tag

```python
t=MyFormTag(name='myform',onsubmit='post(this)')
t.onsubmit="post2(this)"
t.klass="aClassForMyForm"
t.id="f1"                       # !!!
```
