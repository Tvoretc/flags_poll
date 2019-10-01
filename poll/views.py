from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.core.mail import send_mail
from django.contrib import messages
import random

from poll.models import Country, Region
from poll.forms import ScoreRecordForm
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
    # print('\n\npoll')
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
    if request.method == 'POST':
        form = ScoreRecordForm(data = {'email':request.POST['email']})
        if form.is_valid():
            email = form.cleaned_data['email']
            score = request.session.get('score', None)
        if score == None:
            messages.warning(request, 'Sorry, but we cant find your score. Did you actually had poll?')
        else:
            request.session.clear()
            form.save(score)
            send_mail('Your score in Country poll', f'Your score was {score}. Get even better next time!', 'noreply@countrysite', [email])
            messages.success(request, 'We got you an email with your score. Keep up!')
        return redirect('/poll/')
    score = request.session.get('score', 0)
    return render(request, 'poll/result.html', {'score' : score, 'form' : ScoreRecordForm()})

def get_four_random_countries():
    '''returns list[4] of unique random poll.models.Country objects'''
    count = Country.objects.count()
    ids = list(range(1, count))  # id start with 1
    random.shuffle(ids)
    return list(Country.objects.filter(id__in = ids[:4]))

def countriesByRegionsView(request):
    regions = list(Region.objects.all())
    country_list = {region : list(region.country for region in region.countryregion_set.all()) for region in regions}
    # print(country_list)
    return render(request, 'poll/country_by_region.html', context = {
        'country_list' : country_list,
    })

class CountryListView(ListView):
    model = Country
    paginate = 20
