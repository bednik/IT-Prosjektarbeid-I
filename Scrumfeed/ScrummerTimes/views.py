from django.forms import forms
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
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


#@permission_required('entity.can_edit', login_url='/accounts/login/')
@permission_required('ScrummerTimes.review_article', login_url='/accounts/login/')
def proofreading_feed(request):

    articles = Article.objects.filter(is_read=False)

    context = {
        'title': 'The Scrummer Times',
        'articles': articles
    }

    return render(request, 'ScrummerTimes/feedUnread.html',context)



def myarticles(request):
    #Must be logged in
    if(request.user.is_authenticated):
        articles = Article.objects.filter(authors=request.user)

        context = {
            'title': 'The Scrummer Times',
            'articles': articles
        }

        return render(request, 'ScrummerTimes/myArticles.html',context)
    return render(request, 'ScrummerTimes/myArticles.html', None)

def article(request, id):
    thisArticle = Article.objects.get(id=id)
    context = {
        'article': thisArticle
    }
    # Sends to the html file (index.html)
    return render(request, 'ScrummerTimes/article.html',
                  context)


def createarticle(request):

    if(not request.user.is_authenticated and not request.user.has_perm("ScrummerTimes.create_article")):
        return HttpResponseNotFound("You do not have permission for this page. You have to be an Author.")
    form = ArticleForm()
    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES)

        if form.is_valid():
            #Takes the data from the form into the database by creating an article object
            article = Article(text=form.cleaned_data["text"], header_image=form.cleaned_data["header_image"],
                              title=form.cleaned_data["title"])
            article.is_read = False
            article.authors = request.user
                              title=form.cleaned_data["title"], category=form.cleaned_data["category"])
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
    #User has to be either an editor or the author to edit this article
    if (not request.user.has_perm("ScrummerTimes.review_article") and not request.user == article.authors):
        return HttpResponseNotFound("You do not have permission for this page. You have to be an Editor.")

    form = ArticleForm(initial={'header_image': article.header_image, 'title': article.title, 'text': article.text, 'is_read': article.is_read})

    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES)

        if form.is_valid():
            #Takes the data from the form into the database by creating an article object
            image = form.cleaned_data["header_image"]

            if(image != None):
                article.header_image = form.cleaned_data["header_image"]
            article.text = form.cleaned_data["text"]
            article.title = form.cleaned_data["title"]

            #Only editors can publish the article, not the author
            if(request.user.has_perm("ScrummerTimes.publish_article")):
                article.is_read = form.cleaned_data["is_read"]
            article.save()
            #Redirects back to the feed
            # return HttpResponseRedirect(reversed('ScrummerTimes/feed'))
            next = request.POST.get('next','/')
            return HttpResponseRedirect(next)

    context = {
        'form': form,
        'id': id
    }

    return render(request, 'ScrummerTimes/editarticle.html', context)