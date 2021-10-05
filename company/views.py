from django.contrib import messages
from django.contrib import auth
from django.http.response import HttpResponseRedirect
from app.models import CompanyDetails
from django.http import request
from django.contrib.auth import login,authenticate
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.contrib.auth.views import LoginView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import UserForm,CompanyDetailsForm

# Create your views here.
class CompanyLoginView(generic.View):
    template_name = 'company/login.html'

    def get(self,request):
        print("Get")
        return render(request,self.template_name)

    def post(self,request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        # Admin authentication
        user = authenticate(username = username,password = password)
        if user is not None:
            login(request,user)
            return HttpResponseRedirect(request.GET.get('next')) if request.GET.get('next') else HttpResponseRedirect(reverse('app:home'))
        else:
            # Staff authentication
            try:
                user = User.objects.get(username = username,password = password)
                login(request,user)
                return HttpResponseRedirect(reverse('app:transactions'))
            except User.DoesNotExist:
                messages.error(request,"Invalid username and/or password")
                
        return render(request,self.template_name)

class CompanyProfileView(generic.View):
    """ This class is reponsible for displaying the company's profile """
    form_class1 = UserForm
    form_class2 = CompanyDetailsForm
    template_name = 'company/company_profile.html'

    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        form1 = self.form_class1(instance =  request.user)
        form2 = self.form_class2(instance = request.user.companydetails)
        context = {
            'form1': form1,
            'form2': form2
        }
        return render(request,self.template_name,context)

    @method_decorator(login_required)
    def post(self,request,*args,**kwargs):
        form1 = self.form_class1(request.POST,request.FILES,instance =  request.user)
        form2 = self.form_class2(request.POST,request.FILES,instance = request.user.companydetails)
        context = {
            'form1': form1,
            'form2': form2
        }
        if form1.is_valid() and form2.is_valid():
            print("Valid Form")
            form1.save()
            form2.save()
        return render(request,self.template_name,context)
