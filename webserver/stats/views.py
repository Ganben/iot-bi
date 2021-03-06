# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic import (
    DetailView,
    View,
)
import uuid
import pickle
import redis
import pygtrie
import json
import datetime

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
        qshop = models.Shop.objects.filter(pk=shopid)[0]
        # query (inverse) related device
        # qd = models.DeviceDataLive.objects.filter(shop__id=qs.id)
        qd = models.Device.objects.filter(shop__id=shopid)[0:20]
        # qdevs = 
        ctx = context_gen(request)
        ctx['shopmq'] = 'shop%s' % shopid
        if request.session.get('ssid', False):
            ssid = request.session.get('ssid')
        else:
            ssid = uuid.uuid4()
            request.session['ssid'] = str(ssid)
        ctx['shopid'] = shopid
        ctx['sessionid'] = str(ssid)
        ctx['shopname'] = qshop.name
        ctx['date'] = datetime.date.today()
        # following data is from redis live
        ro = pickle.loads(rd.get('liveshopchart'))
        sh = ro[str(shopid)]
        ctx['chartdata'] = {
            'labels': ["%s" % i for i in sh['labels']],
            'data':sh['data'],
            'sum': sh['sum']
        }
        
        # following data is from mysql history
        ctx['charttable'] = list(qd)
        # {
        #     'labels': ["%s" % d.device.id for d in list(qd)],
        #     # 'datasets': [{
        #     #     'label': "visits",
        #         'data': [d.visited for d in list(qd)]
        #         # 'borderWidth': 1
        #     # }]
        # }

        return render(request, self.template_name, context=ctx)

class DeviceView(View):
    # the device which have 4 pins, live status, load/empty/Null
    # and history line figure will query daily data
    template_name = 'device.html'

    def get(self, request, device = 1):
        # get redis
        # rkey = 'dev=%s' % device
        rkey = 'livedevicechart'

        if rd.exists(rkey):
            # d = rd.get(rkey)
            # load some from binary
            d = pickle.loads(rd.get(rkey))

        else:
            return 'rd not found'
            # generate some         

            # generate new
            # save to rd
        qdd = models.DeviceDaily.objects.filter(device__id=device).order_by('date')[0:14]
        # session
        if request.session.get('ssid', False):
            ssid = request.session.get('ssid')
        else:
            ssid = uuid.uuid4()
            request.session['ssid'] = str(ssid)
        ctx = {}
        ctx['sessionid'] = str(ssid)
        ctx['devmq'] = 'dev%s' % device
        ctx['pinlist'] = gen_dev_pin(d.get(str(device)))
        ctx['label'] = d.get(str(device))['label']
        ctx['sum'] = d.get(str(device))['sum']
        #ctx['history'] = list(qdd)
        ctx['chartdata'] = gen_devchartdata(list(qdd))
        return render(request, self.template_name, context=ctx)

def gen_devchartdata(ld):
    chartdata = {}
    chartdata['color'] = "red"
    colors = []
    labels = []
    data = []
    colorarr = ["cyan","blue","yellow","orange","purple"]
    i = 0
    for e in ld:
        labels.append(str(e.date))
        data.append(e.sums)
    chartdata['data'] = data
    chartdata['labels'] = labels
    return chartdata



def gen_dev_pin(devlive):
    #gen live dev data
    r = []
    print('%s' % devlive['stats'])
    for i in range(4):
        r.append({
            'id': i+1,
            'status': devlive['status'][i],
            'stats': devlive['stats'][i],
            'name': devlive['names'][i]
        })
        
    return r