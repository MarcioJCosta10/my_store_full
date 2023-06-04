
from django.forms import SlugField
from django.shortcuts import render, get_object_or_404
from .models import Product
from category.models import Category
from carts.models import CartItem
from carts.views import _cart_id

# Create your views here.
def store(request, category_slug=None):
      categories = None
      products = None
      
      if category_slug != None:
            categories = get_object_or_404(Category, slug=category_slug)
            products = Product.objects.filter(category=categories, is_available=True)
            product_count = products.count()
      else:
            products = Product.objects.filter(is_available=True)
            product_count = products.count()            

      context = {
                'products': products,
                'product_count':product_count
         }
  
      return render(request, 'store/store.html', context)

def product_detail(request, category_slug, product_slug):
      try:                                     #sintaxe to access slug category
            single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
            #cart__cart_id: using double underscore because cart is foreignKey to cart_id in Cart and returns if exists this brings true or false
            in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product= single_product).exists()

      except Exception as e:
            raise e
      context = {
            'single_product': single_product,
            'in_cart'       : in_cart
      }
      return render(request, 'store/product_detail.html' , context)