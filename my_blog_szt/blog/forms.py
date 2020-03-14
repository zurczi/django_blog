from django import forms
from .models import Post, Comment

class ContactForm(forms.Form):
    contact_name = forms.CharField(required=True)
    contact_email = forms.EmailField(required=True)
    content = forms.CharField(
        required=True,
        widget=forms.Textarea
    )

    # the new bit we're adding
    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['contact_name'].label = "Your name:"
        self.fields['contact_email'].label = "Your email:"
        self.fields['content'].label = "What do you want to say?"

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title','content','status']

class NewComment(forms.ModelForm):
    def __init__( self, *args, **kwargs ):
        super(NewComment, self).__init__( *args, **kwargs )
        self.fields['content'].label = ''

    class Meta:
        model = Comment
        fields = ['content',]