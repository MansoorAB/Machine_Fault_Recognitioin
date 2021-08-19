from flask import Flask, render_template, jsonify, request
import os
import shutil
from flask_cors import CORS, cross_origin
import flask_monitoringdashboard as dashboard

import sys
# sys.path.append(os.path.join(sys.path[0], 'src'))  # for local deployment
sys.path.append('src/')  # for heroku deployment

from prediction_service.prediction import ModelPrediction

webapp_root = "webapp"

static_dir = os.path.join(webapp_root, "static")
template_dir = os.path.join(webapp_root, "templates")

os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app = Flask(__name__, static_folder=static_dir, template_folder=template_dir)
dashboard.bind(app)
CORS(app)


@app.route("/", methods=['GET'])
@cross_origin()
def home():
    return render_template('index.html')


@app.route("/predict", methods=["POST"])
def predictWaferStatus():

    # Create Prediction Logs for the current run
    if os.path.exists('Prediction_Logs'):
        shutil.rmtree('Prediction_Logs')

    os.makedirs('Prediction_Logs')
    log_file = open("Prediction_Logs/Prediction_Main_Log.txt", "w")

    # set AWS S3 environment variables here
    os.environ["AWS_DEFAULT_REGION"] = 'us-east-2'
    os.environ["AWS_ACCESS_KEY_ID"] = 'AKIAWPRKS2KYDBRT3CC4'
    os.environ["AWS_SECRET_ACCESS_KEY"] = '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'

    # Invoking the prediction object
    modelPredObj = ModelPrediction(log_file)

    try:
        if request.form:
            dict_req = dict(request.form)
            response = modelPredObj.form_response(dict_req)
            return response
        elif request.json:
            response = modelPredObj.api_response(request.json)
            return jsonify(response)

    except Exception as e:
        print(e)
        error = {"error": "Something went wrong!! Try again later!"}
        error = {"error": e}
        return render_template('404.html', error=error)

    log_file.close()


if __name__ == "__main__":
    # app.run(host='0.0.0.0', port=5000, debug=True)
    app.run(debug=True)