"""
URL configuration for djangocrud project.

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
from django.contrib import admin
from django.urls import include, path
from tasks import views 


urlpatterns = [
    path('admin/', admin.site.urls),
    # path(include('tasks.urls')),
    path('tasks/', include('tasks.urls')),
    path('',views.home, name="home"),
    path('signup/', views.signup, name="signup"),
    path('tasks/', views.tasks, name="tasks"),
    path('tasks_completed/', views.list_tasks_completed, name="tasks_completed"),
    path('tasks/<int:id>/',views.task_detail, name="task_detail"),
    path('tasks/delete/<int:id>',views.task_delete, name="task_delete"),
    path('tasks/complete/<int:id>',views.task_complete, name="task_complete"),
    path('logout/',views.user_logout, name="logout"),
    path('login/',views.user_login, name="login"), # "signin"  
    path('tasks/create/',views.create_task, name="create_task")
]
