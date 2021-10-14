from django.contrib import admin
from .models import Product,CompanyDetails,StockOverview,ProductData,Transaction,TransactionItem,RevenueAnalysis,Staff

# Register your models here.
admin.site.register(Product)
admin.site.register(CompanyDetails)
admin.site.register(StockOverview)
admin.site.register(ProductData)
admin.site.register(Transaction)
admin.site.register(Staff)
admin.site.register(TransactionItem)
admin.site.register(RevenueAnalysis)
