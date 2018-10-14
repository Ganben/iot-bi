# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic import (
    DetailView,
    View,
)
import uuid
import pickle
import redis


from stats import models

# retrieve pickled data from redis
rpool = redis.ConnectionPool(host='localhost', port=6379, db=0)
rd = redis.Redis(connection_pool=rpool)

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
    # this model's live data will be stored in redis
    # TODO: new dict-like data fit new front
    # template name
    template_name = 'shop.html'
    def get(self, request, shopid =1):
        # retrieve model
        qs = self.model.objects.filter(shop__id=shopid)[0]
        # query (inverse) related device
        qd = models.DeviceDataLive.objects.filter(shop__id=qs.id)
        ctx = context_gen(request)
        ctx['shopmq'] = 'shop%s' % shopid
        if request.session.get('ssid', False):
            ssid = request.session.get('ssid')
        else:
            ssid = uuid.uuid4()
            request.session['ssid'] = str(ssid)
        ctx['shopid'] = shopid
        ctx['sessionid'] = str(ssid)
        ctx['chartdata'] = {
            'labels': ["%s" % d.device.id for d in list(qd)],
            # 'datasets': [{
            #     'label': "visits",
                'data': [d.visited for d in list(qd)]
                # 'borderWidth': 1
            # }]
        }

        return render(request, self.template_name, context=ctx)

class DeviceView(View):
    # the device which have 4 pins, live status, load/empty/Null
    # and history line figure will query daily data
    template_name = 'device.html'

    def get(self, request, device = 1):
        # get redis
        rkey = 'dev=%s' % device
        if rd.exists(rkey):
            d = rd.get(rkey)
            # load some from binary
        else:
            pass
            # generate some         

            # generate new
            # save to rd

        # session
        if request.session.get('ssid', False):
            ssid = request.session.get('ssid')
        else:
            ssid = uuid.uuid4()
            request.session['ssid'] = str(ssid)
        ctx = {}
        