from django.shortcuts import render
from poll.models import Country
import random


# Create your views here.

def indexView(request):
    return render(request, 'poll/index.html')

def pollView(request):
    return render(
        request,
        'poll/poll.html',
        context = {
            'items' : get_four_random_countries(),
            'chosen' : random.randrange(4)
        }
    )

def get_four_random_countries():
    '''returns list[4] of unique random poll.models.Country objects'''
    count = Country.objects.count()
    ids = list(range(1, count))  # id start with 1
    random.shuffle(ids)
    return list(Country.objects.filter(id__in = ids[:4]))
