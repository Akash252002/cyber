import os
import sys

from flask_cors import CORS,cross_origin

from flask import Flask, render_template, request, redirect
import numpy as np
import warnings
import pickle 

warnings.filterwarnings('ignore')
from feature import FeatureExtraction

# print("model load start")

model_path=os.path.join('model.pkl')
file = open(model_path,"rb")
model = pickle.load(file)
file.close()

# print("model load end")

application = Flask(__name__)
app=application

@app.route('/')
@cross_origin()
def homePage():
    return render_template('index.html')

@app.route('/predict',methods=['GET','POST'])
@cross_origin()
def index():
    if request.method == "POST":

        url = request.form["input"]
        obj = FeatureExtraction()
        obj.generate_dataframe_from_url(url)

        x = np.array(obj.getFeaturesList()).reshape(1,25) 

        y_pred =model.predict(x)[0]
        
        y_pro_phishing = model.predict_proba(x)[0,0]
        y_pro_non_phishing = model.predict_proba(x)[0,1]
       
        if y_pred == 1:
            result = f"  The site is {round(y_pro_non_phishing,2)*100} % safe ✅"
        else:
            result = f"The site is {round(y_pro_phishing,2)*100} % unsafe ❌"
        return render_template('index.html',result = result)
    return render_template("index.html")

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)
