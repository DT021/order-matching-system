#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 22:05:51 2020

@author: vishalbns
"""
from datetime import datetime
import saveDataToGSheet
from flask import request, redirect, Flask, render_template
app = Flask(__name__)

def index():
    return render_template('index.html')

keyList = ["ordertype", "quantity", "pricetype", "price"]
orderDict = {key: [] for key in keyList}

@app.route('/', methods = ['GET', 'POST'])

def newOrder():
    if request.method == 'POST': 
        orderDict["ordertype"].append(request.form['buyorsell'])
        orderDict["quantity"].append(float(request.form['quantity']))
        orderDict["pricetype"].append(request.form['pricetype'])
        orderDict["price"].append(float(request.form['price']))
        print(orderDict)
        newList = [request.form['buyorsell'], float(request.form['quantity']), float(request.form['price']), datetime.now().strftime("%H:%M:%S")]
        saveDataToGSheet.Export_Data_To_Sheets(newList)
    return render_template('index.html')

if(__name__) == '__main__':
    app.run(debug=True)
