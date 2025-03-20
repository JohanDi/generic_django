from django.contrib import admin

from .models import Section, Compartment, MainCategory, SubCategory, Item

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')

@admin.register(Compartment)
class CompartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'section', 'description')
    search_fields = ('name', 'section__name', 'description')
    list_filter = ('section',)

@admin.register(MainCategory)
class MainCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'main_category', 'description')
    search_fields = ('name', 'main_category__name', 'description')
    list_filter = ('main_category',)

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'subcategory', 'description')
    search_fields = ('name', 'subcategory__name', 'description')
    list_filter = ('subcategory',)


