from django.shortcuts import render

# Create your views here.


def about_us(request):
    return render(request, 'website/about_us.html')


def privacy_policy(request):
    return render(request, 'website/privay_policy.html')