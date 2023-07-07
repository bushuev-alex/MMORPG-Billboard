from django.contrib import admin
from board.models import *
# from modeltranslation.admin import TranslationAdmin
from django_summernote.admin import SummernoteModelAdmin


admin.site.register(Category)
# admin.site.register(Advertisement)
admin.site.register(AdvertisementCategory)
admin.site.register(Author)
admin.site.register(Feedback)


# creating admin class
class blogadmin(SummernoteModelAdmin):
    # displaying posts with title slug and created time
    list_display = ('author', 'date_time', 'title', 'text')
    list_filter = ("author", )
    search_fields = ['title', 'text']
    # prepopulating slug from title
    summernote_fields = ('text', )


admin.site.register(Advertisement, blogadmin)
