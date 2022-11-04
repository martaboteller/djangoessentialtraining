from django.http import Http404
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import NotesForm
from .models import Notes

class NotesDeleteView(LoginRequiredMixin,DeleteView):
    model = Notes
    success_url= "/smart/notes"
    template_name = "notes/notes_delete.html"
    login_url='/login'

class NotesUpdateView (LoginRequiredMixin,UpdateView):
    model = Notes
    success_url = '/smart/notes' #redirect user to the list
    form_class= NotesForm
    login_url='/login'

class NotesCreateView (LoginRequiredMixin,CreateView):
    model = Notes
    # fields = ['title', 'text'] #attributes we allow user to fill
    success_url = '/smart/notes' #redirect user to the list
    form_class= NotesForm
    login_url='/login'

    def form_valid(self,form):
        self.object = form.save(commit=False) #Does not commit save
        self.object.user = self.request.user #Insert user
        self.object.save() #Finally, save 
        return HttpResponseRedirect(self.get_success_url())


class NotesListView(LoginRequiredMixin,ListView):
    model = Notes
    context_object_name = 'notes' #default is objects
    template_name = "notes/notes_list.html"
    login_url="/login"
    #Display only the notes of the logged user
    def get_queryset(self):
        return self.request.user.notes.all()


class NotesDetailView (LoginRequiredMixin,DetailView):
     model = Notes
     context_object_name= "note"
     login_url='/login'
     #extra_content = "note"

# Create your views here.
# def list(request):
#     all_notes = Notes.objects.all()
#     return render (request, 'notes/notes_list.html',
#     {'notes': all_notes}
#     )

# def detail(request, pk):
#     try:
#         note = Notes.objects.get(pk=pk)
#     except Notes.DoesNotExist:
#         raise Http404('This note does not exist')
#     return render(request,'notes/notes_detail.html', {
#         'note':note
#     })