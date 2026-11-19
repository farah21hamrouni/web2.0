
from django.db import models
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.utils import timezone


class Appointment(models.Model):

    # Status
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'En attente'
        CONFIRMED = 'CONFIRMED', 'Confirmé'
        CANCELLED = 'CANCELLED', 'Annulé'

    # Fields
    reason = models.TextField()

    prescription = models.FileField(
        upload_to='prescriptions/',
        blank=True,
        validators=[FileExtensionValidator(['pdf'])]
    )

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING
    )

    duration_minutes = models.PositiveIntegerField(default=30)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    doctor = models.ForeignKey(
        'AccountApp.Doctor',
        on_delete=models.CASCADE,
        related_name='appointments'
    )

    patient = models.ForeignKey(
        'AccountApp.Patient',
        on_delete=models.CASCADE,
        related_name='appointments'
    )

    appointment_date = models.DateTimeField()

    # Validation
    def clean(self):
        super().clean()

        if self.appointment_date:
            is_new = self.pk is None
            date_changed = is_new

            if self.pk is not None:
                old_appointment = Appointment.objects.filter(
                    pk=self.pk
                ).first()

                if old_appointment:
                    date_changed = (
                        old_appointment.appointment_date
                        != self.appointment_date
                    )
                else:
                    date_changed = True

            if date_changed and self.appointment_date <= timezone.now():
                raise ValidationError({
                    'appointment_date':
                    "La date du rendez-vous doit être future."
                })

    # Meta
    class Meta:
        ordering = ['appointment_date']

        constraints = [
            models.UniqueConstraint(
                fields=['doctor', 'appointment_date'],
                name='unique_doctor_appointment_date'
            )
        ]

    def __str__(self):
        return f"{self.doctor} - {self.patient} - {self.appointment_date}"
