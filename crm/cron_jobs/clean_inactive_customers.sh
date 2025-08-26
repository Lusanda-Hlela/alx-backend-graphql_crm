#!/bin/bash
# Script to delete customers with no orders in the past year and log the result

# Move to project root (where manage.py is)
cd "$(dirname "${BASH_SOURCE[0]}")/../.."

# Set Django environment variables
export DJANGO_SETTINGS_MODULE=alx_backend_graphql_crm.settings
export PYTHONPATH=$PWD

# Run Django shell command
COUNT=$(python manage.py shell -c "
from crm.models import Customer
from django.utils import timezone
from datetime import timedelta

one_year_ago = timezone.now() - timedelta(days=365)

# Customers who have NO orders in the past year
to_delete = Customer.objects.exclude(order__order_date__gte=one_year_ago)

deleted, _ = to_delete.delete()
print(deleted)
")

