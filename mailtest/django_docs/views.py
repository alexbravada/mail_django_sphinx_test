from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.shortcuts import redirect
import mimetypes
import os


@login_required
def unmatched(request):
    if (request.path.startswith('/ref/') or request.path.startswith('/_source/ref')) and not (request.user.is_superuser):
        return HttpResponseForbidden()
    file_name = os.path.basename(request.path)
    mimetype = mimetypes.guess_type(file_name)[0] or 'text/html'
    if request.path == '/':
        mimetype = 'text/html'
        file = open('_docs/index.html', 'rb')
    else:
        if not os.path.isfile('_docs' + request.path):
            return HttpResponseNotFound('<h1>Page not found</h1>')
        file = open('_docs' + request.path, 'rb')
    content_type = f'{mimetype}; charset=utf-8'
    return HttpResponse(file, content_type)


def sign_up(request):
    if request.method == 'POST':
      form = UserCreationForm(request.POST)
      if form.is_valid():
        form.save()
        return redirect('/')
    else:
      form = UserCreationForm()
    return render(request, 'registration/sign_up.html', {'form': form})


def signout(request):
    logout(request)
    return redirect('unmatched')

