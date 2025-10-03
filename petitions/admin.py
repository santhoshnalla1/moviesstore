from django.contrib import admin
from .models import Petition, PetitionVote

@admin.register(Petition)
class PetitionAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'created_at', 'active')
    search_fields = ('title',)
    



@admin.register(PetitionVote)
class PetitionVoteAdmin(admin.ModelAdmin):
    list_display = ('petition', 'user', 'session_key', 'value', 'created_at')
    list_filter = ('value',)
