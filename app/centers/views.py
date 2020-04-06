from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView

from centers.models import BiWeeklyClass, LearningCenter
from core_hr.extras.dummy import get_dummy_user


def home(request):
    return HttpResponse('<h3>Centers Home Page Under Construction</h3>')

#
# class CentersHomePageView(TemplateView):
#


# the big one
class ScheduleGridDisplay(ListView):

    template_name = 'centers/schedule-grid.html'
    model = BiWeeklyClass

    context_object_name = 'center_schedule'
    # TODO: USE THIS FOR A LOT OF THINGS!
    # series = ModelChoiceField(queryset=Series.objects.all())  # Or whatever query you'd li

    def get_context_data(self, **kwargs):
        for arg in kwargs:
            print(arg)

        context = super(ScheduleGridDisplay, self).get_context_data()
        # TODO: Stub that needs replacement when user system is in place
        self.request.user = get_dummy_user()
        # get center from the employee
        center = self.request.user.get_current_center()
        context['tue_fri'] = BiWeeklyClass.objects.tue_fri(center=center)
        context['wed_sat'] = BiWeeklyClass.objects.wed_sat(center=center)
        context['thu_sun'] = BiWeeklyClass.objects.thu_sun(center=center)
        context['sat_sun_am'] = BiWeeklyClass.objects.wed_sat(center=center)
        context['sat_sun_pm'] = BiWeeklyClass.objects.sat_sun_pm(center=center)

        return context



