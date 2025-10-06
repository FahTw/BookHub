from django.urls import path

from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),  # Home page
    path("cart/<int:user>/", views.CartView.as_view(), name="cart"),
    path("order/<int:user>/", views.OrderView.as_view(), name="order"),
    path("payment/<int:user>/", views.PaymentView.as_view(), name="payment"),
    path("orderhistory/<int:user>/", views.OrderHistoryView.as_view(), name="order_history_user"),
    path("orderhistory/<int:user>/<int:order>/", views.OrderHistoryDetailView.as_view(), name="order_history_detail"),
    #path("orderhistoryowner/", views.OrderHistoryOwnerView.as_view(), name="order_history_owner"),
    #path("orderhistoryowner/<int:order>/", views.OrderHistoryOwnerDetailView.as_view(), name="order_history_owner_detail"),
]
