'''Модели приложения'''
from django.db import models
from django.urls import reverse
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from app.functions import image_upload_path


class BaseModel(models.Model):
    '''Базовая абстрактная модель'''
    class Meta():
        abstract = True
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class Category(BaseModel):
    '''Модель категории записи'''
    class Meta():
        db_table = 'categories'
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
    name = models.CharField(max_length=255, blank=False)
    title = models.CharField(max_length=255, blank=False)
    snippet = models.TextField(max_length=255, blank=True)
    slug = models.SlugField(unique=True, blank=False)
    menu = models.BooleanField(default=True)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        """Генерация канонического URL для каждого объекта модели"""
        return reverse("category_detail", kwargs={"slug": self.slug})


class PublishedPostManager(models.Manager):
    """Менеджер опубликованных постов"""
    def get_queryset(self):
        queryset = (
            super()
            .get_queryset()
            .filter(publish=True)
            .order_by('-date_created')
            .select_related('category', )
        )
        return queryset


class Post(BaseModel):
    '''Модель записи'''
    class Meta():
        db_table = 'posts'
        ordering = ['-date_created']
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'
    title = models.CharField(max_length=255, blank=False)
    content = models.JSONField(default=dict)
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='posts'
    )
    slug = models.SlugField(unique=True, blank=False)
    publish = models.BooleanField(default=False)

    objects = models.Manager()
    published = PublishedPostManager()

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        """Генерация канонического URL для каждого объекта модели"""
        return reverse("post_detail", kwargs={"slug": self.slug})

    def parent_pk(self):
        return self.id


class PostImage(BaseModel):
    class Meta():
        db_table = 'post_images'
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = ProcessedImageField(
        upload_to=image_upload_path,
        processors=[ResizeToFill(818, 460)],
        format='JPEG',
        options={'quality': 70}
    )

    def __str__(self):
        return self.image.url

    def parent_pk(self):
        return self.post.id
