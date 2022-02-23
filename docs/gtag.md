# GTag

**TODO: COMPLETE**

## static properties
### headers
## properties

-----------------------------------------------------------------------------------------
### main
Get the main GTag (which it's the grandfather of all GTag).

!!! note
    In fact, it returns a proxy object, which expose all properties as "Reactive properties" and expose all methods.

!!! important
    The **main one** is the perfect place to store the state of your app. Because the state is available from all
    gtags childs. (there is one main gtag by session (when runned in serve mode))



-----------------------------------------------------------------------------------------
### parent
Get the parent GTag (which has created this child). It's `None` if you are in the main GTag. 

!!! note
    In fact, it returns a proxy object, which expose all properties as "Reactive properties" and expose all methods.

-----------------------------------------------------------------------------------------
## method to implement

-----------------------------------------------------------------------------------------
### init(...)
The constructor, if you want to initialize the state of your component.

-----------------------------------------------------------------------------------------
### build()
The method to build the **Tag**.

-----------------------------------------------------------------------------------------
## produce js in the component 

call `self("<js>")` see [Interact With js](55_interact_with_js.md)

**TODO: EXPLAIN MORE**

-----------------------------------------------------------------------------------------
## Run features
Theses are [the same as guy](https://guy-docs.glitch.me/run/).
(so you can expect : autoreload, limit one instance at runtime, etc ...)

but you can add a `start` event to call a first async method at start ...
**TODO: EXPLAIN MORE**

-----------------------------------------------------------------------------------------
### run

Use this to run as a desktop app (*), or a mobile application (only android)

(*): you will need to have chrome/chromium installed, because it reuse it as a container.

-----------------------------------------------------------------------------------------
### runCef

Use this to run as a desktop app (use cefpython3 in place of chrome/chromium ^^). So it can be a standalone app (like an electron app).

-----------------------------------------------------------------------------------------
### serve

Use this to run as a web app. In this case, there will be one main gtag per browser session.
