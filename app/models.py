import os
from PIL import Image
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Product(models.Model):
    """ This class stores all the details of a product """
    company = models.ForeignKey(User,on_delete = models.CASCADE)
    name = models.CharField(max_length = 200)
    unit_price = models.DecimalField(decimal_places = 2, max_digits = 65,default = 0.00)
    quantity = models.PositiveIntegerField(default = 1)
    image = models.ImageField(upload_to = f"product_images",default = 'product_logo.png')

    def __str__(self):
        return f"{self.company.companydetails.name} - {self.name}"

    def save(self):
        super().save()
        if self.image.url != '\media\product_logo.png':
            img = Image.open(self.image.path)
            img = img.resize((500,500))
            img.save(self.image.path)

    def delete(self):
        image = self.image
        super().delete()
        if image.url != '/media/product_logo.png':
            os.remove(image.path)

    def get_absolute_url(self):
        return reverse('app:inventory')


class CompanyDetails(models.Model):
    """ This class stores all the details about a company """
    user = models.OneToOneField(User,on_delete = models.CASCADE)
    name = models.CharField(max_length = 100)
    image = models.ImageField(upload_to = 'company_logo',default = "default_company_logo.png")
    mobile1 = models.CharField(max_length = 30)
    mobile2 = models.CharField(max_length = 30, null = True, blank  = True)
    location = models.CharField(max_length = 200)

    def __str__(self):
        return f"{self.name}"

    def save(self):
        super().save()
        img = Image.open(self.image.path)
        img = img.resize((500,400))
        img.save(self.image.path)

    def delete(self):
        img = self.image.path
        super().delete()
        os.remove(img)

class StockOverview(models.Model):
    """ This class stores all the stock for a company """
    company = models.OneToOneField(User,on_delete = models.CASCADE)
    stock = models.PositiveIntegerField(default = 0)
    stock_sold = models.PositiveIntegerField(default = 0)

    def __str__(self):
        return f"{self.company.companydetails.name} stock overview"

    def stock_left(self):
        return self.stock - self.stock_sold

class CostRevenueAnalysis(models.Model):
    """ This class stores the total cost and total revernu made for each day """
    company = models.ForeignKey(User,on_delete = models.CASCADE)
    total_revenue = models.DecimalField(max_digits = 1000,decimal_places = 2,default = 0)
    date = models.DateField(default = timezone.now)

    def __str__(self):
        return f"Total cost and total revenue for {self.company.companydetails.name} on {self.date.strftime('%A')}, {self.date}"

#    def __str__(self):
#        return f"Cost, Revenue analysis for {self.company.companydetails.name}"

    def profit(self):
        return self.total_revenue - self.total_cost

    class Meta:
        ordering = ['-date']


class ProductData(models.Model):
    """ This class stores all data relating to a product which will be used for analysis """
    company = models.ForeignKey(User,on_delete = models.CASCADE)
    product = models.ForeignKey(Product,on_delete = models.CASCADE)
    date = models.DateField(default = timezone.now,blank = True)
    quantity = models.PositiveIntegerField(default = 0)

    def __str__(self):
        return f"{self.company.companydetails.name} - {self.product.name} data for {self.date.strftime('%A')}. {self.date}"


    class Meta:
        ordering = ['-date','product']

class Transaction(models.Model):
    """ This class stores all the transactions relating to a company """
    company = models.ForeignKey(User,on_delete = models.CASCADE)
    total = models.DecimalField(max_digits = 65,decimal_places = 2)
    date = models.DateField(default = timezone.now)

    def __str__(self):
        return f"{self.company.companydetails.name} transaction {self.id}"

    class Meta:
        ordering = ['-date']


class TransactionItem(models.Model):
    """ This class stores all the items for a single transaction """
    transaction = models.ForeignKey(Transaction,on_delete = models.CASCADE)
    product_name = models.CharField(max_length = 200)
    product_price = models.DecimalField(decimal_places = 2,max_digits = 1000,default = '0.00')
    product_quantity = models.PositiveIntegerField(default = 1)
    total = models.DecimalField(decimal_places = 2,max_digits = 1000,default = '0.00')

    def __str__(self):
        return f"{self.transaction.company.companydetails.name} transaction {self.transaction.id} item"


class Staff(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,default = None,null=True)
    company = models.ForeignKey(CompanyDetails,on_delete=models.CASCADE)

