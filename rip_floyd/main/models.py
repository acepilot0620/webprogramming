from django.db import models

# Create your models here.

class Victims(models.Model):
    age = models.TextField(max_length=10)
    gender = models.TextField(max_length=10)
    race = models.TextField(max_length=30)
    date = models.TextField(max_length= 20)
    state = models.TextField(max_length=10)
    cause_of_death = models.TextField(max_length=50)
    mental_illness = models.TextField(max_length=20)
    unarmed = models.TextField(max_length=20)
    alleged_weapon = models.TextField(max_length=30)
    alleged_threat_level = models.TextField(max_length=20)
    fleeing = models.TextField(max_length=20)
    def __str__(self):
        return str(self.id)

class Police_victim(models.Model):
    error_buffer = models.TextField(max_length=20,default="-", verbose_name='error')
    date = models.TextField(max_length= 20, default='yyyy.mm.dd', verbose_name='날짜')
    name = models.TextField(max_length= 50, default='default_name', verbose_name='이름')
    state = models.TextField(max_length=10, default='default_state', verbose_name='주(State)')
    cause_of_death = models.TextField(max_length=50, default='default_manner_of_death', verbose_name='사인')
    def __str__(self):
        return self.name

class News(models.Model):
    title = models.TextField(max_length=500)
    img_url = models.TextField(max_length=100)
    article_url = models.TextField(max_length=100)
    timestamp = models.TextField(max_length=50)
    
    def __str__(self):
        return self.title

    
   