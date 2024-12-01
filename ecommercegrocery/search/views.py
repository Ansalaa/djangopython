from django.shortcuts import render
from shop.models import Product
from django.db.models import Q
def searchproducts(request):
    p = None  # Initialized to none
    query = ""

    if (request.method == 'POST'):  # After form submission
        query = request.POST['q']
        print(query)
        if query:
            p = Product.objects.filter(Q(name__icontains=query) | Q(desc__icontains=query))  # django lookups

    context={'pro':p,'query':query}
    return render(request,'search.html',context)