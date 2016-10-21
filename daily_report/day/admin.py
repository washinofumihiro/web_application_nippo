# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Report, Comment
from django.contrib.auth import get_user
# admin.site.register(Report)
# admin.site.register(Comment)


class ReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content_Y', 'user',)
    list_display_links = ('id', 'title',) 
admin.site.register(Report, ReportAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'comment',)
    list_display_links = ('id', 'comment',)
admin.site.register(Comment, CommentAdmin)
