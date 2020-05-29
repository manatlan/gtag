from gtag import gtag


def test_them():
    assert str(gtag.buildCCSTag(None))==""
    assert str(gtag.buildCCSTag(""))==""
    assert str(gtag.buildJSTag(None))==""
    assert str(gtag.buildJSTag(""))==""

    assert str(gtag.buildCCSTag("body {background:yellow}"))=="""<style type="text/css">body {background:yellow}</style>"""
    assert str(gtag.buildCCSTag("http:/yo.css"))=="""<link type="text/css" rel="stylesheet" href="http:/yo.css"></link>"""

    assert str(gtag.buildJSTag("alert(42)"))=="""<script type="text/javascript">alert(42)</script>"""
    assert str(gtag.buildJSTag("http:/yo.js"))=="""<script type="text/javascript" src="http:/yo.js"></script>"""
