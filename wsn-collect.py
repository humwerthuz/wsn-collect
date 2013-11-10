from flask import Flask
from wsn_driver.driver import WsnCollectDriver

app = Flask(__name__)
app_driver = WsnCollectDriver()

@app.route('/')
def hello_world():
    data = app_driver.get_storage().get('key')
    if data:
        return "Received [%s]" % data
    else:
        return "No data available"


if __name__ == '__main__':
    app.run()
