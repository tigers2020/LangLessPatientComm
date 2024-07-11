from django.db import models


# Define the Specialty model
class Specialty(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Each Specialty must have a unique name
    image = models.ImageField(upload_to='images/Specialty', blank=True,
                              null=True)  # Optional image field, images are saved to the specified directory

    class Meta:
        ordering = ['name']  # Default ordering is by name in ascending order

    def __str__(self):
        return self.name  # Display the name of the Specialty when represented as a string


# Define the Doctor model
class Doctor(models.Model):
    id = models.AutoField(
        primary_key=True)  # AutoField is an IntegerField that automatically increments, serving as primary key
    npi = models.CharField(max_length=20)
    ind_pac_id = models.CharField(max_length=20)
    ind_enrl_id = models.CharField(max_length=20)
    provider_last_name = models.CharField(max_length=100)
    provider_first_name = models.CharField(max_length=100)
    provider_middle_name = models.CharField(max_length=100, null=True, blank=True)
    suffix = models.CharField(max_length=10, null=True, blank=True)
    gender = models.CharField(max_length=10)
    credential = models.CharField(max_length=50, null=True, blank=True)
    med_school = models.CharField(max_length=200)
    grad_year = models.CharField(max_length=4)
    primary_specialty = models.ForeignKey(Specialty, related_name='primary_doctors', on_delete=models.SET_NULL,
                                          null=True)
    # Specialty is a foreign key; if a Specialty is deleted, all associated Doctors will have their primary_specialty field set to NULL
    secondary_specialty = models.CharField(max_length=200, null=True, blank=True)
    telehealth = models.CharField(max_length=10, null=True, blank=True)
    facility_name = models.CharField(max_length=200)
    org_pac_id = models.CharField(max_length=20)
    num_org_members = models.CharField(max_length=10)
    address_line_1 = models.CharField(max_length=200)
    address_line_2 = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=10)
    zip_code = models.CharField(max_length=10)
    telephone_number = models.CharField(max_length=20)
    individual_assignment = models.CharField(max_length=10)
    group_assignment = models.CharField(max_length=10)
    address_id = models.CharField(max_length=20)

    class Meta:
        ordering = ['provider_last_name',
                    'provider_first_name']  # Default ordering is by the provider's last name, then first name

    def __str__(self):
        return f"{self.provider_first_name} {self.provider_last_name}"  # Display the name of the Doctor when represented as a string
