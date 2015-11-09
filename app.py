from flask import Flask,request
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.cors import CORS, cross_origin
import os
import convert as convertPDF
import extract as ex
import analyze as analyzer
import string
import json

app = Flask(__name__)
cors = CORS(app)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

@app.route('/analyzer')
def analyzeCV():
  description = {'Title': 'Software Engineer', 'Skill': ['Microsoft Office', 'Data Mining', 'Image Processing'], 'Certification': 'Random value', 'Volunteering': 'Random value'}
  resume = [{'Name': 'Tom', 'Title': 'Software Engineer at NUS', 'Experience': [{'Title': 'Software Engineer'}], 'Skill': ['Microsoft Office', 'Data Mining'], 'Certification': 'Random value', 'Volunteering': 'Random value'}, {'Name': 'Sam', 'Title': 'Software Engineer at NUS', 'Experience': [{'Title': 'Software Engineer'}], 'Skill': ['Microsoft Office', 'Data Mining'], 'Certification': 'Random value'}]
  multiplier = analyzer.assign_key_multipler(description)
  result = analyzer.process_cv(resume, multiplier, description)
  return json.dumps(result)

@app.route('/')
def hello():
  return convertPDF.convert('static/YaminiBhaskar.pdf')

@app.route('/keyword')
def keyWordExtraction():
  s = ""
  rawText = convertPDF.convertWithCoordinatesPara('static/YaminiBhaskar.pdf')
  temp = ex.get_base

  dec = ex.experience_dec
  temp = dec(temp)

  #dec = ex.language_dec
  #temp = dec(temp)

  dec = ex.skills_dec
  temp = dec(temp)
  print temp(rawText['pdfText'])

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
