from django.db import models


class GeneralModel(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        super(Tags, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    
    class Meta:
        abstract = True


class Tags(GeneralModel):
    name = models.CharField('Tag Name', max_length=100, unique=True)


class Item(models.Model):
    name = models.CharField('Item Name', max_length=400)
    desc = models.TextField('Description', null=True, blank=True)
    code = models.CharField('Code', null=True, blank=True, max_length=20)
    tags = models.ManyToManyField('Tags', blank=True)
    image = models.ManyToManyField('products.Image', blank=True )

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        super(Item, self).save(*args, **kwargs)
        if ItemColorAvailability.objects.filter(item=self).count() == 0:
            ItemColorAvailability.objects.create(item=self)
        
        


class Color(GeneralModel):
    hash_code = models.CharField("Color Code", null=True, max_length=15, blank=True)


class ItemColorAvailability(models.Model):
    item = models.ForeignKey('products.Item', on_delete=models.CASCADE)
    color = models.ForeignKey('products.Color', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        if self.color:
            return "%s:%s" % (self.item.name, self.color)
        else:
            return self.item.name


class Image(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField()
    default = models.BooleanField(default=False)
    width = models.FloatField(default=100)
    length = models.FloatField(default=100)

    def __str__(self):
        return self.name
    
