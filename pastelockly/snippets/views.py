from django.shortcuts import render, get_object_or_404
from .models import Snippet
from .forms import SnippetForm
from django.http import Http404
import random
import string
from cryptography.fernet import Fernet, InvalidToken

def generate_snippet_id():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))

def encrypt_content(content, key):
    if key:
        fernet_key = Fernet.generate_key()
        fernet = Fernet(fernet_key)
        encrypted_content = fernet.encrypt(content.encode()).decode()
        return encrypted_content, fernet_key.decode()
    return content, None

def create_snippet(request):
    if request.method == 'POST':
        form = SnippetForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            key = form.cleaned_data['key']
            snippet_id = generate_snippet_id()
            encrypted_content, fernet_key = encrypt_content(content, key)
            snippet = Snippet(content=encrypted_content, key=fernet_key, snippet_id=snippet_id)
            snippet.save()
            return render(request, 'snippets/snippet_created.html', {'snippet_id': snippet_id})
    else:
        form = SnippetForm()
    return render(request, 'snippets/index.html', {'form': form})

def decrypt_content(encrypted_content, fernet_key, key):
    if fernet_key:
        try:
            fernet = Fernet(fernet_key.encode())
            decrypted_content = fernet.decrypt(encrypted_content.encode()).decode()
            return decrypted_content
        except InvalidToken:
            raise Http404("Invalid secret key")
    return encrypted_content

def view_snippet(request, snippet_id):
    snippet = get_object_or_404(Snippet, snippet_id=snippet_id)
    decrypted_content = snippet.content
    if snippet.key:
        if request.method == 'POST':
            key = request.POST.get('key', '')
            decrypted_content = decrypt_content(snippet.content, snippet.key, key)
        else:
            return render(request, 'snippets/enter_key.html', {'snippet_id': snippet_id})
    return render(request, 'snippets/view_snippet.html', {'content': decrypted_content})
