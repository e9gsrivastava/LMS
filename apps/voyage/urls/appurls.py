from django.urls import path


urlpatterns = [
    path("", ApplicationDefaultView.as_view(), name="home"),
]

