import calendar
from datetime import date,timedelta
from django.shortcuts import get_object_or_404,get_list_or_404

# A function that resets the stock overview and the cost , revenue analysis
def reset_data(company,model1,model2):
    try:
        # Check if there cost,revenue for today has been created
        todays_date = date.today()
        cost_rev = model1.objects.get(company = company,date = todays_date)
    except model1.DoesNotExist:
        # Create a new cost revenue analysis for today
        cost_rev = model1(company = company,date = todays_date)
        cost_rev.save()
        # Find the total number of stock for the
        products = company.product_set.all()
        quantity = 0
        for product in products:
            quantity += product.quantity
        # Find and update the stock overview for the company
        try: 
            stock_overview = model2.objects.get(company = company)
            stock_overview.stock = quantity
            stock_overview.stock_sold = 0
            stock_overview.save()
        except model2.DoesNotExist:
            stock_overview = model2(company = company,stock = quantity,stock_sold = 0)
            stock_overview.save()


def get_days():
    days = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
    start_index = 0
    end_index = 6
    arrange_days = []
    day_number = date.today().weekday()
    for i in range(7):
        if day_number >= 0:
            arrange_days.append(days[day_number])
        else:
            day_number = 6
            arrange_days.append(days[day_number])
        day_number -= 1
    return arrange_days



# Analysis
def general_sales_made_for_last_month(company,model):
    general_sales_data_for_last_month = [0,0,0,0]
    todays_date = date.today()
    # Get the last date of the past month
    last_month_end = todays_date - timedelta(days = todays_date.day)
    # The number of days in that month
    month_range = last_month_end.day
    for day in range(month_range - 1,-1,-1):
        quantity = 0 # Default quantity
        date_for_data = last_month_end - timedelta(days = day)
        datas = model.objects.filter(date = date_for_data,company = company)
        for data in datas:
            quantity += data.quantity
        # Week 4
        if month_range - day > 21:
            general_sales_data_for_last_month[3] += quantity
        # Week 3
        elif month_range - day > 14:
            general_sales_data_for_last_month[2] += quantity
        # Week 2
        elif month_range - day > 7:
            general_sales_data_for_last_month[1] += quantity
        # Week 1
        else:
            general_sales_data_for_last_month[0] += quantity
    return general_sales_data_for_last_month

def general_sales_made_for_the_past_7_days(company):
    general_data_for_7_days = []
    for i in range(1,8): # Loop through 7 days of the week
        quantity = 0 # Default quantity
        date_for_data = date.today() - timedelta(days = i)
#            print(date_for_data)
        # List of products on a particylar date
        datas = company.productdata_set.filter(date = date_for_data)
        for data in datas: # Loop through every product
            quantity += data.quantity # Increment
        general_data_for_7_days.append(quantity) # Quantity of goods sold on that day
    return general_data_for_7_days

def maximum_item_sold_for_the_past_7_days(company,model):
    data_for_maximum_item_sold = [] # List to store all the information for further processing
    label_for_maximum_item_sold = []
    for i in range(1,8):
        date_for_data = date.today() - timedelta(days = i)
        try:
            data = max(get_list_or_404(model,company = company,date = date_for_data),key = lambda x: x.quantity)
            data_for_maximum_item_sold.append(data.quantity)
            label_for_maximum_item_sold.append(data.product.name)
#            print(data.product.name,data.quantity)
        except Exception as e:
            data_for_maximum_item_sold.append(0)
            label_for_maximum_item_sold.append("None")
#            print(e)
    return data_for_maximum_item_sold,label_for_maximum_item_sold


def minimum_item_sold_for_the_past_7_days(company,model):
    data_for_minimum_item_sold = [] # List to store all the information for further processing
    label_for_minimum_item_sold = []
    for i in range(1,8):
        date_for_data = date.today() - timedelta(days = i)
        try:
            data = min(get_list_or_404(model,company = company,date = date_for_data),key = lambda x: x.quantity)
            data_for_minimum_item_sold.append(data.quantity)
            label_for_minimum_item_sold.append(data.product.name)
#            print(data.product.name,data.quantity)
        except Exception as e:
            data_for_minimum_item_sold.append(0)
            label_for_minimum_item_sold.append("None")
#            print(e)
    return data_for_minimum_item_sold,label_for_minimum_item_sold

def maximum_item_sold_last_month(company,model):
    todays_date = date.today() # Get todays date
    # Get the last date for last mont
    last_month_end = todays_date - timedelta(days = todays_date.day)
    data_for_last_month = [0,0,0,0]
    labels_for_maximum_item_sold_last_month = []
    products = {p.name:0 for p in company.product_set.all()} # Get all the company's products

#    print(products)
    for i in range(1,5):
        # Week 1
        if i == 1:
            # Go through 7 days in the first week
            for day in range(23,last_month_end.day):
                date_for_data = last_month_end - timedelta(days = day)
                datas = model.objects.filter(company = company,date = date_for_data)
                # Get data for each day of the week
                for data in datas:
                    # Increase the quantity of items sold for that day
                    products[data.product.name] += data.quantity
            # Find the maximum item sold for that week
            max_product = max(products,key = lambda x: products[x])
            # Update the data and label for that week
            labels_for_maximum_item_sold_last_month.append(max_product)
            data_for_last_month[0] = products[max_product]
            # Clear the products quantity for the next week
            products = {key:0 for key,value in products.items()}
        # Week 2
        elif i == 2:
            for day in range(16,23):
                date_for_data = last_month_end - timedelta(days = day)
                datas = model.objects.filter(company = company,date = date_for_data)
                for data in datas:
                    products[data.product.name] += data.quantity
            max_product = max(products,key = lambda x: products[x])
            labels_for_maximum_item_sold_last_month.append(max_product)
            data_for_last_month[1] = products[max_product]

            products = {key:0 for key,value in products.items()}
        # Week 3
        elif i == 3:
            for day in range(9,16):
                date_for_data = last_month_end - timedelta(days = day)
                datas = model.objects.filter(company = company,date = date_for_data)
                for data in datas:
                    products[data.product.name] += data.quantity
            max_product = max(products,key = lambda x: products[x])
            labels_for_maximum_item_sold_last_month.append(max_product)
            data_for_last_month[2] = products[max_product]
            products = {key:0 for key,value in products.items()}
        # Week 4
        else:
            # The number of days left in the fourth week
            rem = (last_month_end.day % 7) + 7
            for day in range(rem):
                date_for_data = last_month_end - timedelta(days = day)
                datas = model.objects.filter(company = company,date = date_for_data)
                for data in datas:
                    products[data.product.name] += data.quantity
            max_product = max(products,key = lambda x: products[x])
            labels_for_maximum_item_sold_last_month.append(max_product)
            data_for_last_month[3] = products[max_product]
            products = {key:0 for key,value in products.items()}

    return data_for_last_month,labels_for_maximum_item_sold_last_month


def minimum_item_sold_last_month(company,model):
    todays_date = date.today() # Get todays date
    # Get the last date for last mont
    last_month_end = todays_date - timedelta(days = todays_date.day)
    data_for_last_month = [0,0,0,0]
    labels_for_minimum_item_sold_last_month = []
    products = {p.name:0 for p in company.product_set.all()} # Get all the company's products

#    print(products)
    for i in range(1,5):
        # Week 1
        if i == 1:
            # Go through 7 days in the first week
            for day in range(23,last_month_end.day):
                date_for_data = last_month_end - timedelta(days = day)
                datas = model.objects.filter(company = company,date = date_for_data)
                # Get data for each day of the week
                for data in datas:
                    # Increase the quantity of items sold for that day
                    products[data.product.name] += data.quantity
            # Find the minimum item sold for that week
            min_product = min(products,key = lambda x: products[x])
            # Update the data and label for that week
            labels_for_minimum_item_sold_last_month.append(min_product)
            data_for_last_month[0] = products[min_product]
            # Clear the products quantity for the next week
            products = {key:0 for key,value in products.items()}
        # Week 2
        elif i == 2:
            for day in range(16,23):
                date_for_data = last_month_end - timedelta(days = day)
                datas = model.objects.filter(company = company,date = date_for_data)
                for data in datas:
                    products[data.product.name] += data.quantity
            min_product = min(products,key = lambda x: products[x])
            labels_for_minimum_item_sold_last_month.append(min_product)
            data_for_last_month[1] = products[min_product]

            products = {key:0 for key,value in products.items()}
        # Week 3
        elif i == 3:
            for day in range(9,16):
                date_for_data = last_month_end - timedelta(days = day)
                datas = model.objects.filter(company = company,date = date_for_data)
                for data in datas:
                    products[data.product.name] += data.quantity
            min_product = min(products,key = lambda x: products[x])
            labels_for_minimum_item_sold_last_month.append(min_product)
            data_for_last_month[2] = products[min_product]
            products = {key:0 for key,value in products.items()}
        # Week 4
        else:
            # The number of days left in the fourth week
            rem = (last_month_end.day % 7) + 7
            for day in range(rem):
                date_for_data = last_month_end - timedelta(days = day)
                datas = model.objects.filter(company = company,date = date_for_data)
                for data in datas:
                    products[data.product.name] += data.quantity
            min_product = min(products,key = lambda x: products[x])
            labels_for_minimum_item_sold_last_month.append(min_product)
            data_for_last_month[3] = products[min_product]
            products = {key:0 for key,value in products.items()}

    return data_for_last_month,labels_for_minimum_item_sold_last_month

# A function that provides the cost,revenue and profit for the past 7 days
def cost_revenue_and_profit_for_the_past_7_days(company,model):
    # A dictionary to store data for the past 7 days
    data_for_past_7_days = {
        'revenue': [],
    }
    todays_date = date.today()
    # Go through the 7 days
    for i in range(1,8):
        # Date for that day
        date_for_data = todays_date - timedelta(days = i)
        try:
            # Data for that day
            data = model.objects.get(company = company,date = date_for_data)
            # Append data gotten for that day
            data_for_past_7_days['revenue'].append(float(data.total_revenue))
        # No data was found
        except model.DoesNotExist:
            # Append default value of 0.00
            data_for_past_7_days['revenue'].append(float(0.00))

#    print(data_for_past_7_days)
    return data_for_past_7_days


# A function that provides the cost,revenue and profit for last month
def cost_revenue_and_profit_for_last_month(company,model):
    todays_date = date.today()
    # The last day of last month
    last_month_end = todays_date - timedelta(days = todays_date.day)
    # A dictionary that will store data for the month
    data_of_cost_revenue_and_profit_for_last_month = {
        'revenue': []
    }
    # A dictionary that stores the start and end day of a week
    month_range = {'Week1':(0,7),'Week2':(7,14),'Week3':(14,21),"Week4":(21,last_month_end.day)}
    # Go through each week
    for week,week_range in month_range.items():
        # A dictionary that will store data for the week
        weekly_data = {'revenue':float(0.00)}
        # Go through each day of the week
        for day in range(*week_range):
            # Date of that day
            date_for_data = last_month_end - timedelta(days = last_month_end.day - 1 - day)
            try:
                # Data for that date
                data = model.objects.get(company = company,date = date_for_data)
                weekly_data['revenue'] += float(data.total_revenue)
            # No data was found
            except model.DoesNotExist as e:
#                print(e)
                pass

        # Data gathered for the week
        for key,value in weekly_data.items():
            data_of_cost_revenue_and_profit_for_last_month[key].append(value)
#    print(data_of_cost_revenue_and_profit_for_last_month)
    return data_of_cost_revenue_and_profit_for_last_month

# A function that generates a custom product data
def custom_product_analysis(company,model,total_months,start_from):
    todays_date = date.today()
    custom_data = []
    for i in range(total_months):
        if start_from + i < todays_date.month:
            quantity = 0
            month = date(todays_date.year,start_from + i,1)
            datas = model.objects.filter(company = company,date__month = month.month, date__year = todays_date.year)
            custom_data.append(sum([data.quantity for data in datas]))
#    print(custom_data)
    return custom_data


# A function that generates a custom cost,reveneue and profit analysis
def custom_cost_revenue_profit_analysis(company,model,total_months,start_from):
    todays_date = date.today()
    custom_data = {
        'revenue': [],
    }
    for i in range(total_months):
        if start_from + i < todays_date.month:
            quantity = 0
            month = date(todays_date.year,start_from + i,1)
            print(month)
            datas = model.objects.filter(company = company,date__month = month.month,date__year = todays_date.year)
            custom_data['revenue'].append(float(sum(data.total_revenue for data in datas)))
#    print(custom_data)
    return custom_data



# Sales Reports
# A function that creates sales reports for the week
def sales_report_for_the_week(company,model):
    todays_date = date.today()
    # Get the date for last week monday
    last_week_monday = todays_date - timedelta(days = 7 + todays_date.weekday())
    # Dictionary that will store all the items bought for eah day of the week
    weekly_data = {p.name:{} for p in company.product_set.all()}
    # Add total that will be calculated at the end of the day
    weekly_data['Total'] =  {}
    # Go through 7 days in a week
    for i in range(7):
        daily_total = 0 # Daily Total
        # Date for each day
        date_for_data = last_week_monday + timedelta(days = i)
        # Dictionary to store items bought on that day
        products = {p.name:0 for p in company.product_set.all()}
        # All items bought on that day
        datas = model.objects.filter(company = company,date = date_for_data)
        # Go through each item and store it quantity in the dictionary
        for data in datas:
            products[data.product.name] = data.quantity
            daily_total += data.quantity
        # Store the day with its product in the dictionary storing weekly information
        for product,quantity in products.items():
            weekly_data[product][date_for_data.strftime('%A')] = products[product]
        # Store the daily total
        weekly_data['Total'][date_for_data.strftime('%A')] = daily_total

    # Calculate the total items bought for the week for each product
    for product,datas in weekly_data.items():
        product_weekly_total = 0
        for qty in datas.values():
            product_weekly_total += qty
        weekly_data[product]['product_weekly_total'] = product_weekly_total
#    print(weekly_data)
    return weekly_data

# A function that creates a sales report for the day
def sales_report_for_today(company,model):
    date_for_data = date.today()
    daily_data = {p.name:0 for p in company.product_set.all()}
    # Get all the items sold today
    datas = model.objects.filter(company = company,date = date_for_data)
    todays_total = 0
    for data in datas:
        daily_data[data.product.name] = data.quantity
        todays_total += data.quantity
    # Insert the total to daily data
    daily_data['Total'] = todays_total
#    print(daily_data)
    return daily_data


# A function that creates sales report for the past 7 days
def sales_report_for_the_past_7_days(company,model):
    # Get all the  products the company has
    seven_days_data = {p.name:{} for p in company.product_set.all()}
    seven_days_data['Total'] = {} # Store all the total made for each day
    todays_date = date.today()
    # Go through the past 7 days
    for day in range(1,8):
        total = 0 # Default total for that day
        date_for_data = (date.today() - timedelta(days =  day))
        # Data for that day
        datas = model.objects.filter(company = company,date = date_for_data)
        # Provide a default quantity for all the products
        for product in seven_days_data.keys():
            seven_days_data[product][date_for_data.strftime("%A")] = 0
        # Provide the right quantity for the product
        for data in datas:
            seven_days_data[data.product.name][date_for_data.strftime("%A")] = data.quantity
            total += data.quantity
        # Update the total for the day
        seven_days_data['Total'][date_for_data.strftime("%A")] = total

    # Go through each product and find the total made for the past 7 days
    for product,data in seven_days_data.items():
        product_weekly_total = sum([total for total in data.values()])
        seven_days_data[product]['total'] = product_weekly_total
#    print(seven_days_data)
    return seven_days_data


# A function that creates sales report for last month
def sales_report_for_last_month(company,model):
    # Get all the products the company has
    last_month_data = {p.name:{} for p in company.product_set.all()}
    # Add a total section to the products
    last_month_data["Total"] = {}
    last_month_end = date.today() - timedelta(days = date.today().day)
    week_range = {'Week1': (0,7),'Week2':(7,14),'Week3':(14,21),'Week4':(21,last_month_end.day)}
    for week,days_range in week_range.items():
        # Keep track of all the total for a week
        total = 0
        # Provide all the products the company has and give them a default quantity
        products = {p.name: 0 for p in company.product_set.all()}
        for day in range(*days_range):
#            print(day)
            date_for_data = last_month_end - timedelta(days = last_month_end.day - day - 1)
            # Get all the data for that day
            datas = model.objects.filter(company = company,date = date_for_data)
            # Go through every data gathered for that day
            for data in datas:
                products[data.product.name] += data.quantity
                total += data.quantity
        for product,quantity in products.items():
            last_month_data[product][week] = quantity
        # Total product sold for the week
        last_month_data['Total'][week] = total

    # Go through each item in the data and find its data
    for item,data in last_month_data.items():
        product_monthly_total = sum([i for i in data.values() ])
        last_month_data[item]['total'] = product_monthly_total

#    print(last_month_data)
    return last_month_data

# A function that generates a custom sales report
def custom_sales_report(company,model,total_months,start_from):
    todays_date = date.today()
    # A dictionary to store the data
    custom_data = {p.name: {} for p in company.product_set.all()}
    custom_data['Total'] = {} # Total section
    # Go through the range of months
    for i in range(total_months):
        # Check if the month has elapsed the current month
        if start_from + i < todays_date.month:
            total = 0
            # Get the month
            month = date(todays_date.year,start_from + i,1)
#            print(month)
            # A dictionary to store the products
            products = {p.name:0 for p in company.product_set.all()}
            # Data for that month
            datas = model.objects.filter(company = company,date__month = month.month,date__year = todays_date.year)
            # Go through the products and update its quantity
            for data in datas:
                products[data.product.name] += data.quantity
                total += data.quantity
            # Go through the data and update its quantity for the month
            for product,quantity in products.items():
                custom_data[product][month.strftime("%B")] = quantity
            custom_data['Total'][month.strftime("%B")] = total

    # Go throug the data and find its grand total
    for key,value in custom_data.items():
        custom_data[key]['total'] = sum(value.values())
#    print(custom_data)
    return custom_data

