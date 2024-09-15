from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm,UserDetailForm,ProfileChangeForm,PostForm,CommentForm,UpdateForm
from django.http import HttpRequest, HttpResponseForbidden,HttpResponse
from django.contrib.auth.views import LoginView,LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .models import UserProfile,Post,Comment
from django.views.generic import ListView,CreateView,DeleteView,UpdateView,DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import ValidationError
from django.template.defaultfilters import slugify
from django.db.models import Count
from taggit.models import Tag
from django.db.models import Q
def search(request):
    posts = Post.objects.all()
    common_tags = Tag.objects.annotate(num_posts=Count('post')).order_by('-num_posts')[:4]
    if request.method == "GET":
        
        query = request.GET.get('q', '')
        queryset = posts.filter(Q(title__icontains=query) | Q(content__icontains=query)|Q(tags__name__icontains=query)).distinct()
        total = queryset.count()
        return render(request, 'blog/search_results.html', {'posts': queryset,'query':query,"total":total,"common_tags":common_tags})
# Create your views here.
# def post_tags(request):
#     posts = Post.objects.all().order_by('-title')
#     # common_tags = Tag.objects.annotate(num_posts=Count('post')).order_by('-num_posts')[:4]
#     common_tags = Post.tags.most_common()[:4]
#     context = {
#         "posts":posts,
#         "common_tags":common_tags
#     }
#     return render(request,'blog/tags.html',context)
def tagged(request,slug):
    tag = get_object_or_404(Tag,slug=slug)
    posts = Post.objects.filter(tags=tag)
    context = {
        "posts":posts,
        "tags":tag
    }
    return render(request,'blog/tagged_posts.html',context)
class PostByTagListView(ListView):
    template_name = 'blog/tagged_by_posts.html'
    model = Post
    context_object_name = 'posts'
    def get_queryset(self):
        tag_slug = self.kwargs.get('tag_slug') #get slug from url
        posts = Post.objects.filter(tags__slug=tag_slug) #get posts associated with that tag_slug
        return posts
    
    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        tag_slug = self.kwargs.get('tag_slug') #get slug with the url
        context["tag"] = Tag.objects.get(slug=tag_slug)  #use the slug to pull the tag with that slug and pass it the context data from the queryset
        return context
    
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('profile')
        else:
            return HttpResponseForbidden("Form data incorrect")
    else:
        form = CustomUserCreationForm()
    context = {"form":form}
    return render(request,'blog/register.html',context)
def home(request):
    context = {}
    return render(request,'blog/home.html',context)
class LoginUser(LoginView):
    template_name = 'blog/login.html'
class LogoutUser(LogoutView):
    template_name = 'blog/logout.html'
@login_required(login_url='login')
def profileview(request):
    try:
        user_profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user)
    if request.method == 'POST':
        user_update_form = UserDetailForm(request.POST,instance=request.user)
        profile_update_form = ProfileChangeForm(request.POST,instance=user_profile)
        if user_update_form.is_valid() and profile_update_form.is_valid():
            user_update_form.save()
            profile_update_form.save()
            return redirect('profile')
        else:
            return HttpResponseForbidden("Incorrect form format")
    else:
        user_update_form = UserDetailForm(instance=request.user)
        profile_update_form = ProfileChangeForm(instance=user_profile)
    context = {"user_update_form":user_update_form,"profile_update_form":profile_update_form}
    return render(request,'blog/profile.html',context)
# In this list view, the focus is on implement a view that allows all users to see all the posts\
            # The use of the loginmixin is to ensure only logged in users are allowed\
                # The login_url is placed on the settings.py
class ListPostView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    
    def get_queryset(self):
        all_posts = Post.objects.all()
        query = self.request.GET.get('q','').strip() 
        if query:
            posts = all_posts.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(tags__name__icontains=query)
            ).distinct()
            
        else:
            posts = Post.objects.all().order_by('-title')
        self.total = posts.count()
        # return Post.objects.all()
        return posts
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # common_tags = common_tags = Post.tags.most_common()[:4]
        common_tags= Tag.objects.annotate(num_posts=Count('post')).order_by('-num_posts')[:4]
        context["common_tags"] = common_tags
        context["total"] = self.total
        return context
    
# In this detail view, the focus is on implement a view that makes use of the specific post pk\
        # use of the detail operation to view details of a single post with a specific id\
            # The use of the loginmixin is to ensure only logged in users are allowed\
                # The login_url is placed on the settings.py    
class DetailPostView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    # def get_queryset(self):
    #     return Post.objects.all()
    # def get_queryset(self):
    #     post = self.get_object()
    #     comments = Comment.objects.filter(post=post)
    #     return comments
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context["post"] = self.get_object()
        context["comments"] = Comment.objects.filter(post=post)
        return context
    
 # In this create view, the focus is on implement a view that makes\
        # use of the create operation to create a post\
            # The use of the loginmixin is to ensure only logged in users are allowed\
                # The login_url is placed on the settings.py   
class CreatePostView(LoginRequiredMixin, CreateView):
    template_name = 'blog/post_form.html'
    model = Post
    form_class = PostForm
    def form_valid(self, form):
        if form.is_valid():
            posts = form.save(commit=False)
            posts.author = self.request.user
            posts.slug = slugify(posts.title)
            posts.save()
            form.save_m2m()
            return redirect('post_list')
        return super().form_valid(form)
    # In this delete view, the focus is on implement a view that makes\
        # use of the delete operation to delete a post with a specific id
class DeletePostView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post_list')
    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user
# In this update view, the focus is on implement a view that makes\
        # use of the update operation to update a post with a specific id\
            # The use of the loginmixin is to ensure only logged in users are allowed\
                # The login_url is placed on the settings.py
    

class UpdatePostView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/edit_post.html'
    def form_valid(self, form):
        if form.is_valid():
            post = form.save(commit=False)
            post.author = self.request.user
            post.save()
            
        return super().form_valid(form)
    success_url = reverse_lazy('post_list')
    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user
    
#create a createview allowing users to create comments. ensure authenticated users can create comments
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'
    def form_valid(self, form: CommentForm):
        if form.is_valid():
            post = Post.objects.get(pk=self.kwargs['pk'])
            comment = form.save(commit=False)
            comment.author = self.request.user
            comment.post = post
            comment.save()
            return super().form_valid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post"] = Post.objects.get(pk=self.kwargs['pk'])
        
        return context
    
    def get_success_url(self):
        return reverse_lazy('post_detail',kwargs={'pk':self.kwargs['pk']})
class ListComment(LoginRequiredMixin, ListView):
    model = Comment
    template_name = 'blog/comment_list.html'
    # def get_queryset(self):
    #     return Comment.objects.all()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = Post.objects.get(pk=self.kwargs['post_id'])
        context["post"] = post
        context["comments"] = Comment.objects.filter(post=post)
        return context
    
"""class UpdateComment(UpdateView):
    model = Comment
    template = 'blog/edit_comment.html'
    form_class = UpdateForm
    def get_object(self, queryset=None):
        return Comment.objects.get(pk=self.kwargs['comment_pk'])
    def get_success_url(self):
        comment = self.get_object()
        return reverse_lazy('post_detail',kwargs={'pk': comment.post.pk})
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['post_id'] = self.get_object().post.pk
    #     return context
    def form_valid(self, form):
        if form.is_valid():
            comment = self.get_object()
            comment = form.save(commit=False)
            form.instance.author = self.request.user
            comment.post = comment.post
            # comment.post= Post.objects.get(pk=self.kwargs['post_id'])
            comment.save()
        return super().form_valid(form)"""

class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'blog/delete_comment.html'
    def get_success_url(self):
        comment = self.get_object()
        return reverse_lazy('post_detail', kwargs={'pk': comment.post.pk})
class CommentDetail(LoginRequiredMixin, DetailView):
    model = Comment
    template_name = 'blog/comment_detail.html'
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        comment = self.get_object()
        context["comment"] = comment
        context["post"] = comment.post
        return context
# opted for a function view instead. The update view created some conflicts\
    # I was unable to resolve. It kept getting redirected to create comment
@login_required(login_url='login')
def CommentUpdateView(request,pk):
    comment = Comment.objects.get(pk=pk)
    post = Post.objects.get(pk=comment.post.pk)
    print(f"Comment content: {comment.content}")
    if request.method == 'POST':
        form = UpdateForm(request.POST, instance=comment)
        if form.is_valid():
            if len(form.data['content'])<10:
                raise ValidationError("The comment is too short")
            else:
                form.save()
            return redirect('comment_list', post_id=post.pk)
        
    else:
        form = UpdateForm(instance=comment)
    context = {"form":form,"comment":comment}
    return render(request,'blog/edit_comment.html',context)


# class PostByTagListView(ListView):
#     model = Post
#     template_name = 'blog/search_results.html'
    
#     def get_queryset(self):
#         all_posts = Post.objects.all()
#         query = self.request.GET.get('q','').strip() 
#         if query:
#             posts = all_posts.filter(
#                 Q(title__icontains=query) |
#                 Q(content__icontains=query) |
#                 Q(tags__name__icontains=query)
#             ).distinct()
            
#         else:
#             posts = Post.objects.all().order_by('-title')
#         self.total = posts.count()
#         # return Post.objects.all()
#         return posts
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # common_tags = common_tags = Post.tags.most_common()[:4]
#         common_tags= Tag.objects.annotate(num_posts=Count('post')).order_by('-num_posts')[:4]
#         context["common_tags"] = common_tags
#         context["total"] = self.total
#         return context
