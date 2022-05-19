import django_tables2 as tables
from .models import Items

class ItemsTable(tables.Table):
    class Meta:
        model = Items
        template_name = "django_tables2/bootstrap.html"
        fields = ('date_of_purchuase', 'item', 'quantity', 'price_per_quantity', 'price_per_all', 'seller', 'category_id', 'sub_category_01_id', 'item_pretty' )