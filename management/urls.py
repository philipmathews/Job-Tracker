from django.urls import path,re_path

from django.contrib.auth import views as auth_views

from . import views

app_name = 'management'

urlpatterns = [
    path('',views.home, name='home'),
    path('login/',views.log_in, name='login'),
    path('logout/',views.log_out, name='logout'),
    path('register/',views.register, name='register'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.activate, name='activate'),
    path('accounts/password_reset/',auth_views.password_reset,name='password_reset'),
    path('accounts/password_reset/done/',auth_views.password_reset_done,name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/',auth_views.password_reset_confirm,name='password_reset_confirm'),
    path('accounts/reset/done/',auth_views.password_reset_complete,name='password_reset_complete'),
    path('password/',views.change_password, name='change_password'),
    path('dashboard/',views.dashboard, name='dashboard'),
    path('dashboard/createwishlist',views.createwishlist,name='createwishlist'),
    path('dashboard/deletewishlist/<int:wishlist_id>',views.deletewishlist,name='deletewishlist'),
    path('dashboard/createapplied',views.createapplied,name='createapplied'),
    path('dashboard/deleteapplied/<int:applied_id>',views.deleteapplied,name='deleteapplied'),
    path('dashboard/wishlistinfo/<int:wishlist_id>',views.wishlistinfo,name='wishlistinfo'),
    path('dashboard/appliedinfo/<int:applied_id>',views.appliedinfo,name='appliedinfo'),
    path('dashboard/tasks',views.tasks,name='tasks'),
    path('dashboard/createtask',views.createtask,name='createtask'),
    path('dashboard/completetask/<int:task_id>',views.completetask,name='completetask'),
    path('dashboard/deletecompleted',views.deletecompleted,name='deletecompleted'),
    path('dashboard/deletetask/<int:task_id>',views.deletetask,name='deletetask'),
    path('dashboard/jobactivity',views.jobactivity,name='jobactivity'),
    path('dashboard/chartdata',views.chartdata,name='chartdata'),
]