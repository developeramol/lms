from django.contrib import admin
from .models import user_admin, user_client, lead_sources, lead_status, create_lead, Customer

admin.site.register(user_admin)
admin.site.register(user_client)
admin.site.register(lead_status)
admin.site.register(lead_sources)
admin.site.register(create_lead)
admin.site.register(Customer)
