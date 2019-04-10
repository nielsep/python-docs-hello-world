
from flask import Flask, jsonify, request, Response
app = Flask(__name__)

@app.route('/forecast/<int:store_number>/<int:item_number>/')
def forecast_hw(store_number, item_number):
    # show the user with the given id, the id is an integer
    forecast_values = [12, 4, 6]
    #return 'Store {}, item {}, forecast values are {}'.format(store_number,item_number,forecast_values)
    return jsonify({
        'store': store_number,
        'item': item_number,
        'forecast': forecast_values
    })
