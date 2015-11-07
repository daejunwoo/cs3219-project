import os
from cStringIO import StringIO
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter, PDFPageAggregator
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage, PDFTextExtractionNotAllowed
from pdfminer.pdfdevice import PDFDevice
import extract as ex
import pdfminer

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

pdfText = []

def convertWithCoordinates(fname, pages=None):
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

  interpreter = PDFPageInterpreter(manager, device)

  for page in PDFPage.create_pages(document):
    interpreter.process_page(page)
    layout = device.get_result()
    
    parse_obj(layout._objs)

#ex.getExperience(pdfText)
#ex.getLanguage(pdfText)
#ex.getVolunteerExperience(pdfText)
  ex.testCVDecorator(pdfText)
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
