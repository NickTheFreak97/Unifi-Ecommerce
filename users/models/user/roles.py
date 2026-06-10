from django.db import models

# <enum_case> = <db_value>, <display_name>
class Role(models.TextChoices):
    webmaster = "webmaster", "Webmaster"
    customer = "customer", "Customer"
    staff = "staff", "Staff"
