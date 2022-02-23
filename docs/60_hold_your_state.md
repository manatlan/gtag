# Hold your app state

Each components got its own state. All components are recreated at each rendering .... except one : the **main** one.

The **main** one is the grandfather of all others. It's the one which start the app ! 
It's the only component which will keep its state. And so, __it's the perfect place to hold your state app__ !

!!! note
    If your application is runned in server mode (using `app.serve()`) : You will have a **main one** per browser session.
    So your state is per session ! If you want to share a state between session, use your process state !
    
Each **gtag** components can access to :

 - the main one : with `self.main` (If you are in the main one: `self.parent` is `self`)
 - the parent one : with `self.parent` (the gtag's parent which has created this child). If you are in the main one, `self.parent` is `None`
 
So a child's component can interact with its parent : thru `self.parent`.
 
So any components can interact which the main one, thru `self.main`.
 
## Good practice
 
A good practice, if you came from flux/redux/vuex (or others state manager) : is to reuse the sames concepts/patterns in the **main one**.
 
You declare main's methods to do your mutations/actions on the main'state. And, in your childs, you mutate your state with main's methods.