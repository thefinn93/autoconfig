#!/usr/bin/env python3
from flask import Flask, request, render_template

import ios
import k9

app = Flask(__name__)
app.config.from_pyfile('config.py', silent=True)
app.config.from_envvar('AUTOCONFIG_SETTINGS', silent=True)


@app.route("/")
def index():
    return render_template('download_config.html')


@app.route('/config')
def getconfig():
    if request.args.get("platform") == "iOS":
        return ios.makeConfig(request.args.get('email'), app.config)
    elif request.args.get("platform") == "K9":
        return k9.makeConfig(request.args.get('email'), app.config)
    else:
        return "Unknown config platform"

if __name__ == "__main__":
    app.run(host="0.0.0.0")
