from flask import Flask, jsonify, request, Response, render_template
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

def build_graph(values):
    img = io.BytesIO()
    plt.plot(values)
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return 'data:image/png;base64,{}'.format(graph_url)

### Version 1: Forecast from query-string request
@app.route('/forecastv1/<int:store_number>/<int:item_number>/<initial_date>/<final_date>')
def forecast_web(store_number, item_number, initial_date, final_date):

    date_range = pd.date_range(pd.to_datetime(initial_date), pd.to_datetime(final_date))
    point_forecast = np.random.randint(low=15, high=30, size=len(date_range))
    graph1_url = build_graph(point_forecast)

    forecast_model_results = pd.DataFrame({'STORE' : store_number, 'ITEM' : item_number, 'DATE' : date_range,\
                                           'MODEL' : 'Facebook Prophet',
                                           'POINT_FORECAST' : point_forecast})

    return render_template("forecastv1.html",  data=forecast_model_results.to_html(), graph1=graph1_url)

### Version 2: Forecast from submitted form
@app.route('/forecastv2/request')
def student():
   return render_template('forecastv2request.html')

@app.route('/forecastv2/result',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':

      store_number = request.form['Store']
      item_number = request.form['Item']
      initial_date = request.form['InitialDate']
      final_date = request.form['FinalDate']

      #store_number = '13'; item_number = '32'; initial_date = '2018-01-01'; final_date = '2018-01-05'

      date_range = pd.date_range(pd.to_datetime(initial_date), pd.to_datetime(final_date))
      point_forecast = np.random.randint(low=15, high=30, size=len(date_range))
      graph1_url = build_graph(point_forecast)

      forecast_model_results = pd.DataFrame({'STORE' : store_number, 'ITEM' : item_number, 'DATE' : date_range,\
                                             'MODEL' : 'Facebook Prophet', 'POINT_FORECAST' : point_forecast})

   return render_template("forecastv2result.html",  data=forecast_model_results.to_html(), graph1=graph1_url)


### Version 3: Forecast API returning json file
@app.route('/API/forecast/<int:store_number>/<int:item_number>/<initial_date>/<final_date>')
def forecast_api(store_number, item_number, initial_date, final_date):

    date_range = pd.date_range(pd.to_datetime(initial_date), pd.to_datetime(final_date))
    point_forecast = np.random.randint(low=15, high=30, size=len(date_range))

    forecast_model_results = pd.DataFrame({'STORE' : store_number, 'ITEM' : item_number, 'DATE' : date_range,\
                                           'MODEL' : 'Facebook Prophet',
                                           'POINT_FORECAST' : point_forecast})

    return forecast_model_results.to_json(orient='index')

