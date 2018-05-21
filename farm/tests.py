from django.test import TestCase
from django.contrib.auth.models import User

from .models import Farm


class IndexViewInstantiationTest(TestCase):

    def setUp(self):
        User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')
        self.client.login(username='temporary', password='temporary')

    def test_instantiation(self):
        response = self.client.get('/')
        self.assertEqual('farm/index.html', response.template_name[0])


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
