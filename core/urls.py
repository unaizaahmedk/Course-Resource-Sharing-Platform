from django.urls import path
from . import views 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home, name='home'),
    path('browse-courses/', views.browse_courses, name='browse_courses'),
    path('logged-browse-courses/', views.logged_browse_courses, name='logged_browse_courses'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add_resources/', views.add_resource, name='add_resources'),
    path('browse_resource/', views.browse_resource, name='browse_resource'),
    path('my_resources/', views.my_resources, name='my_resources'),
    path('borrowed_resources/', views.borrowed_resources, name='borrowed_resources'),
    path('add_feedback/<int:resource_id>/', views.add_feedback, name='add_feedback'),
    path('resource/<int:resource_id>/', views.resource_details, name='resource_details'),
    path('borrow/resource/<int:resource_id>/', views.borrow_resource, name='borrow_resource'),
    path('return_resource/<int:resource_id>/', views.return_resource, name='return_resource'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

