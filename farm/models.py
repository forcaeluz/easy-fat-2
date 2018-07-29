from django.db import models
from flocks.models import Flock
from buildings.models import Building, AnimalRoomEntry, AnimalRoomExit
from django.contrib.auth.models import User


class Farm(models.Model):
    name = models.CharField(max_length=100, null=False)
    location = models.CharField(max_length=100)

    @property
    def flocks(self):
        return self.farmflockrelations_set.all()

    @property
    def buildings(self):
        return self.farmbuildingrelations_set.all()

    @property
    def owners(self):
        return self.userfarmrelations_set.filter(relation='owner')


class UserFarmRelations(models.Model):
    RELATIONS = [
        'owner',
        'employee',
        'watcher'
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)
    relation = models.CharField(max_length=20, default='owner')


class FarmBuildingRelations(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)
    building = models.ForeignKey(Building, on_delete=models.CASCADE)


class FarmFlockRelations(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)
    flock = models.ForeignKey(Flock, on_delete=models.CASCADE)


class FlockRoomEntryRelations(models.Model):
    flock = models.ForeignKey(Flock, on_delete=models.CASCADE)
    room_entry = models.OneToOneField(AnimalRoomEntry, on_delete=models.CASCADE)


class FlockRoomExitRelations(models.Model):
    flock = models.ForeignKey(Flock, on_delete=models.CASCADE)
    room_exit = models.OneToOneField(AnimalRoomExit, on_delete=models.CASCADE)
