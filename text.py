import os, time
from pyppeteer import launch
import pytesseract
from pdf2image import convert_from_path
import asyncio
import re
from datetime import datetime
import pandas as pd
import json

callSigns =  '{ "YU-FVJ":"PNC1A", "YU-SCM":"PNC4M", "YU-SCJ":"PNC5C","YU-SVL":"PNC1VL", "YU-SVJ":"PNC7D", "YU-SPC":"PND3T", "YU-LSA":"PNC6L"}'
sc=json.loads(callSigns)

async def create_pdf_from_html(html, pdf_path):
    browser = await launch()
    page = await browser.newPage()

    await page.setContent(html)
    await page.pdf({'path': pdf_path, 'format': 'A4'})
    await browser.close()
    print("finished")


path_to_watch = "."
before = dict ([(f, None) for f in os.listdir (path_to_watch)])
while 1:
  time.sleep (5)
  after = dict ([(f, None) for f in os.listdir (path_to_watch)])

  added = [f for f in after if not f in before]
  removed = [f for f in before if not f in after]

  if (added and added[0]!="form1.pdf"): 
      print("started")
    #  file = open(added[0], "r")
    #  content = file.read()
    #  data=(content.split())
      
      pages = convert_from_path(added[0], 500,None, first_page=1, last_page=1)
     
    # Extract text from each page using Tesseract OCR
      text_data = ''
      for page in pages:
        text = pytesseract.image_to_string(page)
        text_data += text + '\n'
     
    # Return the text data
    # return text_data
      data=text_data.split()
      print(data)
      def is_date(date_string):
        try:
            pd.to_datetime(date_string, format='%d/%m/%Y')
            return True
        except Exception:
            return False
    
      x=0
      for index, item in enumerate(data):
            if is_date(item):
                x=(index)
            
      index = data.index("Maximum")
      typeAc="C56X"
      if "F2TH" in data:
        typeAc="F2TH"
      elif "C525" in data: 
        typeAc="C525"       
      currentDate=datetime.today().strftime('%d.%m.%Y')
      reg=data[int(index)-1]
      callSign=sc[reg]
      date1=data[int(x)-7]
      origin1=data[int(x)-5]
      dest1=data[int(x)-3]
      
      time1=(data[int(x)-2])[0:2]
      timeEta1=int(time1)+2
      
      pax1=data[int(x)-1]

      date2=data[x]
      origin2=data[int(x)+2]
      dest2=data[int(x)+4]
      time2=(data[int(x)+5])[0:2]
      timeEta2=int(time2)+2
      pax2=data[int(x)+7]
      regAlt=["YU-FVJ","YU-SVL","YU-SPC","YU-SVJ","YU-SCM"]
      typeAlt=["F2TH","C56X","C56X","C56X","C525"]
      regAlt.remove(reg)
      typeAlt.remove(typeAc)
    

      fname = "uk.html"
      if (dest1[0:2]=="LE"): fname="Spain.html"
      if (dest1[0:2]=="LD"): fname="hrt.html"
   
      html_file = open(fname, 'r', encoding='utf-8')
      html = html_file.read() 
      result1 = re.sub(r'<% currentDate %>', currentDate, html)
      result2 = re.sub(r'<% reg %>', reg, result1)
      result3 = re.sub(r'<% callSign %>', callSign, result2)
      result4 = re.sub(r'<% date1 %>', date1, result3)
      result5 = re.sub(r'<% date2 %>', date2 ,result4)
      result6 = re.sub(r'<% longRoute1 %>', (time1+":00") +" "+origin1 +"-"+dest1+" "+str(timeEta1)+":00",result5)
      result7 = re.sub(r'<% longRoute2 %>', time2+":00" +" "+origin2 +"-"+dest2+" "+str(timeEta2)+":00",result6)
      result8 = re.sub(r'<% shortRoute1 %>', origin1 +"-"+dest1,result7)
      result9 = re.sub(r'<% shortRoute2 %>', origin2 +"-"+dest2 ,result8)
      result10 = re.sub(r'<% regAlt1 %>', regAlt[0] ,result9)
      result11 = re.sub(r'<% regAlt2 %>', regAlt[1] ,result10)
      result12 = re.sub(r'<% regAlt3 %>', regAlt[2] ,result11)
      result13 = re.sub(r'<% regAlt4 %>', regAlt[3] ,result12)
      result14 = re.sub(r'<% regType1 %>', typeAlt[0] ,result13)
      result15 = re.sub(r'<% regType2 %>', typeAlt[1] ,result14)
      result16 = re.sub(r'<% regType3 %>', typeAlt[2] ,result15)
      result17 = re.sub(r'<% regType4 %>', typeAlt[3] ,result16)
      result = re.sub(r'<% typeAc %>', typeAc ,result17)
      asyncio.get_event_loop().run_until_complete(create_pdf_from_html(result, 'form1.pdf'))
     # file.close()
  before = after
  
