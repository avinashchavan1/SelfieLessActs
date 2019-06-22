import time,threading,csv
from fundef import stop,launch
global t_counter,count
t_counter=0
count=1
global num_con
num_con=1
def timer():
	while(True):	
		global t_counter,count
		while(t_counter<120):
			t_counter=t_counter+1
			time.sleep(1)
			#print t_counter
		t_counter=0
		count=0
		print "Reset to 0"

def read_count():
	lcount=[]
	with open('orcount.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		for row in csv_reader:
			lcount.append(row[0])
	l=lcount[0]		
	return l

def read_numberof_containers():
	l=[]
	with open('log1.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		for row in csv_reader:
			l.append(row)
	return len(l)

def auto_stop(c):
	t1=0
	t2=0
	temp=1
	if c<20:
		t1=read_numberof_containers()
		print "Requests ",c
		while(t1!=1):
			t1=read_numberof_containers()
			if t1<=1:
				break
			stop()
	if c>=20 and c<40:
		print "Requests ",c
		t1=read_numberof_containers()
		while(t1!=2):
			t1=read_numberof_containers()
			if t1<=2:
				break
			stop()
	if c>=40 and c<60:
		t1=read_numberof_containers()
		print "Requests ",c
		while(t1!=3):
			t1=read_numberof_containers()
			temp=temp+1
			if t1<=3:
				break
			stop()
	if c>=60 and c<80:
		t1=read_numberof_containers()
		print "Requests ",c
		while(t1!=4):
			t1=read_numberof_containers()
			if t1<=4:
				break
			stop()
	if c>=80 and c<100:
		t1=read_numberof_containers()
		print "Requests ",c
		while(t1!=5):
			t1=read_numberof_containers()
			if t1<=5:
				break
			stop()

	if c>=100 and c<120:
		t1=read_numberof_containers()
		print "Requests ",c
		while(t1!=6):
			if t1<=6:
				break
			stop()

	if c>=120 and c<140:
		t1=read_numberof_containers()
		print "Requests ",c
		while(t1!=7):
			t1=read_numberof_containers()
			if t1<=7:
				break
			stop()

	if c>=140 and c<160:
		t1=read_numberof_containers()
		print "Requests ",c
		while(t1!=8):
			t1=read_numberof_containers()
			if t1<=8:
				break
			stop()

	if c>=160 and c<180:
		t1=read_numberof_containers()
		print "Requests ",c
		while(t1!=9):
			t1=read_numberof_containers()
			if t1<=9:
				break
			stop()

	if c>=180 and c<200:
		t1=read_numberof_containers()
		print "Requests ",c
		while(t1!=10):
			t1=read_numberof_containers()
			if t1<=10:
				break
			stop()





def auto_start(c):
	t1=0
	t2=0
	temp=1
	if c<20:
		print "Requests ",c
		t1=read_numberof_containers()
		if t1<1:
			t1=read_numberof_containers()
			launch()
	if c>=20 and c<40:
		print "Requests ",c
		t1=read_numberof_containers()
		while(t1!=2):
			t1=read_numberof_containers()
			if t1>=2:
				break
			launch()
	if c>=40 and c<60:
		t1=read_numberof_containers()
		print "Requests ",c
		while(t1!=3):
			t1=read_numberof_containers()
			if t1>=3:
				break
			launch()
	if c>=60 and c<80:
		t1=read_numberof_containers()
		print "Requests ",c
		while(t1!=4):
			t1=read_numberof_containers()
			if t1>=4:
				break
			launch()
	if c>=80 and c<100:
		t1=read_numberof_containers()
		print "Requests ",c
		while(t1!=5):
			t1=read_numberof_containers()
			if t1>=5:
				break
			launch()

	if c>=100 and c<120:
		t1=read_numberof_containers()
		print "Requests ",c
		while(t1!=6):
			t1=read_numberof_containers()
			if t1>=6:
				break
			launch()

	if c>=120 and c<140:
		t1=read_numberof_containers()
		print "Requests ",c
		while(t1!=7):
			t1=read_numberof_containers()
			if t1>=7:
				break
			launch()

	if c>=140 and c<160:
		t1=read_numberof_containers()
		print "Requests ",c
		while(t1!=8):
			t1=read_numberof_containers()
			if t1>=8:
				break
			launch()

	if c>=160 and c<180:
		t1=read_numberof_containers()
		print "Requests ",c
		while(t1!=9):
			t1=read_numberof_containers()
			if t1>=9:
				break
			launch()

	if c>=180 and c<200:
		t1=read_numberof_containers()
		print "Requests ",c
		while(t1!=10):
			t1=read_numberof_containers()
			if t1>=10:
				break
			launch()


threading.Thread(target=timer).start()
while(True):
	c=0
	a=read_count()
	#print a,"before"
	time.sleep(120)
	b=read_count()
	#print b,"After\n"
	c=int(b)-int(a)
	print "\n\n\n"
	auto_stop(c)
	auto_start(c)

