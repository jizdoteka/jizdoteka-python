from django.views.generic import DetailView

# FIXME: Really, really ugly!
from .. import models


class UserDetail(DetailView):
    model = models.User
