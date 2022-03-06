from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class File(models.Model):
  # define fields
  # https://docs.djangoproject.com/en/3.2/ref/models/fields/
  file_name = models.CharField(max_length=100, blank=False)
  file_text = models.TextField(blank=True)
  has_text = models.BooleanField()
  file_video_description = models.CharField(max_length=100, blank=True)
  file_video = models.CharField(max_length=200, blank=True)
  has_video = models.BooleanField()
  file_picture_description = models.CharField(max_length=100, blank=True)
  file_picture = models.CharField(max_length=200, blank=True)
  has_picture = models.BooleanField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  owner = models.ForeignKey(
      get_user_model(),
      on_delete=models.CASCADE
  )
  folder = models.ForeignKey('Folder', related_name='file', on_delete=models.CASCADE)

  def __str__(self):
    # This must return a string
    return f"In the file named '{self.file_name}' it is {self.has_text} that it has text. It is {self.has_video} that it has a video. it is {self.has_picture} it has a picture."

  def as_dict(self):
    """Returns dictionary version of Mango models"""
    return {
        'id': self.id,
        'file_name': self.file_name,
        'file_text': self.file_text,
        'has_text': self.has_text,
        'file_video_description': self.file_video_description,
        'file_video': self.file_video,
        'has_video': self.has_video,
        'file_picture_description': self.file_picture_description,
        'file_picture': self.file_picture,
        'has_picture': self.has_picture
    }
