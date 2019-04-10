
from flask import Flask, jsonify, request, Response, render_template
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route('/forecast/<int:store_number>/<int:item_number>/<initial_date>/<final_date>')
def forecast(store_number, item_number, initial_date, final_date):

    date_range = pd.date_range(pd.to_datetime(initial_date), pd.to_datetime(final_date))
    forecast_model_results = pd.DataFrame({'STORE' : store_number, 'ITEM' : item_number, 'DATE' : date_range,\
                                           'MODEL' : 'Facebook Prophet',
                                           'POINT_FORECAST' : np.random.randint(low=15, high=30, size=len(date_range))})

    return render_template("forecast.html",  data=forecast_model_results.to_html())

@app.route('/plot/<int:store_number>/<int:item_number>/')
def forecast_hw(store_number, item_number):

    sales = np.random.rand(50)
    plt.plot(sales)

    return render_template('WebPage1.html', name = plt.show())
