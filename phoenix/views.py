from django.shortcuts import render

def homepage(request):
    context = {}
    return render(request, 'homepage.html', context)

def section(request):
    context = {}
    return render(request, 'section.html', context)

def article(request):
    context = {}
    return render(request, 'article.html', context)

def page(request):
    context = {}
    return render(request, 'page.html', context)
