# your_app/urls.py
from django.urls import path
from sampleeapp import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm
from .views import ProductView, ProductDetailView
# urls.py

from django.urls import path
from .views import ProductDetailView
from .views import add_to_cart
urlpatterns = [
    # path('', views.home),
   
    path('products/', ProductView.as_view(), name='product_list'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail_view'),
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('mens/', views.mens, name='mens'),
    path('womens/', views.womens, name='womens'),
    path('contact/', views.contact, name='contact'),
    path('shop/', views.shop, name='shop'),
    path('cart/', views.cart, name='cart'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),


    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('add-to-cart/', add_to_cart, name='add_to_cart'),
    path('show_cart/', views.show_cart, name='show_cart'),
    path('plus_cart/', views.plus_cart, name='plus_cart'),
    path('minus_cart/', views.minus_cart, name='minus_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('payment_done/', views.payment_done, name='payment_done'),
    path('remove_cart/', views.remove_cart, name='remove_cart'),

    path('mobile/', views.category, name='mobile'),
    path('mobile/<slug:data>', views.category, name='mobiledata'),

    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html', authentication_form=LoginForm), name='login'),
    # path('profile/', views.profile, name='profile'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name='passwordchange.html', success_url='/passwordchangedone/'), name='passwordchange'),
    path('passwordchangedone/', auth_views.PasswordChangeDoneView.as_view(template_name='passwordchangedone.html'), name='passwordchangedone'),
    
    path("password-reset/", auth_views.PasswordResetView.as_view(template_name='password_reset.html'),name="password_reset"),
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name="password_reset_done"),
    path("password-reset-confirm/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name="password_reset_confirm"),
    path("password-reset-complete/", auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name="password_reset_complete"),

    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
