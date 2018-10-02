from django.forms import forms
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required
# Create your views here.
from django.urls import reverse

from .models import Article

from .forms import ArticleForm


def feed(request):
    articles = Article.objects.filter(is_read=True)[:10]

    context = {
        'title': 'The Scrummer Times',
        'articles': articles
    }

    return render(request, 'ScrummerTimes/feed.html',context)


def user_can_edit_article(user):
    return user.is_authenticated() and user.has_perm("article.can_change")

#@permission_required('entity.can_edit', login_url='/accounts/login/')
@permission_required('ScrummerTimes.review_article', login_url='/accounts/login/')
def proofreading_feed(request):

    articles = Article.objects.filter(is_read=False)

    context = {
        'title': 'The Scrummer Times',
        'articles': articles
    }

    return render(request, 'ScrummerTimes/feedUnread.html',context)

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

            # redirects to previous visited paged, does not work if browser is in incognito mode
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)

    context = {
        'form': form
    }

    return render(request, 'ScrummerTimes/createarticle.html', context)



@login_required(login_url="/accounts/login/")
def editarticle(request, id=None):
    article = get_object_or_404(Article, pk=id)
    form = ArticleForm(initial={'header_image': article.header_image, 'title': article.title, 'text': article.text})

    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES)

        if form.is_valid():
            #Takes the data from the form into the database by creating an article object
            image = form.cleaned_data["header_image"]

            if(image != None):
                article.header_image = form.cleaned_data["header_image"]
            article.text = form.cleaned_data["text"]
            article.title = form.cleaned_data["title"]
            article.save()
            #Redirects back to the feed
            # return HttpResponseRedirect(reversed('ScrummerTimes/feed'))
            next = request.POST.get('next','/')
            return HttpResponseRedirect(next)
            #redirects to previous visited paged, does not work if browser is in incognito mode
            #return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
            #return HttpResponseRedirect(reverse(feed))
        else:
            raise forms.ValidationError({"lo"})
    context = {
        'form': form,
        'id': id
    }

    return render(request, 'ScrummerTimes/editarticle.html', context)