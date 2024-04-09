from django.shortcuts import render, get_object_or_404, redirect

def about(request):
    return render(request, 'app/about.html')

def contact_us(request):
    return render(request, 'app/contact.html')
