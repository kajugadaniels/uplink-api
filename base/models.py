from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

class Category(models.Model):
    """
    Represents a category with a human-readable name and an automatically generated slug.

    Attributes:
        name (str): The name of the category.
        slug (str): A URL-friendly version of the category name, generated automatically.
    """
    name = models.CharField(max_length=255, unique=True, help_text="Enter the name of the category.")
    slug = models.SlugField(max_length=255, unique=True, editable=False, help_text="Automatically generated from the category name.")

    def save(self, *args, **kwargs):
        """
        Overrides the default save method to automatically generate/update the slug from the name.
        When the category name is changed, the slug is regenerated using the slugify function.
        """
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        """
        Returns a string representation of the category.
        """
        return self.name

    class Meta:
        verbose_name_plural = _('Categories')