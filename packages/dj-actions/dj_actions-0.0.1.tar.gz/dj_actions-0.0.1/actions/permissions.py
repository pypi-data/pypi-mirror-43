"""
A permission is a function that returns a boolean and an error message.

False = failed
True = all good, carry on

Permissions will always receive the active user as the first argument.
Other arguments can be mapped in
"""

def is_admin(user, **kwargs):
    is_ok = user.is_superuser
    if not is_ok:
        return False, "Permission denied"
    return True, None
