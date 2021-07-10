from django.db import models
from django.db.models.deletion import CASCADE
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


# Crie seus modelos aqui.
# Criando um gerenciador de modelos
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


# Criando um modelo.
class Post(models.Model):
    STATUS_CHOSES = (
        ('draft', 'Draft'),
        ('published', 'Published'), 
    )

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOSES, default='draft')

    objects = models.Manager() # O gerencaidor Default
    published = PublishedManager() # O gerenciador personalizado. 

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    # Criando um urls canônicos
    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day, self.slug])
