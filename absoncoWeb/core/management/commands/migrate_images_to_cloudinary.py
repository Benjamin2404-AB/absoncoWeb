# core/management/commands/migrate_images_to_cloudinary.py
from django.core.management.base import BaseCommand
from core.models import Item
import cloudinary.uploader
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Migrate local images to Cloudinary for Item model'

    def handle(self, *args, **kwargs):
        for item in Item.objects.all():
            if item.image:  # Check if image field is not null
                # For CloudinaryField, item.image is a string (public ID)
                # For old ImageField, it may be a local path (e.g., item_images/sample.jpg)
                image_value = str(item.image)
                # Check if the value looks like a local path (not a Cloudinary public ID)
                if not image_value.startswith('http') and os.path.exists(os.path.join(settings.MEDIA_ROOT, image_value)):
                    try:
                        # Upload local image to Cloudinary
                        result = cloudinary.uploader.upload(
                            os.path.join(settings.MEDIA_ROOT, image_value),
                            resource_type="image"
                        )
                        # Store the Cloudinary public ID
                        item.image = result['public_id']
                        item.save()
                        self.stdout.write(self.style.SUCCESS(f'Migrated image for {item.title} to {result["public_id"]}'))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'Failed to migrate {item.title}: {e}'))
                else:
                    self.stdout.write(self.style.WARNING(f'Skipped {item.title}: Already Cloudinary or invalid path'))
            else:
                self.stdout.write(self.style.WARNING(f'No image for {item.title}'))