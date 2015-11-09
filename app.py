from flask import Flask,request
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.cors import CORS, cross_origin
import os
import convert as convertPDF
import extract as ex
import analyze as analyzer
import string
import json
from cStringIO import StringIO

app = Flask(__name__)
cors = CORS(app)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

@app.route('/analyzer')
def analyzeCV():
  description = {'Title': 'Software Engineer', 'Skill': ['Microsoft Office', 'Data Mining', 'Image Processing'], 'Certification': 'Random value', 'Volunteering': 'Random value'}
  resume = [{'Name': 'Tom', 'Title': 'Software Engineer at NUS', 'Experience': [{'Title': 'Software Engineer'}], 'Skill': ['Microsoft Office', 'Data Mining'], 'Certification': 'Random value', 'Volunteering': 'Random value'}, {'Name': 'Sam', 'Title': 'Software Engineer at NUS', 'Experience': [{'Title': 'Software Engineer'}], 'Skill': ['Microsoft Office', 'Data Mining']}]
  result = analyzer.process_analyzer(description, resume)
  return json.dumps(result)

@app.route('/')
def hello():
  # return convertPDF.convertWithCoordinatesPara('static/YaminiBhaskar.pdf')
  return json.dumps(convertPDF.convertWithCoordinatesPara('static/YaminiBhaskar.pdf'))

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
  if request.method == 'POST':
    upload_files = request.files.getlist("files")
    for file in upload_files:
      filename = file.filename
      save_path = os.path.dirname(os.path.abspath(__file__))+'/static/'
      file.save(save_path+filename )
      print json.dumps(convertPDF.convertWithCoordinatesPara('static/'+ filename))
  # # return jsonify({'status': 'created'}), 201
  
if __name__ == '__main__':
  app.debug = True
  app.run()
