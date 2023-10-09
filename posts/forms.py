from django import forms

from .models import Post, Comment, Category


class PostModelForm(forms.ModelForm):
    content = forms.CharField(label='', widget=forms.Textarea(attrs={'style': 'width: 100%;', 'rows': 2}))
    image = forms.ImageField(label='', required=False, widget=forms.FileInput(attrs={'style': 'display: none;'}))
    video = forms.FileField(label='', required=False, widget=forms.FileInput(attrs={'style': 'display: none;'}))
    category = forms.ModelChoiceField(label='', queryset=Category.objects.all(), required=True)

    class Meta:
        model = Post
        fields = ('content', 'image', 'video', 'category')


class CommentModelForm(forms.ModelForm):
    body = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Add a comment'}))
    class Meta:
        model = Comment
        fields = ('body',)


class PostUpdateForm(forms.ModelForm):
    image = forms.ImageField(label='', required=False, widget=forms.FileInput(attrs={'style': 'display: none;'}))
    video = forms.FileField(label='', required=False, widget=forms.FileInput(attrs={'style': 'display: none;'}))
    category = forms.ModelChoiceField(label='', queryset=Category.objects.all(), required=True)

    class Meta:
        model = Post
        widgets = {
            'content': forms.Textarea(attrs={'class': 'sn-field'}),
        }
        fields = ('content', 'image', 'video', 'category')