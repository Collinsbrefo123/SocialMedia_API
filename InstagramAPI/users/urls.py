from django.urls import path
from users import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('register/',  views.RegisterView.as_view(), name="register"),
    path('login/',  views.LoginView.as_view(), name="login"),
    path('logout/',  views.LogoutAPIView.as_view(), name="login"),
    path('user/',  views.UserAPIView.as_view(), name="user"),
    path('create/',  views.CreateFeedAPIView.as_view(), name="createfeed"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
