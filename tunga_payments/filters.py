import django_filters
from django_filters import FilterSet

from tunga_payments.models import Invoice, Payment
from tunga_utils.filters import GenericDateFilterSet


class InvoiceFilter(GenericDateFilterSet):
    class Meta:
        model = Invoice
        fields = ('type', 'batch_ref', 'number', 'user', 'project', 'created_by', 'paid', 'status', 'archived')


class PaymentFilter(FilterSet):
    batch_ref = django_filters.CharFilter(name='invoice__batch_ref', label='Invoice Batch Ref', lookup_expr='exact')
    number = django_filters.NumberFilter(name='invoice__number', label='Invoice number', lookup_expr='exact')
    project = django_filters.NumberFilter(name='invoice__project', label='Project Invoice', lookup_expr='exact')
    user = django_filters.NumberFilter(name='invoice__user', label='Invoice user', lookup_expr='exact')
    min_date = django_filters.IsoDateTimeFilter(name='paid_at', lookup_expr='gte')
    max_date = django_filters.IsoDateTimeFilter(name='paid_at', lookup_expr='lte')

    class Meta:
        model = Payment
        fields = ('min_date', 'max_date', 'batch_ref', 'number', 'user', 'project', 'created_by',)
