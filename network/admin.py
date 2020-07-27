from django.contrib import admin
from .models import Post, User
# Register your models here.
class MyModelAdmin(admin.ModelAdmin):
    readonly_fields = ["timestamp"]


admin.site.register(Post, MyModelAdmin)
admin.site.register(User)