#!flask/bin/python
from flask import Flask, jsonify,abort,make_response,request
import csv,time,os,requests
from flask_cors import CORS,cross_origin
global port,con
port=8000
con=0
import csv
temp_list=[]
lcount=[]

with open('launched.csv') as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=',')
	for row in csv_reader:
		lcount.append(row[0])
csv_file.close()
if int(lcount[0])==0:
		command='sudo '+'docker '+'run '+'-v '+' /home/ubuntu/data:/data '+'-d '+'-p '+str(port)+':'+str(80)+' acts:latest'
		res=os.system(command)
		print(res)
		con=con+1
		tp='container'+str(con)
		wrt=[tp,port,True,1]
		temp_list.append(wrt)
		port=port+1
		time.sleep(1)
		lcount[0]=1
		with open("log1.csv", "wb") as f:
			writer = csv.writer(f)	
			writer.writerows(temp_list)

		f.close()
with open("launched.csv", "wb") as f:
		writer = csv.writer(f)
		f.write(str(lcount[0]))
f.close()

#list_map=[container_name,host_port,turn,active]
global list_maps,listall_maps
listall_maps=[]
list_maps=[]
def returnport():
	i=0
	global list_maps,listall_maps
	list_maps=[]
	listall_maps=[]
	flag=0
	with open('log1.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		for row in csv_reader:
			listall_maps.append(row)
			#if(row[3]==1):
			#	flag=1
			if (row[2]=='True') or (row[2]==True):
				row[2]=True
				list_maps.append(row)
	csv_file.close()
#	if flag==0:
#		list_maps[0][3]=1	
	csv_file.close()
	retval=[]
	for i in range(len(list_maps)):
		if(int(list_maps[i][3])==1)and(list_maps[i][2]==True):
			list_maps[i][3]=0
			lmap=[list_maps[i][0],list_maps[i][1]]
			try:				
				list_maps[i+1][3]=1
			except:
				i=-1
			list_maps[i+1][3]=1
			print list_maps
			print "\n"
			retval=lmap
			break
	for line in listall_maps:
		for line1 in list_maps:
			if line[0]==line[1]:
				line[3]=line1[3]
	#print listall_maps
	

	with open("log1.csv", "wb") as f:
		writer = csv.writer(f)
		writer.writerows(listall_maps)
	f.close()
	return retval






app = Flask(__name__)
@app.errorhandler(404)
def not_found(error):	
	return make_response(jsonify({'error': 'Not found'}), 404)



#1 List all categories
@app.route('/api/v1/categories', methods=['GET'])
def list_all_Cat():
	lcount=[]
	with open('orcount.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		for row in csv_reader:
			row[0]=int(row[0])+1
			lcount.append(row[0])
	print(lcount[0])
	with open("orcount.csv", "wb") as f:
		writer = csv.writer(f)
		f.write(str(lcount[0]))
	f.close()
	a=returnport()
	tempstr='http://localhost:'+str(a[1])+'/api/v1/categories'
	resp=requests.get(tempstr)
	print(a[1],resp.status_code)
	try:
		tempcat=resp.json()
	except:
		tempcat=[]
	return make_response(jsonify(tempcat),resp.status_code)


#2 Add a category
@app.route('/api/v1/categories',methods=['POST'])
def add_cat():
	lcount=[]
	with open('orcount.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		for row in csv_reader:
			row[0]=int(row[0])+1
			lcount.append(row[0])
	print(lcount[0])
	with open("orcount.csv", "wb") as f:
		writer = csv.writer(f)
		f.write(str(lcount[0]))
	f.close()
	a=returnport()
	tempstr='http://localhost:'+str(a[1])+'/api/v1/categories'
	data=request.get_data()	
	p=data
	print p,a[1]
	headers = {'Content-type': 'application/json'}
	resp=requests.post(tempstr,data=p,headers=headers)
	return make_response(jsonify(),resp.status_code)

#3 Delete a category
#Acts in the deleted category should be deleted -- Todo
@app.route('/api/v1/categories/<categoryname>', methods=['DELETE'])
def del_cat(categoryname):
	lcount=[]
	with open('orcount.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		for row in csv_reader:
			row[0]=int(row[0])+1
			lcount.append(row[0])
	print(lcount[0])
	with open("orcount.csv", "wb") as f:
		writer = csv.writer(f)
		f.write(str(lcount[0]))
	f.close()
	a=returnport()
	tempstr='http://localhost:'+str(a[1])+'/api/v1/categories/'+str(categoryname)
	print a[1]
	headers = {'Content-type': 'application/json'}
	resp=requests.delete(tempstr,headers=headers)
	return make_response(jsonify(),resp.status_code)
#6 List acts for a given category || #8 Acts in range of a given category
@app.route('/api/v1/categories/<categoryname>/acts', methods=['GET'])
def listall_cat(categoryname):
	lcount=[]
	with open('orcount.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		for row in csv_reader:
			row[0]=int(row[0])+1
			lcount.append(row[0])
	print(lcount[0])
	with open("orcount.csv", "wb") as f:
		writer = csv.writer(f)
		f.write(str(lcount[0]))
	f.close()
	if (request.args.get('start')==None):
		a=returnport()
		tempstr='http://localhost:'+str(a[1])+'/api/v1/categories/'+str(categoryname)+'/acts'
		resp=requests.get(tempstr)
		print(a[1],resp.status_code)
		try:
			tempcat=resp.json()
		except:
			tempcat=[]
		return make_response(jsonify(tempcat),resp.status_code)
	else:		
		a=returnport()
		start=int(request.args.get('start'))
		end=int(request.args.get('end'))
		tempstr='http://localhost:'+str(a[1])+'/api/v1/categories/'+str(categoryname)+'/acts?start='+str(start)+'&end='+str(end)
		resp=requests.get(tempstr)
		print(a[1],resp.status_code)
		try:
			tempcat=resp.json()
		except:
			tempcat=[]
		return make_response(jsonify(tempcat),resp.status_code)

#7 list number of acts in a given category
@app.route('/api/v1/categories/<categoryname>/acts/size', methods=['GET'])
def list_no_acts(categoryname):
	lcount=[]
	with open('orcount.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		for row in csv_reader:
			row[0]=int(row[0])+1
			lcount.append(row[0])
	print(lcount[0])
	with open("orcount.csv", "wb") as f:
		writer = csv.writer(f)
		f.write(str(lcount[0]))
	f.close()
	a=returnport()
	tempstr='http://localhost:'+str(a[1])+'/api/v1/categories/'+str(categoryname)+'/acts/size'
	resp=requests.get(tempstr)
	print(a[1],resp.status_code)
	try:
		tempcat=resp.json()
	except:
		tempcat=[]
	return make_response(jsonify(tempcat),resp.status_code)

#9 upvote an act
@app.route('/api/v1/acts/upvote',methods=['POST'])
def upvote():
	lcount=[]
	with open('orcount.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		for row in csv_reader:
			row[0]=int(row[0])+1
			lcount.append(row[0])
	print(lcount[0])
	with open("orcount.csv", "wb") as f:
		writer = csv.writer(f)
		f.write(str(lcount[0]))
	f.close()
	a=returnport()
	tempstr='http://localhost:'+str(a[1])+'/api/v1/acts/upvote'
	data=request.get_data()	
	p=data
	print p,a[1]
	headers = {'Content-type': 'application/json'}
	resp=requests.post(tempstr,data=p,headers=headers)
	return make_response(jsonify(),resp.status_code)

#10 Remove an act
@app.route('/api/v1/acts/<actId>',methods=['DELETE'])
def remove_acts(actId):
	lcount=[]
	with open('orcount.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		for row in csv_reader:
			row[0]=int(row[0])+1
			lcount.append(row[0])
	print(lcount[0])
	with open("orcount.csv", "wb") as f:
		writer = csv.writer(f)
		f.write(str(lcount[0]))
	f.close()
	a=returnport()
	tempstr='http://localhost:'+str(a[1])+'/api/v1/acts/'+str(actId)
	print a[1]
	headers = {'Content-type': 'application/json'}
	resp=requests.delete(tempstr,headers=headers)
	return make_response(jsonify(),resp.status_code)

#11 Add and act
@app.route('/api/v1/acts',methods=['POST'])
def add_acts():
	lcount=[]
	with open('orcount.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		for row in csv_reader:
			row[0]=int(row[0])+1
			lcount.append(row[0])
	print(lcount[0])
	with open("orcount.csv", "wb") as f:
		writer = csv.writer(f)
		f.write(str(lcount[0]))
	f.close()
	a=returnport()
	tempstr='http://localhost:'+str(a[1])+'/api/v1/acts'
	data=request.get_data()	
	p=data
	print p,a[1]
	headers = {'Content-type': 'application/json'}
	resp=requests.post(tempstr,data=p,headers=headers)
	return make_response(jsonify(),resp.status_code)

@app.route('/api/v1/_healthcheck', methods=['GET'])
def health():
	return make_response(jsonify(),200)


if __name__ == '__main__':
	app.run(debug=True,host="0.0.0.0",port=80)
