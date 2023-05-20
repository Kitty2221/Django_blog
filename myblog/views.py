from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import BlogPostForm
from django.views.generic import UpdateView
from django.contrib import messages


def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('/register')

        user = User.objects.create_user(username, email, password1)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return render(request, 'auth/login.html')
    return render(request, "auth/register.html")


def log_in(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("/")
        else:
            messages.error(request, "Invalid Credentials")
        return render(request, 'posts/all_posts.html')
    return render(request, "auth/login.html")


def log_out(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('/login')


def blogs(request):
    posts = BlogPost.objects.all()
    posts = BlogPost.objects.filter().order_by('-created')
    return render(request, "posts/all_posts.html", {'posts': posts})


def post_by_id(request, id):
    post = BlogPost.objects.get(id=id)
    context = {'title': post.title, 'body': post.body, 'author': post.author,
               'image': post.image}

    return render(request, 'posts/post_details.html', context)


@login_required(login_url='/login')
def add_blogs(request):
    if request.method == "POST":
        form = BlogPostForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            blogpost = form.save(commit=False)
            blogpost.author = request.user
            blogpost.save()
            obj = form.instance
            alert = True
            return render(request, "posts/add_post.html", {'obj': obj, 'alert': alert})
    else:
        form = BlogPostForm()
    return render(request, "posts/add_post.html", {'form': form})


class UpdatePostView(UpdateView):
    model = BlogPost
    template_name = 'posts/edit_post.html'
    fields = ['title', 'body', 'image']


def delete_post(request, id):
    item = get_object_or_404(BlogPost, id=id)
    if item:
        item.delete()
        return redirect('/')


def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        blogs = BlogPost.objects.filter(title__contains=searched)
        return render(request, "posts/search.html", {'searched': searched, 'blogs': blogs})
    else:
        return render(request, "posts/search.html", {})


def profile(request):
    return render(request, "profile.html")
