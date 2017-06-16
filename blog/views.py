from __future__ import unicode_literals

from django.shortcuts import render
from django.utils import timezone
from .models import Post
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from django.shortcuts import redirect
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.core.mail import EmailMessage

from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import DetailView, TemplateView
from hitcount.views import HitCountDetailView


# Create your views here.
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


def email_two(request):
    subject = "I am an HTML email"
    to = ['adric.warth@jisc.ac.uk']
    from_email = 'sebastian_cheung@yahoo.com'

    ctx = {
        'user': 'buddy',
        'purchase': 'Books'
    }

    message = get_template('blog/email.html').render(Context(ctx))
    msg = EmailMessage(subject, message, to=to, from_email=from_email)
    msg.content_subtype = 'html'
    msg.send()

    return HttpResponse('email_sent')


class PostMixinDetailView(object):
    """
    Mixin to same us some typing.  Adds context for us!
    """
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostMixinDetailView, self).get_context_data(**kwargs)
        context['post_list'] = Post.objects.all()[:5]
        context['post_views'] = ["ajax", "detail", "detail-with-count"]
        return context


class IndexView(PostMixinDetailView, TemplateView):
    template_name = 'blog/post_list.html'


class PostDetailJSONView(PostMixinDetailView, DetailView):
    template_name = 'blog/post_list.html'

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(PostDetailJSONView, cls).as_view(**initkwargs)
        return ensure_csrf_cookie(view)


class PostDetailView(PostMixinDetailView, HitCountDetailView):
    """
    Generic hitcount class based view.
    """
    pass


class PostCountHitDetailView(PostMixinDetailView, HitCountDetailView):
    """
    Generic hitcount class based view that will also perform the hitcount logic.
    """
    count_hit = True
