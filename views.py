from django import template
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.template import Context
from django.template.loader import get_template
from django.contrib.auth.forms import AuthenticationForm
from blog.models import staff
from blog.models import mattress 
from blog.models import transaction
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json

# Create your views here.
def index(request):
    return render(request,template_name='home.html')
def addemp(request):
    if request.method == 'POST' and request.POST.get('go') and request.POST.get('chk') in ["1"]:
        newstaff = staff()
        newstaff.firstname = request.POST.get('fn')
        newstaff.lastname = request.POST.get('ln')
        newstaff.address = request.POST.get('add')
        newstaff.phone = request.POST.get('mob')
        newstaff.nok_firstname = request.POST.get('nokfn')
        newstaff.nok_lastname = request.POST.get('nokln')
        newstaff.nok_phone = request.POST.get('nokmob')
        newstaff.section = request.POST.get('sect')
        newstaff.email = request.POST.get('email')
        newstaff.staffid = 1
        newstaff.save()
        return render(request,template_name='addEmployee.html',context = {'staffs':staff.objects.all(),'message':'Save Success!!'})
    elif request.method == 'POST' and request.POST.get('go') and request.POST.get('chk') in ["2"]:
        eid = request.POST.get('eid')
        exstaff = staff.objects.get(id = eid)
        exstaff.firstname = request.POST.get('fn')
        exstaff.lastname = request.POST.get('ln')
        exstaff.address = request.POST.get('add')
        exstaff.phone = request.POST.get('mob')
        exstaff.nok_firstname = request.POST.get('nokfn')
        exstaff.nok_lastname = request.POST.get('nokln')
        exstaff.nok_phone = request.POST.get('nokmob')
        exstaff.section = request.POST.get('sect')
        exstaff.email = request.POST.get('email')
        exstaff.staffid = 1
        exstaff.save()
        return render(request,template_name='addEmployee.html',context = {'staffs':staff.objects.all(),'message':'Update Success!!'})
    elif request.method == 'POST' and request.POST.get('more'):
        eid = request.POST.get('select')
        employee  = staff.objects.get(id = eid)
        return render(request,template_name ='addEmployee.html',context = {'emp':employee,'staffs':staff.objects.all()})

    else:
        allstaffs = staff.objects.all()
        return render(request,template_name ='addEmployee.html',context = {'staffs':allstaffs})
def addproduct(request):
    if request.method == 'POST' and request.POST.get('go') and request.POST.get('chk') in ["1"]:
        prod = mattress()
        prod.length = request.POST.get('len')
        prod.width = request.POST.get('wid')
        prod.thickness = request.POST.get('thick')
        prod.shortname =  request.POST.get('sname')
        prod.price = request.POST.get('price')
        prod.wrap = request.POST.get('wrap')
        prod.lap  = request.POST.get('lap')
        prod.mattressID = 101
        prod.OrgID = 'VitaFoam'
        prod.save()
        return render(request,template_name='addProduct.html',context = {'products':mattress.objects.all(),'message':'Save Success!!'})
    elif request.method == 'POST' and request.POST.get('go') and request.POST.get('chk') in ["2"]:
        prod = mattress.objects.get(id = request.POST('pid'))
        prod.length = request.POST.get('len')
        prod.width = request.POST.get('wid')
        prod.thickness = request.POST.get('thick')
        prod.shortname =  request.POST.get('sname')
        prod.price = request.POST.get('price')
        prod.wrap = request.POST.get('wrap')
        prod.lap  = request.POST.get('lap')
        prod.mattressID = 101
        prod.OrgID = 'VitaFoam'
        prod.save()
        return render(request,'addProduct.html',{'products':mattress.objects.all(),'message':'Update Success'})
    elif request.method == 'POST' and  request.POST.get('more'):
        pid = request.POST.get('select')
        mattInfo  = mattress.objects.get(id = pid)
        return render(request,template_name ='addProduct.html',context = {'mat':mattInfo,'products':mattress.objects.all()})

    else:
        return render(request,'addProduct.html',{'products':mattress.objects.all()})
@csrf_exempt
def addtransaction(request):
    if request.method == 'POST' and request.POST.getlist('items[]'):
        items = request.POST.getlist('items[]')
        try:
            for item in items:
                pars = item.split(',')
                t = transaction()
                t.mattressID = int(pars[0])
                t.staffId = int(pars[1])
                t.quantity = int(pars[2])
                t.datesewn = pars[3]
                t.save()
            return HttpResponse('Commit Success')
        except:
            return HttpResponse(' Commit Failure')
    elif request.method == 'POST' and request.POST.get('qnty') and request.POST.get('trid'):
        try:
            qty = request.POST.get('qnty')
            tranid = request.POST.get('trid')
            tx = transaction.objects.get(id = tranid)
            tx.quantity = int(qty)
            tx.save()
            return HttpResponse('Update Success')
        except:
            return HttpResponse('Update Failure')
    elif request.method == 'POST' and request.POST.get('sname') and request.POST.get('sdate'):
        try:
            sname = request.POST.get('sname')
            sdate = request.POST.get('sdate')
            bydate = request.POST.get('bydate')
            byname = request.POST.get('byname')
            trans= transaction.objects.filter(staffId = int(sname),datesewn = sdate)
            values = []
            for t in trans:
             p = staff.objects.get(id = t.staffId)
             prod = mattress.objects.get(id = t.mattressID)
             matcode = str(prod.length) +' X '+str(prod.width)+' X '+str(prod.thickness)+prod.shortname
             value = {'prodid':prod.id,'transid':t.id,'operator':p.firstname + ' ' + p.lastname,'mattress':matcode,'quantity':t.quantity}
             values.append(value)
            jobject = json.dumps(values)
            return HttpResponse(jobject)
            #return HttpResponse('Success')
        except transaction.DoesNotExist:
            return HttpResponse('Transaction does not exist')
        except Exception as e:
            return HttpResponse(e)

    else:
        return render(request,'addtransaction.html',{'staffs':staff.objects.all,'products':mattress.objects.all()})
@csrf_exempt
def reporting(request):
    if request.method == 'POST' and request.POST.get('name') and request.POST.get('byname'):
        return HttpResponse('Filter By Name')
    elif request.method == 'POST'and request.POST.get('start') and request.POST.get('end'):
        try:
         start = request.POST.get('start')
         end = request.POST.get('end')
         txs  = transaction.objects.filter(datesewn__gte = start,datesewn__lte =end).order_by('staffId')
         values = []
         name = ''
         for tx in txs:
             p = 5

        except Exception as e:
            return HttpResponse(e)
    return render(request,'reporting.html',{'staffs': staff.objects.all})