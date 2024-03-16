from enum import Enum


class Role(Enum):
    admin = "ADMIN"
    customer = "CUSTOMER"
    manager = "MANAGER"


class CategoryStatus(Enum):
    ACTIVE = "ACTIVE"
    DELETED = "DELETED"
    REQUESTED = "REQUESTED"
    REJECTED = "REJECTED"


class ProductStatus(Enum):
    ACTIVE = "ACTIVE"
    DELETED = "DELETED"
    REQUESTED = "REQUESTED"
    REJECTED = "REJECTED"
