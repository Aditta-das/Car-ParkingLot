from django.urls import path
from dashboard import views

urlpatterns = [
    # path('', views.IndexView.as_view(), name='index'),
    path('', views.api_root),
    path('cars/', views.CarparkList.as_view(), name='cars'),
    # path('delete/<int:slot_no>', views.UnparkList.as_view()),
    path('unpark/<int:slot_no>', views.UnparkList.as_view(), name='unpark'),
    path('info/', views.InfoCar.as_view(), name='info'),
]