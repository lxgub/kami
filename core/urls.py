from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI
from airlines.api import router as airlines_router

api = NinjaAPI(title='Kami airlines')
api.add_router('/v1/', airlines_router)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),
]