from django.forms import ModelForm, HiddenInput

from .models import PostComment


class PostCommentForm(ModelForm):
    class Meta:
        model = PostComment
        fields = ['name', 'email', 'comment', 'post']
        widgets = {'post': HiddenInput()}

    def __init__(self, *args, **kwargs):
        super(PostCommentForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'