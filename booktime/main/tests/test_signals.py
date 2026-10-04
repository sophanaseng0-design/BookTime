from decimal import Decimal
from io import BytesIO
from PIL import Image

from django.core.files.images import ImageFile
from django.test import TestCase

from main import models


class TestSignal(TestCase):
    def test_thumbnails_are_generated_on_save(self):
        # ១. បង្កើត Product គំរូ
        product = models.Product(
            name="The cathedral and the bazaar",
            price=Decimal("10.00"),
        )
        product.save()

        # ២. ភ្ជាប់ ProductImage និង រក្សាទុក
        with open("main/fixtures/the-cathedral-the-bazaar.jpg", "rb") as f:
            image = models.ProductImage(
                product=product,
                image=ImageFile(f, name="tctb.jpg"),
            )
            with self.assertLogs("main", level="INFO") as cm:
                image.save()
                self.assertGreaterEqual(len(cm.output), 1)

        # ៣. ទាញយកទិន្នន័យ Thumbnail ពី DB មកផ្ទៀងផ្ទាត់
        image.refresh_from_db()
        thumb_bytes = image.thumbnail.read()

        # ប្រើ Pillow ដើម្បីបើក Thumbnail
        thumb_image = Image.open(BytesIO(thumb_bytes))

        # # 1. ពិនិត្យមើលថា Thumbnail ត្រូវបានបង្កើតឡើង (មិនមែន None)
        self.assertIsNotNone(thumb_image)

        # # 2. ពិនិត្យមើលទំហំថាមិនលើសពី 300x300
        self.assertLessEqual(thumb_image.width, 300)
        self.assertLessEqual(thumb_image.height, 300)

        # # 3. ពិនិត្យមើល Format ថាជា JPEG
        self.assertEqual(thumb_image.format, "JPEG")

        # # 4. លុបរូបភាពចេញ (Cleanup)
        image.thumbnail.delete(save=False)
        image.image.delete(save=False)


class TestModel(TestCase):
    def test_active_manager_works(self):
        # បង្កើតទិន្នន័យសាកល្បងទី ១ (active = True)
        models.Product.objects.create(
            name="The cathedral and the bazaar",
            price=Decimal("10.00")
        )

        # បង្កើតទិន្នន័យសាកល្បងទី ២ (active = True)
        models.Product.objects.create(
            name="Pride and Prejudice",
            price=Decimal("2.00")
        )

        # បង្កើតទិន្នន័យសាកល្បងទី ៣ (active = False)
        models.Product.objects.create(
            name="A Tale of Two Cities",
            price=Decimal("2.00"),
            active=False
        )

        # ផ្ទៀងផ្ទាត់ថា Product.objects.active() ទាញបានតែ ២ ផលិផលប៉ុណ្ណោះ
        self.assertEqual(len(models.Product.objects.active()), 2)