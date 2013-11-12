from flask import Flask, url_for, redirect, render_template, Response, request
from wsn_driver.driver import WsnCollectDriver
import json

app = Flask(__name__)
app_driver = WsnCollectDriver()


def parse_data(raw, item_delimiter=', ', key_delimiter=': '):
    return {kv.split(key_delimiter)[0]: kv.split(key_delimiter)[1] for kv in raw.split(item_delimiter)}

@app.route("/load/<ip>/last")
def load_last(ip):
    data = app_driver.get_storage().get(ip)
    if data:
        return Response(json.dumps(parse_data(data[-1])), content_type="application/json")
    else:
        return Response(json.dumps({"status": "no data"}), content_type="application/json")


@app.route('/load/<ip>/all')
def load_all(ip):
    data = app_driver.get_storage().get(ip)
    if data:
        return Response(json.dumps(data), content_type="application/json")
    else:
        return Response(json.dumps({"status": "no data"}), content_type="application/json")


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/graph')
def graph():
    return render_template('graph.html')

if __name__ == '__main__':
    app.run()
