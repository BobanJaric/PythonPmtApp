import os, time
from pyppeteer import launch
import asyncio
import re
from datetime import datetime

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

      file = open(added[0], "r")
      content = file.read()
      data=(content.split())

        
      currentDate=datetime.today().strftime('%d.%m.%Y')
      reg=data[0]
      callSign=data[3]
      date1=data[2]
      origin1=data[4]
      dest1=data[9]
      time1=data[6]
      timeEta1=data[7]
      pax1=data[12]

      date2=data[14]
      origin2=data[16]
      dest2=data[21]
      time2=data[18]
      timeEta2=data[19]
      pax2=data[24]
      regAlt=["YU-FVJ","YU-SVL","YU-SPC","YU-SVJ","YU-SCM"]
      regAlt.remove(reg)
      print(regAlt)

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
      result6 = re.sub(r'<% longRoute1 %>', time1 +" "+origin1 +"-"+dest1+" "+str(timeEta1),result5)
      result7 = re.sub(r'<% longRoute2 %>', time2 +" "+origin2 +"-"+dest2+" "+str(timeEta2),result6)
      result8 = re.sub(r'<% shortRoute1 %>', origin1 +"-"+dest1,result7)
      result9 = re.sub(r'<% shortRoute2 %>', origin2 +"-"+dest2 ,result8)
      result10 = re.sub(r'<% regAlt1 %>', regAlt[0] ,result9)
      result11 = re.sub(r'<% regAlt2 %>', regAlt[1] ,result10)
      result12 = re.sub(r'<% regAlt3 %>', regAlt[2] ,result11)
      result = re.sub(r'<% regAlt4 %>', regAlt[3] ,result12)
      asyncio.get_event_loop().run_until_complete(create_pdf_from_html(result, 'form1.pdf'))
      file.close()
  before = after
  
