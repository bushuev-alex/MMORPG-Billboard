from django.contrib import admin
from board.models import *
# from modeltranslation.admin import TranslationAdmin


admin.site.register(Category)
admin.site.register(Advertisement)
admin.site.register(AdvertisementCategory)
admin.site.register(Author)
admin.site.register(Feedback)
