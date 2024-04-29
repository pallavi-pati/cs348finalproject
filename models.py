from django.db import models
from django.utils import timezone
from django.urls import reverse

# Create your models here.
def ten_day_hence():
    return timezone.now() + timezone.timedelta(days=10)

class ToDoList(models.Model):
    title = models.CharField(max_length=150, unique=True) #title can be max 150 characters and has to be unique

    def get_absolute_url(self):
        return reverse("list", args=[self.id])

    def __str__(self):
        return self.title

class ToDoItem(models.Model):
    title = models.CharField(max_length=150, unique=True)
    description = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, db_index=True)
    due_date = models.DateTimeField(default=ten_day_hence, db_index=True)
    todo_list = models.ForeignKey(ToDoList, on_delete=models.CASCADE, db_index=True)

    def get_absolute_url(self):
        return reverse(
            "item-update", args=[str(self.todo_list.id), str(self.id)]
        )

    def __str__(self):
        return f"{self.title}: due {self.due_date}"

    class Meta:
        ordering = ["due_date"]