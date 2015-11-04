from flask import Flask,request
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.cors import CORS, cross_origin
import os
from cStringIO import StringIO
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
import pdfminer
import extract as ex
import string

app = Flask(__name__)
cors = CORS(app)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

pdfText = []

def convert(fname, pages=None):
  print fname
  if not pages:
    pagenums = set()
  else:
    pagenums = set(pages)

  infile = file(fname, 'rb')
  parser = PDFParser(infile)
  document = PDFDocument(parser)

  laparams = LAParams()

  manager = PDFResourceManager()
  device = PDFPageAggregator(manager, laparams=laparams)

  # converter = TextConverter(manager, output, laparams=LAParams(word_margin = 0.1))
  interpreter = PDFPageInterpreter(manager, device)

  for page in PDFPage.create_pages(document):
    interpreter.process_page(page)
    layout = device.get_result()
    
    parse_obj(layout._objs)

  ex.getExperience(pdfText)

  # text = output.getvalue()
  # return text.decode('utf8')
  return None

def parse_obj(lt_objs):

  # loop over the object list
  for obj in lt_objs:

    # if it's a textbox, print text and location
    if isinstance(obj, pdfminer.layout.LTTextBoxHorizontal):
      #print "%6d, %6d, %s" % (obj.bbox[0], obj.bbox[1], obj.get_text().replace('\n', '_'))
      text = obj.get_text().replace('\n', '_')
      pdfText.append(text)

    # if it's a container, recurse
    elif isinstance(obj, pdfminer.layout.LTFigure):
      parse_obj(obj._objs)


@app.route('/')
def hello():
  return convert('static/YaminiBhaskar.pdf')

@app.route('/keyword')
def keyWordExtraction():  
  rawText = convert('static/DesmondLim.pdf')
  keyWords = ex.extractKeyWords(rawText)
  s = "/".join(keyWords)
  return s
  
@app.route('/<name>')
def hello_name(name):
  return "Hello {}!".format(name)

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
  app.run()
