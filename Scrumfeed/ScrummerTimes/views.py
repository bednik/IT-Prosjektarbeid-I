from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
# Create your views here.

from .models import Article

from .forms import ArticleForm


def feed(request):
    articles = Article.objects.all()[:10]

    context = {
        'title': 'The Scrummer Times',
        'articles': articles
    }

    return render(request, 'ScrummerTimes/feed.html',context)


def article(request, id):
    thisArticle = Article.objects.get(id=id)
    context = {
        'article': thisArticle
    }
    # Sends to the html file (index.html)
    return render(request, 'ScrummerTimes/article.html',
                  context)

@login_required(login_url="/accounts/login/")
def createarticle(request):
    form = ArticleForm()
    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES)

        if form.is_valid():
            #Takes the data from the form into the database by creating an article object
            article = Article(text=form.cleaned_data["text"], header_image=form.cleaned_data["header_image"],
                              title=form.cleaned_data["title"])
            article.save()
            #Redirects back to the feed
            # return HttpResponseRedirect(reversed('ScrummerTimes/feed'))
            return HttpResponseRedirect('ScrummerTimes/feed')

    context = {
        'form': form
    }

    return render(request, 'ScrummerTimes/createarticle.html', context)


@login_required(login_url="/accounts/login/")
def editarticle(request, id):
    article = Article.objects.get(id=id)
    form = ArticleForm(inital={'header_image':article.header_image, 'title':article.title, 'text':article.text})
    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES)

        if form.is_valid():
            #Takes the data from the form into the database by creating an article object
            article.header_image = form.cleaned_data["header_image"]
            article.text = form.cleaned_data["text"]
            article.title = form.cleaned_data["title"]
            article.save()
            #Redirects back to the feed
            # return HttpResponseRedirect(reversed('ScrummerTimes/feed'))
            return HttpResponseRedirect('ScrummerTimes/feed')

    context = {
        'form': form
    }

    return render(request, 'ScrummerTimes/editarticle.html', context)