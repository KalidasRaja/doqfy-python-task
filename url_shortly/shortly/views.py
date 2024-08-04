from django.shortcuts import render, redirect, get_object_or_404
from .models import URL
from .forms import URLForm
import string
import random

def generate_short_code():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(6))

def create_short_url(request):
    if request.method == 'POST':
        form = URLForm(request.POST)
        if form.is_valid():
            original_url = form.cleaned_data['url']
            short_code = generate_short_code()
            while URL.objects.filter(short_code=short_code).exists():
                short_code = generate_short_code()
            url = URL(original_url=original_url, short_code=short_code)
            url.save()
            return render(request, 'shortly/url_created.html', {'short_code': short_code})
    else:
        form = URLForm()
    return render(request, 'shortly/index.html', {'form': form})

def redirect_to_url(request, short_code):
    url = get_object_or_404(URL, short_code=short_code)
    return redirect(url.original_url)
