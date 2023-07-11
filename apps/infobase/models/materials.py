from django.db import models

class Material(models.Model):

    class Meta:
        verbose_name  = "Материал"
        verbose_name_plural  = "Материалы"

    title = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    color = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    structure = models.CharField(max_length=255)
    density = models.CharField(max_length=255)  # Updated field type to CharField
    image_url = models.ImageField(upload_to='infobase/materials/images', blank=True, null=True)
    description = models.TextField()

    def __str__(self):
        return self.title
    

class MaterialType(models.Model):
    class Meta:
        verbose_name = "Вид материала"
        verbose_name = "Виды материалов"

    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title
