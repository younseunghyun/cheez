from django.shortcuts import render
from django.http import HttpResponseNotFound
from django.contrib.auth.decorators import permission_required
from rest_framework.permissions import AllowAny
from posts.models import Post


# Create your views here.
def share_view(request, pk):
    try:
        post = Post.objects.get(id=pk)
    except:
        return HttpResponseNotFound()

    return render(request,
                  'post.html',
                  {
                      'post': post
                  })
