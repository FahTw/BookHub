from django.urls import path

from book.views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),  # Home page
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('home/', HomeView.as_view(), name='home'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('book/', BookListView.as_view(), name='book'),
    path('book/<int:book_id>/', BookDetailView.as_view(), name='book_detail'),
    path('category/<int:category_id>/', CategoryView.as_view(), name='category'),
    path("cart/<int:user>/", CartView.as_view(), name="cart"),
    path("payment/<int:user>/", PaymentView.as_view(), name="payment"),
    path("orderhistory/<int:user>/", OrderHistoryView.as_view(), name="order_history_user"),
    path("orderhistory/<int:user>/<int:order>/", OrderHistoryDetailView.as_view(), name="order_history_detail"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("orderhistoryowner/", OrderHistoryOwnerView.as_view(), name="order_history_owner"),
    path("orderhistoryowner/<int:order>/", OrderHistoryOwnerDetailView.as_view(), name="order_history_owner_detail"),
    path('managebooks/', ManageBookView.as_view(), name='manage_book'),
    path('stat/', StatView.as_view(), name='stat'),
]
