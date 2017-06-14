from django.shortcuts import render
from .models import Event, City, Country, Scholarship, Job, EventType
from .forms import EventSearchForm
from django.http import HttpResponseRedirect


# Create your views here.
def index(request):
    events = Event.objects.all()
    counts = (1, 2, 3, 4, 5, 6)
    return render(request, 'event/index.html', locals())


def event(request, event_id):
    this_event = Event.get_event_by_id(event_id)
    tags = this_event.tags.split(",")
    other_events = Event.get_other_events(event_id)
    counts = (1, 2, 3, 4, 5, 6)
    return render(request, 'event/event.html', locals())


def event_results(request, category):
    if category == 'conferences':
        pk = 1
    elif category == 'training-workshops':
        pk = 4
    else:
        pk = 1
    event_category = EventType.objects.get(pk=pk)

    events = Event.objects.filter(type=event_category)
    counts = (1, 2, 3, 4, 5, 6)
    return render(request, 'event/search.html', locals())


def get_events(request):
    if request.method == 'POST':
        form = EventSearchForm(request.POST)
        if form.is_valid():
            search_field = form.cleaned_data['search_field']
            events_region = form.cleaned_data['events_region']
            events_date = form.cleaned_data['events_date']

            counts = (1, 2, 3, 4, 5, 6)
            return render(request, 'event/search.html', locals())

    else:
        form = EventSearchForm()

    return render(request, 'event/index.html', locals())


def scholarships(request):
    scholarship = Scholarship.objects.all()
    counts = (1, 2, 3, 4, 5, 6)
    return render(request, 'event/scholarships.html', locals())


def scholarship_details(request):
    counts = (1, 2, 3, 4, 5, 6)
    return render(request, 'event/scholarship-details.html', locals())


def jobs(request):
    job = Job.objects.all()
    counts = (1, 2, 3, 4, 5, 6)
    return render(request, 'event/jobs.html', locals())


def job_details(request):
    counts = (1, 2, 3, 4, 5, 6)
    return render(request, 'event/job-details.html', locals())