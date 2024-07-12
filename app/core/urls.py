from django.urls import path
from app.core.views import supplier, product, brand, line, category, iva, price, customer, paymentmethod, company, modulos, menus, groupModulePermissions, user
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
 
app_name = 'core' # define un espacio de nombre para la aplicación
urlpatterns = [
    #-- URLS DE MANTENIMIENTO --#    
    #-- URLs de proveedores--#
    path('supplier_list/', supplier.SupplierListView.as_view(),name='supplier_list'),
    path('supplier_create/', supplier.SupplierCreateView.as_view(),name='supplier_create'),
    path('supplier_update/<int:pk>/', supplier.SupplierUpdateView.as_view(),name="supplier_update"),
    path('supplier_delete/<int:pk>/', supplier.SupplierDeleteView.as_view(),name="supplier_delete"),
    #-- URLS DE PRODUCTOS--#
    path('product_list/', product.ProductListView.as_view(),name='product_list'),
    path('product_create/', product.ProductCreateView.as_view(),name='product_create'),
    path('product_update/<int:pk>/', product.ProductUpdateView.as_view(),name="product_update"),
    path('product_delete/<int:pk>/', product.ProductDeleteView.as_view(),name="product_delete"),
    #-- URLS DE MARCAS--#
    path("brand_list/", brand.BrandListView.as_view(), name="brand_list"),
    path("brand_create/", brand.BrandCreateView.as_view(), name="brand_create"),
    path('brand_update/<int:pk>/', brand.BrandUpdateView.as_view(),name="brand_update"),
    path('brand_delete/<int:pk>/', brand.BrandDeleteView.as_view(),name="brand_delete"),
    #-- URLS DE LINEAS creado--#
    path("line_list/", line.LineListView.as_view(), name="line_list"),
    path("line_create/", line.LineCreateView.as_view(), name="line_create"),
    path('line_update/<int:pk>/', line.LineUpdateView.as_view(),name="line_update"),
    path('line_delete/<int:pk>/', line.LineDeleteView.as_view(),name="line_delete"),
    #-- URLS DE CATEGORIAS--#
    path("category_list/", category.CategoryListView.as_view(), name="category_list"),
    path("category_create/", category.CategoryCreateView.as_view(), name="category_create"),
    path('category_update/<int:pk>/', category.CategoryUpdateView.as_view(),name="category_update"),
    path('category_delete/<int:pk>/', category.CategoryDeleteView.as_view(),name="category_delete"),
    #-- URLS DE IVA creado--#
    path("iva_list/", iva.IvaListView.as_view(), name="iva_list"),
    path("iva_create/", iva.IvaCreateView.as_view(), name="iva_create"),
    path("iva_update/<int:pk>/", iva.IvaUpdateView.as_view(), name="iva_update"),
    path("iva_delete/<int:pk>/", iva.IvaDeleteView.as_view(), name="iva_delete"),
    #-- URLS DE PRECIOS--#
    path("price_list/", price.ProductPriceListView.as_view(), name="price_list"),
    path("price_create/", price.ProductPriceCreateView.as_view(), name="price_create"),
    path("price_update/<int:pk>/", price.ProductPriceUpdateView.as_view(), name="price_update"),
    path("price_delete/<int:pk>/", price.ProductPriceDeleteView.as_view(), name="price_delete"),
    #-- URLS DE CLIENTES--#
    path("customer_list/", customer.CustomerListView.as_view(), name="customer_list"),
    path("customer_create/", customer.CustomerCreateView.as_view(), name="customer_create"),
    path("customer_update/<int:pk>/", customer.CustomerUpdateView.as_view(), name="customer_update"),
    path("customer_delete/<int:pk>/", customer.CustomerDeleteView.as_view(), name="customer_delete"),
    #-- URLS DE METODOS DE PAGO--#
    path("paymentmethod_list/", paymentmethod.PaymentMethodListView.as_view(), name="paymentmethod_list"),
    path("paymentmethod_create/", paymentmethod.PaymentMethodCreateView.as_view(), name="paymentmethod_create"),
    path("paymentmethod_update/<int:pk>/", paymentmethod.PaymentMethodUpdateView.as_view(), name="paymentmethod_update"),
    path("paymentmethod_delete/<int:pk>/", paymentmethod.PaymentMethodDeleteView.as_view(), name="paymentmethod_delete"),
    #-- URLS DE EMPRESA--#
    path("company_list/", company.CompanyListView.as_view(), name="company_list"),
    path("company_create/", company.CompanyCreateView.as_view(), name="company_create"),
    path("company_update/<int:pk>/", company.CompanyUpdateView.as_view(), name="company_update"),
    path("company_delete/<int:pk>/", company.CompanyDeleteView.as_view(), name="company_delete"),

    #-- URLS DE SEGURIDAD --#

    #--URLS DE MODULOS--#

    path('modules_list/', modulos.ModulesListView.as_view(), name='modules_list'),
    path('modules_create/', modulos.ModuleCreateView.as_view(), name='modules_create'),
    path('modules_update/<int:pk>/', modulos.ModuleUpdateView.as_view(), name='modules_update'),
    path('modules_delete/<int:pk>/', modulos.ModuleDeleteView.as_view(), name='modules_delete'),

    #--URLS DE MENUS--#
    path('menus_list/', menus.MenuListView.as_view(), name='menus_list'),
    path('menus_create/', menus.MenuCreateView.as_view(), name='menus_create'),
    path('menus_update/<int:pk>/', menus.MenuUpdateView.as_view(), name='menus_update'),
    path('menus_delete/<int:pk>/', menus.MenuDeleteView.as_view(), name='menus_delete'),
    
    #URLS DE GRUPO DE MODULOS DE PERMISOS
    path('group_module_permission_list/', groupModulePermissions.GroupModulePermissionListView.as_view(), name='group_module_permission_list'),
    path('group_module_permission_add/', groupModulePermissions.GroupModulePermissionCreateView.as_view(), name='group_module_permission_add'),
    path('group_module_permission_update/<int:pk>/', groupModulePermissions.GroupModulePermissionUpdateView.as_view(), name='group_module_permission_update'),
    path('group_module_permission_delete/<int:pk>/', groupModulePermissions.GroupModulePermissionDeleteView.as_view(), name='group_module_permission_delete'),

    #URLS DE USUARIOS Y GRUPOS
    path('users_list/', user.UsersListView.as_view(), name='users_list'),
    path('users_groups/<int:user_id>/', user.UserGroupView.as_view(), name='user_groups'),
    path('users_delete/<int:user_id>/', user.UserDeleteView.as_view(), name='user_delete'),

 ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

 



    