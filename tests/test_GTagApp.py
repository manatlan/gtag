from gtag import GTag,bind,ReactiveMethod
from gtag.tags import Div,Tag
import pytest

def test_GTagApp():
    class My(GTag):
        size=(100,100)
        def init(self):
            self.exit(42)
        def build(self):
            return Div("hello")

    m=My()
    assert m.run()==42
