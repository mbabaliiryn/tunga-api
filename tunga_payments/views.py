# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Create your views here.
from dry_rest_permissions.generics import DRYObjectPermissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from tunga_payments.filters import InvoiceFilter
from tunga_payments.models import Invoice, Payment
from tunga_payments.serializers import InvoiceSerializer, PaymentSerializer
from tunga_utils.filterbackends import DEFAULT_FILTER_BACKENDS


class InvoiceViewSet(ModelViewSet):
    serializer_class = InvoiceSerializer
    queryset = Invoice.objects.all()
    permission_classes = [IsAuthenticated, DRYObjectPermissions]
    filter_class = InvoiceFilter
    filter_backends = DEFAULT_FILTER_BACKENDS  # + (TaskFilterBackend,)


class PaymentViewSet(ModelViewSet):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated, DRYObjectPermissions]
