from django.contrib import admin

from .models import (
    Department,
    Doctor,
    Patient,
    Appointment,
    Medicine,
    Prescription,
    PrescriptionMedicine,
    Bill,
)


admin.site.register(Department)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Appointment)
admin.site.register(Medicine)
admin.site.register(Prescription)
admin.site.register(PrescriptionMedicine)
admin.site.register(Bill)