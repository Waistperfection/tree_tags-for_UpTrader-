from django.shortcuts import render, get_object_or_404

from .models import MenuItem


def index(request, path):
    context = dict()
    context['path'] = path
    context['object'] = get_object_or_404(MenuItem, slug=context['path'].split('/')[-1])
    return render(request, 'menu/index.html', context)
