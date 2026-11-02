from django.db import models


class Position(models.Model):
    name = models.CharField(max_length=100, unique=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Trainer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=12, unique=True, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.last_name} {self.first_name}'


class Client(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=12, unique=True)
    email = models.EmailField(unique=True, blank=True, null=True)

    def __str__(self):
        return f'{self.last_name} {self.first_name}'


class MembershipType(models.Model):
    type = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.type} - {self.price} руб.'


class Membership(models.Model):
    membership = models.ForeignKey(MembershipType, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.client} — {self.membership.type}'


class Workout(models.Model):
    workout_start = models.DateTimeField()
    workout_end = models.DateTimeField()
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.workout_start} — {self.client}'