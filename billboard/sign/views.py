from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from sign.models import BaseRegisterForm
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'




@login_required
def upgrade_me(request):
    user = request.user
    author_group = Group.objects.get(name='basic')
    if not request.user.groups.filter(name='basic').exists():
        author_group.user_set.add(user)
    return redirect('/')