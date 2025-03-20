from django.db import models

class Section(models.Model):
    """
    Represents a section of the boat. One section may contain multiple compartments.
    """
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Sections'
        ordering = ['name']

class Compartment(models.Model):
    """
    Represents a compartment within a section of the boat.
    """
    section = models.ForeignKey(Section, related_name='compartments', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.section.name} - {self.name}"

    class Meta:
        unique_together = ('section', 'name')
        verbose_name_plural = 'Compartments'
        ordering = ['section__name', 'name']

class MainCategory(models.Model):
    """
    Represents a main category of items in the inventory.
    """
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Main Categories'
        ordering = ['name']

class SubCategory(models.Model):
    """
    Represents a subcategory of items in the inventory, linked to a main category.
    """
    main_category = models.ForeignKey(MainCategory, related_name='subcategories', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.main_category.name} - {self.name}"

    class Meta:
        unique_together = ('main_category', 'name')
        verbose_name_plural = 'Subcategories'
        ordering = ['main_category__name', 'name']

class Item(models.Model):
    """
    Represents an item in the inventory, linked to a subcategory.
    """
    subcategory = models.ForeignKey(SubCategory, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name