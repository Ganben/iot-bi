from django.shortcuts import render
from django.views.generic import (
    DetailView,
    View,
)
from stats import models

def context_gen(request):
    # generate context
    return {}

# Create your views here.
def index(request):
    # get list of shops
    q = models.Shop.objects.all() # need page and other sort
    ctx = context_gen(request)
    # print(list(q))
    ctx['table'] = list(q)
    return render(request, 'index.html', context=ctx)

# def detail(request):
class ShopDetail(View):
    # the detail shows live data
    model = models.ShopDataLive
    # template name
    template_name = 'shop.html'
    def get(self, request, shopid =1):
        # retrieve model
        qs = self.model.objects.filter(shop__id=shopid)[0]
        # query (inverse) related device
        qd = models.DeviceDataLive.objects.filter(shop__id=qs.id)
        ctx = context_gen(request)
        ctx['shopmq'] = 'shop%s' % shopid
        ctx['chartdata'] = {
            'labels': ["%s" % d.device.id for d in list(qd)],
            # 'datasets': [{
            #     'label': "visits",
                'data': [d.visited for d in list(qd)]
                # 'borderWidth': 1
            # }]
        }

        return render(request, self.template_name, context=ctx)