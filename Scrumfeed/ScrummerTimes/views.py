from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.contenttypes.models import ContentType
from django.forms import forms
from django.shortcuts import render, get_object_or_404, render_to_response
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.datetime_safe import datetime
from django.urls import reverse
from .models import Article, Category
from .forms import ArticleForm, FilterForm, CreateCategoryForm, NewCommentForm
from comments.models import Comment


def analytics(request):
    data = [['100', 10], ['500', 9], ['80', 8]]
    context = {
        'data':data,
    }
    return render(request, 'ScrummerTimes/analytics.html', context)


def manage_site(request):
    form = CreateCategoryForm(initial={'name': ''})
#
    if request.method == "POST":
        form = CreateCategoryForm(request.POST)
        if form.is_valid():
            category_object = form.cleaned_data["category"]
            name = form.cleaned_data["name"]
            # If editing
            if 'edit_category' in request.POST:
                if name == "":
                    messages.info(request, "Name can not be blank")

                elif not category_object:
                    category = Category(name=name)
                    category.save()
                    messages.info(request, "Successfully added the category  " + form.cleaned_data["name"])
                else:
                    messages.info(request, "Successfully changed the name of the category  " + category_object.name + "  to  " + form.cleaned_data["name"])
                    category_object.name = form.cleaned_data["name"]
                    category_object.save()
            # if deleting
            if 'delete_category' in request.POST :
                if category_object:
                    category_object.delete()
                    messages.info(request, "Successfully deleted the category  " + category_object.name)
                else:
                    messages.info(request, "You did not select or write anything")

            #Redirect to same page
            return HttpResponseRedirect(reverse(manage_site))
        else:
            messages.info(request, form.errors)
            # Redirect to same page
            return HttpResponseRedirect(reverse(manage_site))

    all_categories = Category.objects.all()
    context = {
        'form': form,
        'categories': all_categories,
    }

    return render(request, 'ScrummerTimes/managesite.html', context)


def feed(request):
    form = FilterForm()
    articles = Article.objects.filter(is_read=True)[:10]
    if request.method == "POST":
        form = FilterForm(request.POST)

        if form.is_valid():
            selected_category = form.cleaned_data["category"]
            articles = Article.objects.filter(is_read=True, category=selected_category)

    context = {
        'title': 'The Scrummer Times',
        'articles': articles,
        'form': form
    }

    return render(request, 'ScrummerTimes/feed.html', context)


# @permission_required('entity.can_edit', login_url='/accounts/login/')
@permission_required('ScrummerTimes.review_article', login_url='/accounts/login/')
def proofreading_feed(request):
    articles = Article.objects.filter(is_read=False).filter(draft=False).filter(is_completed=False)[:10]

    context = {
        'title': 'The Scrummer Times',
        'articles': articles
    }

    return render(request, 'ScrummerTimes/feedUnread.html', context)

@permission_required('ScrummerTimes.publish_article', login_url='/accounts/login/')
def publishing_feed(request):
    form = FilterForm()
    articles = Article.objects.filter(is_completed=True)[:10]
    if request.method == "POST":
        form = FilterForm(request.POST)

        if form.is_valid():
            selected_category = form.cleaned_data["category"]
            articles = Article.objects.filter(is_read=True, category=selected_category)

    context = {
        'title': 'The Scrummer Times',
        'articles': articles
    }
    return render(request, 'ScrummerTimes/feedUnpublished.html', context)

# View for articles that are not supposed to be reviewed/published/edited by copy editors just yet
def mydrafts(request):
    # Must be logged in
    if request.user.is_authenticated:
        articles = Article.objects.filter(authors=request.user).filter(draft=True)

        if request.method == "POST":
            form = DeleteForm(request.POST, request.FILES)

            if form.is_valid:
                Article.objects.filter(draft=True).delete()


        context = {
            'title': 'The Scrummer Times',
            'articles': articles
        }

        return render(request, 'ScrummerTimes/myDrafts.html', context)
    return render(request, 'ScrummerTimes/myDrafts.html', None)


def myarticles(request):
    # Must be logged in
    if request.user.is_authenticated:
        articles = Article.objects.filter(authors=request.user).filter(draft=False).order_by('-date') # Kun ferdige artikler dukker opp. Drafts legger seg i "My Drafts"

        context = {
            'title': 'The Scrummer Times',
            'articles': articles
        }

        return render(request, 'ScrummerTimes/myArticles.html',context)
    return render(request, 'ScrummerTimes/myArticles.html', None)


def article(request, id):
    thisArticle = Article.objects.get(id=id)

    # Adds the form for people to comment on stuff
    initial_data_comment = {
        "content_type": thisArticle.get_content_type,
        "object_id": thisArticle.id
    }

    # Checks the form and posts the comment if all is well
    comment_form = NewCommentForm(request.POST or None, initial=initial_data_comment)

    if comment_form.is_valid():
        c_content_type = ContentType.objects.get(model=comment_form.cleaned_data.get("content_type"))
        c_obj_id = comment_form.cleaned_data.get("object_id")
        c_data = comment_form.cleaned_data.get("content")
        new_comment, created = Comment.objects.get_or_create(
            user = request.user,
            content_type = c_content_type,
            object_id = c_obj_id,
            content = c_data
        )
    comments = Comment.objects.filter_by_instance(thisArticle)

    context = {
        'article': thisArticle, 'comments': comments, 'comment_form': comment_form
    }
    # Sends to the html file (index.html)
    return render(request, 'ScrummerTimes/article.html',
                  context)


def createarticle(request):

    if not request.user.is_authenticated and not request.user.has_perm("ScrummerTimes.create_article"):
        return HttpResponseNotFound("You do not have permission for this page. You have to be an Author.")
    form = ArticleForm()
    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES)

        if form.is_valid():
            header_image = form.cleaned_data["header_image"]

            # Takes the data from the form into the database by creating an article object
            article = Article(header_image=form.cleaned_data["header_image"],
                              title=form.cleaned_data["title"],
                              first_text=form.cleaned_data["first_text"],
                              in_line_image=form.cleaned_data["in_line_image"],
                              second_text=form.cleaned_data["second_text"],
                              category=form.cleaned_data["category"])

            article.is_read = False
            article.authors = request.user
            article.date = datetime.now()
            article.draft = form.cleaned_data["draft"]
            article.editors = None
            article.save()

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
    # User has to be either an editor or the author to edit this article
    if not request.user.has_perm("ScrummerTimes.review_article") and not request.user == article.authors:
        messages.info(request, "You do not have permission for this page. You have to be an Editor.")
        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

    form = ArticleForm(initial={'header_image': article.header_image,
                                'title': article.title,
                                'first_text': article.first_text,
                                'in_line_image': article.in_line_image,
                                'second_text': article.second_text,
                                'category': article.category,
                                'is_read': article.is_read,
                                'draft': article.draft,
                                'is_completed' : article.is_completed}
                       )

    # Adds the form for people to comment on stuff
    initial_data_comment = {
        "content_type": article.get_content_type,
        "object_id": article.id
    }

    # Checks the form and posts the comment if all is well
    comment_form = NewCommentForm(request.POST or None, initial=initial_data_comment)

    if 'post_comment' in request.POST:
        print("test1")
        if comment_form.is_valid():
            c_content_type = ContentType.objects.get(model=comment_form.cleaned_data.get("content_type"))
            c_obj_id = comment_form.cleaned_data.get("object_id")
            c_data = comment_form.cleaned_data.get("content")
            new_comment, created = Comment.objects.get_or_create(
                user=request.user,
                content_type=c_content_type,
                object_id=c_obj_id,
                content=c_data
            )

    comments = Comment.objects.filter_by_instance(article)

    # if request.method == "POST":
    if 'submit_article' in request.POST:
        form = ArticleForm(request.POST, request.FILES)

        if form.is_valid():
            if 'delete' in form.data:
                article.delete()
            else:
                # Takes the data from the form into the database by creating an article object
                image = form.cleaned_data["header_image"]
                image2 = form.cleaned_data["in_line_image"]

                if image is not None:
                    article.header_image = image
                if image2 is not None:
                    article.in_line_image = image2
                article.title = form.cleaned_data["title"]
                article.first_text = form.cleaned_data["first_text"]
                article.second_text = form.cleaned_data["second_text"]
                article.category = form.cleaned_data["category"]
                article.draft = form.cleaned_data["draft"]
                article.is_completed = form.cleaned_data["is_completed"]

                #Only editors can publish the article, not the author
                if(request.user.has_perm("ScrummerTimes.publish_article")):

                    # Deleting comments if this option was changed
                    if article.is_read != form.cleaned_data["is_read"]:
                        Comment.objects.filter_by_instance(article).delete()
                        article.is_read = form.cleaned_data["is_read"]
                # if request.user.has_perm("ScrummerTimes.publish_article"):
                #     article.is_read = form.cleaned_data["is_read"]
                article.save()


                #Redirects back to the feed
                # return HttpResponseRedirect(reversed('ScrummerTimes/feed'))

            next = request.POST.get('next','/')
            return HttpResponseRedirect(next)

    context = {
        'form': form,
        'id': id,
        'article': article,
        'comments': comments,
        'comment_form': comment_form
    }

    return render(request, 'ScrummerTimes/editarticle.html', context)


def assignEditor(request, id=None):

    article = get_object_or_404(Article, pk=id)

    if request.method == "POST":
        article.editors = request.user
        article.save()
        next = request.POST.get('next', '/ScrummerTimes/feedUnread')
        return HttpResponseRedirect(next)

    context = {
        'form': form,
        'id': id,
        'article': article,
    }

    return render(request, 'ScrummerTimes/feedUnread.html', context)


def deleteEditor(request, id=None):

    article = get_object_or_404(Article, pk=id)

    if request.method == "POST":
        article.editors = None
        article.save()
        next = request.POST.get('next', '/ScrummerTimes/feedUnread')
        return HttpResponseRedirect(next)

    context = {
        'form': form,
        'id': id
    }

    return render(request, 'ScrummerTimes/feedUnread.html', context)


def assignEditor(request, id=None):

    article = get_object_or_404(Article, pk=id)

    if request.method == "POST":
        article.editors = request.user
        article.save()
        next = request.POST.get('next', '/ScrummerTimes/feedUnread')
        return HttpResponseRedirect(next)

    context = {
        'form': form,
        'id': id
    }

    return render(request, 'ScrummerTimes/feedUnread.html', context)


def deleteEditor(request, id=None):

    article = get_object_or_404(Article, pk=id)

    if request.method == "POST":
        article.editors = None
        article.save()
        next = request.POST.get('next', '/ScrummerTimes/feedUnread')
        return HttpResponseRedirect(next)

    context = {
        'form': form,
        'id': id
    }

    return render(request, 'ScrummerTimes/feedUnread.html', context)



def newContent(request, id=None):

    subscribedAuthors = None  # request.user.subscriptions.authors  # TODO: Må samkjøres med story 15
    subscribedCategories = Category.objects.all()  # request.user.subscriptions.categories # TODO: Må samkjøres med story 15

    if request.user.is_authenticated:

        authorArticles = Article.objects.none()
        for author in subscribedAuthors
            authorArticles = Article.objects.filter(draft=False).filter(authors=author) | authorArticles

        categoryArticles = Article.objects.none()
        for category in subscribedCategories:
            categoryArticles = Article.objects.filter(draft=False).filter(category=category) | categoryArticles

        articles = (authorArticles | categoryArticles).order_by('-date')

        context = {
            'title': 'The Scrummer Times',
            'articles': articles
        }

        return render(request, 'ScrummerTimes/newContent.html', context)
    return render(request, 'ScrummerTimes/newContent.html', None)

