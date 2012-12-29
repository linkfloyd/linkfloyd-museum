# Create your views here.
from links.models import Link
from comments.models import Comment
from comments.forms import CommentForm
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect


def submit(request):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.posted_by = request.user
            comment.save()
            return HttpResponseRedirect("%s#%s" % (
                comment.link.get_absolute_url(), comment.id))
        else:
            print form.errors
    link_id = request.POST.get("link", False)
    if link_id:
        link = Link.objects.get(id=link_id)
        return HttpResponseRedirect(link.get_absolute_url())

    return HttpResponseRedirect("/")


def update(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("%s#%s" % (
                comment.link.get_absolute_url(), comment.id))
        else:
            print form.errors
