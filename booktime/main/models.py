from django.db import models

class ActiveManager(models.Manager):
    def active(self):
        return self.filter(active=True)

# បន្ថែម Manager សម្រាប់ Natural Key
class ProductTagManager(models.Manager):
    def get_by_natural_key(self, slug):
        return self.get(slug=slug)

class ProductTag(models.Model):
    name = models.CharField(max_length=40)
    slug = models.SlugField(max_length=48)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)

    objects = ProductTagManager()  # ភ្ជាប់ Manager ត្រង់នេះ

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.slug,)

class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=48)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    in_stock = models.BooleanField(default=True)
    active = models.BooleanField(default=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    tags = models.ManyToManyField(ProductTag, blank=True)

    objects = ActiveManager()

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="product-images")
    thumbnail = models.ImageField(upload_to="product-thumbnails", null=True, blank=True)

    def __str__(self):
        return f"Image for {self.product.name}"