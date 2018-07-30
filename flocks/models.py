from django.db import models
from django.db.models import Sum, F, Q, Count
from django.db.models.functions import Coalesce
from django.utils.dateparse import parse_date

from math import ceil
import datetime


class CurrentFlocksManager(models.Manager):
    def present(self):
        return super().all() \
            .annotate(dead_animals=Count('animaldeath')) \
            .annotate(exited=Coalesce(Sum('animalflockexit__number_of_animals'), 0)) \
            .annotate(current_count=F('number_of_animals') - F('exited') - F('dead_animals')) \
            .filter(current_count__gt=0)

    def old_flocks(self):
        return super().all() \
            .annotate(dead_animals=Count('animaldeath')) \
            .annotate(exited=Coalesce(Sum('animalflockexit__number_of_animals'), 0)) \
            .annotate(current_count=F('number_of_animals') - F('exited') - F('dead_animals')) \
            .filter(current_count__lte=0)


class Flock(models.Model):

    """ Flock model representing a flock of animals that entered the farm.

    The flock is the basic element of the whole application. It is a group of
    animals entering the farm.
    """

    entry_date = models.DateField()
    entry_weight = models.FloatField()
    number_of_animals = models.IntegerField()
    objects = CurrentFlocksManager()

    @property
    def flock_name(self):
        return '%d_%d' % (self.entry_date.year, self.id)

    @property
    def expected_exit_date(self):
        date_year_before = self.entry_date - datetime.timedelta(days=365)
        exits = AnimalFlockExit.objects.filter(farm_exit__date__gte=date_year_before)
        grow_rate = self.__compute_grow_rate_for_exits_set(exits)
        if grow_rate is None:
            grow_rate = 0.850

        growing_days = ceil((115 - self.average_entry_weight) / grow_rate)
        date = self.entry_date + datetime.timedelta(days=growing_days)
        return date

    @property
    def number_of_living_animals(self):
        number_of_gone_animals = 0

        for exits in self.animalflockexit_set.all():
            number_of_gone_animals += exits.number_of_animals

        number_of_gone_animals += self.animaldeath_set.count()
        return self.number_of_animals - number_of_gone_animals

    @property
    def average_entry_weight(self):
        return self.entry_weight / self.number_of_animals

    @property
    def computed_daily_growth(self):
        exits_set = self.animalflockexit_set.all()
        return self.__compute_grow_rate_for_exits_set(exits_set)

    @property
    def average_exit_weight(self):
        exits_set = self.animalflockexit_set.all()
        weight = sum([obj.weight for obj in exits_set])
        animals = sum([obj.number_of_animals for obj in exits_set])
        if animals > 0:
            return weight/animals
        else:
            return 0

    @property
    def separated_animals(self):
        separation_set = self.animalseparation_set.all()
        active_separations = len([obj for obj in separation_set])
        return active_separations

    @property
    def estimated_avg_weight(self):
        return self.estimated_average_weight_at_date(datetime.date.today())

    def estimated_average_weight_at_date(self, at_date):
        if isinstance(at_date, str):
            at_date = parse_date(at_date)
        date_year_before = self.entry_date - datetime.timedelta(days=365)
        exits = AnimalFlockExit.objects.filter(farm_exit__date__gte=date_year_before)
        grow_rate = self.__compute_grow_rate_for_exits_set(exits)
        if grow_rate is None:
            grow_rate = 0.850

        days_at_farm = at_date - self.entry_date
        return self.average_entry_weight + grow_rate * days_at_farm.days

    @staticmethod
    def __compute_grow_rate_for_exits_set(exits_set):
        total_number_of_animals = 0
        average_grow = 0
        for animal_exit in exits_set:
            total_number_of_animals += animal_exit.number_of_animals
            average_grow += animal_exit.grow_rate * animal_exit.number_of_animals

        if total_number_of_animals == 0:
            return None

        return average_grow / total_number_of_animals

    @property
    def death_percentage(self):
        return (self.animaldeath_set.count() / self.number_of_animals) * 100

    def __str__(self):
        return self.flock_name


class AnimalDeath(models.Model):
    date = models.DateField()
    weight = models.FloatField()
    cause = models.TextField()
    flock = models.ForeignKey(Flock, on_delete=models.CASCADE)

    def __str__(self):
        return 'Animal death: ' + str(self.flock) + ' on ' + str(self.date) + ' because of ' + self.cause


class AnimalFarmExit(models.Model):
    date = models.DateField()
    destination = models.CharField(max_length=140, default='Unknown')

    @property
    def average_weight(self):
        return self.weight / self.number_of_animals

    @property
    def number_of_animals(self):
        return self.animalflockexit_set.all().aggregate(Sum('number_of_animals'))

    @property
    def weight(self):
        return self.animalflockexit_set.all().aggregate(Sum('weight'))


class AnimalFlockExit(models.Model):
    weight = models.FloatField()
    number_of_animals = models.IntegerField()
    flock = models.ForeignKey(Flock, on_delete=models.CASCADE)
    farm_exit = models.ForeignKey(AnimalFarmExit, on_delete=models.CASCADE)

    @property
    def grow_rate(self):
        entry_weight = self.flock.average_entry_weight
        exit_weight = self.average_weight
        time_interval = self.farm_exit.date - self.flock.entry_date
        return (exit_weight - entry_weight) / time_interval.days

    @property
    def average_weight(self):
        return self.weight / self.number_of_animals

    @property
    def date(self):
        return self.farm_exit.date


class AnimalSeparation(models.Model):
    date = models.DateField()
    reason = models.CharField(max_length=250)
    flock = models.ForeignKey(Flock, models.CASCADE)
    death = models.ForeignKey(AnimalDeath, null=True, blank=True, on_delete=models.SET_NULL)
    exit = models.ForeignKey(AnimalFlockExit, null=True, blank=True, on_delete=models.SET_NULL)

    @property
    def active(self):
        return (self.death is None) and (self.exit is None)

    def __str__(self):
        return 'Animal separation: ' + str(self.flock) + ' on ' + str(self.date) + ' with reason ' + self.reason
