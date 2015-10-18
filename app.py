
from flask import Flask, request, Response
from flask.ext.cors import CORS, cross_origin
from flask.ext.sqlalchemy import SQLAlchemy
import os
from cStringIO import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import extract as ex
import string

app = Flask(__name__)
CORS(app)

cors = CORS(app, resources={r"/upload": {"origins": "localhost"}})
app.config['CORS_HEADERS'] = 'Content-Type'

app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

def convert(fname, pages=None):
  print fname
  if not pages:
    pagenums = set()
  else:
    pagenums = set(pages)
  output = StringIO()
  manager = PDFResourceManager()

  converter = TextConverter(manager, output, laparams=LAParams(word_margin = 0.1))
  interpreter = PDFPageInterpreter(manager, converter)
  infile = file(fname, 'rb')
  for page in PDFPage.get_pages(infile, pagenums):
    interpreter.process_page(page)
  infile.close()
  converter.close()
  text = output.getvalue()
  output.close
  return text.decode('utf8')

@app.route('/')
def hello():
  return convert('static/DesmondLim.pdf')

@app.route('/keyword')
def keyWordExtraction():  
  rawText = convert('static/DesmondLim.pdf')
  keyWords = ex.extractKeyWords(rawText)
  s = "/".join(keyWords)
  return s
  
@app.route('/<name>')
def hello_name(name):
  return "Hello {}!".format(name)

@app.route('/upload', methods=['POST, OPTIONS'])
@cross_origin(origin='localhost')
def upload_file(name):
  print "test"
  if request.method == 'POST':
    file = request.files['file']
    print file.filename
  return jsonify({'status': 'created'}), 201
  
if __name__ == '__main__':
  app.run()
