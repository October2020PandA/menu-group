from django.shortcuts import render, redirect, HttpResponse

# Create your views here.
def index(request):
    return render(request, 'order.html')

def checkout(request):
    return render(request, 'checkout.html')

def logout(request):
    request.session.flush()
    return redirect('/')