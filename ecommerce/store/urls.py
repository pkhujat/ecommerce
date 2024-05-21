from django.urls import path
from . import views

urlpatterns = [
    path('',views.store,name='store'),
    path('cart/', views.cart ,name="cart"),
    path('checkout/',views.checkout , name="checkout"),
    path('update_item/',views.updateItem , name="update_item"),
    path('process_order/',views.processOrder,name="process_order"),
    path('viewproduct/<id>/',views.viewproduct,name="viewproduct"),
    path('login/',views.userlogin,name="login"),
    path('login_process/',views.login_process,name="login_process"),
    path('logout_user/',views.logout_user,name="logout_user"),
    path('signup/',views.signup_form,name="signup"),
    path('signup_process/',views.signup_process,name="signup_process"),
    path('filter_store/',views.filter_store,name="filter_store")
]