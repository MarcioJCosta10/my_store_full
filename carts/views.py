from django.http import HttpResponse
from django.shortcuts import render, redirect
from store.models import Product
from .models import Cart, CartItem

#_ underscore before name functions is to private function

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart
        

def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request)) # get the cart_id using cart_id present in the session 
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
    cart.save() 
    
    #combine product and cart to we get the item from cart
    try:        
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1 #cart_item.quantity =  cart_item.quantity + 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product = product, 
            quantity = 1,
            cart=cart
            )
        cart_item.save()
    return HttpResponse(cart_item.product)
    #return redirect('cart')       

# Create your views here.art
def cart(request, total=0, quantity=0, cart_items=None):
    try:
        #get cart object by cart_id from request
        cart = Cart.objects.get(cart_id=_cart_id(request))
        # filter cart items
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        #calculate total quantity and total items in cart
        for cart_item in cart_items:
            total += (cart_item.price * cart_item.quantity)
            quantity += cart_item.quantity
    except cart.ObjectNotExists:
        pass # just ignore
    
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,        
    }
        
    return render(request, 'store/cart.html', context)
    
