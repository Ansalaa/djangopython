from django.shortcuts import render,redirect
from shop.models import Category,Product
from django.contrib.auth.models import User
def categories(request):
    c=Category.objects.all()
    context={'cat':c}
    return render(request,'categories.html',context)

def products(request,i):
    c=Category.objects.get(id=i)
    p=Product.objects.filter(category=c)
    context={'cat':c,'pro':p}
    return render(request,'products.html',context)

def productdetail(request,i):
    p=Product.objects.get(id=i)
    context={'pro':p}
    return render(request,'details.html',context)

def register(request):
    if (request.method == 'POST'):
        u = request.POST['u']
        p = request.POST['p']
        cp= request.POST['cp']
        e = request.POST['e']
        f = request.POST['f']
        l = request.POST['l']
        if (p == cp):
            u = User.objects.create_user(username=u, password=p, email=e, first_name=f, last_name=l)
            u.save()
        else:
            return HttpResponse("Password should be same")

        return redirect('shop:categories')

    return render(request, 'register.html')


from django.contrib.auth import login,authenticate,logout
from django.http import HttpResponse

def user_login(request):
    if(request.method=="POST"):
        u=request.POST['u']
        p=request.POST['p']

        user=authenticate(username=u,password=p)  #check wether the details entered by the user is correct or not

        if user:
            login(request,user)
            return redirect('shop:categories')

        else:   #if user doesnot exist
            return HttpResponse("Invalid credentials")

    return render(request,'login.html')

def user_logout(request):
    logout(request)
    return redirect('shop:login')

def addcategories(request):
    if(request.method=="POST"):
        t=request.POST['t']
        d=request.POST['d']
        c=request.FILES['c']
        b=Category.objects.create(name=t,desc=d,image=c)
        b.save()
        return redirect('shop:categories')

    return render(request, 'addcategories.html')

def addproducts(request):
    if(request.method=="POST"):
        v=request.POST['v']
        w=request.POST['w']
        x=request.POST['x']
        y=request.POST['y']
        z=request.FILES['z']
        c=request.POST['c']
        cat=Category.objects.get(name=c)
        p=Product.objects.create(name=v,desc=w,image=z,price=x,stock=y,category=cat)
        p.save()

        return redirect('shop:categories')

    return render(request, 'addproducts.html')

def addstock(request,i):
    p=Product.objects.get(id=i)
    if(request.method=="POST"):
        p.stock=request.POST['s']
        p.save()
        return redirect('shop:details',i)

    context={'pro':p}
    return render(request,'addstock.html',context)

