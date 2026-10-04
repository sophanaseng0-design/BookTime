from collections import Counter
import csv
import os.path
from django.core.files.images import ImageFile
from django.core.management.base import BaseCommand
from django.template.defaultfilters import slugify
from main import models


class Command(BaseCommand):
    help = "Import products in BookTime"

    def add_arguments(self, parser):
        parser.add_argument("csvfile", type=open)  # ផ្លូវទៅកាន់ CSV File
        parser.add_argument("image_basedir", type=str)  # Folder រូបភាព

    def handle(self, *args, **options):
        self.stdout.write("Importing products")
        c = Counter()
        reader = csv.DictReader(options["csvfile"])

        for row in reader:
            # ១. បង្កើត ឬធ្វើបច្ចុប្បន្នភាពផលិតផល
            product, created = models.Product.objects.get_or_create(
                name=row["name"],
                price=row["price"],
            )
            product.description = row["description"]
            product.slug = slugify(row["name"])

            # ២. ដំណើរការស្លាក (Many-to-Many Tags)
            for import_tag in row["tags"].split("|"):
                tag, tag_created = models.ProductTag.objects.get_or_create(
                    name=import_tag.strip()
                )
                product.tags.add(tag)
                c.update({"tags": 1, "tags_created": 1 if tag_created else 0})

            # ៣. បន្ថែមរូបភាពផលិតផល (ប្រសិនបើមាន)
            image_path = os.path.join(options["image_basedir"], row["image_filename"])
            if os.path.exists(image_path):
                with open(image_path, "rb") as f:
                    image = models.ProductImage(
                        product=product,
                        image=ImageFile(f, name=row["image_filename"]),
                    )
                    image.save()
                    c["images"] += 1

            product.save()
            c["products"] += 1
            if created:
                c["products_created"] += 1

        # បោះពុម្ពលទ្ធផលសរុប
        self.stdout.write(
            "Products processed=%d (created=%d)"
            % (c["products"], c["products_created"])
        )
        self.stdout.write(
            "Tags processed=%d (created=%d)"
            % (c["tags"], c["tags_created"])
        )
        self.stdout.write("Images processed=%d" % c["images"])