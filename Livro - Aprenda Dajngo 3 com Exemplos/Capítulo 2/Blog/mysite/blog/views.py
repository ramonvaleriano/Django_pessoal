from django.core import paginator
from django.shortcuts import render, get_object_or_404
from django.core.paginator import  Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from blog.models import Post, Comment
from blog.forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count

# Crie suas views aqui.
"""def post_list(request):
    
        Função para recebe apenas a requisão via path. Essa view é responsábel por mostrar todos os deados que tiverem com o status de published.
    
    posts = Post.published.all()
    return render(request, 'blog/post/list.html', {'posts':posts})"""

def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

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
    return render(request, 'blog/post/list.html', {'page':page, 
                                                   'posts':posts,
                                                   'tag':tag})

"""class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'"""

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

    # Lista dos comentários ativos para esta postagem
    comments = post.comments.filter(active=True)

    new_comment = None

    if request.method == 'POST':
        # Um comentário foi postado
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Cria o objeto Comment, mas não o salva ainda no banco de dados
            new_comment = comment_form.save(commit=False)
            # Atribua a postagem atual ao comentário
            new_comment.post = post
            # Salva o comentário no banco de dados
            new_comment.save()
    else:
        comment_form = CommentForm()

    # lista de postagens Semeslhantes
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]

    return render(request, 'blog/post/detail.html', {'post':post,
                                                     'comments':comments,
                                                     'comment_form':comment_form,
                                                     'new_comment':new_comment,
                                                     'smilar_posts':similar_posts})

def post_share(request, post_id):
    # Obter a postagem com base no id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        # Formulário foi submetido
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Campos do formulário passaram pela validação
            cd = form.cleaned_data # Todos os dados no formato de dicionário
            post_url =  request.build_absolute_uri(post.get_absolute_url())
            subject = f'{cd["name"]} Recomenda você ler {post.title}'
            message = f'Leia {post.title} at {post_url}\n\n {cd["name"]}\'s Comentários: {cd["comments"]}'
            send_mail(subject, message, 'desenvolvedorvaleriano@gmail.com', [cd['to']])
            sent=True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post':post, 
                                                    'form':form,
                                                    'sent':sent})
    