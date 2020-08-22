from flask import Flask,request
from flask_restful import Api,Resource,abort
from flask import jsonify
import dbconfig as dbc
from flask_cors import CORS
from flask_cors import cross_origin
import json
from bson import json_util

app=Flask(__name__)
api=Api(app)
cors=CORS(app, resources={r"/surveydata": {"origins": "*"},r"/qdata":{"origins":"*"},r"/qdata/delete/":{"origins":"*"}})
app.config['CORS_HEADERS'] = 'Content-Type'
Survey = dbc.get_client().SurveyData.survey
Questions=dbc.get_client().SurveyData.questions


@app.route("/surveydata",methods=['GET', 'POST'])
@cross_origin(origin='*',headers=['Content-Type'])
def post_sd():
    json_data=request.get_json()
    print(json_data)
    Survey.insert_one(json_data)
    return {"message":"data added succesfully"}

@app.route("/qdata",methods=['GET'])
@cross_origin(origin='*',headers=['Content-Type'])
def checkconnection():
    return {"message":"Connection Okay"}

@app.route("/qdata/<string:tid>",methods=['POST'])
@cross_origin(origin='*',headers=['Content-Type'])
def post_questions(tid):
    json_data=request.get_json()
    print(json_data)
    Questions.update({"topicID":tid},{"$push":{"data":json_data}})
    # Questions.insert_one(json_data)
    return {"message":"data added succesfully"}

@app.route("/qdata/<string:tid>",methods=['GET'])
@cross_origin(origin='*',headers=['Content-Type'])
def getqbytid(tid):
    pipeline=[
    {
        '$project': {
            '_id': 0
        }
    }, {
        '$match': {
            'topicID': tid
        }
    }
    ]

    docs=[doc for doc in Questions.aggregate(pipeline)]
    details=json.dumps(docs,default=json_util.default)
    return jsonify(json.loads(details))
@app.route("/qdata/delete/<string:ref>",methods=['GET'])
@cross_origin(origin='*',headers=['Content-Type'])
def deleteQ(ref):  
    pipeline=[
    {
        '$unwind': {
            'path': '$data', 
            'includeArrayIndex': 'index'
        }
    }, {
        '$match': {
            'data.ref':ref
        }
    }, {
        '$project': {
            'data': 0, 
            '_id': 0
        }
    }
    ]
    docs=[doc for doc in Questions.aggregate(pipeline)]
    details=json.dumps(docs,default=json_util.default)
    details=(json.loads(details))
    index=details[0]['index']
    tid=details[0]['topicID']
    matchstr=f"data.{index}"
    print(index)
    # Questions.update({"topicID":tid},{"$unset":{matchstr:1}})
    Questions.update({"topicID":tid},{"$pull":{"data":{"ref":ref}}})
   
    return {"message":"connection okay"}

app.run(port=5000,debug=True)