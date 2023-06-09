import logging
from xso import XSOMessage, XSOWarning, XSOError, XSOMessageSender
from flask import Flask, request

## If you are running this via wsgi or another Flask app runner,
## make sure you have it available on IP 0.0.0.0. Additionally,
## this MUST run on the same host that XS Overlay is running on.
## That is, it must be running within Windows, not via WSL.

logging.basicConfig(level=logging.DEBUG)
l = logging.getLogger("VR")
app = Flask(__name__)
xs = XSOMessageSender()

@app.route('/vr_notify', methods=['POST'])
def vr_notify(type="default"):
    assert type in {'default','error','warning'}
    title = request.form.get('title', None)
    content = request.form.get('message',None)
    if title is None and content is None:
        l.error('No message received')
        return {'status':'error','reason':'No message received'}, 400
    if title is None:
        l.info("No title received, setting title to message value")
        title = content[:]
        content = ""
    if type == "warning":
        message = XSOWarning(title, content)
    elif type == "error":
        message = XSOError(title, content)
    else:
        message = XSOMessage(title, content)
    if title == "Home Assistant":
        message.icon = "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"
        message.useBase64Icon = True
    xs.send(message)
    return {'status':'success'}

@app.route('/vr_warning', methods=['GET','POST'])
def vr_warning():
    return vr_notify(type="warning")

@app.route('/vr_error', methods=['GET','POST'])
def vr_error():
    return vr_notify(type="error")

if __name__ == "__main__":
    app.run(host="0.0.0.0",port="64209")
