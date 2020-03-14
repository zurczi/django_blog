from django.views import generic
from .models import Post, Comment
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse

from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.template.loader import get_template
from .forms import NewComment, ContactForm, PostForm
from django.views.generic.edit import FormMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404 
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from rest_framework import viewsets
from .serializers import PostSerializer, CommentSerializer

class PostList(generic.ListView):
    queryset = Post.objects.filter(status = 1).order_by('-created_on')
    template_name = 'index.html'

class UserPostList(generic.ListView):
   # queryset = Post.objects.filter(user = self.request.user).order_by('-created_on')
    template_name = 'user_post_list.html'
    def get_queryset(self):
        return Post.objects.filter(author=self.request.user).order_by('-created_on')

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_on')
    serializer_class = PostSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class PostUpdate(UpdateView):
    model = Post
    fields = ['title','content','status']
    template_name = "post_edit.html"


def post_detail(request, slug):
    post = Post.objects.get(slug=slug)
    if request.method == 'POST':
        form = NewComment(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.post = post
            instance.author = request.user
            instance.save()
    form = NewComment()
    comments = Comment.objects.filter(post=post)
    return render(request, 'post_detail.html', { 'post': post, 'comments': comments, 'form': form } )

@login_required(login_url="/accounts/login/")
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.slug = (form.cleaned_data['title']).lower().replace(" ","_")
            instance.save()
            return redirect('blog:list')
    else:
        form = PostForm()
    return render(request, 'post_create.html', {'form': form })

'''
class PostDetail(generic.DetailView, FormMixin):
    model = Post
    template_name = 'post_detail.html'
    form_class = forms.NewComment

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        context['form'] = forms.NewComment(initial={'post': self.object})
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            instance = form.save(commit=False)
            instance.post = post
            instance.author = request.user
            instance.save()
            

    def form_valid(self, form):
        form.save()
        return super(PostDetail, self).form_valid(form)
'''


def contact(request):
    form_class = ContactForm

    # new logic!
    if request.method == 'POST':
        form = form_class(data=request.POST)

        if form.is_valid():
            contact_name = request.POST.get(
                'contact_name'
            , '')
            contact_email = request.POST.get(
                'contact_email'
            , '')
            form_content = request.POST.get('content', '')

            # Email the profile with the
            # contact information
            template = get_template('contact_template.txt')
            context = {
                'contact_name': contact_name,
                'contact_email': contact_email,
                'form_content': form_content,
            }
            content = template.render(context)

            email = EmailMessage(
                "New contact form submission",
                content,
                "Your website" +'',
                ['youremail@gmail.com'],
                headers = {'Reply-To': contact_email }
            )
            email.send()
            return redirect('blog:success')

    return render(request, 'contact.html', {
        'form': form_class,
    })

def successView(request):
    return render(request, 'success.html')
    #return HttpResponse("Success! Thank you for your message.)

def about(request):
    return render(request, 'about_me.html')