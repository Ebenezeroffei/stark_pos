from django.urls import path
from . import views as app_views

app_name = 'app'
urlpatterns = [
    path('dashboard/',app_views.IndexView.as_view(),name = 'home'),
    path('home/analysis/',app_views.IndexAnalysisView.as_view(),name = 'home_analysis'),
    path('home/analysis/general/',app_views.GeneralAnalysisView.as_view(),name = 'general_analysis'),
    path('inventory/',app_views.InventoryView.as_view(),name = 'inventory'),
    path('inventory/create/',app_views.InventoryCreateView.as_view(),name = 'inventory_create'),
    path('inventory/<int:pk>/detail/',app_views.InventoryDetailView.as_view(),name = 'inventory_detail'),
    path('inventory/<int:pk>/edit/',app_views.InventoryEditView.as_view(),name = 'inventory_edit'),
    path('inventory/search/',app_views.InventorySearchView.as_view(),name = 'inventory_search'),
    path('inventory/analysis/',app_views.InventoryAnalysisView.as_view(),name = 'inventory_analysis'),
    path('inventory/delete/',app_views.InventoryDeleteView.as_view(),name = 'inventory_delete'),
    path('transactions/',app_views.TransactionsView.as_view(),name = 'transactions'),
    path('transaction/create/',app_views.TransactionCreateView.as_view(),name = 'transaction_create'),
    path('staffs/',app_views.StaffsView.as_view(),name = 'staffs'),
    path('product/search/',app_views.SearchProductView.as_view(),name = 'search_product'),
    path('transaction/save/',app_views.SaveTransactionView.as_view(),name = 'transaction_save'),
    path('analysis/',app_views.AnalysisView.as_view(),name = 'analysis'),
    path('analysis/custom/<str:type>/',app_views.CustomAnalysisView.as_view(),name = 'custom_analysis'),
    path('analysis/generate/custom/',app_views.GenerateCustomAnalysisView.as_view(),name = 'generate_custom_analysis'),
    path('sales/reports/',app_views.SalesReportView.as_view(),name = 'sales_report'),
    path('sales/report/template/<str:duration>/',app_views.SalesReportTemplateView.as_view(),name = 'sales_report_template')
]
