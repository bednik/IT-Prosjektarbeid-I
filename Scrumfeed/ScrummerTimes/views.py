from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.contenttypes.models import ContentType
from django.forms import forms
from django.shortcuts import render, get_object_or_404, render_to_response
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.urls import reverse
# Create your views here.


from .models import Article

from .forms import ArticleForm, FilterForm

from comments.models import Comment


def feed(request):
    form = FilterForm()
    if ("news" in request.get_full_path()):
        articles = Article.objects.filter(is_read=True, category="news")
    elif ("movies" in request.get_full_path()):
        articles = Article.objects.filter(is_read=True, category="movies/tv")
    elif ("music" in request.get_full_path()):
        articles = Article.objects.filter(is_read=True, category="music")
    elif ("sport" in request.get_full_path()):
        articles = Article.objects.filter(is_read=True, category="sports")
    elif ("travel" in request.get_full_path()):
        articles = Article.objects.filter(is_read=True, category="travel")
    elif ("capital" in request.get_full_path()):
        articles = Article.objects.filter(is_read=True, category="capital")
    else:
        articles = Article.objects.filter(is_read=True)[:10]

    context = {
        'title': 'The Scrummer Times',
        'articles': articles,
        'form': form
    }

    return render(request, 'ScrummerTimes/feed.html',context)


#@permission_required('entity.can_edit', login_url='/accounts/login/')
@permission_required('ScrummerTimes.review_article', login_url='/accounts/login/')
def proofreading_feed(request):

    if ("news" in request.get_full_path()):
        articles = Article.objects.filter(is_read=False, category="news")
    elif ("movies" in request.get_full_path()):
        articles = Article.objects.filter(is_read=False, category="movies/tv")
    elif ("music" in request.get_full_path()):
        articles = Article.objects.filter(is_read=False, category="music")
    elif ("sport" in request.get_full_path()):
        articles = Article.objects.filter(is_read=False, category="sports")
    elif ("travel" in request.get_full_path()):
        articles = Article.objects.filter(is_read=False, category="travel")
    elif ("capital" in request.get_full_path()):
        articles = Article.objects.filter(is_read=False, category="capital")
    else:
        articles = Article.objects.filter(is_read=False)[:10]

    context = {
        'title': 'The Scrummer Times',
        'articles': articles
    }

    return render(request, 'ScrummerTimes/feedUnread.html', context)



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
    content_type = ContentType.objects.get_for_model(Article)
    obj_id = thisArticle.id
    comments = Comment.objects.filter(object_id=obj_id)

    context = {
        'article': thisArticle, 'comments': comments,
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
                              title=form.cleaned_data["title"], category=form.cleaned_data["category"])


            article.is_read = False
            article.authors = request.user
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
        messages.info(request, "You do not have permission for this page. You have to be an Editor.")
        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

    form = ArticleForm(initial={'header_image': article.header_image, 'title': article.title, 'text': article.text, 'is_read': article.is_read,
                                'category': article.category})

    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES)

        if form.is_valid():
            #Takes the data from the form into the database by creating an article object
            image = form.cleaned_data["header_image"]

            if(image != None):
                article.header_image = form.cleaned_data["header_image"]
            article.text = form.cleaned_data["text"]
            article.title = form.cleaned_data["title"]
            article.category = form.cleaned_data["category"]

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