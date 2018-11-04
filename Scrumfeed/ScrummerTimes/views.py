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
from .models import Article, Category, Role, Style
from .forms import ArticleForm, FilterForm, CreateCategoryForm, NewCommentForm, RequestRole, DeleteForm, FilterEditor, StyleForm
from comments.models import Comment
from django.contrib.auth.models import Permission, User


def analytics(request):
    styles = Style.objects.filter()
    data = [['100', 10], ['500', 9], ['80', 8]]
    context = {
        'data':data,
        'styles': styles
    }
    return render(request, 'ScrummerTimes/analytics.html', context)


def manage_site(request):
    form = CreateCategoryForm(initial={'name': ''})
    styles = Style.objects.filter()
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
        'styles': styles
    }

    return render(request, 'ScrummerTimes/managesite.html', context)

@permission_required('ScrummerTimes.set_style', login_url='/accounts/login/')
def styleChange(request):
    form = StyleForm(initial={'name': ''})
    styles = Style.objects.filter()
    if request.method == "POST":
        form = StyleForm(request.POST)

        if form.is_valid():
            styles.update(is_marked=False)
            style_object = form.cleaned_data["style"]
            style_object.is_marked = True
            style_object.save()

    context = {
        'form': form,
        'styles': styles
    }

    return render(request, 'ScrummerTimes/style.html', context)


def feed(request):
    form = FilterForm()
    articles = Article.objects.filter(is_read=True).order_by('-date')[:10]
    styles = Style.objects.filter()
    if request.method == "POST":
        form = FilterForm(request.POST)

        if form.is_valid():
            selected_category = form.cleaned_data["category"]
            articles = Article.objects.filter(is_read=True, category=selected_category).order_by('-date')

    context = {
        'title': 'The Scrummer Times',
        'articles': articles,
        'form': form,
        'styles': styles
    }

    return render(request, 'ScrummerTimes/feed.html', context)


# @permission_required('entity.can_edit', login_url='/accounts/login/')
@permission_required('ScrummerTimes.review_article', login_url='/accounts/login/')
def proofreading_feed(request):
    articles = Article.objects.filter(is_read=False).filter(draft=False).filter(is_completed=False).order_by('-date')[:10]
    styles = Style.objects.filter()
    form = FilterEditor()

    context = {
        'title': 'The Scrummer Times',
        'articles': articles,
        'styles': styles,
        'form': form
    }

    return render(request, 'ScrummerTimes/feedUnread.html', context)

@permission_required('ScrummerTimes.publish_article', login_url='/accounts/login/')
def publishing_feed(request):
    form = FilterForm()
    articles = Article.objects.filter(is_completed=True).order_by('-date')[:10]
    styles = Style.objects.filter()
    if request.method == "POST":
        form = FilterForm(request.POST)

        if form.is_valid():
            selected_category = form.cleaned_data["category"]
            articles = Article.objects.filter(is_read=True, category=selected_category).order_by('-date')

    context = {
        'title': 'The Scrummer Times',
        'articles': articles,
        'styles': styles
    }
    return render(request, 'ScrummerTimes/feedUnpublished.html', context)

# View for articles that are not supposed to be reviewed/published/edited by copy editors just yet
def mydrafts(request):
    # Must be logged in
    styles = Style.objects.filter()
    if request.user.is_authenticated:
        articles = Article.objects.filter(authors=request.user).filter(draft=True).order_by('-date')

        if request.method == "POST":
            form = DeleteForm(request.POST, request.FILES)

            if form.is_valid:
                Article.objects.filter(draft=True).delete()


        context = {
            'title': 'The Scrummer Times',
            'articles': articles,
            'styles': styles
        }

        return render(request, 'ScrummerTimes/myDrafts.html', context)
    return render(request, 'ScrummerTimes/myDrafts.html', None)


def myarticles(request):
    # Must be logged in
    styles = Style.objects.filter()
    if request.user.is_authenticated:
        articles = Article.objects.filter(authors=request.user).filter(draft=False).order_by('-date') # Kun ferdige artikler dukker opp. Drafts legger seg i "My Drafts"

        context = {
            'title': 'The Scrummer Times',
            'articles': articles,
            'styles': styles
        }

        return render(request, 'ScrummerTimes/myArticles.html',context)
    return render(request, 'ScrummerTimes/myArticles.html', None)


def article(request, id):
    thisArticle = Article.objects.get(id=id)
    styles = Style.objects.filter()
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
        'article': thisArticle, 'comments': comments, 'comment_form': comment_form, 'styles':styles
    }
    # Sends to the html file (index.html)
    return render(request, 'ScrummerTimes/article.html',
                  context)


def give_author_permissions(user):
    p1 = Permission.objects.get(codename='create_article')
    p2 = Permission.objects.get(codename='save_as_draft')
    user.user_permissions.add(p1)
    user.user_permissions.add(p2)


def give_copyeditor_permissions(user):
    p1 = Permission.objects.get(codename='review_article')
    user.user_permissions.add(p1)


def give_executiveeditor_permissions(user):
    p1 = Permission.objects.get(codename='publish_article')
    p2 = Permission.objects.get(codename='edit_categories')
    p3 = Permission.objects.get(codename='assign_article')
    user.user_permissions.add(p1)
    user.user_permissions.add(p2)
    user.user_permissions.add(p3)
    give_copyeditor_permissions(user)


def requestrole(request):
    styles = Style.objects.filter()
    if not request.user.is_authenticated:
        messages.info(request, "You have to be a registered user")
        return HttpResponseRedirect(reverse(requestrole))
    form = RequestRole()
    if request.method == "POST":
        form = RequestRole(request.POST)
        if form.is_valid():
            if 'create_request' in request.POST:
                role = Role(reason=form.cleaned_data["reason"],
                            role=form.cleaned_data["role"])
                role.user = request.user
                role.save()
                messages.info(request, "Successfully created a role request")
            return HttpResponseRedirect(reverse(requestrole))

    roles = None
    if request.user.is_superuser:
        roles = Role.objects.all()
    context = {
        'form': form,
        'roles': roles,
        'styles': styles
    }

    return render(request, 'ScrummerTimes/requestRole.html', context)


def assignroles(request, id=None):
    styles = Style.objects.filter()
    if not request.user.is_authenticated and not request.user.is_superuser:
        messages.info(request, "You have to be admin")
        return HttpResponseRedirect(reverse(requestrole))
    if request.method == "POST":
        if 'allow_request' in request.POST:
            roleRequest = get_object_or_404(Role, pk=id)
            user = User.objects.get(pk=roleRequest.user.id)
            if roleRequest.role == "1":
                give_author_permissions(user)
            elif roleRequest.role == "2":
                give_copyeditor_permissions(user)
            elif roleRequest.role == "3":
                give_executiveeditor_permissions(user)

            messages.info(request, "Successfully accepted request from " + user.username + " to become " + roleRequest.getrolename())
            roleRequest.delete()


        elif 'deny_request' in request.POST:
            roleRequest = get_object_or_404(Role, pk=id)
            roleRequest.delete()
            messages.info(request, "Successfully denied request")

        # redirects to previous visited paged, does not work if browser is in incognito mode
        # next = request.POST.get('next', '/')
        return HttpResponseRedirect(reverse(requestrole))


    context = {
        'form': form,
        'styles': styles
    }

    return render(request, 'ScrummerTimes/requestRole.html', context)


def createarticle(request):
    styles = Style.objects.filter()
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
            article.theme = form.cleaned_data["theme"]
            article.save()

            # redirects to previous visited paged, does not work if browser is in incognito mode
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)

    context = {
        'form': form,
        'styles': styles
    }

    return render(request, 'ScrummerTimes/createarticle.html', context)


@login_required(login_url="/accounts/login/")
def editarticle(request, id=None):
    styles = Style.objects.filter()
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
                                'is_completed' : article.is_completed,
                                'theme' : article.theme}
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
                article.theme = form.cleaned_data["theme"]

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
        'comment_form': comment_form,
        'styles': styles
    }

    return render(request, 'ScrummerTimes/editarticle.html', context)


def assignEditor(request, id=None):
    styles = Style.objects.filter()
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
        'styles': styles
    }

    return render(request, 'ScrummerTimes/feedUnread.html', context)


def deleteEditor(request, id=None):
    styles = Style.objects.filter()
    article = get_object_or_404(Article, pk=id)

    if request.method == "POST":
        article.editors = None
        article.save()
        next = request.POST.get('next', '/ScrummerTimes/feedUnread')
        return HttpResponseRedirect(next)

    context = {
        'form': form,
        'id': id,
        'styles': styles
    }

    return render(request, 'ScrummerTimes/feedUnread.html', context)


def select_copyEditor(request, id=None):

    if not request.user.has_perm("ScrummerTimes.publish_article"):
        messages.info(request, "You have to be an executive editor")
        return HttpResponseRedirect(reverse(proofreading_feed))

    article = get_object_or_404(Article, pk=id)
    form = FilterEditor()
    if request.method == "POST":
        form = FilterEditor(request.POST)
        if form.is_valid():

            article.editors = form.cleaned_data["copyeditor"]
            article.save()
            return HttpResponseRedirect(reverse(proofreading_feed))

    context = {
        'form': form,
        'id': id
    }

    return render(request, 'ScrummerTimes/feedUnread.html', context)
