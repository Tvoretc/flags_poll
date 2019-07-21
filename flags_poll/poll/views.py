from django.shortcuts import render, redirect
from poll.models import Country
import random


# Create your views here.

def indexView(request):
    return render(request, 'poll/index.html')

def pollView(request):
    if request.method == 'POST':
        answer_id = request.session['answer_id']
        answer = Country.objects.get(id = answer_id)
        if answer.name == request.POST['answer']:
            request.session['score'] += 1
        else:
            return redirect('/poll/result/')
    else:
        request.session['score'] = 0

    items = get_four_random_countries()
    choice = random.randrange(4)
    request.session['answer_id'] = items[choice].id
    return render(
        request,
        'poll/poll.html',
        context = {
            'items' : items,
            # 'chosen' : random.randrange(4),
            'img' : 'poll/flags/'+items[choice].flag_128,
        }
    )

def pollResultView(request):
    score = request.session.get('score', 0)
    request.session.clear()
    return render(request, 'poll/result.html', {'score' : score})

def get_four_random_countries():
    '''returns list[4] of unique random poll.models.Country objects'''
    count = Country.objects.count()
    ids = list(range(1, count))  # id start with 1
    random.shuffle(ids)
    return list(Country.objects.filter(id__in = ids[:4]))
