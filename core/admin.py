from django.contrib import admin

from MVC.models import Category, Listing, UserBase

admin.site.register(UserBase)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name','slug','details']
    prepopulated_fields = {'slug':('name',)}

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ['name','details','slug','price','in_stock','for_sale','date_added','date_updated']
    list_filter = ['need_prescription','in_stock','for_sale']
    list_editable = ['price','in_stock','for_sale']
    prepopulated_fields = {'slug':('name',)} 