from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from forms import PageForm
from models import Page

from django.contrib.auth.decorators import login_required
from django.contrib import messages


def index(request):
    """Lists all pages stored in the wiki."""
    context = {
        'pages': Page.objects.all(),
    }

    return render_to_response('wiki/index.html',
        RequestContext(request, context))


def view(request, name):
    """Shows a single wiki page."""
    try:
        page = Page.objects.get(name=name)
    except Page.DoesNotExist:
        page = Page(name=name)

    pages = Page.objects.filter(listed=True)
    op = []

    if page.id:
        if page.translation_of:
            op.extend([page.translation_of, ])
        op.extend(list(page.page_set.all()))

    context = {
        'page': page,
        'pages': pages,
        'other_pages': op
    }

    return render_to_response('wiki/view.html',
        RequestContext(request, context))


@login_required
def edit(request, name):
    try:
        page = Page.objects.get(name=name)
    except Page.DoesNotExist:
        page = None

    if request.method == 'POST':
        form = PageForm(request.POST, instance=page)
        if form.is_valid():
            page = form.save()
            page.contributors.add(request.user)
            messages.add_message(request, messages.SUCCESS,
                'Successfully updated \'%s\' page' % page.name)
            return redirect(view, name=page.name)
    else:
        if page:
            form = PageForm(instance=page)
        else:
            form = PageForm(initial={'name': name})

    return render_to_response('wiki/edit.html',
        RequestContext(request, {'form': form}))


"""
@login_required
def edit(request, name):
    # Allows users to edit wiki pages.
    try:
        page = Page.objects.get(name=name)
    except Page.DoesNotExist:
        page = None

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if not page:
                page = Page()

            page.name = form.cleaned_data['name']
            page.content = form.cleaned_data['content']
            page.rendered = form.cleaned_data['content']

            page.save()
            page.contributors.add(request.user)
            return redirect(view, name=page.name)
    else:
        if page:
            form = PageForm(initial=page.__dict__)
        else:
            form = PageForm(initial={'name': name})

    context = {
        'form': form,
    }

    return render_to_response('wiki/edit.html',
        RequestContext(request, context))
"""