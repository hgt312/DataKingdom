from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponseRedirect

from .models import Competition, AttendedPerson
from utils.mixin_utils import LoginRequiredMixin


class AllCompetitionsView(View):
    def get(self, request):
        all_competitions = Competition.objects.all()
        return render(request, "all-competitions.html", {"all_competitions": all_competitions})


class CompetitionView(LoginRequiredMixin, View):
    def get(self, request, competition_id):
        is_attended = False
        competition = Competition.objects.get(id=competition_id)
        attended_person = AttendedPerson.objects.filter(person=request.user, competition=competition)
        if attended_person.count() > 0:
            is_attended = True
        return render(request, "competition.html", {"competition": competition, "is_attended": is_attended})


class AttendedView(LoginRequiredMixin, View):
    def post(self, request, competition_id):
        attended_person = AttendedPerson()
        competition = Competition.objects.get(id=competition_id)
        attended_person.person = request.user
        attended_person.competition = competition
        attended_person.save()
        return HttpResponseRedirect('/user/attend/')
