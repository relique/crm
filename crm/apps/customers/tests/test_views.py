from django import test
from lib.test import setup_view
from apps.accounts.models import User, Company
from apps.customers.models import Customer
from apps.customers.forms import CustomerForm
from apps.customers.views import (CustomerList, CustomerCreate, CustomerUpdate)


class CustomersListTest(test.TestCase):
    def setUp(self):
        self.request = test.RequestFactory().get('/fake-path')
        self.view = setup_view(CustomerList(), self.request)
        comp = Company.objects.create(name='test')
        user = User.objects.create(email='t@t.com', company=comp)
        self.request.user = user
        object_list = [Customer.objects.create(first_name="test",
                                               last_name="test",
                                               user=user)]
        setattr(self.view, 'object_list', object_list)

    def test_get(self):
        resp = self.view.get(self.request)
        self.assertEqual(resp.status_code, 200)

    def test_attrs(self):
        self.assertEqual(self.view.model, Customer)

    def test_get_context_data(self):
        self.ctx = self.view.get_context_data()
        self.assertIn('title', self.ctx)


class CustomersCreateTest(test.TestCase):
    def setUp(self):
        self.request = test.RequestFactory().get('/fake-path')
        self.view = setup_view(CustomerCreate(), self.request)
        comp = Company.objects.create(name='test')
        user = User.objects.create(email='t@t.com', company=comp)
        object_ = Customer.objects.create(first_name="test", last_name="test",
                                          user=user)
        setattr(self.view, 'object', object_)

    def test_get(self):
        resp = self.view.get(self.request)
        self.assertEqual(resp.status_code, 200)

    def test_attrs(self):
        self.assertEqual(self.view.model, Customer)
        self.assertEqual(self.view.form_class, CustomerForm)

    def test_get_context_data(self):
        self.ctx = self.view.get_context_data()
        self.assertIn('title', self.ctx)


class CustomersUpdateTest(test.TestCase):
    def setUp(self):
        self.request = test.RequestFactory().get('/fake-path')
        comp = Company.objects.create(name='test')
        user = User.objects.create(email='t@t.com', company=comp)
        self.request.user = user
        self.object = Customer.objects.create(first_name="test",
                                              last_name="test",
                                              user=user)
        self.view = setup_view(CustomerUpdate(), self.request,
                               pk=self.object.pk)
        setattr(self.view, 'object', self.object)

    def test_get(self):
        resp = self.view.get(self.request)
        self.assertEqual(resp.status_code, 200)

    def test_attrs(self):
        self.assertEqual(self.view.model, Customer)
        self.assertEqual(self.view.form_class, CustomerForm)
        self.assertIsNotNone(self.view.success_message)

    def test_get_context_data(self):
        self.ctx = self.view.get_context_data()
        self.assertIn('title', self.ctx)

    def test_get_success_url(self):
        self.assertIsNotNone(self.view.get_success_url())
