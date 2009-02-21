from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from uitester.models import *
from django.template import RequestContext

def index(request):
    return render_to_response("index.html", {}, context_instance=RequestContext(request))

def rankings(request):
    pages = Page.objects.all()
    #todo: do sorting
    return render_to_response("rankings.html", {"pages": pages}, context_instance=RequestContext(request))

def startSurvey(request):
    if request.session.has_key('rating_id'):
        # user is in the middle of a survey
        try:
            rating = Rating.objects.get(pk=request.session['rating_id'])
            if not rating.finished:
                # they're not done yet, let them resume where they left off
                pages = Page.objects.all()
                for nextpage in pages:
                    scores = Score.objects.filter(rating=rating, page=nextpage)
                    if not scores:
                        return HttpResponseRedirect("/survey/%s/" % nextpage.id)

        except Rating.DoesNotExist:
            pass
    rating = Rating()
    rating.ip = request.META['REMOTE_ADDR']
    rating.hostname = request.META['REMOTE_HOST']
    rating.save()
    request.session['rating_id'] = rating.id
    pages = Page.objects.all()
    if not pages:
        #todo: show message saying no pages are available yet
        return HttpResponseRedirect("/rankings/")
    return HttpResponseRedirect("/survey/%s/" % pages[0].pk)

def surveyPage(request, id):
    try:
        rating = Rating.objects.get(pk=request.session['rating_id'])
    except Rating.DoesNotExist:
        return HttpResponseRedirect("/survey/start/")
    page = get_object_or_404(Page, pk=id)
    factors = Factor.objects.all()
    
    # check if we already have a score for that page
    scores = Score.objects.filter(rating=rating, page=page)
    if scores:
        # find the next page
        pages = Page.objects.all()
        for nextpage in pages:
            scores = Score.objects.filter(rating=rating, page=nextpage)
            if not scores:
                return HttpResponseRedirect("/survey/%s/" % nextpage.id)


    request.session['last_page'] = page.id
    return render_to_response("runtest.html", {'page': page, 'factors': factors}, context_instance=RequestContext(request))

def logSurveyScores(request):
    # get the rating
    try:
        rating = Rating.objects.get(pk=request.session['rating_id'])
    except Rating.DoesNotExist:
        return HttpResponseRedirect("/survey/start/")

    # get the page
    try:
        page = Page.objects.get(pk=request.POST['page_id'])
    except Page.DoesNotExist:
        return HttpResponseRedirect("/survey/start/")

    # record the scores for this page
    factors = Factor.objects.all()
    for factor in factors:
       value = request.POST['factor_%s' % factor.name]
       score = Score(page=page, rating=rating, factor=factor, value=value)
       score.save()

    # figure out the next page
    pages = Page.objects.all()
    for nextpage in pages:
        scores = Score.objects.filter(rating=rating, page=nextpage)
        if not scores:
            return HttpResponseRedirect("/survey/%s/" % nextpage.id)
    
    # when there are no more pages left, we're done.
    rating.finished=True
    rating.save()
    #todo: show confirmation message alerting that the survey is done
    return HttpResponseRedirect("/rankings/")
