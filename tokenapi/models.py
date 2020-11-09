from django.db import models
import uuid
class BaseModel(models.Model):
    id = models.CharField(primary_key = True, max_length =50 ,blank=True, unique =True, default=uuid.uuid4, editable=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)
    class Meta:
      abstract = True

class Token(BaseModel,models.Model):
  expireTime = models.DateTimeField(blank=True, null = True)
  isDeleted = models.BooleanField(default=False)
  isFree = models.BooleanField(default=True)
  deleteTime = models.DateTimeField(blank=True, null = True)
  