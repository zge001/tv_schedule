from tv_programs.models import TVChannel, TVProgram
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
import datetime
from dal import autocomplete
from .forms import TVChannelForm, TVProgramForm

# Create your views here.
def check_admin(user):
    return user.is_superuser

def tv_schedule(request):
    channels = TVChannel.objects.all().order_by("-priority") # descending order because highest priority channels display first
    now = datetime.datetime.now()
    programs = TVProgram.objects.filter(date__date=datetime.date.today()).order_by("date")
    return render(request, 'tv_programs/channel_list.html', {'channels': channels, 'programs': programs})

def channel_schedule(request, id):
    channel = TVChannel.objects.get(id=id)
    
    grouped_programs = {}

    programs = TVProgram.objects.filter(tv_channel=channel).order_by("date")
    for program in programs:
        date = datetime.date(program.date.year, program.date.month, program.date.day)
        if date not in grouped_programs:
            grouped_programs[date] = []
        grouped_programs[date].append(program)

    grouped_programs_list = sorted(grouped_programs.items())
    return render(request, 'tv_programs/channel_schedule.html', {'channel': channel, 'channel_programs': grouped_programs_list})

class TVChannelAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        tv_channels = TVChannel.objects.all()
        if self.q:
            tv_channels = tv_channels.filter(name__istartswith=self.q)
        return tv_channels

@user_passes_test(check_admin)
def tv_program_create(request, id=None):
    if request.method == 'POST':
        form = TVProgramForm(request.POST, request.FILES)
        if form.is_valid():
            tv_program = form.save()
            messages.success(request, 'Телепрограмма добавлена')
            return redirect('tv:tv_schedule')
    else:
        tv_channel = TVChannel.objects.filter(id=id).first()
        form = TVProgramForm(initial={"tv_channel": tv_channel})
    return render(request, 'tv_programs/tv_program/create.html', {'form': form})

@user_passes_test(check_admin)
def tv_program_update(request, id):
    tv_program = get_object_or_404(TVProgram, id=id)
    if request.method == 'POST':
        form = TVProgramForm(request.POST, request.FILES, instance=tv_program)
        if form.is_valid():
            form.save()
            messages.success(request, 'Телепрограмма изменена')
            return redirect(f'tv:tv_schedule')
    else:
        form = TVProgramForm(instance=tv_program, initial={"date": tv_program.date})
    return render(request, 'tv_programs/tv_program/update.html',
                  {'form': form})

@user_passes_test(check_admin)
def tv_program_delete(request, id):
    tv_program = get_object_or_404(TVProgram, id=id)
    if request.method == 'POST':
        tv_program.delete()
        messages.success(request, 'Телепрограмма удалена')
        return redirect('tv:tv_schedule')
    return render(request, 'tv_programs/tv_program/delete.html',
                  {'tv_program': tv_program})

@user_passes_test(check_admin)
def tv_channel_create(request):
    if request.method == 'POST':
        form = TVChannelForm(request.POST, request.FILES)
        if form.is_valid():
            tv_channel = form.save()
            messages.success(request, 'Телеканал добавлен')
            return redirect('tv:tv_schedule')
    else:
        form = TVChannelForm()
    return render(request, 'tv_programs/tv_channel/create.html', {'form': form})

@user_passes_test(check_admin)
def tv_channel_update(request, id):
    tv_channel = get_object_or_404(TVChannel, id=id)
    if request.method == 'POST':
        form = TVChannelForm(request.POST, request.FILES, instance=tv_channel)
        if form.is_valid():
            form.save()
            messages.success(request, 'Телеканал изменён')
            return redirect(f'tv:tv_schedule', id=tv_channel.id)
    else:
        form = TVChannelForm(instance=tv_channel)
    return render(request, 'tv_programs/tv_channel/update.html',
                  {'form': form})

@user_passes_test(check_admin)
def tv_channel_delete(request, id):
    tv_channel = get_object_or_404(TVChannel, id=id)
    if request.method == 'POST':
        tv_channel.delete()
        messages.success(request, 'Телеканал удалён')
        return redirect('tv:tv_schedule')
    return render(request, 'tv_programs/tv_channel/delete.html',
                  {'tv_channel': tv_channel})

# @user_passes_test(check_admin)
# def tvprogram_update(request, id):
#     film = get_object_or_404(Film, id=id)
#     if request.method == 'POST':
#         form = FilmForm(request.POST, request.FILES, instance=film)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Фильм изменён')
#             return redirect('films:film_detail', id=film.id)
#     else:
#         form = FilmForm(instance=film)
#     return render(request, 'films/film/update.html',
#                   {'form': form})

