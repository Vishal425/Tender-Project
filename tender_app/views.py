from django.shortcuts import render,redirect
from django.http.response import HttpResponse
from matplotlib.style import context
from .models import test_tender_model

from numpy import frombuffer

from tender_app.forms import CountryForm,CreateUserForm
from django.template import RequestContext
import pandas as pd
from django.db.models import Q
from django.db import connection
#registration
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,logout,login
from django.contrib import messages
# from tender_app import scrap


# def search(request):
    
#     form = CountryForm(request.POST or None)

#     if request.method == "GET":

#         query = request.GET.get('search')

#         if query:

#             ## results = test_tender_model.objects.filter(Q(Tender_Title__icontains=query) )
#             dfs_query="SELECT * FROM TEST_TENDER_MODEL WHERE Tender_Title like  upper('% {} %') ".format(query)
#             tenders_=pd.read_sql_query(dfs_query,connection)

#             if int(len(tenders_))>0:
#                 tenders_=tenders_.to_dict(orient='records')
#             # #print(tenders_)
#             return render(request,r'D:\Python_Project\py\web_scraping\task\tender_project\tender\tender_app\templates\dashboard.html', {'student': tenders_,'form': form})
#         else:
#             return render(request,r'D:\Python_Project\py\web_scraping\task\tender_project\tender\tender_app\templates\dashboard.html',{'form': form})#, {'student': tenders_} 
      
        
#     # #if request.method == 'GET':
#     else:

#         return render(request,r'D:\Python_Project\py\web_scraping\task\tender_project\tender\tender_app\templates\dashboard.html',{'form': form})#, {'student': tenders_})


#########################################
  
def show(request):  

    form = CountryForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form = CountryForm()

        fruits_ = request.POST.getlist("KEYWORDS")
        print(fruits_)
        # fruits_ = request.POST.getlist('fruits') 
        
        fruits_ = list(map(lambda x:x.upper(), fruits_))
        print(fruits_)

        pattern = '|'.join(fruits_)
        # pattern = r'\b{}\b'.format('|'.join(fruits_))
        print(pattern)

        dfs_query="SELECT * FROM TEST_TENDER_MODEL WHERE regexp_like (Tender_Title, '{}') ".format(pattern)
        tenders_=pd.read_sql_query(dfs_query,connection)
    

        if int(len(tenders_))>0:
            tenders_=tenders_.to_dict(orient='records')
            # print(tenders_)
            return render(request,'dashboard.html', {'student': tenders_,'form': form})
        else:
            return render(request,'dashboard.html',{'form': form})#, {'student': tenders_} 
 
        
    # if request.method == 'GET':
    else:

        return render(request,'dashboard.html',{'form': form})#, {'student': tenders_})

        ###########################
def search(request):
        
    form = CountryForm(request.POST or None)

    if request.method == "GET":

        query = request.GET.get('search')

        if query:

            # results = test_tender_model.objects.filter(Q(Tender_Title__icontains=query) )
            dfs_query="SELECT * FROM TEST_TENDER_MODEL WHERE Tender_Title like  upper('% {} %') ".format(query)
            tenders1=pd.read_sql_query(dfs_query,connection)

            if int(len(tenders1))>0:
                tenders1=tenders1.to_dict(orient='records')
                return render(request, 'dashboard.html', { 'student': tenders1})
            else:
                return render(request,'dashboard.html')
        if request.method == 'GET':        
            return render(request, 'dashboard.html')
    

#registration
def logout(request):
    return render(request, 'home.html')        
#registration
def indexView(request):
    return render(request,'home.html')   
@login_required
def dashboardView(request):
    return redirect (request,'index')

def registerView(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user=form.cleaned_data.get('username')
            messages.success (request,'account was created for' + user)
            return redirect('login_url')
            

    else:
        form = CreateUserForm()
    return render(request,'registration/register.html',{'form':form}) 
    # context ={'form':form}
    # return render (request,'register.html',context)
    
def index(request):
    shelf = test_tender_model.objects.all()
    return render(request, 'dashboard.html', {'shelf': shelf})

def demo(request):
    return render(request, 'demo.html')    
    
def base(request):
    return render(request, 'base.html') 

def sample(request):
    #your python script code
    # output=code output
    return render(request,'scroll.html')    

    