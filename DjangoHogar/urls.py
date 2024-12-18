"""
URL configuration for DjangoHogar project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.conf.urls.static import static
from django.conf import settings


from django.contrib import admin
from django.urls import path, include
from tasks import views




urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('singup/', views.singup, name='singup'),
    path('task/', views.task, name='task'),
    path('task_completed/', views.task_completed, name='task_completed'),
    path('task/create', views.create_task, name='create_task'),
    path('task/<int:task_id>', views.task_detail, name='task_detail'),
    path('task/<int:task_id>/delete',
         views.delete_task, name='delete_task'),
    path('task/<int:task_id>/complete',
         views.complete_task, name='complete_task'),
    path('logout/', views.singout, name='logout'),
    path('singin/', views.singin, name='singin'),
    path('', include('tasks.urls')),
  
   
] + static(settings.MEDIA_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
