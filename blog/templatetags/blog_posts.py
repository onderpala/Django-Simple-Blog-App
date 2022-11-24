from django import template

from blog.models import Post

register = template.Library()



@register.simple_tag
def RecentPosts():
    posts = Post.get_posts(0, 3)
    return posts