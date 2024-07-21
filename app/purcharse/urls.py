from django.urls import path
from app.purcharse.views import purchase

app_name = 'purcharse'  # define un espacio de nombre para la aplicación
urlpatterns = [
    # URLs de proveedores
    path('purchase_list/', purchase.PurchaseListView.as_view(), name='purchase_list'),
    path('purchase_create/', purchase.PurchaseCreateView.as_view(), name='purchase_create'),
    path("purchase/update/<int:pk>/", purchase.PurchaseUpdateView.as_view(), name="purchase_update"),
    path('purchase/<int:pk>/cancel/', purchase.PurchaseCancelView.as_view(), name='purchase_cancel'),
    path("purchase/delete/<int:pk>/", purchase.PurchaseDeleteView.as_view(), name="purchase_delete"),
    path("purchase/consult/<int:pk>/", purchase.PurchaseConsultView.as_view(), name="purchase_consult"),
    path('generate_pdf/<int:purchase_id>/', purchase.generate_purchase_pdf, name='generate_purchase_pdf'),
    # path('supplier_update/<int:pk>/', supplier.SupplierUpdateView.as_view(),name='supplier_update'),
    # path('supplier_delete/<int:pk>/', supplier.SupplierDeleteView.as_view(),name='supplier_delete'),
]