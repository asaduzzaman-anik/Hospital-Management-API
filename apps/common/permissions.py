from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (
                request.user.is_superuser
                or request.user.role == "admin"
            )
        )

class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (
                request.user.is_superuser
                or request.user.role == 'doctor'
            )
        )


class IsPatient(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (
                request.user.is_superuser
                or request.user.role == 'patient'
            )
        )


class IsReceptionist(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (
                request.user.is_superuser
                or request.user.role == 'receptionist'
            )
        )


class IsAdminOrReceptionist(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (
                request.user.is_superuser
                or request.user.role in ['admin', 'receptionist']
            )
        )


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):

        if request.method in SAFE_METHODS:
            return request.user.is_authenticated

        return (
            request.user.is_authenticated
            and (
                request.user.is_superuser
                or request.user.role == "admin"
            )
        )

class IsAdminReceptionistOrReadOnly(BasePermission):

    def has_permission(self, request, view):

        if request.method in SAFE_METHODS:
            return request.user.is_authenticated

        return (
            request.user.is_authenticated
            and (
                request.user.is_superuser
                or request.user.role in [
                    "admin",
                    "receptionist",
                ]
            )
        )


class IsAdminReceptionistOrPatientOwner(BasePermission):
    """
    Authenticated users may read.
    Admin/receptionist may create/update/delete any patient.
    Patients may create their own profile and update only that profile.
    """

    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False

        if request.method in SAFE_METHODS:
            return True

        if user.is_superuser or user.role in ['admin', 'receptionist']:
            return True

        if user.role == 'patient' and view.action in [
            'create',
            'update',
            'partial_update',
        ]:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        user = request.user
        if request.method in SAFE_METHODS:
            return True

        if user.is_superuser or user.role in ['admin', 'receptionist']:
            return True

        if user.role == 'patient':
            return obj.user_id == user.id

        return False