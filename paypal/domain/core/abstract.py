from abc import ABC
from typing import Optional

from django.db.models import QuerySet
from django.db.utils import IntegrityError
from paypal.domain.core.models import BaseUUIDModel


class AbstractRepository(ABC):
    """
    Base repository class implementation.
    """
    BASE_CLASS = BaseUUIDModel

    def get_all(self) -> QuerySet[BASE_CLASS]:
        return self.BASE_CLASS.objects.all()

    def get_by_id(self, object_id: str) -> Optional[BASE_CLASS]:
        try:
            return self.BASE_CLASS.objects.get(id=object_id)
        except self.BASE_CLASS.DoesNotExist:
            return None

    def create(self, data: dict) -> BASE_CLASS:
        obj = self.BASE_CLASS(**data)
        self.save(obj)
        return obj

    def update(self, obj: BASE_CLASS, data: dict) -> BASE_CLASS:
        for name, value in data.items():
            setattr(obj, name, value)
        self.save(obj)
        return obj

    def save(self, obj: BASE_CLASS, update_fields: Optional[list] = None) -> None:
        obj.save(update_fields=update_fields)

    def delete_by_id(self, object_id: str) -> Optional[BASE_CLASS]:
        obj = self.get_by_id(object_id)
        return self.delete_obj(obj)

    def delete_obj(self, obj: BASE_CLASS) -> Optional[BASE_CLASS]:
        try:
            obj.delete()
            return obj
        except IntegrityError:
            return None

    def delete_all(self) -> None:
        self.get_all().delete()
