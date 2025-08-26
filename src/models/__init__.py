"""
Database Models Package

This package contains all SQLModel database models for the Transport Management System.
Models define the database schema and are used for both database operations and API schemas.

Available Models:
- Vendor: Transport service providers and logistics partners

Usage:
    from src.models import Vendor
    from src.models.vendor import Vendor  # Direct import also works
"""

from .vendor import Vendor

# Export all models for easy importing
__all__ = [
    "Vendor",
    # Add future models here as they are created:
    # "Customer",
    # "Order",
    # "Shipment",
    # "Vehicle",
    # "Driver",
    # "Route",
]

# Model registry for easy access to all models
MODELS = {
    "vendor": Vendor,
    # Add future models here:
    # "customer": Customer,
    # "order": Order,
    # "shipment": Shipment,
    # "vehicle": Vehicle,
    # "driver": Driver,
    # "route": Route,
}


def get_all_models():
    """
    Get a list of all registered SQLModel classes.

    Returns:
        list: List of all model classes
    """
    return list(MODELS.values())


def get_model_by_name(name: str):
    """
    Get a model class by its name.

    Args:
        name: The model name (e.g., 'vendor', 'customer')

    Returns:
        The model class or None if not found
    """
    return MODELS.get(name.lower())
