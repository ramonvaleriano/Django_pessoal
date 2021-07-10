from django.core import paginator
from django.shortcuts import render, get_object_or_404
from django.core.paginator import  Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from blog.models import Post
from blog.forms import EmailPostForm


# Crie suas views aqui.
"""def post_list(request):
    
        Função para recebe apenas a requisão via path. Essa view é responsábel por mostrar todos os deados que tiverem com o status de published.
    
    posts = Post.published.all()
    return render(request, 'blog/post/list.html', {'posts':posts})"""

"""def post_list(request):
    object_list = Post.published.all()
    paginator = Paginator(object_list, 3) # Três publicações por página
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # Se a página não foi um número inteiro, exibir a primeira página
        posts = paginator.page(1)
    except EmptyPage:
        # Se a página estiver fora do intervalo, 
        # exibir a última página de resultados. 
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'page':page, 'posts':posts})"""

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'

def post_detail(request, year, month, day, post):
    """
        View responsável por mostrar um dado de forma individual, uma postagem por vez.
        recebe por parâmetro os seguintes aspécitos via path, request, a própria requsição, o ano, o mês, e o dia, todos em valor inteior. Por fim a variável post. 
    """
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request, 'blog/post/detail.html', {'post':post})

def post_share(request, post_id):
    # Obter a postagem com base no id
    post = get_object_or_404(Post, id=post_idm, status='published')

    if request.method == 'POST':
        # Formulário foi submetido
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Campos do formulário passaram pela validação
            cd = form.cleaned_data
            # Envio do e-mail
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post':post}, {'form':form})
    