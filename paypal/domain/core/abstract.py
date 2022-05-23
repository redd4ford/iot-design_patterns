from abc import ABC
from typing import Optional

from django.core.exceptions import ValidationError
from django.db.models import QuerySet

from paypal.domain.core.models import BaseUUIDModel


class AbstractRepository(ABC):
    """
    Base repository class implementation.
    """
    BASE_CLASS = BaseUUIDModel

    def get_all(self) -> QuerySet[BASE_CLASS]:
        return self.BASE_CLASS.objects.all()

    def get_by_id(self, object_id: str) -> BASE_CLASS:
        try:
            return self.BASE_CLASS.objects.get(id=object_id)
        except self.BASE_CLASS.DoesNotExist:
            raise ValidationError(message=f"Object does not exist: {object_id}")

    def create(self, data: dict) -> BASE_CLASS:
        obj = self.BASE_CLASS(**data)
        self.save(obj)
        return obj

    def save(self, obj: BASE_CLASS, update_fields: Optional[list] = None) -> None:
        obj.save(update_fields=update_fields)

    def delete_by_id(self, object_id: str) -> None:
        obj = self.get_by_id(object_id)
        obj.delete()

    def delete_all(self) -> None:
        self.get_all().delete()
