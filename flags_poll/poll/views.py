from django.shortcuts import render

# Create your views here.

def indexView(request):
    return render(request, 'poll/index.html')

def pollView(request):
    return render(request, 'poll/poll.html')
