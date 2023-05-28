from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
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
    return redirect('cart')

def remove_cart(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
                                #model Product 
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)  
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()        
    return redirect('cart')

def remove_cart_item(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
                                #model Product 
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)  
    cart_item.delete()      
    return redirect('cart')  
    
    
      

# Create your views here.art
def cart(request, total=0, quantity=0, cart_items=None):
    try:
        #get cart object by cart_id from request
        cart = Cart.objects.get(cart_id=_cart_id(request))
        # filter cart items
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        #calculate total quantity and total items in cart
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity        
        tax = (2*total)/100
        grand_total = total + tax
            
    except ObjectDoesNotExist:
        pass # just ignore
    
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'taxa':              tax,
        'grand_total': grand_total,       
    }
                
    return render(request, 'store/cart.html', context)
    
