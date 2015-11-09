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
import ast 

app = Flask(__name__)
cors = CORS(app)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

title_multiplier = 0
skills_multiplier = 0
more_multiplier = 0

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
  description = {'Title': 'Software Engineer', 'Skill': ['Microsoft Office', 'Data Mining', 'Image Processing','Android','MySQL'], 'Certification': 'Random value', 'Volunteering': 'Random value'}
  resumesInput = []
  resumes = []
  decorators = {'Skill':ex.skills_dec , 'Language':ex.language_dec}
  extractor = ex.get_base
  decorator = decorators["Language"]
  extractor = decorator(extractor)

  resumesInput.append('static/IsenNg.pdf')
  resumesInput.append('static/DonnabelleEmbodo.pdf')
  resumesInput.append('static/DesmondLim.pdf')
  resumesInput.append('static/JinYuanTeo.pdf')
 
  for resumeInput in resumesInput:
    forExtractorInput = convertPDF.convertWithCoordinatesPara(resumeInput)
    resume = extractor(forExtractorInput['pdfText'])
    resume = "{" + resume +"}"
    resumes.append(resume)

  first = True
  output = "["
  for resume in resumes:
    if first:
      output = output + resume
      first = False
    else:
      output = output + "," + resume

  output = output + "]"

  forAnalyzer = ast.literal_eval(output)
  #print forAnalyzer
  result = analyzer.process_analyzer(description, forAnalyzer)

  return output
  
@app.route('/upload', methods=['POST'])
@cross_origin()
def upload_file():
  if request.method == 'POST':
    title_multiplier = request.form['title']
    skills_multiplier = request.form['skills']
    more_multiplier = request.form['more']
    upload_files = request.files.getlist("files")
    for file in upload_files:
      filename = file.filename
      save_path = os.path.dirname(os.path.abspath(__file__))+'/static/'
      file.save(save_path+filename )
      print json.dumps(convertPDF.convertWithCoordinatesPara('static/'+ filename))
  return json.dumps({'status': '200'})
  
if __name__ == '__main__':
  app.debug = True
  app.run()
