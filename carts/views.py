from django.shortcuts import render



# Create your views here.art
def cart(request):
    
    return render(request, 'store/cart.html')
    
