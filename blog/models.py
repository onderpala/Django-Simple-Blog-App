from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericRelation
from django.core.files.uploadedfile import InMemoryUploadedFile

from ckeditor_uploader.fields import RichTextUploadingField
from hitcount.models import HitCount
from io import BytesIO
from PIL import Image
from sys import getsizeof

# Create your models here.

class PostTag(models.Model):
    label = models.CharField(max_length=50)
    active = models.BooleanField(default=True, blank=True)

    def __str__(self):
        return self.label
    
    def get_tags_inuse():
        tags = PostTag.objects.filter(post__isnull=False).distinct()
        return tags

class PostCategory(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Categories'

    def get_categories_inuse():
        categories = list(PostCategory.objects.filter(post__isnull=False))
        result = {i: categories.count(i) for i in categories}
        # result example: {<PostCategory: Fashion>: 3, <PostCategory: Luxury>: 1}
        return result

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ManyToManyField(PostCategory)
    thumbnail = models.ImageField(upload_to='post-thumbnails/')
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, blank=True)
    tag = models.ManyToManyField(PostTag)
    content = RichTextUploadingField()
    summary = models.CharField(max_length=100)
    active = models.BooleanField(default=False, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    hitcount_generic = GenericRelation(HitCount, object_id_field='object_pk', related_query_name='hitcount_generic_relation')

    def __str__(self):
        return self.title

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._original_thumbnail = self.thumbnail

    def get_absolute_url(self):
        return reverse('postdetail_view', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['-created']

    def get_popular_posts(amount=3):
        return Post.objects.filter(active=True).order_by('-hitcount_generic')[:amount]

    def get_posts(start=0, finish=5):
        return Post.objects.filter(active=True).order_by('-created')[start:finish].defer(
            'author',
            'tag',
            'content',
            'active',
            'hitcount_generic'
        )
    
    def get_comments(self):
        return self.postcomment_set.all().filter(active=True)

    def save(self, *args, **kwargs):
        # Convert thumbnail to webp format
        if self.thumbnail != self._original_thumbnail:
            img = Image.open(self.thumbnail).convert('RGB')
            output = BytesIO()
            img.save(output, format='webp', optimize=True, quality=95)
            output.seek(0)
            self.thumbnail = InMemoryUploadedFile(
                output,
                'ImageField',
                '%s.webp' % self.thumbnail.name.split('.')[0],
                'image/webp',
                getsizeof(output),
                None
            )

        # Slugify
        if not self.slug:
            self.slug = slugify(self.title)
        
        return super().save(*args, **kwargs)

class PostComment(models.Model):
    name = models.CharField(max_length=49)
    email = models.EmailField()
    comment = models.TextField(max_length=366)
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False, null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.name + ' - ' + self.email