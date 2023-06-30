from django_filters import FilterSet, NumberFilter, CharFilter, DateTimeFilter, DateFilter
from django.forms import DateInput
from django.utils.translation import gettext
from django_filters.widgets import RangeWidget
from .models import Feedback


# Создаем свой набор фильтров для модели Product.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.
class FeedbackFilter(FilterSet):

    class Meta:
        model = Feedback
        fields = {
            'advertisement': ['exact']
        }
