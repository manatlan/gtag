from gtag import gtag


def test_them():
    assert str(gtag.CSS("body {background:yellow}"))=="""<style type="text/css">body {background:yellow}</style>"""
    assert str(gtag.CSS("http:/yo.css"))=="""<link type="text/css" rel="stylesheet" href="http:/yo.css"></link>"""

    assert str(gtag.JS("alert(42)"))=="""<script type="text/javascript">alert(42)</script>"""
    assert str(gtag.JS("http:/yo.js"))=="""<script type="text/javascript" src="http:/yo.js"></script>"""
