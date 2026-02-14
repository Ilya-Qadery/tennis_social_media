"""
Utility functions following HackSoft style guide.
"""
from typing import List

from django.db import models


def model_update(*, instance: models.Model, fields: List[str], data: dict) -> models.Model:
    """
    Update a model instance with the given data.
    Only updates fields specified in the fields list.
    
    Args:
        instance: The model instance to update
        fields: List of field names that are allowed to be updated
        data: Dictionary containing the new values
    
    Returns:
        The updated instance
    """
    has_updated = False
    
    for field in fields:
        if field not in data:
            continue
            
        if getattr(instance, field) != data[field]:
            has_updated = True
            setattr(instance, field, data[field])
    
    if has_updated:
        instance.full_clean()
        instance.save(update_fields=fields + ["updated_at"])
    
    return instance
