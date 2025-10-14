from .models import Cart
def cart_item_count(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user, status='in_cart')
        item_count = sum(item.quantity for item in cart_items)
    else:
        item_count = 0
    return {'cart_item_count': item_count}
