from django.db import models

# Create your models here.


class Tags(models.Model):
    name = models.CharField('Tag Name', max_length=100)

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField('Item Name', max_length=400)
    desc = models.TextField('Description', null=True, blank=True)
    code = models.CharField('Code', null=True, blank=True, max_length=20)
    tags = models.ManyToManyField('Tags', blank=True)
    image = models.ManyToManyField('products.Image', blank=True )

    def __str__(self):
        return self.name


class Image(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField()
    default = models.BooleanField(default=False)
    width = models.FloatField(default=100)
    length = models.FloatField(default=100)

    def __str__(self):
        return self.name
    
