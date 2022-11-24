#from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import FormMixin
from django.urls import reverse

# Create your views here.

from .models import Post, PostCategory, PostTag
from .forms import PostCommentForm

from hitcount.views import HitCountDetailView

must_context = {
    'popular_posts': Post.get_popular_posts(),
    'categories': PostCategory.get_categories_inuse(),
    'tags': PostTag.get_tags_inuse(),
}

class PostListView(ListView):
    paginate_by = 5
    context_object_name = 'posts'
    queryset = Post.get_posts()
    template_name = 'blog/blog.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(must_context)
        return context


class PostDetailView(HitCountDetailView, FormMixin):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    slug_field = 'slug'
    count_hit = True
    form_class = PostCommentForm

    def get_success_url(self):
        return reverse('postdetail_view', kwargs={'slug': self.object.slug})

    def form_valid(self, form):
        form.save()
        return super(PostDetailView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context.update(must_context)
        context.update({'form': PostCommentForm(initial={'post': self.object})})
        context.update({'comments': self.object.get_comments()})
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            print('ffff')
            return self.form_valid(form)
        else:
            return self.form_invalid(form)