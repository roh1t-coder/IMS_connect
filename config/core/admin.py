from django.contrib import admin
from .models import User, Employee, Idea, Vote, Collaboration, Reward

class IdeaAdmin(admin.ModelAdmin):
    list_display = ('title', 'employee', 'status', 'submission_date')
    list_filter = ('status', 'submission_date')
    search_fields = ('title', 'description')
    ordering = ('submission_date',)
    fields = ('title', 'description', 'status', 'employee')

admin.site.register(User)
admin.site.register(Employee)
admin.site.register(Idea, IdeaAdmin)
admin.site.register(Vote)
admin.site.register(Collaboration)
admin.site.register(Reward)