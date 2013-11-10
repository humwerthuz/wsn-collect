from flask import Flask, url_for, redirect, render_template
from wsn_driver.driver import WsnCollectDriver

app = Flask(__name__)
app_driver = WsnCollectDriver()


@app.route('/load')
def load():
    data = app_driver.get_storage().get('key')
    if data:
        return "Received [%s] from [%s]" % (data[0], data[1])
    else:
        return "No data available"


@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
