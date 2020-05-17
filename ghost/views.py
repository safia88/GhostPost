from django.shortcuts import render, HttpResponseRedirect, reverse
from ghost.forms import PostForm
from ghost.models import Post
import random
import string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.functional import SimpleLazyObject
from django.contrib import messages


def index(request):
    html = 'index.html'
    posts = Post.objects.all().order_by('-submit_time')
    return render(request, html, {'posts': posts})


def getRandomString(stringLength=6):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


def isUnique(secret_key):
    post = Post.objects.get(secret_key=secret_key)
    if post:
        return False
    return True


def add_post(request):
    html = 'add_post.html'

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            randomString = getRandomString()
            Post.objects.create(
                is_boast=data['is_boast'],
                content=data['content'],
                secret_key=randomString
            )

            private_url = get_private_url(request, randomString)
            messages.success(request, private_url)
            return HttpResponseRedirect(reverse('homepage'))
    form = PostForm(request.POST)
    return render(request, html, {'form': form})


def boast(request):
    html = 'index.html'
    posts = Post.objects.filter(is_boast=True).order_by('-submit_time')
    return render(request, html, {'posts': posts})


def roast(request):
    html = 'index.html'
    posts = Post.objects.filter(is_boast=False).order_by('-submit_time')
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
    instance = Post.objects.get(secret_key=id)
    instance.delete()
    return HttpResponseRedirect(reverse('homepage'))


def get_site(request):
    site = SimpleLazyObject(lambda: get_current_site(request))
    protocol = 'https' if request.is_secure() else 'http'

    return SimpleLazyObject(lambda: "{0}://{1}".format(protocol, site.domain))


def get_private_url(request, random_string, path='posts'):
    return SimpleLazyObject(
        lambda: "{0}/{1}/{2}/".format(get_site(request), path, random_string))


def posts(request, id):
    html = "post_detail.html"
    post = None
    private_url = None

    if isinstance(id, int):
        items = Post.objects.filter(id=id)
    elif isinstance(id, str):
        items = Post.objects.filter(secret_key=id)
        private_url = get_private_url(request, id, 'delete')

    if items:
        post = items[0]
    return render(request, html,
                  {"post": post, "private_url": private_url})
