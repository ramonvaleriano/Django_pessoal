from django.db import models
from django.db.models.deletion import CASCADE
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager 

# Crie seus modelos aqui.

# Criando nosso próprio gerenciador de modelos.
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published') 

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Drafit'),
        ('published','Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')
    author = models.ForeignKey(User,
                               on_delete=CASCADE,
                               related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=250,
                              choices=STATUS_CHOICES,
                              default='draft')

    objects = models.Manager() # O gerenciado padrão
    published = PublishedManager() # O novo gerenciador que criamos

    tags = TaggableManager()

    class Meta:
        ordering = ('-publish',)
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                       self.publish.month,
                       self.publish.day, self.slug])

class Comment(models.Model):
    post = models.ForeignKey(Post, 
                             on_delete=CASCADE,
                             related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'Comentado por {self.name} no {self.post}'