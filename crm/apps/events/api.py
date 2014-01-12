import json
import datetime as dt

from django import http
from django.core.urlresolvers import reverse
from django.db.models import Q
from lib.date import parsedate, LONG_MONTH_NAMES
from apps.events.models import FollowUp, Meeting


def details(request):
    if request.method == 'GET':
        s = request.GET['s']
        try:
            datedict = parsedate(s, month_as_str=True)
        except ValueError:
            res = dict()
        else:
            res = dict(status='success', data=datedict)
        return http.HttpResponse(
            json.dumps(res), content_type='application/json')
    return http.HttpResponseNotAllowed(['POST'])


def filter_by_date(request):
    if request.method == 'GET':
        datestr = request.GET['date']
        date = dt.datetime.strptime(datestr, '%d-%m-%Y').date()

        range_ = (dt.datetime.combine(date, dt.time.min),
                  dt.datetime.combine(date, dt.time.max))
        meeting_qs = Meeting.objects.filter(Q(date_started__range=range_) |
                                            Q(date_ended__range=range_))
        followup_qs = FollowUp.objects.filter(date=date)
        data = list()
        list_ = list(meeting_qs) + list(followup_qs)

        for ob in list_:
            d = dict(type=ob._meta.model.__name__, subject=ob.subject,
                     url=ob.get_absolute_url())
            if isinstance(ob, Meeting):
                d['delete_url'] = reverse('events:delete-meeting',
                                          args=[ob.pk])
                hr = str(ob.date_started.hour)
                if len(hr) == 1:
                    hr = '0' + hr
                min_ = str(ob.date_started.minute)
                if len(min_) == 1:
                    min_ = '0' + min_
                d['time'] = '{hr}:{min}'.format(hr=hr, min=min_)
            else:
                d['delete_url'] = reverse('events:delete-followup',
                                          args=[ob.pk])
            data.append(d)

        res = dict(status='success', data=data)

        daterepr = ''
        if dt.date.today() == date:
            daterepr = 'Today&nbsp; – &nbsp;'
        daterepr += '{month} {day}'.format(month=LONG_MONTH_NAMES[date.month],
                                           day=date.day)
        res['date'] = daterepr

        return http.HttpResponse(
            json.dumps(res), content_type='application/json')
    return http.HttpResponseNotAllowed(['POST'])
