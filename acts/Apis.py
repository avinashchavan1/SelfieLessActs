#!flask/bin/python
from flask import Flask, jsonify,abort
import csv
import time
import hashlib
import re
from flask import make_response
import datetime
from flask_cors import CORS,cross_origin

app = Flask(__name__)
CORS(app)	
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

#1 List all categories
@app.route('/api/v1/categories', methods=['GET'])
def list_cat():
	l={}
	with open('t.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		for row in csv_reader:
			l[row[0]] = int(row[1])
	if(len(l)==0):
		return make_response(jsonify(),204)		
	return make_response(jsonify(l),200)



#2 Add a category
from flask import request
@app.route('/api/v1/categories',methods=['POST'])
def add_cat():
	if not request.json :
		abort(400)
	data=request.json
	aa=len(data)
	with open('t.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		flag=0
		for row in csv_reader:
			if(row[0]==data[0]):
				flag=1
			if(flag==1):
				return make_response(jsonify({}),400)
	if(aa>1):
		return make_response(jsonify({}),400)
	with open('t.csv', 'a') as csvFile:
		writer = csv.writer(csvFile)
		r=[data[0],0]
		writer.writerow(r)
	return jsonify({}), 201 
			

#3 Delete a category
#Acts in the deleted category should be deleted -- Todo
@app.route('/api/v1/categories/<categoryname>', methods=['DELETE'])
def delete_cat(categoryname):
	with open('t.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		flag=0
		for row in csv_reader:
			#print(row)
			if(row[0]==categoryname):
				flag=1
		if(flag==0):
			return make_response(jsonify({'error':'Resource does not exist'}),400	)
	tl=[]	
	with open('t.csv', 'rb') as f:
		reader = csv.reader(f)
		l = list(reader)
		for line in l:
			if(line[0]!=categoryname):
				tl.append(line)	
	print(tl)
	with open("t.csv", "wb") as f:
		writer = csv.writer(f)
		writer.writerows(tl)
	return jsonify({}), 200

#4 Add a user
@app.route('/api/v1/users', methods=['POST'])
def add_user():
	if not request.json or not 'username' in request.json:
		abort(400)
	data={'username':request.json['username'],
		'password':request.json['password']
		}
	with open('users.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		flag=0
		for row in csv_reader:
			if(row[0]==data["username"]):
				flag=1
			if(flag==1):
				return make_response(jsonify(),400)
	hexval=data["password"]
	pattern = re.compile(r'\b[0-9a-f]{40}\b')
	match = re.match(pattern, hexval)
	f=0
	try:
		if(match.group(0)==hexval):
			f=1
	except:			
		pass
	if(f==1):
		with open('users.csv', 'a') as csvFile:
			writer = csv.writer(csvFile)
			r=[data["username"],data["password"]]
			writer.writerow(r)
		return jsonify({}),201 
	else:
		return jsonify(),400


#5 Delete a user
@app.route('/api/v1/users/<username>', methods=['DELETE'])
def delete_user(username):
	with open('users.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		flag=0
		for row in csv_reader:
			#print(row)
			if(row[0]==username):
				flag=1
		if(flag==0):
			return make_response(jsonify(),400)
	tl=[]	
	with open('users.csv', 'rb') as f:
		reader = csv.reader(f)
		l = list(reader)
		for line in l:
			if(line[0]!=username):
				tl.append(line)	
	print(tl)
	with open("users.csv", "wb") as f:
		writer = csv.writer(f)
		writer.writerows(tl)
	return jsonify({}), 200


#6 List acts for a given category || #8 Acts in range of a given category
@app.route('/api/v1/categories/<categoryname>/acts', methods=['GET'])
def list_acts(categoryname):
	if (request.args.get('start')==None):
		ll=[]
		with open('acts.csv', 'rb') as f:
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
		with open('acts.csv', 'rb') as f:
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
		try:
			for i in range(start,end+1):
				final.append(ll[i])
		except:
			make_response(jsonify(),400)
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
	with open('t.csv') as csv_file:
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
	if not request.json :
		abort(400)
	data=request.json
	data=int(data[0])
	ll1=[]
	with open('acts.csv') as csv_file:
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
	with open('acts.csv', 'w') as csvFile:
		writer = csv.writer(csvFile)
		writer.writerows(ll1)

	csvFile.close()
	return make_response(jsonify(llll),200)

#10 Remove an act
@app.route('/api/v1/acts/<actId>',methods=['DELETE'])
def remove_act(actId):
	category="temp"
	with open('acts.csv') as csv_file:
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
	with open('acts.csv', 'rb') as f:
		reader = csv.reader(f)
		l = list(reader)
		for line in l:
			if(line[0]!=actId):
				tl.append(line)	
	#print(tl)
	with open("acts.csv", "wb") as f:
		writer = csv.writer(f)
		writer.writerows(tl)
	data=category
	ll1=[]
	with open('t.csv') as csv_file:
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
	with open('t.csv', 'w') as csvFile:
		writer = csv.writer(csvFile)
		writer.writerows(ll1)

	csvFile.close()
	return make_response(jsonify({}), 200)

#11 Add and act
@app.route('/api/v1/acts',methods=['POST'])
def add_act():
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
	with open('acts.csv') as csv_file:
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
	with open('t.csv') as csv_file:
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
	with open('t.csv', 'w') as csvFile:
		writer = csv.writer(csvFile)
		writer.writerows(ll1)

	csvFile.close()

	
	with open('acts.csv', 'a') as csvFile:
		writer = csv.writer(csvFile)
		r=d
		writer.writerow(r)
	return jsonify({}), 201 

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0")
