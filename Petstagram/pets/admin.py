from django.contrib import admin
from Petstagram.common.models import Comment
from Petstagram.pets.models import Like, Pet


class LikeInline(admin.TabularInline):
    model = Like


class PetAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'name', 'age')
    list_filter = ('type', 'age')
    inlines = [
        LikeInline,
    ]


admin.site.register(Pet, PetAdmin)
admin.site.register(Like)
admin.site.register(Comment)
