from gtag.tags import Tabs

def test():
    t=Tabs()
    assert str(t)=='<div class="tabs is-centered"><ul class="ul"></ul></div>'

    t.addTab(False,"t1")
    t.addTab(True,"t2")
    t.addTab(False,"t3")

    assert str(t)=='<div class="tabs is-centered"><ul class="ul"><li class="li"><a class="a">t1</a></li> <li class="is-active"><a class="a">t2</a></li> <li class="li"><a class="a">t3</a></li></ul></div>'

