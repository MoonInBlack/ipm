from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name = 'Наименование')
    slug = models.CharField(max_length=100, unique=True)

    def save(self, *args, **kwargs):  # формирование слага
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Size(models.Model):
    name = models.CharField(max_length=20, verbose_name = 'Размер')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Размер'
        verbose_name_plural = 'Размеры'


# класс для показа остатка по размерам
class ProductSize(models.Model):
    product = models.ForeignKey(
        "Product", on_delete=models.CASCADE, related_name="product_size"
    )
    size = models.ForeignKey(Size, on_delete=models.CASCADE, verbose_name = 'Размер')
    stock = models.PositiveIntegerField(default=0, verbose_name = 'Остаток')

    def __str__(self):
        return f"{self.size.name} ({self.stock} in stock) for {self.product.name}"
    
    class Meta:
        verbose_name = 'Выбор размера'
        verbose_name_plural = 'Выбор размеров'


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name = 'Наименование')
    slug = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products", verbose_name = 'Категория'
    )
    nationality = models.CharField(max_length=100, verbose_name = 'Национальность')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name = 'Стоимость')
    description = models.TextField(blank=True, verbose_name = 'Описание')
    main_image = models.ImageField(upload_to="products/main/", verbose_name = 'Карточка')
    created_at = models.DateField(auto_now_add=True, verbose_name = 'Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name = 'Дата изменения')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


# класс для вывода картинок на странице товара
class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="products/extra/", verbose_name = 'Фото')

    class Meta:
        verbose_name = 'Выбор изображения'
        verbose_name_plural = 'Выбор изображений'
