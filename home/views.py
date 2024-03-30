from django.shortcuts import render , redirect
from django.views import View
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
# Create your views here.

# def home(request) :
#     return render(request,'home/index.html')

class HomeView(View) :

    def get(self,request):
        post = Post.objects.all()
        return render(request,'home/index.html',{'posts':post})


class PostDetailView(View) :
    def get(self,request,post_id,post_slug):
        post = Post.objects.get(pk=post_id,slug=post_slug)
        return render(request,'home/detail.html',{'post':post})


class PostDeleteView( LoginRequiredMixin ,View):
    def get(self,request,post_id):
        post = Post.objects.get(pk=post_id)
        if post.user.id == request.user.id :
            post.delete()
            messages.success(request,'Post Deleted Successfully','success')
        else :
            messages.error(request,'you cant delete this post ','danger')

        return redirect('home:home')
