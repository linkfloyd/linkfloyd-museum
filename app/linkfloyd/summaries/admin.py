from django.contrib import admin
from summaries.models import Unseen

class UnseenAdmin(admin.ModelAdmin):
    list_display = ("user", "link")

admin.site.register(Unseen, UnseenAdmin)
