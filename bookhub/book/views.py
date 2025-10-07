from django.shortcuts import render, redirect
from django.views import View
from .models import *
from django.db.models import *
from django.db.models.functions import *
from book.forms import *
from django.db import transaction

class IndexView(View):
    def get(self, request):
        return render(request, "index.html")

class CartView(View):

    def get(self, request, user):
        cart = Cart.objects.get(id=user)
        cart_details = CartDetail.objects.filter(cart=cart)

        context = {
            "cart": cart,
            "cart_details": cart_details,
        }
        return render(request, "cart.html", context)

class PaymentView(View):
    def get(self, request, user):
        order = Order.objects.get(id=user)
        context = {
            "order": order,
        }
        return render(request, "payment.html", context)

class OrderHistoryView(View):
    def get(self, request, user):
        orders = Order.objects.filter(user=user).order_by("-order_date")
        context = {
            "orders": orders,
        }
        return render(request, "orderhistory.html", context)

class OrderHistoryDetailView(View):
    def get(self, request, user, order):
        order = Order.objects.get(id=order, user=user)
        order_details = OrderDetail.objects.filter(order=order)

        context = {
            "order": order,
            "order_details": order_details,
        }
        return render(request, "orderhistorydetail.html", context)