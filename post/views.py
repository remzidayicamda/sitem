from os import stat
from django.db.models import query
from django.shortcuts import render, HttpResponse, get_object_or_404, redirect, HttpResponseRedirect
from .models import *
from .forms import *
from django.contrib import messages
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
import ipapi

# Create your views here.


def post_index(request):
    post_list = Post.objects.all()

    query = request.GET.get('q')
    if query:
        post_list = post_list.filter(
            Q(title__icontains = query) | 
            Q(content__icontains = query) 
        ).distinct()

        if not post_list:
            return Http404()

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
    return render(request, "post/index.html", {"posts": posts})


def post_detail(request, slug):
    search = request.POST.get("search")
    data = ipapi.location(ip=search, output = "json")
    a = request.GET.get('q')
    if a:
        return HttpResponseRedirect("/post/index/" + "?q=" + a)

    post = get_object_or_404(Post, slug=slug)

    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.ip = data
        comment.save()
        return HttpResponseRedirect(post.get_absolute_url())

    context = {
        "data": data,
        "post": post,
        "form": form,
    }

    return render(request, "post/detail.html", context)


def post_create(request):

    a = request.GET.get('q')
    if a:
        return HttpResponseRedirect("/post/index/" + "?q=" + a)

    if not request.user.is_authenticated:
        return Http404()

    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        post = form.save()
        messages.success(
            request, 'Yazınızı Başarılı Bir Şekilde Oluşturdunuz.')
        return HttpResponseRedirect(post.get_absolute_url())

    context = {
        'form': form
    }
    return render(request, "post/form.html", context)


def post_update(request, slug):

    a = request.GET.get('q')
    if a:
        return HttpResponseRedirect("/post/index/" + "?q=" + a)

    if not request.user.is_authenticated:
        return Http404()

    post = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)

    if form.is_valid():
        form.save()
        messages.success(request, 'Yazınız Başarıyla Güncellendi.')
        return HttpResponseRedirect(post.get_absolute_url())

    context = {
        "form": form,
    }
    return render(request, "post/form.html", context)


def post_delete(request, slug):
    if not request.user.is_authenticated:
        # Eğer kullanıcı giriş yapmamış ise hata sayfası gönder
        return Http404()

    post = get_object_or_404(Post, slug=slug)
    post.delete()
    return redirect("post:index")

def hendler_400(request, exception):
    return render(request, "404.html", status=400)

def hendler_403(request, exception):
    return render(request, "404.html", status=403)

def hendler_404(request, exception):
    return render(request, "404.html", status=404)

def server_error(request):
    return render(request, "500.html", status=500)

