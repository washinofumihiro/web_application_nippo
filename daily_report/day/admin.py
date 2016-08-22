from django.contrib import admin
from .models import Book, Impression
from django.contrib.auth import get_user
# admin.site.register(Book)
# admin.site.register(Impression)


class BookAdmin(admin.ModelAdmin):
    # list_display = ('id', 'date', 'title', 'user',)  # 一覧に出したい項目
    # # list_display = ('id', 'name', 'publisher',)  # 一覧に出したい項目
    # list_display_links = ('id', 'name',)  # 修正リンクでクリックできる項目
    #
    list_display = ('id', 'title', 'content', 'user',)  # 一覧に出したい項目
    # list_display = ('id', 'name', 'publisher',)  # 一覧に出したい項目
    list_display_links = ('id', 'title',)  # 修正リンクでクリックできる項目
admin.site.register(Book, BookAdmin)


class ImpressionAdmin(admin.ModelAdmin):
    list_display = ('id', 'comment',)
    list_display_links = ('id', 'comment',)
admin.site.register(Impression, ImpressionAdmin)

# from django.contrib import admin
# from day.models import Book, Impression
#
# admin.site.register(Book)
# admin.site.register(Impression)


