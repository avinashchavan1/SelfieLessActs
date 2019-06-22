#!flask/bin/python
from flask import Flask, jsonify,abort,request
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


#4 Add a user
@app.route('/api/v1/users', methods=['POST'])
def add_user():
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

#1 List all users
@app.route('/api/v1/users', methods=['GET'])
def list_users():
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
	l=[]
	with open('users.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		for row in csv_reader:
			l.append(row[0])
	if(len(l)==0):
		return make_response(jsonify(),204)		
	return make_response(jsonify(l),200)

#Assignment_4 Extra APIs
@app.route('/api/v1/_count', methods=['GET'])
def disp_count():
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
	with open("count.csv", "wb") as f:
		writer = csv.writer(f)
		f.write(str(0))
	f.close()
	return make_response(jsonify(),200)

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=80)

