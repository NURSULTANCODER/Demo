from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from PIL import Image
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime

from django.urls import reverse


class User(AbstractUser):
    pass



class Review(models.Model):
    rating = models.IntegerField(default=0)
    employee = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    content = models.TextField(default='')
    date_posted = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"Review to {self.employee.username}"

    class Meta:
        ordering = ['-date_posted']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_user_grade()

    def update_user_grade(self):
        # Calculate average rating of all reviews for the user
        reviews = Review.objects.filter(employee=self.employee)
        if reviews.exists():
            total_rating = sum(review.rating for review in reviews)
            average_rating = total_rating / reviews.count()
            self.employee.profile.grade = round(average_rating, 1)
            self.employee.profile.save()

    def get_absolute_url(self):
        return reverse('users:profile', kwargs={'username': self.employee.username})


class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    grade = models.DecimalField(max_digits=5, decimal_places=1, default=0.0)


    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


