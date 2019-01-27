from flask import Flask, Response, request
import csv
import requests
import operator
import time
import datetime

app = Flask(__name__)
#python receiveDataServerTest.py
@app.route("/")
def CSVtoServer():
	url = 'https://sigma-myth-229819.appspot.com/truckapi'
	with open('ITM_20190121.csv') as csv_file:
		csv_read = csv.reader(csv_file, delimiter=',')
		sortedCSV = sorted(csv_read, key=operator.itemgetter(7))
		
		for i in range(len(sortedCSV)):
			if sortedCSV[i][9] != 'NULL' and sortedCSV[i][8] != 'NULL' and sortedCSV[i][1] != 'NULL':
				tempDict = {"Longitude": float(sortedCSV[i][9]), "Latitude": float(sortedCSV[i][8]), "DeviceSerial": int(sortedCSV[i][1]), "MessageType": sortedCSV[i][3], "ReportType":sortedCSV[i][4]}
				response = requests.post(url, tempDict)
				print(tempDict, response)				
				if(i + 1 != len(sortedCSV)):
			
					newStr = sortedCSV[i][7]
					newStr2 = sortedCSV[i+1][7]
					newStr = newStr[12:-4]
					newStr2 = newStr2[12:-4]
					ftr = [3600,60,1]
					x = sum([a*b for a,b in zip(ftr, map(int,newStr.split(':')))])
					x2 = sum([a*b for a,b in zip(ftr, map(int,newStr2.split(':')))])
					tempDiff = (x2-x) / 10
					print(tempDiff)
					time.sleep(tempDiff)

			
		return "Data Sent."
		
if __name__ == "__main__":
	app.run()