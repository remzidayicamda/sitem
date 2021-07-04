from django.shortcuts import render, HttpResponseRedirect
from post.models import *
from post.forms import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.


def home_view(request):
    post_list = Post.objects.all()

    paginator = Paginator(post_list, 5) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)
    a = request.GET.get('q')
    if a:
        return HttpResponseRedirect("/post/index/" + "?q=" + a)

    return render(request, "home.html", {"posts": posts})

def info_view(request):
    a = request.GET.get('q')
    if a:
        return HttpResponseRedirect("/post/index/" + "?q=" + a)
    return render(request, "hakkimda.html")

def contact(request):
    a = request.GET.get('q')
    if a:
        return HttpResponseRedirect("/post/index/" + "?q=" + a)
    return render(request, "iletisim.html")


def gizlilik_politika(request):
    a = request.GET.get('q')
    if a:
        return HttpResponseRedirect("/post/index/" + "?q=" + a)
    return render(request, "gizlilik-politikasi.html")

def cerez_politika(request):
    a = request.GET.get('q')
    if a:
        return HttpResponseRedirect("/post/index/" + "?q=" + a)
    return render(request, "cerez-politikasi.html")
