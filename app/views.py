from datetime import date,timedelta
import calendar
from django.shortcuts import render,get_object_or_404,get_list_or_404
from django.views import generic
from django.http import JsonResponse,HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Product,Transaction,StockOverview,RevenueAnalysis,ProductData,Staff
from . import utils


# Create your views here.
# Dashboard


class IndexView(generic.View):
    """ This class shows the landing page """
    template_name = 'app/dashboard.html'

    @method_decorator(user_passes_test(test_func = lambda x : x.is_superuser))
    @method_decorator(login_required)
    def dispatch(self,request,*args,**kwargs):
        todays_date = date.today()
        transactions = request.user.companydetails.transaction_set.filter(date = todays_date)[:10]
        try:
            utils.reset_data(request.user.companydetails,RevenueAnalysis,StockOverview)
            user_stock = request.user.companydetails.stockoverview
            if user_stock.stock_left() > 0:
                stock = {
                    'width':user_stock.stock_left()/user_stock.stock,
                    'max': user_stock.stock,
                    'text': f"{user_stock.stock_left()} of {user_stock.stock} left",
                    'value': user_stock.stock_left()
                }
            else:
                stock = False
        except StockOverview.DoesNotExist:
            stock = False
        context = {
            'transactions': transactions,
            'stock':stock
        }
        response =  render(request,self.template_name,context)
        return response



class IndexAnalysisView(generic.View):
    """ This class provides the information for analysis """

    @method_decorator(user_passes_test(test_func = lambda x : x.is_superuser))
    @method_decorator(login_required)
    def post(self,request,*args,**kwargs):
        # Sales made for the past 7 days
        sales_data_for_7_days = utils.general_sales_made_for_the_past_7_days(request.user.companydetails)

        # Maximum item sold for the past 7 days
        data_for_maximum_item_sold = utils.maximum_item_sold_for_the_past_7_days(request.user.companydetails,ProductData)

        data = {
            'data_for_7_days': sales_data_for_7_days,
            'data_for_maximum_item_sold': data_for_maximum_item_sold[0],
            'product_name_for_maximum_item_sold': data_for_maximum_item_sold[1],
            'days_of_the_week': utils.get_days()
        }
        return JsonResponse(data)

# Inventory
class InventoryView(LoginRequiredMixin,UserPassesTestMixin,generic.ListView):
    """ This class shows all the inventory """
    model = Product
    template_name = 'app/inventory.html'

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        total_inventory = sum([p.quantity for p in self.request.user.companydetails.product_set.all()])
        context['total_inventory'] = total_inventory
        context['products'] = Product.objects.filter(company = self.request.user.companydetails)
        return context


class InventoryDetailView(LoginRequiredMixin,UserPassesTestMixin,generic.DetailView):
    """  This class displays all the details containing a product """
    model = Product
    template_name = 'app/inventory_detail.html'

    def test_func(self):
        return self.request.user.is_superuser


class InventoryCreateView(LoginRequiredMixin,UserPassesTestMixin,generic.CreateView):
    """ This class displays a class that creates a product """
    model = Product
    fields = ['name','quantity','unit_price','image']
    template_name = 'app/inventory_form.html'

    def form_valid(self,form):
        # Before the item is saved into the database it will be added to the stock for today
        form.instance.company = self.request.user.companydetails
        quantity = form.cleaned_data.get('quantity')
        name = form.cleaned_data.get('name')
        # Check if user's stock is being monitored
        try:
            stock = self.request.user.companydetails.stockoverview
            stock.stock += quantity # Increase it's quantity
            stock.save()
        except StockOverview.DoesNotExist:
            # Start montoring user's stock
            stock = StockOverview(
                company = self.request.user.companydetails,
                stock = quantity
            )
            stock.save()
        form.save()
        last_entered_product = Product.objects.last()
        # Create product data
        product_data = ProductData(
            company = self.request.user.companydetails,
            product = last_entered_product
        )
        product_data.save()
        messages.success(self.request,f'{name} has been successfully added to your inventory')
        return HttpResponseRedirect(reverse('app:inventory'))

    def test_func(self):
        return self.request.user.is_superuser

class InventoryEditView(LoginRequiredMixin,UserPassesTestMixin,generic.UpdateView):
    """ This class displays a class that edits a product """
    model = Product
    fields = ['name','quantity','unit_price','image']
    template_name = 'app/inventory_form.html'

    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        context['update'] = True
        return context
        
     
    def form_valid(self,form):
        # Update the stock overview
        product = super().get_object()
        name = form.cleaned_data.get('name')
        diff = form.cleaned_data.get('quantity') - product.quantity
        stock = self.request.user.companydetails.stockoverview
        stock.stock += diff
        stock.save()
        form.save()
        messages.success(self.request,f"{name} has been successfully modified")
        return HttpResponseRedirect(reverse('app:inventory'))

    def test_func(self):
        return self.request.user.is_superuser

class InventorySearchView(generic.View):
    """ This class allows the user to search for a product """

    @method_decorator(user_passes_test(test_func = lambda x : x.is_superuser))
    @method_decorator(login_required)
    def post(self,request,*args,**kwargs):
        query = request.POST.get('q').strip()
        if query:
            products = [
                {'image':p.image.url,'name':p.name,'price':p.unit_price,'qty':p.quantity,'id':p.id}
                for p in request.user.companydetails.product_set.filter(name__icontains = query)
            ]
        else:
            products = [
                {'image':p.image.url,'name':p.name,'price':p.unit_price,'qty':p.quantity,'id':p.id}
                for p in request.user.companydetails.product_set.all()
            ]
        data = {
            'products':products,
            'create_inventory_url': reverse('app:inventory_create')
        }
        return JsonResponse(data)


class InventoryAnalysisView(generic.View):
    """ This class is responsible for delivering all the information for analysing a product """

    @method_decorator(user_passes_test(test_func = lambda x : x.is_superuser))
    @method_decorator(login_required)
    def post(self,request,*args,**kwargs):
        product_id = int(request.POST.get('productId'))
        product = get_object_or_404(Product,id = product_id)
        product_date = get_list_or_404(ProductData,company = request.user.companydetails,product = product)[0].date
        days_left = timedelta(days = product_date.day)
        past_month = (product_date - days_left).strftime("%B")
        data_for_7_days = []
        data_for_last_month = [0,0,0,0]

        # 7 days in a week
        for i in range(1,8):
            date_for_data = date.today() - timedelta(days = i)
            try:
                # Get the data for each day
                data = get_object_or_404(ProductData,company = request.user.companydetails,product = product,date = date_for_data)
                data_for_7_days.append(data.quantity)
            except Exception as e:
                # No data for that date
#                print(e)
                data_for_7_days.append(0)


        past_month_date = product_date - days_left
        # Past Month
        for day in range(past_month_date.day -1,-1,-1):
            date_for_data =  past_month_date - timedelta(days = day)
#            print(date_for_data,day)
            try:
                data = get_object_or_404(ProductData,company = request.user.companydetails,product = product,date = date_for_data)
                if past_month_date.day - day > 21:
#                    print("More than 21",date_for_data.strftime("%A"),date_for_data)
                    data_for_last_month[3] += data.quantity
                elif past_month_date.day - day > 14:
#                    print("More than 14",date_for_data.strftime("%A"),date_for_data)
                    data_for_last_month[2] += data.quantity
                elif past_month_date.day - day > 7:
#                    print("More than 7",date_for_data.strftime("%A"),date_for_data)
                    data_for_last_month[1] += data.quantity
                else:
#                    print("More than 0",date_for_data.strftime("%A"),date_for_data)
                    data_for_last_month[0] += data.quantity
            except Exception as e:
                print(e)

        data = {
            'data_for_7_days' : data_for_7_days,
            'days_of_the_week' : utils.get_days(),
            'past_month': past_month,
            'data_for_last_month': data_for_last_month,
            'weeks': ['Week 1','Week 2','Week 3','Week 4']
        }
        return JsonResponse(data)

class InventoryDeleteView(generic.View):
    """ This class deletes a product """

    @method_decorator(user_passes_test(test_func = lambda x : x.is_superuser))
    @method_decorator(login_required)
    def post(self,request,*args,**kwargs):
        product_id = int(request.POST.get('productId'))
        # Get The Product
        prod = get_object_or_404(Product,company = request.user.companydetails,id = product_id)
        # Modify the stock overview
        stock = request.user.companydetails.stockoverview
        stock.stock -= prod.quantity
        stock.save()
        # Delete the stock
        prod.delete()
        data = {}
        return JsonResponse(data)


# Staffs
class StaffsListView(LoginRequiredMixin,UserPassesTestMixin,generic.ListView):
    model = Staff
    context_object_name = 'staffs'
    template_name = 'app/staffs.html'

    def get_queryset(self):
        return Staff.objects.filter(company = self.request.user.companydetails)

    def test_func(self):
        return self.request.user.is_superuser



class StaffAddView(generic.View):

    @method_decorator(user_passes_test(test_func = lambda x : x.is_superuser))
    @method_decorator(login_required)
    def post(self,request):
        # Get info
        company = request.user.companydetails
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        password = request.POST.get('password')
        # Generate username
        username = f"{first_name[0].lower()}{last_name.replace(' ','').lower()}"
        # # Number of different username
        usernameCount = User.objects.filter(username__contains = username)
        username += str(usernameCount.count() + 1)
        password = request.POST.get('password')
        user = User(username=username,password=password,first_name=first_name,last_name=last_name)
        user.save()
        staff = Staff(user = user, company = company)
        staff.save()

        return JsonResponse({'status':'success','username':username,'staffId':user.id})


class StaffDeleteView(generic.View):

    @method_decorator(user_passes_test(test_func = lambda x : x.is_superuser))
    @method_decorator(login_required)
    def post(self,request):
        staff_id = int(request.POST.get('staffId'))
        staff = User.objects.get(id = staff_id)
        staff.delete()
        return JsonResponse({'status':'success'})


# Transaction
class TransactionsView(LoginRequiredMixin,UserPassesTestMixin,generic.ListView):
    """ This class shows all the transactions """
    context_object_name = 'transactions'
    template_name = 'app/transactions.html'

    def get_queryset(self,*args,**kwargs):
        todays_date = date.today()
        return self.request.user.staff.company.transaction_set.filter(date = todays_date)[::-1]

    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        todays_date = date.today()
        context['total_transaction_for_today'] = len(context['transactions'])
        return context

    def test_func(self):
        return not self.request.user.is_superuser



class TransactionCreateView(generic.View):
    """ This page creates a transaction """
    template_name = 'app/transaction_create.html'


    @method_decorator(user_passes_test(test_func = lambda x : not x.is_superuser))
    @method_decorator(login_required)
    def dispatch(self,request,*args,**kwargs):
        return render(request,self.template_name)

class SearchProductView(generic.View):
    """ This class is reponsible for searching for a product """

    @method_decorator(user_passes_test(test_func = lambda x : not x.is_superuser))
    @method_decorator(login_required)
    def post(self,request,*args,**kwargs):
        query = request.POST.get('value').strip()
        product_list = [{'image':p.image.url,'name':p.name,'price':p.unit_price,'qty':p.quantity} for p in request.user.staff.company.product_set.all().filter(name__icontains = query)]
#        print(product_list)
        data = {
            'products': product_list[:2]
        }
        return JsonResponse(data)

class SaveTransactionView(generic.View):
    """ This class is responsible for saving a new transaction """


    @method_decorator(user_passes_test(test_func = lambda x : not x.is_superuser))
    @method_decorator(login_required)
    def post(self,request,*args,**kwargs):
        total = float(request.POST.get('total'))
        product_names = list(filter(lambda x: x!='',request.POST.get('productNames').split(',')))
        product_qty = list(filter(lambda x: x!='',request.POST.get('productQty').split(',')));
        total_products_sold = 0
        data = {}
        try:
            # Create a new transaction
            transaction = Transaction(company = request.user.staff.company,total = total)
            transaction.save()
            for num,name in enumerate(product_names):
                # First reduce the products quantity
                prod = request.user.staff.company.product_set.all().get(name = name)
                prod.quantity -= int(product_qty[num])
                prod.save()
                # Then save the product's item to the transaction
                transaction.transactionitem_set.create(
                    product_name = name,
                    product_price = prod.unit_price,
                    product_quantity = int(product_qty[num]),
                    total = prod.unit_price * int(product_qty[num])
                )
                # Save the product being added to the transaction to its data which will be used for analysis
                try:
                    product_data = get_object_or_404(ProductData,date = date.today(),product = prod)
                    product_data.quantity += int(product_qty[num])
                    product_data.save()
                except Exception as e:
                    product_data = ProductData(company = request.user.staff.company,product = prod,quantity = int(product_qty[num]))
                    product_data.save()
                # Increase the total reveneue and total number of products gotten from the transaction
                total_products_sold += int(product_qty[num])
            # Modify the revenue and revenue made for the day
            revenue_analysis = get_object_or_404(RevenueAnalysis,company = request.user.staff.company,date = date.today())
            revenue_analysis.total_revenue += revenue_analysis.total_revenue.from_float(float(total))
            revenue_analysis.save()
            # Modify the stock overview for the day
            stock_overview = get_object_or_404(StockOverview,company = request.user.staff.company)
            stock_overview.stock_sold += total_products_sold
            stock_overview.save()
            data['status'] = 'success'
            data['redirect_url'] = reverse('app:transactions')

        except Exception as e:
#            print(e)
            data['status'] = 'error'
        return JsonResponse(data)


# Analysis
class AnalysisView(generic.View):
    """ This class shows all the analysis for a company """
    template_name = 'app/analysis.html'

    @method_decorator(user_passes_test(test_func = lambda x : x.is_superuser))
    @method_decorator(login_required)
    def dispatch(self,request,*args,**kwargs):
        context = {}
        context['data_available'] = True if request.user.companydetails.productdata_set.all().count() > 0 and request.user.companydetails.revenueanalysis_set.all().count() > 0 else False
        return render(request,self.template_name,context)

class GeneralAnalysisView(generic.View):
    """ This class provides all the information for making analysis """

    @method_decorator(user_passes_test(test_func = lambda x : x.is_superuser))
    @method_decorator(login_required)
    def post(self,request,*args,**kwargs):
        past_month = (date.today() - timedelta(days = date.today().day)).strftime("%B")

        # Sales made for the past 7 days
        sales_data_for_7_days = utils.general_sales_made_for_the_past_7_days(request.user.companydetails)

        # Sales for last month
        sales_data_for_last_month = utils.general_sales_made_for_last_month(request.user.companydetails,ProductData)

        # Maximum Item Sold For The Past 7 Days
        data_for_maximum_item_sold_last_7_days = utils.maximum_item_sold_for_the_past_7_days(request.user.companydetails,ProductData)

        # Minimum Item Sold For The Past 7 Days
        data_for_minimum_item_sold_last_7_days = utils.minimum_item_sold_for_the_past_7_days(request.user.companydetails,ProductData)

        # Maximum item sold last month
        data_for_maximum_item_sold_last_month = utils.maximum_item_sold_last_month(request.user.companydetails,ProductData)

        # Minimum item sold last month
        data_for_minimum_item_sold_last_month = utils.minimum_item_sold_last_month(request.user.companydetails,ProductData)

        # Revenue For The Past 7 Days
        data_for_reveue_for_the_past_7_days = utils.revenue_for_the_past_7_days(request.user.companydetails,RevenueAnalysis)

        # Revenue For Last Month
        data_for_revenue_for_last_month = utils.revenue_for_last_month(request.user.companydetails,RevenueAnalysis)

        data = {
            'sales_data_for_7_days': sales_data_for_7_days,
            'days_of_the_week': utils.get_days(),
            'sales_data_for_last_month': sales_data_for_last_month,
            'weeks': ['Week 1','Week 2','Week 3','Week 4'],
            'data_for_maximum_item_sold_last_7_days': data_for_maximum_item_sold_last_7_days[0],
            'product_name_for_maximum_item_sold_last_7_days': data_for_maximum_item_sold_last_7_days[1],
            'data_for_minimum_item_sold_last_7_days': data_for_minimum_item_sold_last_7_days[0],
            'product_name_for_minimum_item_sold_last_7_days': data_for_minimum_item_sold_last_7_days[1],
            'data_for_maximum_item_sold_last_month': data_for_maximum_item_sold_last_month[0],
            'product_name_for_maximum_item_sold_last_month': data_for_maximum_item_sold_last_month[1],
            'data_for_minimum_item_sold_last_month': data_for_minimum_item_sold_last_month[0],
            'product_name_for_minimum_item_sold_last_month': data_for_minimum_item_sold_last_month[1],
            'past_month': past_month,
            'revenue_for_the_past_7_days': data_for_reveue_for_the_past_7_days['revenue'],
            'revenue_for_last_month': data_for_revenue_for_last_month['revenue'],
        }
        return JsonResponse(data)


# Sales Report
class SalesReportView(generic.View):
    """ This class is responsible for displaying the sales reports page """
    template_name = 'app/sales_reports.html'

    @method_decorator(user_passes_test(test_func = lambda x : x.is_superuser))
    @method_decorator(login_required)
    def dispatch(self,request,*args,**kwargs):
        return render(request,self.template_name)


class SalesReportTemplateView(generic.View):
    template_name = 'app/sales_report_template.html'


    @method_decorator(user_passes_test(test_func = lambda x : x.is_superuser))
    @method_decorator(login_required)
    def dispatch(self,request,*args,**kwargs):
        duration = self.kwargs.get("duration");
        if duration == 'last-week':
            # Get the date of last week monday
            last_week_monday = date.today() - timedelta(days = 7 + date.today().weekday())
            # Get the date of last week sunday
            last_week_sunday = last_week_monday + timedelta(days = 6)
            title = f"Sales Report For {last_week_monday.strftime('%A %b %d, %Y')} To {last_week_sunday.strftime('%A %b %d, %Y')}"
            data = utils.sales_report_for_the_week(request.user.companydetails,ProductData)
            context = {
                'data': data,
                'title': title,
                'total': data['Total']['product_weekly_total']
            }

        elif duration == 'today':
            todays_date = date.today()
            data = utils.sales_report_for_today(request.user.companydetails,ProductData)
            context = {
                'title': f"Sales Report For Today {date.today().strftime('%A %b %d, %Y')}.",
                'data': data,
                'total': data['Total']
            }
        elif duration == 'past-7-days':
            yesterday = date.today() - timedelta(days = 1)
            last_7_days = date.today() - timedelta(days = 7)
            title = f"Sales Report From {last_7_days.strftime('%A %b %d,%Y')} To {yesterday.strftime('%A %b %d, %Y')}."
            data = utils.sales_report_for_the_past_7_days(request.user.companydetails,ProductData)
            context = {
                'data' : data,
                'past_7_days': utils.get_days(),
                'total': data['Total']['total'],
                'title': title
            }
        elif duration == 'last-month':
            data = utils.sales_report_for_last_month(request.user.companydetails,ProductData)
            last_month = date.today() - timedelta(days = date.today().day)
            title = f"Sales Report For Last Month, {last_month.strftime('%B %Y')}"
            context = {
                'data': data,
                'total': data['Total']['total'],
                'title': title
            }
        elif duration == 'custom':
            # Get the total number of months and start month
            total_months = int(request.GET.get('tm'))
            start_from = int(request.GET.get('sf'))
            start_month = date(2020,start_from,1).strftime('%B')
            end_month = date(2020,start_from + total_months - 1,1).strftime("%B") if start_from + total_months < date.today().month else date(2020,date.today().month - 1,1).strftime("%B")
            # Get the data
            data = utils.custom_sales_report(request.user.companydetails,ProductData,total_months,start_from)
            # Generate the title
            title = f"Sales Report From {start_month} {date.today().year} To {end_month} {date.today().year}."
            # A list to store the months
            months = []
            for i in range(total_months):
                if start_from + i < date.today().month:
                    months.append(date(date.today().year,start_from + i,1).strftime("%B"))

            context = {
                'data': data,
                'total': data['Total']['total'],
                'title': title,
                'months': months
            }
            pass
        context['duration'] = duration
        response = render(request,self.template_name,context)
        return response


class CustomAnalysisView(generic.View):
    """ This view displays a page where users can generate a custom product or revenue analysis """
    template_name = 'app/custom_analysis.html'


    @method_decorator(user_passes_test(test_func = lambda x : x.is_superuser))
    @method_decorator(login_required)
    def dispatch(self,request,*args,**kwargs):
        context = {'type': self.kwargs.get('type')}
        return render(request,self.template_name,context)


class GenerateCustomAnalysisView(generic.View):
    """ This class genrates a custom data for analysis """


    @method_decorator(user_passes_test(test_func = lambda x : x.is_superuser))
    @method_decorator(login_required)
    def post(self,request,*args,**kwargs):
        analysis_type = request.POST.get('analysisType')
        total_months = int(request.POST.get('totalMonths'))
        start_from  = int(request.POST.get('startFrom'))
        start_month = date(date.today().year,start_from,1).strftime("%B");
        end_month = date(date.today().year,start_from + total_months - 1,1).strftime("%B") if start_from + total_months < date.today().month else date(date.today().year,date.today().month - 1,1).strftime("%B")
#        print(start_month)
#        print(end_month)
        if analysis_type == 'product':
            title = f"Total Number Of Goods Sold From {start_month} {date.today().year} To {end_month} {date.today().year}"
            custom_data = utils.custom_product_analysis(request.user.companydetails,ProductData,total_months,start_from)
            data = {
                'custom_data': custom_data
            }
        elif analysis_type == 'revenue':
            title = f"Total Number Of Goods Sold From {start_month} {date.today().year} To {end_month} {date.today().year}"
            custom_data = utils.custom_revenue_analysis(request.user.companydetails,RevenueAnalysis,total_months,start_from)
            data = {
                'revenue': custom_data['revenue'],
            }

        months = []
        for i in range(total_months):
            if start_from + i < date.today().month:
                months.append(date(date.today().year,start_from + i, 1).strftime("%B"))


        data['title'] = title
        data['months'] = months
        return JsonResponse(data)
