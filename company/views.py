from django.shortcuts import render
from django.views import generic
from django.contrib.auth.views import LoginView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import UserForm,CompanyDetailsForm

# Create your views here.
class CompanyLoginView(LoginView):
    template_name = 'company/login.html'

    def get_success_url(self,*args,**kwargs):
        print("Wow")
        if self.request.POST.get('next'):
            return self.request.POST.get('next')
        return reverse('app:home')


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
