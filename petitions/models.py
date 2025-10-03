from django.db import models
from django.contrib.auth import get_user_model
from movies.models import Movie

User = get_user_model()

class Petition(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    movie = models.ForeignKey(Movie, on_delete=models.SET_NULL, null=True, blank=True, help_text='Optional: which movie this petition is about')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def upvotes(self):
        return self.votes.filter(value=1).count()
    
    def downvotes(self):
        return self.votes.filter(value=-1).count()
    def score(self):
        return self.upvotes() - self.downvotes()
    def __str__(self):
        return self.title
    
class PetitionVote(models.Model):
    petition = models.ForeignKey(Petition, related_name='votes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=50, null=True, blank=True)
    value = models.SmallIntegerField(choices=((1, 'Upvote'), (-1, 'Downvote')))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('petition', 'user'), ('petition', 'session_key'))

    def __str__(self):
        who = self.user.username if self.user else f'session: {self.session_key}'
        return f"{who} --> {self.petition.title} ({self.value})"

