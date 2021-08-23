from flask import Flask, render_template, jsonify, request
import os
import shutil
from flask_cors import CORS, cross_origin
import flask_monitoringdashboard as dashboard
from rq import Queue
from worker import conn


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

    # set AWS S3 environment variables (for windows)
    # @ "C:\Users\<UserName>\.aws\credentials"
    # & "C:\Users\<UserName>\.aws\config"

    # Creating a RQ queue to execute worker tasks on heroku
    q = Queue(connection=conn)

    # Invoking the prediction object
    modelPredObj = ModelPrediction(log_file)

    try:
        if request.form:
            dict_req = dict(request.form)
            response = q.enqueue(modelPredObj.form_response(dict_req))  # q.enqueue() added
            log_file.close()
            return response
        elif request.json:
            response = q.enqueue(modelPredObj.api_response(request.json))
            log_file.close()
            return jsonify(response)

    except Exception as e:
        print(e)
        error = {"error": "Something went wrong!! Try again later!"}
        error = {"error": e}
        log_file.close()
        return render_template('404.html', error=error)


if __name__ == "__main__":
    # app.run(host='0.0.0.0', port=5000, debug=True)
    app.run(debug=True)