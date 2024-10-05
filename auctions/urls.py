from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static


from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.createlisting, name="create"),
    path('product_details/<int:product_details_id>/', views.product_details, name='product_details'),
    path('product/<int:product_id>/bid/', views.New_bid, name='New_bid'),
    path("product/<int:product_id>/watchlist/", views.toggle_watchlist, name="toggle_watchlist"),
    path("product/<int:product_id>/disable/", views.disable, name="disable"),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
