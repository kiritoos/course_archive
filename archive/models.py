from django.conf import settings
from django.db import models

class Discipline(models.Model):
    name = models.CharField("Название дисциплины", max_length=100, unique=True)
    def __str__(self):
        return self.name

class Keyword(models.Model):
    name = models.CharField("Ключевое слово", max_length=50, unique=True)
    def __str__(self):
        return self.name

class Work(models.Model):
    title = models.CharField("Тема работы", max_length=200)
    content = models.TextField("Краткое содержание", blank=True)
    year = models.IntegerField("Год защиты")
    supervisor = models.CharField("Руководитель", max_length=150)
    grade = models.IntegerField("Оценка", default=0)
    is_defended = models.BooleanField("Защищена", default=False)
    created_at = models.DateTimeField("Создано", auto_now_add=True)
    updated_at = models.DateTimeField("Изменено", auto_now=True)
    
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="works", verbose_name="Автор")
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE, related_name="works", verbose_name="Дисциплина")
    keywords = models.ManyToManyField(Keyword, blank=True, related_name="works", verbose_name="Ключевые слова")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Курсовая работа"
        verbose_name_plural = "Курсовые работы"
        indexes = [
            models.Index(fields=["-created_at"], name="work_created_idx"),
            models.Index(fields=["discipline", "-created_at"], name="work_discipline_idx"),
            models.Index(fields=["supervisor"], name="work_supervisor_idx"),
        ]

    def __str__(self):
        return self.title