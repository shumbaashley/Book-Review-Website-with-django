from django.contrib.auth.models import User
from django.urls import reverse
from django.db import models
from django.utils.timezone import now
from datetime import datetime
from django.template.defaultfilters import slugify


# Create your models here.

class Editor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="editor")
    image = models.ImageField(upload_to='editor-images/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    facebook = models.URLField(max_length=64, blank=True, null=True)
    instagram = models.URLField(max_length=64, blank=True, null=True)
    twitter = models.URLField(max_length=64, blank=True, null=True)
    phone = models.CharField(max_length=64, blank=True, null=True)
    email = models.EmailField(max_length=64, blank=True, null=True)
    web = models.CharField(max_length=64, blank=True, null=True)
    link = models.URLField(max_length=64, blank=True, null=True)
    slug = models.SlugField(max_length=150, null = True, blank = True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.user.username)

        super(Editor, self).save(*args, **kwargs)


    def __str__(self):
        return  f"{self.user}"

class Comment(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True)
    email = models.EmailField(max_length=64, unique=True, null=True)
    message = models.TextField(max_length=300, blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True, default=datetime.now())

    def __str__(self):
        return f"{self.name} - {self.message}"
class Book(models.Model):
    title = models.CharField(max_length=150)
    authors = models.ManyToManyField("Author", related_name="books")
    image = models.ImageField(upload_to='book-images/', blank=True, null=True)
    genre = models.CharField(max_length=64, blank=True, null=True)
    review = models.TextField(blank=True, null=True)
    reviewed_by = models.ForeignKey(Editor, blank=True, null=True, related_name="reviews", on_delete=models.CASCADE)
    date_reviewed = models.DateTimeField(blank=True, null=True, default=datetime.now())
    is_favourite = models.BooleanField(default=False, verbose_name="Favourite?")
    comments = models.ManyToManyField(Comment, related_name="feedback", blank=True)
    slug = models.SlugField(max_length=150, null = True, blank = True)
    audible = models.URLField(max_length=500, null=True, blank=True)
    kindle = models.URLField(max_length=500, null=True, blank=True)

    def __str__(self):
        return "{} by {}".format(self.title, self.list_authors())
    

    def list_authors(self):
        return ", ".join([author.name for author in self.authors.all()])

    def save(self, *args, **kwargs):
        if (self.review and self.date_reviewed is None):
            self.date_reviewed = now()

        if not self.id:
            self.slug = slugify(self.title)

        super(Book, self).save(*args, **kwargs)

class Author(models.Model):
    name = models.CharField(max_length=70, help_text="Use real name", unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('author-detail', kwargs={'pk', self.pk})

