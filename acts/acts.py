#!flask/bin/python
from flask import Flask, jsonify,abort
import csv
import time
import hashlib
import re
import requests
from flask import make_response
import datetime
from flask_cors import CORS,cross_origin
import os
app = Flask(__name__)
CORS(app)	
global stat
stat =1
@app.errorhandler(404)
def not_found(error):
	global stat
	if(stat==0):
		return make_response(jsonify(),500)
	lcount=[]
	with open('count.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		for row in csv_reader:
			row[0]=int(row[0])+1
			lcount.append(row[0])
	print(lcount[0])
	with open("count.csv", "wb") as f:
		writer = csv.writer(f)
		f.write(str(lcount[0]))
	f.close()
		
	return make_response(jsonify({'error': 'Not found'}), 404)

#1 List all categories
@app.route('/api/v1/categories', methods=['GET'])
def list_cat():
	global stat
	if(stat==0):
		return make_response(jsonify(),500)
	lcount=[]
	with open('count.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		for row in csv_reader:
			row[0]=int(row[0])+1
			lcount.append(row[0])
	print(lcount[0])
	with open("count.csv", "wb") as f:
		writer = csv.writer(f)
		f.write(str(lcount[0]))
	f.close()	
	l={}
	with open('/data/t.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		for row in csv_reader:
			l[row[0]] = int(row[1])
	if(len(l)==0):
		return make_response(jsonify(),204)		
	return jsonify(l)



#2 Add a category
from flask import request
@app.route('/api/v1/categories',methods=['POST'])
def add_cat():
	global stat
	if(stat==0):
		return make_response(jsonify(),500)
	lcount=[]
	with open('count.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		for row in csv_reader:
			row[0]=int(row[0])+1
			lcount.append(row[0])
	print(lcount[0])
	with open("count.csv", "wb") as f:
		writer = csv.writer(f)
		f.write(str(lcount[0]))
	f.close()
	if not request.json :
		abort(400)
	data=request.json
	aa=len(data)
	with open('/data/t.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		flag=0
		for row in csv_reader:
			if(row[0]==data[0]):
				flag=1
			if(flag==1):
				return make_response(jsonify({}),400)
	if(aa>1):
		return make_response(jsonify({}),400)
	with open('/data/t.csv', 'a') as csvFile:
		writer = csv.writer(csvFile)
		r=[data[0],0]
		writer.writerow(r)
	return jsonify({}), 201 
			

#3 Delete a category
#Acts in the deleted category should be deleted -- Todo
@app.route('/api/v1/categories/<categoryname>', methods=['DELETE'])
def delete_cat(categoryname):
	global stat
	if(stat==0):
		return make_response(jsonify(),500)
	lcount=[]
	with open('count.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		for row in csv_reader:
			row[0]=int(row[0])+1
			lcount.append(row[0])
	print(lcount[0])
	with open("count.csv", "wb") as f:
		writer = csv.writer(f)
		f.write(str(lcount[0]))
	f.close()
	with open('/data/t.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		flag=0
		for row in csv_reader:
			#print(row)
			if(row[0]==categoryname):
				flag=1
		if(flag==0):
			return make_response(jsonify({'error':'Resource does not exist'}),400	)
	tl=[]	
	with open('/data/t.csv', 'rb') as f:
		reader = csv.reader(f)
		l = list(reader)
		for line in l:
			if(line[0]!=categoryname):
				tl.append(line)	
	print(tl)
	with open("/data/t.csv", "wb") as f:
		writer = csv.writer(f)
		writer.writerows(tl)
	return jsonify({}), 200


#6 List acts for a given category || #8 Acts in range of a given category
@app.route('/api/v1/categories/<categoryname>/acts', methods=['GET'])
def list_acts(categoryname):
	global stat
	if(stat==0):
		return make_response(jsonify(),500)
	lcount=[]
	with open('count.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		for row in csv_reader:
			row[0]=int(row[0])+1
			lcount.append(row[0])
	print(lcount[0])
	with open("count.csv", "wb") as f:
		writer = csv.writer(f)
		f.write(str(lcount[0]))
	f.close()
	if (request.args.get('start')==None):
		ll=[]
		with open('/data/acts.csv', 'rb') as f:
			reader = csv.reader(f)
			l = list(reader)
		for line in l:
			details={}
			if(line[1]==categoryname):
				details["actId"]=int(line[0])
				details["category"]=line[1]
				details["username"]=line[2]
				details["timestamp"]=line[3]
				details["caption"]=line[4]
				details["upvotes"]=int(line[5])
				details["imgB64"]=line[6]
				ll.append(details)
		if(len(ll)>100):
			return make_response(jsonify({}),413)
		if(len(ll)==0):
			return make_response(jsonify({}),204)				
		return make_response(jsonify(ll),200)

		
	else:
		ll=[]
		start=int(request.args.get('start'))
		end=int(request.args.get('end'))
		with open('/data/acts.csv', 'rb') as f:
			#next(f)
			reader = csv.reader(f)
			l = list(reader)
		for line in l:
			if(line[1]==categoryname):
				ll.append(line)
		if(len(ll)==0):
			return make_response(jsonify({}),204)
		ll.sort(key=lambda x: x[3][12])
		ll.sort(key=lambda x: x[3][11])
		ll.sort(key=lambda x: x[3][15])
		ll.sort(key=lambda x: x[3][14])
		ll.sort(key=lambda x: x[3][18])
		ll.sort(key=lambda x: x[3][17])
		ll.sort(key=lambda x: x[3][0])
		ll.sort(key=lambda x: x[3][1])
		ll.sort(key=lambda x: x[3][3])
		ll.sort(key=lambda x: x[3][4])
		ll.sort(key=lambda x: x[3][3])
		ll.sort(key=lambda x: x[3][9])
		ll.sort(key=lambda x: x[3][8])
		ll.sort(key=lambda x: x[3][7])
		ll.sort(key=lambda x: x[3][6])
		ll.reverse()
		a=end-start+1
		if(a>100):
			return make_response(jsonify({}),413)
		if(start<1 or end>len(ll) or start>end):
			return make_response(jsonify({}),400)
			
		
		#ll.reverse()
		final=[]
		for i in range(start,end+1):
			final.append(ll[i])
		ll=[]
		for line in final:
			details={}
			details["actId"]=int(line[0])
			details["category"]=line[1]
			details["username"]=line[2]
			details["timestamp"]=line[3]
			details["caption"]=line[4]
			details["upvotes"]=int(line[5])
			details["imgB64"]=line[6]
			ll.append(details)
		return make_response(jsonify(ll),200)
		

#7 list number of acts in a given category
@app.route('/api/v1/categories/<categoryname>/acts/size', methods=['GET'])
def list_num_acts_cat(categoryname):
	global stat
	if(stat==0):
		return make_response(jsonify(),500)
	lcount=[]
	with open('count.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		for row in csv_reader:
			row[0]=int(row[0])+1
			lcount.append(row[0])
	print(lcount[0])
	with open("count.csv", "wb") as f:
		writer = csv.writer(f)
		f.write(str(lcount[0]))
	f.close()
	with open('/data/t.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		flag=0
		for row in csv_reader:
			if(row[0]==categoryname):
				flag=1
			if(flag==1):
				return make_response(jsonify([row[1]]),200)

	
	return make_response(jsonify({}),204)


#9 upvote an act
@app.route('/api/v1/acts/upvote',methods=['POST'])
def upvote_act():
	global stat
	if(stat==0):
		return make_response(jsonify(),500)
	lcount=[]
	with open('count.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		for row in csv_reader:
			row[0]=int(row[0])+1
			lcount.append(row[0])
	print(lcount[0])
	with open("count.csv", "wb") as f:
		writer = csv.writer(f)
		f.write(str(lcount[0]))
	f.close()
	if not request.json :
		abort(400)
	data=request.json
	data=int(data[0])
	ll1=[]
	with open('/data/acts.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		flag=0
		for line in csv_reader:
			ll1.append(line)
	llll=[]
	for row in ll1:
		if(int(row[0])==data):
			llll.append(row[0])
			row[5]=int(row[5])+1
			flag=1
	if(flag==0):
		return make_response(jsonify(flag),400)			
	with open('/data/acts.csv', 'w') as csvFile:
		writer = csv.writer(csvFile)
		writer.writerows(ll1)

	csvFile.close()
	return make_response(jsonify(llll),200)

#10 Remove an act
@app.route('/api/v1/acts/<actId>',methods=['DELETE'])
def remove_act(actId):
	global stat
	if(stat==0):
		return make_response(jsonify(),500)
	lcount=[]
	with open('count.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		for row in csv_reader:
			row[0]=int(row[0])+1
			lcount.append(row[0])
	print(lcount[0])
	with open("count.csv", "wb") as f:
		writer = csv.writer(f)
		f.write(str(lcount[0]))
	f.close()
	category="temp"
	with open('/data/acts.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		flag=0
		for row in csv_reader:
			#print(row)
			if(row[0]==actId):
				flag=1
				category=row[1]
		if(flag==0):
			return make_response(jsonify("i m here in delete"),400)
	tl=[]	
	with open('/data/acts.csv', 'rb') as f:
		reader = csv.reader(f)
		l = list(reader)
		for line in l:
			if(line[0]!=actId):
				tl.append(line)	
	#print(tl)
	with open("/data/acts.csv", "wb") as f:
		writer = csv.writer(f)
		writer.writerows(tl)
	data=category
	ll1=[]
	with open('/data/t.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		flag=0
		for line in csv_reader:
			ll1.append(line)
	for row in ll1:
		if(row[0]==data):
			flag=1
		if(flag==1):
			row[1]=int(row[1])-1
	if(flag==0):
		return make_response(jsonify(flag),400)			
	with open('/data/t.csv', 'w') as csvFile:
		writer = csv.writer(csvFile)
		writer.writerows(ll1)

	csvFile.close()
	return make_response(jsonify({}), 200)

#11 Add and act
@app.route('/api/v1/acts',methods=['POST'])
def add_act():
	global stat
	if(stat==0):
		return make_response(jsonify(),500)
	lcount=[]
	with open('count.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		for row in csv_reader:
			row[0]=int(row[0])+1
			lcount.append(row[0])
	print(lcount[0])
	with open("count.csv", "wb") as f:
		writer = csv.writer(f)
		f.write(str(lcount[0]))
	f.close()
	if not request.json or not 'actId' in request.json or not 'username' or not 'timestamp' in request.json or not 'caption' in request.json or not 'imgB64' in request.json or not 'categoryName' in request.json: 
		return jsonify("I m here 1"),400
	d=[]
	actId=request.json['actId']
	category=request.json['categoryName']
	username=request.json['username']
	timestamp=request.json['timestamp']
	caption=request.json['caption']
	base64=request.json['imgB64']
	upvote=0
	try:
		datetime.datetime.strptime(timestamp, '%d-%m-%Y:%S-%M-%H')
		#print("valid")
	except ValueError:
		return make_response(jsonify(timestamp),400)
	d.append(actId)
	d.append(category)
	d.append(username)
	d.append(timestamp)
	d.append(caption)
	d.append(upvote)
	d.append(base64)
	try:
		resp=requests.get('http://52.44.207.160:80/api/v1/users')
	except:
		return make_response(jsonify(),400)
	if resp.status_code==204:
		return make_response(jsonify(),400)
	users=resp.json()
	if username in users:
		pass
	else:
		return make_response(jsonify(),400)
	with open('/data/acts.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		flag=0
		for row in csv_reader:
			if(int(row[0])==int(d[0])):
				flag=1
			if(flag==1):
				return make_response(jsonify("i m here 2"),400)
#	with open('acts.csv') as csv_file:
#		csv_reader = csv.reader(csv_file, delimiter=',')
#		flag=0
#		for row in csv_reader:
#			if(row[2]==d[2]):
#				flag=1
#			if(flag==1):
#				return make_response(jsonify("i m here"),400)

	
	data=category
	ll1=[]
	with open('/data/t.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		flag=0
		for line in csv_reader:
			ll1.append(line)
	for row in ll1:
		if(row[0]==data):
			flag=1
		if(flag==1):
			row[1]=int(row[1])+1
	if(flag==0):
		return make_response(jsonify(flag),400)			
	with open('/data/t.csv', 'w') as csvFile:
		writer = csv.writer(csvFile)
		writer.writerows(ll1)

	csvFile.close()

	
	with open('/data/acts.csv', 'a') as csvFile:
		writer = csv.writer(csvFile)
		r=d
		writer.writerow(r)
	return jsonify({}), 201 

#Assignment_4 Extra APIs

@app.route('/api/v1/_count', methods=['GET'])
def disp_count():
	global stat
	if(stat==0):
		return make_response(jsonify(),500)
	lcount=[]
	with open('count.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		for row in csv_reader:
			row[0]=int(row[0])
			lcount.append(row[0])
	print(lcount[0])
	return make_response(jsonify(lcount),200)

@app.route('/api/v1/_count', methods=['DELETE'])
def reset_count():
	global stat
	if(stat==0):
		return make_response(jsonify(),500)
	with open("count.csv", "wb") as f:
		writer = csv.writer(f)
		f.write(str(0))
	f.close()
	return make_response(jsonify(),200)

@app.route('/api/v1/acts/count', methods=['GET'])
def total_acts():
	global stat
	if(stat==0):
		return make_response(jsonify(),500)
	lcount=[]
	with open('count.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		for row in csv_reader:
			row[0]=int(row[0])+1
			lcount.append(row[0])
	print(lcount[0])
	with open("count.csv", "wb") as f:
		writer = csv.writer(f)
		f.write(str(lcount[0]))
	f.close()	
	ct=[]
	count=0
	with open('t.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		for row in csv_reader:
			count= count+int(row[1])
	ct.append(count)		
	return make_response(jsonify(ct),200)

@app.route('/api/v1/_health', methods=['GET'])
def health():
	global stat
	if(stat==0):
		return make_response(jsonify(),500)
	return make_response(jsonify(),200)

@app.route('/api/v1/_crash', methods=['POST'])
def crash():
	global stat
	stat=0
	return make_response(jsonify(),200)
if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=80)
