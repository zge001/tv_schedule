from django.db import models

class MyModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class TVChannel(MyModel):
    name = models.CharField(verbose_name="Название", max_length=100, unique=True)
    logo = models.ImageField(
        verbose_name="Логотип", upload_to='tv/channels', blank=True, null=True)
    priority = models.IntegerField(verbose_name="Приоритет", default=0)

    class Meta:
        ordering = ["name"]
        verbose_name = "Телеканал"
        verbose_name_plural = "Телеканалы"

    def __str__(self):
        return self.name
    

class TVProgram(MyModel):
    tv_channel = models.ForeignKey(
        TVChannel, on_delete=models.CASCADE, verbose_name="Телеканал")
    date = models.DateTimeField(verbose_name="Дата", unique=True)
    title = models.CharField(verbose_name="Название", max_length=200)
    cover = models.ImageField(verbose_name="Обложка", upload_to="tv/covers", blank=True, null=True)

    class Meta:
        ordering = ["date"]
        verbose_name = "Телепрограмма"
        verbose_name = "Телепрограммы"