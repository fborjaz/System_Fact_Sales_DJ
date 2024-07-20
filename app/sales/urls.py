from django.urls import path
from app.sales.views import sale
 
app_name='sales' # define un espacio de nombre para la aplicación
urlpatterns = [    
    # URLs de proveedores
    path('sales_list/', sale.SaleListView.as_view() ,name='sales_list'),
    path('sales_create/', sale.SaleCreateView.as_view(),name='sales_create'),
    path('sales_update/<int:pk>/', sale.SaleUpdateView.as_view(),name='sales_update'),
    # path('supplier_delete/<int:pk>/', supplier.SupplierDeleteView.as_view(),name='supplier_delete'),
 ]