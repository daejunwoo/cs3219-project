from flask import Flask,request
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.cors import CORS, cross_origin
import os
import convert as convertPDF
import extract as ex
import string

app = Flask(__name__)
cors = CORS(app)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

@app.route('/')
def hello():
  return convertPDF.convert('static/YaminiBhaskar.pdf')

@app.route('/keyword')
def keyWordExtraction():
  s = ""
  rawText = convertPDF.convertWithCoordinates('static/YaminiBhaskar.pdf')
  #keyWords = ex.extractKeyWords(rawText)
  #s = "/".join(keyWords)
  print rawText
  return s
  
@app.route('/upload', methods=['POST'])
@cross_origin()
def upload_file():
  #import pdb;
  #pdb.set_trace()
  print "test"
  if request.method == 'POST':
    file = request.files['files']
    print file.filename
  return jsonify({'status': 'created'}), 201
  
if __name__ == '__main__':
  app.debug = True
  app.run()
