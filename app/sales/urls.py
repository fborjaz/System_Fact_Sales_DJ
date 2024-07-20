from django.urls import path
from app.sales.views import sale
 
app_name='sales' # define un espacio de nombre para la aplicación
urlpatterns = [    
    # URLs de proveedores
    path('sales_list/', sale.SaleListView.as_view() ,name='sales_list'),
    path('sales_create/', sale.SaleCreateView.as_view(),name='sales_create'),
    path('sales_update/<int:pk>/', sale.SaleUpdateView.as_view(),name='sales_update'),
    path('sales/cancel/<int:pk>/', sale.SaleCancelView.as_view(), name='sales_cancel'),
    path("sales/delete/<int:pk>/", sale.SaleDeleteView.as_view(), name="sales_delete"),
    path("sales/consult/<int:pk>/", sale.SalesConsultView.as_view(), name="sales_consult"),
    path('sales/<int:invoice_id>/pdf/', sale.generate_invoice_pdf, name='invoice_pdf'),
    # path('supplier_delete/<int:pk>/', supplier.SupplierDeleteView.as_view(),name='supplier_delete'),
 ]