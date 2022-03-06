from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Folder(models.Model):
  # define fields
  # https://docs.djangoproject.com/en/3.2/ref/models/fields/
  folder_name = models.CharField(max_length=100, blank=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  owner = models.ForeignKey(
      get_user_model(),
      on_delete=models.CASCADE
  )

  def __str__(self):
    # This must return a string
    return f"The folders name is '{self.folder_name}'."

  def as_dict(self):
    """Returns dictionary version of Mango models"""
    return {
        'id': self.id,
        'folder': self.folder_name
    }
