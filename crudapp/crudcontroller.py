import MySQLdb as mdb 
import sys
from django.http import HttpResponse,HttpResponseRedirect
import cgi
from django.shortcuts import render	
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import redirect
from django.contrib import messages

def make_connection():
	try:
		con = mdb.connect('localhost','demo','demo123','crud')
		return con
	
	except mdb.Error, e:
		print "Error %d: %s" % (e.args[0],e.args[1])
		sys.exit(1)

def fn_sidebar(request):
	return render(request, 'sidebar.html')

def fn_insertTable(request,up_id):
	try:
		con=make_connection()
		cur = con.cursor(mdb.cursors.DictCursor)

		# cur.execute("DROP TABLE IF EXISTS Department")

		# cur.execute("CREATE TABLE Department(Id INT PRIMARY KEY AUTO_INCREMENT, \
		#  	Name VARCHAR(25),Noofemp INT,Hod VARCHAR(25))")

		Empname=request.POST.get('empname')
		Salary=request.POST.get('salary')
		Id=request.POST.get('deptid')
		# Id=request.POST.get('upid')

		if request.POST.get('save')=='SAVE' and up_id!='':
			cur.execute("UPDATE Department SET Name='"+Depname+"', Noofemp='"+Noofemp+"', Hod='"+Hod+"' where Id="+up_id)
			con.commit()
			con.close()
			msg='Record has been updated Successfully'
			dict1={'message':msg}
			return render(request,'insert.html',dict1)

		elif up_id:
			cur.execute('SELECT * FROM Department where Id='+up_id)
			rows = cur.fetchone()
			dict2={'data':rows}
			con.close()
			return render(request,'insert.html',dict2) 	

		else:
			cur.execute('INSERT INTO Employee_1(Ename,Salary,Dept_id) VALUES(%s,%s,%s)',(Empname,Salary,Id))
			con.commit()
			cur.execute('SELECT Id,Name FROM Department')
			rows = cur.fetchall()
			con.close()
			msg='Record has been inserted Successfully'
			dict1={'data':rows,'message':msg}
			return render(request,'insert.html',dict1) 	
			# print 'abc'
			# # messages.success(request,'Record has been inserted Successfully')
			# msg='savedata'
			# url = reverse('insertdata')
			# url = url + '?msg='+str(msg)
			# return redirect(url)	

	except Exception as e:
		print "Error %d: %s" % (e.args[0],e.args[1])
		msg='Error! Please check again'
		dict1={'errormsg':msg}
		return render(request,'insert.html',dict1)				
			
def fn_retrieveTable(request):
	con=make_connection()
	cur = con.cursor(mdb.cursors.DictCursor)
	Id=request.POST.get('deptid')
	
	# Submit=request.POST.get('submitid')
	

	if Id:
		
		cur.execute('SELECT e.Ename,e.Salary,d.Name,d.Noofemp,d.Hod FROM Employee_1 e INNER JOIN Department d ON d.Id =e.Dept_id WHERE d.Id='+Id)
		rows = cur.fetchall()
		dict2={'data':rows}
		con.close()
		return render(request,'retrieveresult.html',dict2) 
	
	else:
		
		cur.execute('SELECT e.Ename,e.Salary,d.Name,d.Noofemp,d.Hod FROM Employee_1 e INNER JOIN Department d ON e.Dept_id =d.Id')
		
		rows = cur.fetchall()
		print rows
		page = request.GET.get('page', 1)
		paginator = Paginator(rows, 8)
		try:
			rows = paginator.page(page)
		except PageNotAnInteger:
			rows = paginator.page(1)
		except EmptyPage:
			rows = paginator.page(paginator.num_pages)
		
		dict2={'data':rows}
		con.close()
		return render(request,'retrieveresult.html',dict2) 	

def fn_deleteTable(request,del_id):
	try:
		con=make_connection()
		cur = con.cursor()
		cur.execute('DELETE FROM Department where Id='+del_id)
		con.commit()
		
		# msg='abc'
		# url = reverse('retrieve')
		# url = url + '?msg='+str(msg)
		# return redirect(url)	
		messages.success(request,'Record has been deleted Successfully')
		response = redirect('retrieve')
		return response

	except Exception as e:
		print "Error %d: %s" % (e.args[0],e.args[1])
		messages.error(request,'Error! Please check again')	
		response = redirect('retrieve')
		return response	

def fn_selectdata(request,ins='',ret=''):
	
	
	Message=request.GET.get("msg")
	# print Message
	con=make_connection()
	cur = con.cursor(mdb.cursors.DictCursor)
	cur.execute('SELECT Id,Name FROM Department')
	rows = cur.fetchall()
	dict3={'data':rows}
	con.close()
	if ret:
		return render(request,'retrieve.html',dict3) 

	if ins or Message: 
		return render(request,'insert.html',dict3) 			
