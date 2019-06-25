from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Post, Comment
from .forms import PostForm, CommentForm


def login(request):
    return render(request, 'registration/home.html', )


def post_list(request):
    posts = Post.objects.all().order_by('-created_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.comments = post.comments().order_by('date')
    return render(request, 'blog/post_detail.html', {'post': post})


@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')


@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)


def add_comm(request):
    if request.user.is_authenticated and request.user.is_active and request.method == "POST":
        form = request.POST
        if form.get('post-id') and form.get('post-id').isnumeric():
            post = Post.objects.filter(pk=int(form.get("post-id")))
            if len(post) == 0:
                return redirect('post_list')
        else:
            return redirect('post_list')

        if form.get('comm-id') and form.get('comm-id').isnumeric():
            comm = Comment.objects.filter(pk=int(form.get("comm-id")))
            if len(comm) == 1:
                returnComm = Comment(author=request.user, text=form.get('text'),
                                     answer_message=post[0], answer_comment=comm[0])
        else:
            returnComm = Comment(author=request.user, text=form.get('text'),
                                 answer_message=post[0])

        returnComm.save()

    return redirect('post_list')


@login_required
def edit_com(self, request):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_list')
    else:
        form = CommentForm()
    return render(request, 'blog/post_list.html', {'form': form})
