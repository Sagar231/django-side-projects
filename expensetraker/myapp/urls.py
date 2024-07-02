
from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.user_login,name="login"),
    path('logout/',views.user_logout,name="logout"),
    path('register/',views.register,name="register"),
    path('',views.index,name="index"),
    path('edit/<int:id>/',views.edit,name="edit"),
    path('delete/<int:id>/',views.delete,name="delete")
]
