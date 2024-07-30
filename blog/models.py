from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    objects = None
    name = models.CharField(max_length=30, verbose_name="Назва")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"


class Tag(models.Model):
    objects = None
    name = models.CharField(max_length=30, verbose_name="Назва")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"


class Post(models.Model):
    objects = None
    title = models.CharField(max_length=30, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Опис")
    published_date = models.DateTimeField(auto_created=True, verbose_name="Дата публікації")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категорія")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор", default='1')
    tags = models.ManyToManyField(Tag, verbose_name="Теги", blank=True)
    image = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Пости"


class Comment(models.Model):
    objects = None
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name="Пост")
    author = models.CharField(max_length=100, default='Guest', verbose_name="Автор")
    text = models.TextField(verbose_name="Текст")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    image = models.URLField(default='/static/blog/images/avatar.jpg', verbose_name="Зображення")
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

    def __str__(self):
        return self.text[:20]

    class Meta:
        verbose_name = "Коментар"
        verbose_name_plural = "Коментарі"


class Subscriber(models.Model):
    objects = None
    email = models.EmailField(unique=True, verbose_name="Електронна пошта")

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Підписник"
        verbose_name_plural = "Підписники"


class Profile(models.Model):
    objects = None
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Користувач")
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name="Аватар")
    bio = models.TextField(max_length=500, blank=True, verbose_name="Біографія")
    phone_number = models.CharField(max_length=15, blank=True, verbose_name="Номер телефону")
    location = models.CharField(max_length=30, blank=True, verbose_name="Місцезнаходження")

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Профіль"
        verbose_name_plural = "Профілі"


class PostImage(models.Model):
    objects = None
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images', verbose_name="Пост")
    image = models.ImageField(upload_to='post_images/', blank=True, null=True, verbose_name="Зображення")

    def __str__(self):
        return f"Image for {self.post.title}"

    class Meta:
        verbose_name = "Зображення Поста"
        verbose_name_plural = "Зображення Постів"
