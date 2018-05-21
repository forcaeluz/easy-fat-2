from django.test import TestCase
from django.contrib.auth.models import User
from django.shortcuts import reverse
from .models import Farm
from .views import FarmAccessMixin


class IndexViewInstantiationTest(TestCase):

    def setUp(self):
        user = User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')
        farm = Farm.objects.create(name='EasyFarm', location='EasyCity')
        farm.userfarmrelations_set.create(user=user)
        self.client.login(username='temporary', password='temporary')

    def test_instantiation(self):
        response = self.client.get('/')
        self.assertEqual(200, response.status_code)
        self.assertEqual('farm/index.html', response.template_name[0])
        self.assertEqual(['EasyFarm', 'Dashboard'], response.context['bread_crumbs'])


class EmptyFarmModelTest(TestCase):

    def setUp(self):
        self.farm = Farm(name='EasyFarm', location='Wonderland')

    def test_owners(self):
        self.assertEqual(0, self.farm.owners.count())

    def test_buildings(self):
        self.assertEqual(0, self.farm.owners.count())

    def test_flocks(self):
        self.assertEqual(0, self.farm.flocks.count())


class OwnedFarmModelTest(TestCase):
    def setUp(self):
        self.farm = Farm(name='EasyFarm', location='Wonderland')
        self.farm.save()
        self.owner = User.objects.create_user('FarmOwner')
        self.owner.save()
        self.employee = User.objects.create_user('Employee')
        self.employee.save()
        self.farm.userfarmrelations_set.create(user=self.owner, relation='owner')
        self.farm.userfarmrelations_set.create(user=self.employee, relation='employee')

    def test_owners_property(self):
        self.assertEqual(1, self.farm.owners.count())


class NewFarmViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')
        self.client.login(username='temporary', password='temporary')
        self.response = self.client.get('/new_farm')

    def test_bread_crumbs(self):
        self.assertEquals(['Forms', 'New Farm'], self.response.context['bread_crumbs'])

    def test_title(self):
        self.assertEquals('New Farm', self.response.context['form'].title)

    def test_save(self):
        data = {'name': 'Ventania', 'location': 'Carambei'}
        self.response = self.client.post('/new_farm', data=data)
        self.assertEqual(302, self.response.status_code)
        self.assertEqual(1, self.user.userfarmrelations_set.count())


class FarmAccessMixinTest(TestCase):

    def setUp(self):
        user = User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')
        user2 = User.objects.create_user('user2', 'another@somemail.com', 'password')
        self.farm = Farm.objects.create(name='EasyFarm', location='EasyCity')
        self.farm.userfarmrelations_set.create(user=user)

    def test_without_login(self):
        response = self.client.get('/')
        self.assertEqual(302, response.status_code)
        self.assertEqual(reverse('login') + '?next=/', response.url)

    def test_logged_in(self):
        self.client.login(username='temporary', password='temporary')
        response = self.client.get('/')
        self.assertEqual(200, response.status_code)

    def test_user_without_farm(self):
        self.client.login(username='user2', password='password')
        response = self.client.get('/')
        self.assertEqual(302, response.status_code)
        self.assertEqual(reverse('accounts:index'), response.url)

    def test_user_without_access(self):
        self.client.login(username='user2', password='password')
        response = self.client.get(reverse('farm:dashboard', kwargs={'farm_id': self.farm.id}))
        self.assertEqual(403, response.status_code)

    def test_invalid_farm(self):
        self.client.login(username='user2', password='password')
        response = self.client.get(reverse('farm:dashboard', kwargs={'farm_id': 2}))
        self.assertEqual(403, response.status_code)

    def test_farm_change(self):
        self.client.login(username='temporary', password='temporary')
        response = self.client.get(reverse('farm:dashboard', kwargs={'farm_id': self.farm.id}))
        self.assertEqual(200, response.status_code)
        response = self.client.get('/')
        self.assertEqual(200, response.status_code)