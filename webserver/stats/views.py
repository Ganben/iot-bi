from django.shortcuts import render
from django.views.generic import DetailView
from stats import models

def context_gen(request):
    # generate context
    return {}

# Create your views here.
def index(request):
    # get list of shops
    q = models.Shop.objects.all() # need page and other sort
    ctx = context_gen(request)
    ctx['table'] = list(q)
    return render(request, 'index.html', context=ctx)

# def detail(request):
class ShopDetail(DetailView):
    model = models.Shop

    template_name = 'shop.html'