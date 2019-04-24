from flask import Flask, jsonify, request, Response, render_template, flash
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import numpy as np
from scipy.stats import norm
import pandas as pd
from flask_bootstrap import Bootstrap
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import io
import base64

app = Flask(__name__)

class ReusableForm(Form):
    store_number = TextField('Store Number:', validators=[validators.required()])
    item_number = TextField('Item Number:', validators=[validators.required(), validators.Length(min=3, max=35)])
    initial_date = TextField('Inital Date:', validators=[validators.required(), validators.Length(min=3, max=35)])
    final_date = TextField('Final Date:', validators=[validators.required(), validators.Length(min=3, max=35)])
    frequency = TextField('Frequency:', validators=[validators.required(), validators.Length(min=3, max=35)])

def build_dist_graph_final(df, quantile):

    img = io.BytesIO(); plt.style.use('seaborn-darkgrid'); fig, ax = plt.subplots();
    if quantile == 'M':
        column_list = ['Q_05', 'Q_25', 'Q_50','Q_75', 'Q_95']
        for column in column_list:
            plt.plot(pd.to_datetime(df['DATE']).apply(lambda x: x.strftime('%d-%m-%y')).astype(str), df[column], marker='', color='grey', linewidth=2, alpha=0.4)
        plt.plot(df['DATE'].apply(lambda x: x.strftime('%d-%m-%y')).astype(str), df['Q_50'], marker='', color='green', linewidth=4, alpha=0.7)
    else:
        plt.plot(df['DATE'].apply(lambda x: x.strftime('%d-%m-%y')).astype(str), df['POINT_FORECAST'], marker='', color='green', linewidth=4, alpha=0.7)
    plt.xticks(rotation=45)
    plt.xlabel("Time"); plt.ylabel("Sales")
    plt.savefig(img, format='png'); img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode(); plt.close()

    return 'data:image/png;base64,{}'.format(graph_url)


###################################################
### Version 1: Forecast from submitted form
###################################################

@app.route('/',methods = ['POST', 'GET'])
def forecastv2request():

    form = ReusableForm(request.form)
    print(form.errors)

    if request.method == 'POST':

        if form.validate():
            # Save the comment here.
            flash('Thank you for your request. ')
        else:
            flash('Error: All the form fields are required.')

    return render_template('forecastv2request.html', form=form)

@app.route('/result',methods = ['POST', 'GET'])
def forecastv2result():
   if request.method == 'POST':

      store_number = request.form['store_number']
      item_number = request.form['item_number']
      initial_date = request.form['initial_date']
      final_date = request.form['final_date']
      frequency = request.form['frequency']
      quantile = request.form['quantile']

      date_range = pd.date_range(pd.to_datetime(initial_date), pd.to_datetime(final_date), freq=frequency)
      point_forecast = np.random.randint(low=15, high=30, size=len(date_range))
      q05_forecast = np.round(norm.ppf(0.05, loc=point_forecast, scale=2),2)
      q25_forecast = np.round(norm.ppf(0.25, loc=point_forecast, scale=2),2)
      q50_forecast = np.round(norm.ppf(0.50, loc=point_forecast, scale=2),2)
      q75_forecast = np.round(norm.ppf(0.75, loc=point_forecast, scale=2),2)
      q95_forecast = np.round(norm.ppf(0.95, loc=point_forecast, scale=2),2)

      if quantile == 'M':
        forecast_model_results = pd.DataFrame({'STORE' : store_number, 'ITEM' : item_number, 'DATE' : date_range,\
                                             'Q_05' : q05_forecast, 'Q_25' : q25_forecast, 'Q_50' : q50_forecast, \
                                             'Q_75' : q75_forecast, 'Q_95' : q95_forecast})
      else:
        forecast_model_results = pd.DataFrame({'STORE' : store_number, 'ITEM' : item_number, 'DATE' : date_range, 'POINT_FORECAST' : point_forecast})


      graph1_url = build_dist_graph_final(forecast_model_results, quantile)

   return render_template("forecastv2result.html",  data=forecast_model_results.to_html(col_space=500,justify='center',index=False), graph1=graph1_url)

###################################################
### Version 2: Forecast API returning json file
###################################################

@app.route('/API/forecast/<int:store_number>/<int:item_number>/<initial_date>/<final_date>/<frequency>/<quantile>')
def forecast_api(store_number, item_number, initial_date, final_date, frequency, quantile):

    date_range = pd.date_range(pd.to_datetime(initial_date), pd.to_datetime(final_date), freq=frequency)
    point_forecast = np.random.randint(low=15, high=30, size=len(date_range))
    q05_forecast = np.round(norm.ppf(0.05, loc=point_forecast, scale=2),2)
    q25_forecast = np.round(norm.ppf(0.25, loc=point_forecast, scale=2),2)
    q50_forecast = np.round(norm.ppf(0.50, loc=point_forecast, scale=2),2)
    q75_forecast = np.round(norm.ppf(0.75, loc=point_forecast, scale=2),2)
    q95_forecast = np.round(norm.ppf(0.95, loc=point_forecast, scale=2),2)

    if quantile == 'M':
        forecast_model_results = pd.DataFrame({'STORE' : store_number, 'ITEM' : item_number, 'DATE' : date_range.astype(str),\
                                             'Q_05' : q05_forecast, 'Q_25' : q25_forecast, 'Q_50' : q50_forecast, \
                                             'Q_75' : q75_forecast, 'Q_95' : q95_forecast})
    else:
        forecast_model_results = pd.DataFrame({'STORE' : store_number, 'ITEM' : item_number, 'DATE' : date_range.astype(str), 'POINT_FORECAST' : point_forecast})

    return forecast_model_results.to_json(orient='index')
