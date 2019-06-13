# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from datetime import datetime

from django.contrib.auth import get_user_model
# Create your tests here.
from django.test import RequestFactory
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from tunga_payments.models import Invoice, Payment
from tunga_projects.models import Project
from tunga_utils.constants import USER_TYPE_PROJECT_OWNER, USER_TYPE_DEVELOPER, USER_TYPE_PROJECT_MANAGER, \
    TASK_TYPE_WEB, TASK_SCOPE_PROJECT, TASK_SCOPE_TASK


class APIInvoiceTestCase(APITestCase):

    def setUp(self):
        self.project_owner = get_user_model().objects.create_user(
            'project_owner', 'po@example.com', 'secret',
            **dict(type=USER_TYPE_PROJECT_OWNER)
        )
        self.developer = get_user_model().objects.create_user(
            'developer', 'developer@example.com', 'secret',
            **dict(type=USER_TYPE_DEVELOPER)
        )
        self.project_manager = get_user_model().objects.create_user(
            'project_manager', 'pm@example.com', 'secret',
            **dict(type=USER_TYPE_PROJECT_MANAGER)
        )
        self.admin = get_user_model().objects.create_superuser(
            'admin', 'admin@example.com', 'secret'
        )

        self.factory = RequestFactory()

    def test_create_invoice(self):
        url = reverse('invoice-list')
        data_outer = dict(
            first_name='David', last_name='Semakula', email='guest@example.com',
            type=TASK_TYPE_WEB, scope=TASK_SCOPE_PROJECT
        )


        project_data = {
            "description": "Web test project",
            "title": "Tunga Dev Phase 1",
            "deadline": "2018-08-21T12:00",
            "user": self.project_owner,
        }
        project = Project.objects.create(**project_data)

        invoice_data = {
            "processing_fee": 0,
            "created_by": self.admin.id,
            "number": "100001",
            "project": {'id': project.id},
            "currency": "EUR",
            "amount": 1500,
            "tax_rate": 12,
            "user": {'id': self.project_owner.id},
            "type": "tunga"
        }
        data_inner = dict(
            title='Task 1', skills='Django, React.js',
            type=TASK_TYPE_WEB, scope=TASK_SCOPE_TASK,
            description='This is a sample task'
        )

        # Guests can fill the wizard
        self.client.force_authenticate(user=None)
        response = self.client.post(url, invoice_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Developer's can't create tasks
        self.client.force_authenticate(user=self.developer)
        response = self.client.post(url, invoice_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Project Owner's can't create tasks
        self.client.force_authenticate(user=self.project_owner)
        response = self.client.post(url, invoice_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # PM's can create invoices
        self.client.force_authenticate(user=self.project_manager)
        response = self.client.post(url, invoice_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Admins can create tasks
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(url, invoice_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_bulk_invoice(self):
        url = reverse('invoice-bulk-create-invoices')
        data_outer = dict(
            first_name='David', last_name='Semakula', email='guest@example.com',
            type=TASK_TYPE_WEB, scope=TASK_SCOPE_PROJECT
        )

        project_data = {
            "description": "Web test project",
            "title": "Tunga Dev Phase 1",
            "deadline": "2018-08-21T12:00",
            "user": self.project_owner,
        }
        project = Project.objects.create(**project_data)

        invoice_data = {
            "processing_fee": 0,
            "created_by": self.admin.id,
            "number": "100001",
            "project": {'id': project.id},
            "currency": "EUR",
            "amount": 1500,
            "tax_rate": 12,
            "user": {'id': self.project_manager.id},
            "type": "tunga"
        }
        invoice_bulk = [invoice_data, invoice_data]
        data_inner = dict(
            title='Task 1', skills='Django, React.js',
            type=TASK_TYPE_WEB, scope=TASK_SCOPE_TASK,
            description='This is a sample task'
        )

        # Guests can fill the wizard
        self.client.force_authenticate(user=None)
        response = self.client.post(url, invoice_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Developer's can't create tasks
        self.client.force_authenticate(user=self.developer)
        response = self.client.post(url, invoice_bulk)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Project Owner's can't create tasks
        self.client.force_authenticate(user=self.project_owner)
        response = self.client.post(url, invoice_bulk)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # PM's can create invoices
        self.client.force_authenticate(user=self.project_manager)
        response = self.client.post(url, invoice_bulk)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Admins can create tasks
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(url, invoice_bulk)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(json.loads(response.content)), len(invoice_bulk))

    def test_read_invoice(self):
        url = reverse('invoice-list')

        project_data = {
            "description": "Web test project",
            "title": "Tunga Dev Phase 1",
            "deadline": "2018-08-21T12:00",
            "user": self.project_manager,
            "owner": self.project_owner,
            "pm": self.project_manager

        }
        project = Project.objects.create(**project_data)

        invoice_data = {
            "processing_fee": 0,
            "created_by": self.admin,
            "number": "100001",
            "project": project,
            "currency": "EUR",
            "amount": 1500,
            "tax_rate": 12,
            "user": self.project_owner,
            "type": "tunga"
        }
        invoice = Invoice.objects.create(**invoice_data)

        # Guests
        self.client.force_authenticate(user=None)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Developer
        self.client.force_authenticate(user=self.developer)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get('/api/invoices/%s/' % invoice.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Project Owner
        self.client.force_authenticate(user=self.project_owner)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get('/api/invoices/%s/' % invoice.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # PM's
        self.client.force_authenticate(user=self.project_manager)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get('/api/invoices/%s/' % invoice.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Admins can create tasks
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get('/api/invoices/%s/' % invoice.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class APIPaymentTestCase(APITestCase):

    def setUp(self):
        self.project_owner = get_user_model().objects.create_user(
            'project_owner', 'po@example.com', 'secret',
            **dict(type=USER_TYPE_PROJECT_OWNER)
        )
        self.developer = get_user_model().objects.create_user(
            'developer', 'developer@example.com', 'secret',
            **dict(type=USER_TYPE_DEVELOPER)
        )
        self.project_manager = get_user_model().objects.create_user(
            'project_manager', 'pm@example.com', 'secret',
            **dict(type=USER_TYPE_PROJECT_MANAGER)
        )
        self.admin = get_user_model().objects.create_superuser(
            'admin', 'admin@example.com', 'secret'
        )

        self.factory = RequestFactory()

    def test_create_invoice_payment(self):
        url = reverse('payment-list')
        data_outer = dict(
            first_name='David', last_name='Semakula', email='guest@example.com',
            type=TASK_TYPE_WEB, scope=TASK_SCOPE_PROJECT
        )

        project_data = {
            "description": "Web test project",
            "title": "Tunga Dev Phase 1",
            "deadline": "2018-08-21T12:00",
            "user": self.project_owner,
        }
        project = Project.objects.create(**project_data)

        invoice_data = {
            "processing_fee": 0,
            "created_by": self.admin,
            "number": "100001",
            "project": project,
            "currency": "EUR",
            "amount": 1500,
            "tax_rate": 12,
            "user": self.project_owner,
            "type": "tunga"
        }
        invoice = Invoice.objects.create(**invoice_data)

        payment_data = {
            "payment_method": "bank",
            "currency": "EUR",
            "amount": 600,
            "invoice": {'id': invoice.id},
            "paid_at": datetime.now()
        }
        data_inner = dict(
            title='Task 1', skills='Django, React.js',
            type=TASK_TYPE_WEB, scope=TASK_SCOPE_TASK,
            description='This is a sample task'
        )

        # Guests can fill the wizard
        self.client.force_authenticate(user=None)
        response = self.client.post(url, payment_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Developer's can't create tasks
        self.client.force_authenticate(user=self.developer)
        response = self.client.post(url, payment_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Project Owner's can't create tasks
        self.client.force_authenticate(user=self.project_owner)
        response = self.client.post(url, payment_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # PM's can't create tasks
        self.client.force_authenticate(user=self.project_manager)
        response = self.client.post(url, payment_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Admins can create tasks
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(url, payment_data)
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_read_invoice_payment(self):
        url = reverse('payment-list')

        project_data = {
            "description": "Web test project",
            "title": "Tunga Dev Phase 1",
            "deadline": "2018-08-21T12:00",
            "user": self.project_owner,
            "pm": self.project_manager
        }
        project = Project.objects.create(**project_data)

        invoice_data = {
            "processing_fee": 0,
            "created_by": self.admin,
            "number": "100001",
            "project": project,
            "currency": "EUR",
            "amount": 1500,
            "tax_rate": 12,
            "user": self.project_owner,
            "type": "tunga"
        }
        invoice = Invoice.objects.create(**invoice_data)

        payment_data = {
            "payment_method": "bank",
            "currency": "EUR",
            "amount": 600,
            "invoice": invoice,
            "paid_at": datetime.now(),
            "created_by": self.admin,
        }

        payment = Payment.objects.create(**payment_data)

        # Guests
        self.client.force_authenticate(user=None)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Developer
        self.client.force_authenticate(user=self.developer)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get('/api/payments/%s/' % payment.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Project Owner
        self.client.force_authenticate(user=self.project_owner)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get('/api/payments/%s/' % payment.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # PM's
        self.client.force_authenticate(user=self.project_manager)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get('/api/payments/%s/' % payment.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Admins can create tasks
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get('/api/payments/%s/' % payment.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
