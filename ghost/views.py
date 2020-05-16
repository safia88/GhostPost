from django.shortcuts import render, HttpResponseRedirect, reverse
from ghost.forms import PostForm
from ghost.models import Post


def index(request):
    html = 'index.html'
    posts = Post.objects.all().order_by('-submit_time')
    return render(request, html, {'posts': posts})


def add_post(request):
    html = 'add_post.html'

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Post.objects.create(
                is_boast=data['is_boast'],
                content=data['content'],
            )
            return HttpResponseRedirect(reverse('homepage'))
    form = PostForm(request.POST)
    return render(request, html, {'form': form})


def boast(request):
    html = 'index.html'
    posts = Post.objects.all().filter(is_boast=True).order_by('-submit_time')
    return render(request, html, {'posts': posts})


def roast(request):
    html = 'index.html'
    posts = Post.objects.all().filter(is_boast=False).order_by('-submit_time')
    return render(request, html, {'posts': posts})


def sorted_posts(request):
    posts = Post.objects.order_by('-total_votes')
    return render(request, 'index.html', {'posts': posts})


def up_votes(request, id):
    post = Post.objects.get(id=id)
    post.up_votes += 1
    post.total_votes += 1
    post.save()
    return HttpResponseRedirect(reverse('homepage'))


def down_votes(request, id):
    post = Post.objects.get(id=id)
    post.down_votes += 1
    post.total_votes -= 1
    post.save()
    return HttpResponseRedirect(reverse('homepage'))


def delete_post(request, id):
    instance = Post.objects.get(id=id)
    instance.delete()
    return HttpResponseRedirect(reverse('homepage'))
