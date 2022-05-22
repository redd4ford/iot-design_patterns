import uuid

from django.db import models


class BaseUUIDModel(models.Model):
    """Base model."""

    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    @property
    def class_name(self) -> str:
        return self._meta.verbose_name
