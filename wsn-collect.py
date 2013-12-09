from flask import Flask, url_for, redirect, render_template, Response, request
from wsn_driver.driver import WsnCollectDriver
import json

app = Flask(__name__)
app_driver = WsnCollectDriver()


def parse_data(raw, item_delimiter=', ', key_delimiter=': '):
    result = dict()
    for kv in raw.split(item_delimiter):
        key, val = kv.split(key_delimiter)
        try:
            result[key] = int(val)
        except ValueError:
            result[key] = val

    return result

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


@app.route('/load/<ip>/sink')
def load_sink(ip):
    data = app_driver.get_storage().get(ip)
    nl = [parse_data(_d) for _d in data if 'ttl' in _d]
    var_array = ','.join([str(val['ttl']) for val in nl])
    return render_template('fragments/tx-stats.html', data=nl, var_array=var_array)


@app.route('/load/<ip>/accel/<dtype>')
def load_accel(ip, dtype):
    data = app_driver.get_storage().get(ip)
    nl = [parse_data(_d) for _d in data]
    var_array_x = ','.join([str(val['acx']) for val in nl])
    var_array_y = ','.join([str(val['acy']) for val in nl])
    if dtype == 'html':
        return render_template('fragments/mote-accel.html',
                               current_mote=ip,
                               data=nl,
                               var_array_x=var_array_x[-500:],
                               var_array_y=var_array_y[-500:])
    elif dtype == 'json':
        return Response(json.dumps({'datax': nl[-1]['acx'], 'datay': nl[-1]['acy']}), content_type='application/json')


@app.route('/load/motelist')
def load_mote_list():
    data = app_driver.get_storage().get_all()
    data_list = list()
    for key in data:
        nlist = [kv for kv in data[key] if 'ttl' not in kv]
        _d = {
            'ip': key,
            'data': parse_data(nlist[-1])
        }
        data_list.append(_d)
    return render_template('fragments/mote-list.html', data=data_list)

@app.route('/')
def home():
    data = app_driver.get_storage().get_all()

    data_list = [{'ip': key, 'data': parse_data(data[key][-1])} for key in data]
    return render_template('index.html', data=data_list)


@app.route('/graph')
def graph():
    return render_template('graph.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
