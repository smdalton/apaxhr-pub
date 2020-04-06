from django.contrib.admindocs.views import ModelDetailView
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.base import TemplateView


from core_hr.models import Employee

def logout_view(request):
    logout(request)
    return redirect('home_simple')
    # Redirect to a success page.

class HomePage(LoginView):

    template_name = 'apaxhr/home.html'
    def get_success_url(self):
        return reverse_lazy('home_simple')

    def dispatch(self, request, *args, **kwargs):
        # store permissions session data at login time
        self.access_tier = kwargs.get('access_tier', "access tier not present")
        #print(self.request.get_host())
        # assign permissions this way

        self.request.user.groups.filter(name__in=['group1', 'group2']).exists()
        return super(HomePage, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(HomePage, self).get_context_data(**kwargs)
        # TODO: Implement user request authentication and slotting here
        tier_list = ['tier0', 'tier1', 'tier2', 'tier3', 'tier4', ]

        def pop_session(save_tier='none'):
            for tier in tier_list:
                try:
                    self.request.session.pop(tier)
                    print(tier, " Deactivated")
                except:
                    print(tier, "Not Set")

        if self.access_tier == '0':
            pop_session()
            print('---> tier0 set')
            self.request.session['privilege_level'] = self.access_tier
            self.request.session['tier0']=True

        if self.access_tier == '1':
            pop_session()
            print('---> tier1 set')
            self.request.session['privilege_level'] = self.access_tier
            self.request.session['tier1']=True
            # context['user_is_tier1'] = self.request.user.groups.filter(name='Instructors').exists()
        if self.access_tier == '2':
            pop_session()
            print('---> tier2 set')
            self.request.session['privilege_level'] = self.access_tier
            self.request.session['tier2'] = True

        if self.access_tier == '3':
            pop_session()
            print('---> tier3 set')
            self.request.session['privilege_level'] = self.access_tier
            self.request.session['tier3'] = True

        if self.access_tier == '4':
            pop_session()
            print('---> tier4 set')
            self.request.session['privilege_level']= self.access_tier
            self.request.session['tier4'] = True

        context['privilege_level'] = self.access_tier

        return context
#
# class Logout(LogoutView):
#     template_name = 'users/logout.html'
#     next_page = reverse_lazy('home_simple')