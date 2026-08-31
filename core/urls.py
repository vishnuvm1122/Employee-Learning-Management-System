from django.urls import path
from . import views

urlpatterns = [

    # 🔷 Home / News & Events
    path('', views.home_view, name='home'),

    # 🔷 Dashboard (Admin only)
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # 🔷 Posts (CRUD)
    path('post/add/', views.post_add, name='post_add'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/edit/', views.edit_post, name='edit_post'),
    path('post/<int:pk>/delete/', views.delete_post, name='delete_post'),

]


handler404 = "core.views.custom_404"
handler500 = "core.views.custom_500"
handler403 = "core.views.custom_403"
handler400 = "core.views.custom_400"