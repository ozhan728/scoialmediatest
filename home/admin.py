from django.contrib import admin
from .models import Post
# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user','slug','created','updated')
    search_fields = ('slug','body','user')
    list_filter = ('created','updated','user')
    prepopulated_fields = {'slug':('body',)}
    raw_id_fields = ('user',)


# admin.site.register(Post)
