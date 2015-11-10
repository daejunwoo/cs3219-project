from flask import Flask,request
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.cors import CORS, cross_origin
import os
import shutil
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

job_description = {}

@app.route('/analyzer')
def analyzeCV():
  # description = {'Title': 'Software Engineer', 'Skill': ['Microsoft Office', 'Data Mining', 'Image Processing'], 'Certification': 'Random value', 'Volunteering': 'Random value'}
  #resume = [{'Name': 'Tom', 'Title': 'Software Engineer at NUS', 'Experience': [{'Title': 'Software Engineer'}], 'Skill': ['Microsoft Office', 'Data Mining'], 'Certification': 'Random value', 'Volunteering': 'Random value'}, {'Name': 'Sam', 'Title': 'Software Engineer at NUS', 'Experience': [{'Title': 'Software Engineer'}], 'Skill': ['Microsoft Office', 'Data Mining']}]
  
  #setup extractor with base and decorators
  decorators = {'Skill':ex.skills_dec , 'Language':ex.language_dec}
  decorators = {'Skill':ex.skills_dec , 'Language':ex.language_dec}
  extractor = ex.get_base
  decorator = decorators["Language"]
  extractor = decorator(extractor)

  #retrieve files from static
  resumesDir = os.listdir('static')
  resumeFiles = []
  resumes = []

  for resumeFile in resumesDir:
    if resumeFile.endswith(".pdf"):
      resumeFiles.append('static/'+ resumeFile)
  
  for resumeFile in resumeFiles:
    forExtractorInput = convertPDF.convertWithCoordinatesPara(resumeFile)
    resume = extractor(forExtractorInput['pdfText'])
    resume = "{" + resume +"}"
    resumes.append(resume)

  first = True
  analyzerResumesInput = "["
  for resume in resumes:
    if first:
      analyzerResumesInput = analyzerResumesInput + resume
      first = False
    else:
      analyzerResumesInput = analyzerResumesInput + "," + resume

  print job_description
  analyzerResumesInput = analyzerResumesInput + "]"
  analyzerDictResumesInput = ast.literal_eval(analyzerResumesInput)
  result = analyzer.process_analyzer(job_description, analyzerDictResumesInput)
  return json.dumps(result)

@app.route('/')
def hello():
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
    title = request.form['title']
    skill = request.form['skills']
    other1, other1value = "", ""
    other2, other2value = "", ""
    other3, other3value = "", ""
    if request.form['other1'] != "" and request.form['other1value'] != "":
      other1 = request.form['other1']
      other1value = request.form['other1value'].split(',')
    if request.form['other2'] != "" and request.form['other2value'] != "":
      other2 = request.form['other2']
      other2value = request.form['other2value'].split(',')
    if request.form['other3'] != "" and request.form['other3value'] != "":
      other3 = request.form['other3']
      other3value = request.form['other3value'].split(',')

    skill_list = skill.split(',')
    global job_description 
    job_description = {'Title': title, 'Skill': skill_list, other1: other1value, other2: other2value, other3: other3value}

    upload_files = request.files.getlist("files")

    #clear static directory
    resumesDir = os.listdir('static')
    resumeFiles = []
    resumes = []
    for resumeFile in resumesDir:
      if resumeFile.endswith(".pdf"):
        resumeFiles.append('static/'+ resumeFile)
    for f in resumeFiles:
      os.remove(f)

    for file in upload_files:
      filename = file.filename
      save_path = os.path.dirname(os.path.abspath(__file__))+'/static/'
      file.save(save_path+filename)
      #print json.dumps(convertPDF.convertWithCoordinatesPara('static/'+ filename))
  return json.dumps({'status': '200'})

if __name__ == '__main__':
  app.debug = True
  app.run()
