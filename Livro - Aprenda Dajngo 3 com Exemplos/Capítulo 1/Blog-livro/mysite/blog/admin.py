from django.contrib import admin
from blog.models import Post

# Registre seus modelos aqui.

"""
    Essa é a forma mais rápida de se registrar o modelo
    para o admin do django.
"""
#admin.site.register(Post) 

"""
    Essa é uma forma mais dinâmica de registrar o modelo,
    assim podemos fazer várias definições e alterações 
    usando um decorador, como um classe. 
"""
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug':('title',)}
    raw_id_fields = ('author', )
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')
