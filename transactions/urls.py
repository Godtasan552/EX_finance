from django.urls import path
from . import views

urlpatterns = [
    path('', views.indexPage, name='index'),
    # เพิ่มเส้นทางอื่นๆที่คุณต้องการ
]
