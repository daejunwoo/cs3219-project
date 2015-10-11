from flask import Flask
from cStringIO import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

app = Flask(__name__)

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
  
@app.route('/<name>')
def hello_name(name):
  return "Hello {}!".format(name)

if __name__ == '__main__':
  app.run()