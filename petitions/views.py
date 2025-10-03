from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView
from .models import Petition, PetitionVote
from .forms import PetitionForm

class PetitionListView(ListView):
    model = Petition
    template_name = 'petitions/list.html'
    context_object_name = 'petitions'
    queryset = Petition.objects.filter(active=True).order_by('-created_at')

class PetitionCreateView(View):
    def get(self, request):
        form = PetitionForm()
        return render(request, 'petitions/create.html', {'form': form})
    
    def post(self, request, movie_id=None):
        form = PetitionForm(request.POST)
        if form.is_valid():
            pet = form.save(commit=False)
            # if a movie_id was provided via URL, associate it
            if movie_id and not pet.movie:
                from movies.models import Movie
                pet.movie = Movie.objects.filter(pk=movie_id).first()
            if request.user.is_authenticated:
                pet.created_by = request.user
            pet.save()
            return redirect('petitions:list')
        return render(request, 'petitions/create.html', {'form': form})
    
class PetitionDetailView(View):
    def get(self, request, pk):
        petition = get_object_or_404(Petition, pk=pk)
        return render(request, 'petitions/detail.html', {'petition': petition})
    
    def vote(self, request, pk):
        petition = get_object_or_404(Petition, pk=pk)
        # This method is not used directly by the URLconf; prefer module-level view below.
        # Keep it defensive in case it's called elsewhere.
        action = request.POST.get('action') or request.GET.get('action')
        value = 1 if action == 'up' else -1
        user = request.user if getattr(request, 'user', None) and request.user.is_authenticated else None
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        vote = None
        if user:
            vote = PetitionVote.objects.filter(petition=petition, user=user).first()
        else:
            vote = PetitionVote.objects.filter(petition=petition, session_key = session_key).first()
        
        if vote:
            if vote.value == value:
                vote.delete()
            else:
                vote.value = value
                vote.save()
        else:
            PetitionVote.objects.create(
                petition=petition,
                user=user,
                session_key=session_key if user is None else None,
                value=value
            )
        
        return redirect('petitions:detail', pk=petition.pk)


def vote(request, pk, action):
    """Module-level view used by URLs for voting.

    URL: /petitions/<pk>/vote/<action>/ where action is 'up' or 'down'
    """
    petition = get_object_or_404(Petition, pk=pk)
    value = 1 if action == 'up' else -1
    user = request.user if getattr(request, 'user', None) and request.user.is_authenticated else None
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    if user:
        vote_obj = PetitionVote.objects.filter(petition=petition, user=user).first()
    else:
        vote_obj = PetitionVote.objects.filter(petition=petition, session_key=session_key).first()

    if vote_obj:
        if vote_obj.value == value:
            vote_obj.delete()
        else:
            vote_obj.value = value
            vote_obj.save()
    else:
        PetitionVote.objects.create(
            petition=petition,
            user=user,
            session_key=(None if user else session_key),
            value=value,
        )

    return redirect('petitions:detail', pk=petition.pk)
