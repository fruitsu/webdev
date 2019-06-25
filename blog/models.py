from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, default=1, blank=True, null=True)
    title = models.CharField(max_length=200)
    text = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def comm_count(self):
        return Comment.objects.filter(answer_message=self).count()

    def comments(self):
        return Comment.objects.filter(answer_message=self)


class Comment(models.Model):
    date = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, default=1, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    answer_message = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    answer_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def approve(self):
        self.approved_comment = True
        self.save()

    def answer(self):
        return self.answer_comment and "ответ на комментарий" or "ответ на пост"

    def __str__(self):
        return str(self.id)


class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    def __str__(self):              # __unicode__ on Python 2
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self):              # __unicode__ on Python 2
        return self.name


class Entry(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    headline = models.CharField(max_length=255)
    body_text = models.TextField()
    pub_date = models.DateField()
    mod_date = models.DateField()
    authors = models.ManyToManyField(Author)
    n_comments = models.IntegerField()
    n_pingbacks = models.IntegerField()
    rating = models.IntegerField()

    def __str__(self):              # __unicode__ on Python 2
        return self.headline


def approved_comments(self):
    return self.comments.filter(approved_comment=True)
