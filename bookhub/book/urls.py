from django.urls import path
from django.contrib.auth.decorators import login_required

from book.views import *

urlpatterns = [
    # path ที่ไม่ต้องการ login ก่อน
    path('', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),

    # path ที่ต้องการ login ก่อน
    path('home/', login_required(HomeView.as_view()), name='home'),
    path('profile/', login_required(ProfileView.as_view()), name='profile'),
    path('book/', login_required(BookListView.as_view()), name='book'),
    path('book/<int:book_id>/', login_required(BookDetailView.as_view()), name='book_detail'),
    path('category/<int:category_id>/', login_required(CategoryView.as_view()), name='category'),
    path("cart/<int:user>/", login_required(CartView.as_view()), name="cart"),
    path('add_to_cart/<int:book_id>/', login_required(AddToCartView.as_view()), name='add_to_cart'),
    path("payment/<int:user>/", login_required(PaymentView.as_view()), name='payment'),
    path("orderhistory/<int:user>/", login_required(OrderHistoryView.as_view()), name="order_history_user"),
    path("orderhistory/<int:user>/<int:order>/", login_required(OrderHistoryDetailView.as_view()), name="order_history_detail"),
    path("dashboard/", login_required(DashboardView.as_view()), name="dashboard"),
    path('managebooks/', login_required(ManageBookListView.as_view()), name='managelist_book'),
    path('managebooks/<int:book_id>/', login_required(ManageBookView.as_view()), name='manage_book'),
    path('managebooks/delete/<int:book_id>/', login_required(ManageBookDeleteView.as_view()), name='manage_book_delete'),
    path("orderhistoryowner/", login_required(OrderHistoryOwnerView.as_view()), name="order_history_owner"),
    path("orderhistoryowner/<int:order>/", login_required(OrderHistoryOwnerDetailView.as_view()), name="order_history_owner_detail"),
    path('users/', login_required(UserListView.as_view()), name='user_list'),
    path('users/<int:user_id>/', login_required(UserDetailView.as_view()), name='user_detail'),
    path('users/delete/<int:user_id>/', login_required(UserView.as_view()), name='user_delete'),
    path('stat/', login_required(StatView.as_view()), name='stat'),
]
