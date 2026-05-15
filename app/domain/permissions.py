from app.domain.models import AccessLevel, UserRole

ROLE_ACCESS: dict[UserRole, set[AccessLevel]] = {
    "guest": {"public"},
    "employee": {"public", "internal"},
    "engineer": {"public", "internal"},
    "admin": {"public", "internal", "restricted"},
}


def can_access(user_role: UserRole, access_level: AccessLevel) -> bool:
    return access_level in ROLE_ACCESS[user_role]
