"""Helpers for EKS Console related operations.

Usage example:
    eks_console_helper = EKSConsoleHelper()
    result = eks_console_helper.get_login_magic_link("ben.he+sz909093@crypto.com")
"""
from .rails import RailsConsoleHelper

__all__ = [
    "RailsConsoleHelper",
]
