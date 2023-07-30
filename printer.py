import serial
import time
from datetime import datetime

#Sends the command encoded in UTF-8 and listens for replies until receiving the 'ok' from the printer, signaling that it is time for the next command
def command(ser, command):
  start_time = datetime.now() 
  ser.write(str.encode(command)) 
  while True:
    line = str(ser.readline().decode()).replace("\r", "").encode() 
    print(line)
    if line == b'ok\n':
      break  
      
#defines the port through which serial connection will occur
def defineP(pN, bR): 
  g = serial.Serial(pN, int(bR))  
  return g 

#converts each individual command of G-code into a more sendable format
def convert(fileIn, fileOut): 
  final = ';converted' 
  with open(fileIn, 'r') as g:  
      M107 = 0
      content = g.read().splitlines()  
      for x in range(len(content)):  
          if content[x] == 'M105': 
              content[x] = 'M155'
          if content[x] != '' and content[x] != ' ' and content[x][0] != ';': 
              final = final + content[x] + r'\r\n' + '\r\n' 
          if 'M107' in content[x] and M107 == 0: 
              M107 = 1  
          elif 'M107' in content[x] and M107 == 1: 
              final = final + 'G0 X111 Y150 Z200' + r'\r\n' + '\r\n'  
              final = final + 'G0 Y220 Z200' + r'\r\n' + '\r\n' 
              final = final + 'G0 Z2' + r'\r\n' + '\r\n' 
              final = final + 'G28' + r'\r\n' + '\r\n'
  with open(fileOut, 'w') as h: 
      h.write(final)  
      print('Done!') 
  return fileOut  

#opens the selected G-code file and sends it through the port inputted as the parameter
def  sendFile(ser, file): 
   with open(file, 'r') as d: 
    content = d.read().splitlines()
    for i in range(len(content)): 
       content[i] = content[i].replace('\\r\\n', '\r\n') 
    for x in range(len(content)):  
      print(content[x]) 
      command(ser, content[x]) 

  
 
