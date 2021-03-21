import django_filters
from webapp.models import create_lead
from django_filters import DateFilter, ChoiceFilter
from django.utils.timezone import now
from datetime import timedelta
from django.forms import DateInput

cur_date = now().date()


# today = create_lead.objects.filter(created=cur_date)
# yesterday = create_lead.objects.filter(created=cur_date - timedelta(days=1))
# date_filter = (
#     ('Today', today),
#     ('Yesterday', yesterday),
# )


class LeadFilters(django_filters.FilterSet):
    start_date = DateFilter(field_name='created', lookup_expr='gte')
    end_date = DateFilter(field_name='created', lookup_expr='lte')

    # date = ChoiceFilter(date_filter)

    class Meta:
        model = create_lead
        fields = ('lead_sour', 'lead_stat', 'lead_assign')
        # widgets = {
        #     'start_date': DateInput(attrs={'type': 'date'}),
        #     'end_date': DateInput(attrs={'type': 'date'}),
        # }

    # week = create_lead.objects.filter(created_on_gte=datetime.now() - timedelta(days=7)).count()
    # yesterday = create_lead.objects.filter(created_on_gte=datetime.now() - timedelta(days=1)).count()
    # today = create_lead.objects.filter(created_on_gte=datetime.now())
    #
    # context = {
    #     'week': week,
    #     'yesterday': yesterday,
    #     'today': today,
    # }
