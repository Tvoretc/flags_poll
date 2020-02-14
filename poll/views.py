from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.core.mail import send_mail
from django.contrib import messages

import random

from poll.models import Country, Region, ScoreRecord
from poll.forms import ScoreRecordForm

RESULT_WARNING_MESSAGE_NO_SCORE='Sorry, but we cant find your score. \
Did you actually had a poll?'
RESULT_WARNING_MESSAGE_BAD_EMAIL='Invlid email'
RESULT_SUCCESS_MESSAGE_EMAIL_SENT='We got you an email with your score. \
Keep up!'
RESULT_MESSAGE_SCORE='Your score: '


def indexView(request):
    return render(request, 'poll/index.html')


def pollView(request):
    if request.method == 'POST':
        answer_id = request.session['answer_id']
        answer = Country.objects.get(id=answer_id)

        if answer.name == request.POST['answer']:
            request.session['score'] += 1
        else:
            return redirect('poll:result')

    else:
        request.session['score'] = 0

    items = get_four_random_countries()
    choice = random.randrange(4)
    request.session['answer_id'] = items[choice].id

    return render(
        request,
        'poll/poll.html',
        context = {
            'items': items,
            'img': f'poll/flags/{items[choice].flag_128}',
        }
    )


def countryView(request, code3):
    item = Country.objects.get(code3l=code3)

    return render(
        request,
        'poll/country.html',
        context={
            'item': item,
            'img': f'poll/flags/{item.flag_128}'
        }
    )


def pollResultView(request):
    score = request.session.get('score', None)

    if score == None:
        messages.warning(request, RESULT_WARNING_MESSAGE_NO_SCORE)
    elif request.method == 'POST':
        form = ScoreRecordForm(data=request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            request.session.clear()
            ScoreRecord.objects.create(email=email, score=score)

            send_mail(
                'Your score in Country poll',
                f'Your score was {score}. Get even better next time!',
                'noreply@countrysite',
                [email]
            )
            messages.success(request, RESULT_SUCCESS_MESSAGE_EMAIL_SENT)

        # if form invalid
        else:
            messages.warning(request, RESULT_WARNING_MESSAGE_BAD_EMAIL)

    # if request.method == get
    else:
        messages.success(request, RESULT_MESSAGE_SCORE+str(score))

    return render(
        request,
        'poll/result.html',
        {'form': ScoreRecordForm()}
    )


def get_four_random_countries():
    '''returns list[4] of unique random poll.models.Country objects'''

    count = Country.objects.count()
    ids = list(range(1, count))  # id start with 1
    random.shuffle(ids)
    return list(Country.objects.filter(id__in=ids[:4]))


def countriesByRegionsView(request):
    regions = list(Region.objects.all())
    country_list = {
        region: list(
            region.country for region in region.countryregion_set.all()
        ) for region in regions
    }

    return render(
        request,
        'poll/country_by_region.html',
        context={
            'country_list': country_list,
        }
    )


class CountryListView(ListView):
    model = Country
    paginate_by = 15
