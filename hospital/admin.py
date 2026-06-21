from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    User,
    Doctor,
    Patient,
    Department,
    Appointment,
    Prescription,
    PrescriptionMedicine,
    Medicine,
    Bill,
)


admin.site.register(User, UserAdmin)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Department)
admin.site.register(Appointment)
admin.site.register(Prescription)
admin.site.register(PrescriptionMedicine)
admin.site.register(Medicine)
admin.site.register(Bill)