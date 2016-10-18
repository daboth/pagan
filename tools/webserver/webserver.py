"""pagan webserver"""
from bottle import Bottle
from bottle import debug
from bottle import request
from bottle import response
from bottle import run
from bottle import static_file
from bottle import template
import hashlib
import logging
import pagan
import tempfile

# TODO() Long input on main page destroys page
# TODO() Better Layout on main page
# TODO() Beautify 404 Error

logging.warning("\n%s\n\
early work in progress, try at your own risk\n\
this will pollute your temp dir!\n\
%s" % ("= "*32, "= "*32))

TEMPLATEINDEX = """<html><head>    <style type="text/css">
            div {
                            position: absolute;
                            height: 80%;
                            width: 80%;
                            top: 10%;
                            left: 10%;
                        }
                    </style></head><body>
<div>
<h1>pagan</h1>
<hr>
Welcome to the python avatar generator for absolute nerds.
<p> Generate your own Avatar.
<p>
<form method=post><input type="search" name="slogan" value="{{slogan}}">
<input type=submit></form>
<hr>
<table width=100%><tr><th>Current Search<th><th>Previous Search</tr><tr><td>
<p>{{slogan}}
<p><img src="/himage/{{sloganHash}}">
<td width=10%>
<td>
<p>{{hist1}}
<p><img src="/himage/{{hist1Hash}}">
<td>{{hist2}}
<p><img src="/himage/{{hist2Hash}}">
<td>{{hist3}}
<p><img src="/himage/{{hist3Hash}}">
</tr></table</tr></table></body></html>
"""

app = Bottle()


@app.error(404)
def error404(code):
    """handle error 404 """
    return """<table><tr><td>
<img src='/himage/1234567890abcde1234567890abcde1234567890abcdef'/ height=300>
<p><center><small>the pagan warriors - to protect and to serve</small>
</td><td>
<h1>These aren't <br> the pages you're<br>looking for.</h1>
</td></tr>
</table>"""


@app.route('/')
@app.post('/')
def index():
    """main functionality of webserver"""
    default = ["pagan", "python", "avatar", "github"]
    slogan = request.forms.get("slogan")

    if not slogan:
        if request.get_cookie("hist1"):
            slogan = request.get_cookie("hist1")
        else:
            slogan = "pagan"

    if not request.get_cookie("hist1"):
        hist1, hist2, hist3, hist4 = default[:]
    else:
        hist1 = request.get_cookie("hist1")
        hist2 = request.get_cookie("hist2")
        hist3 = request.get_cookie("hist3")
        hist4 = request.get_cookie("hist4")

    if slogan in (hist1, hist2, hist3, hist4):
        history = [hist1, hist2, hist3, hist4]
        history.remove(slogan)
        hist1, hist2, hist3 = history[0], history[1], history[2]

    response.set_cookie("hist1", slogan, max_age=60*60*24*30, httponly=True)
    response.set_cookie("hist2", hist1, max_age=60*60*24*30, httponly=True)
    response.set_cookie("hist3", hist2, max_age=60*60*24*30, httponly=True)
    response.set_cookie("hist4", hist3, max_age=60*60*24*30, httponly=True)
    # slogan, hist1, hist2, hist3 = escape(slogan), escape(hist1),\
    #     escape(hist2), escape(hist3)
    md5 = hashlib.md5()
    md5.update(slogan)
    slogan_hash = md5.hexdigest()
    md5.update(hist1)
    hist1_hash = md5.hexdigest()
    md5.update(hist2)
    hist2_hash = md5.hexdigest()
    md5.update(hist3)
    hist3_hash = md5.hexdigest()
    return template(TEMPLATEINDEX, slogan=slogan,
                    hist1=hist1, hist2=hist2, hist3=hist3,
                    sloganHash=slogan_hash, hist1Hash=hist1_hash,
                    hist2Hash=hist2_hash, hist3Hash=hist3_hash)


@app.route('/himage/<hashvalue>')
def hashimage(hashvalue):
    """generate image by hash, usese tempfile :-/"""
    tmpf = tempfile.mkstemp(".png")[1]
    image = pagan.Avatar("")
    try:
        image.img = pagan.generator.generate_by_hash(hashvalue)
    except pagan.generator.FalseHashError:
        return "HashError, see log and check hash value, %s" % hashvalue
    image.save("/", tmpf)
    return static_file(tmpf, root="/")


@app.route('/coverage_exit')
def coverage_exit():
    """exit function for coverage"""
    import os
    import signal
    if os.environ["COVERAGE_EXIT"] != "True":
        return ""
    os.kill(os.getpid(), signal.SIGTERM)

debug(True)
run(app, host='localhost', port=8080)
