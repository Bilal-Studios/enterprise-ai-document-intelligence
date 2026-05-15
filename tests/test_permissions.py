from app.domain.permissions import can_access


def test_guest_can_access_public_documents():
    assert can_access("guest", "public") is True


def test_guest_cannot_access_internal_documents():
    assert can_access("guest", "internal") is False


def test_employee_can_access_internal_documents():
    assert can_access("employee", "internal") is True


def test_engineer_can_access_restricted_documents():
    assert can_access("engineer", "restricted") is False


def test_admin_can_access_restricted_documents():
    assert can_access("admin", "restricted") is True
