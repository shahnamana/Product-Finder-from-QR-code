from django.contrib import admin
from .models import ProductDet, Address

# Register your models here.

class CustomerAddressInline(admin.StackedInline):
    model = Address

@admin.register(ProductDet)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["product_id"]
    inlines = [CustomerAddressInline]

    search_fields = ["product_id"]
    fields = ("product_id", "product_image",'product_name')
