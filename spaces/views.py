from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from .forms import PostForm
from .models import Post


# index = ListView.as_view(model=Post)

from django.http import HttpResponse
def index(request):
    return HttpResponse('Hello World 2')


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('spaces:index')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, '포스팅을 저장했습니다.')
        return response

post_new = PostCreateView.as_view()

