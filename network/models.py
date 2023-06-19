
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.db.models import Sum




class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class User(AbstractUser):
    profile_pic = models.ImageField(upload_to='profile_pic/')
    bio = models.TextField(max_length=160, blank=True, null=True)
    cover = models.ImageField(upload_to='covers/', blank=True)
    role = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.username

    def serialize(self):
        return {
            'id': self.id,
            "username": self.username,
            "profile_pic": self.profile_pic.url,
            "first_name": self.first_name,
            "last_name": self.last_name
        }


###################################

class Post(models.Model):
    creater = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    date_created = models.DateTimeField(default=timezone.now)
    content_text = models.TextField(max_length=140, blank=True)
    content_image = models.ImageField(upload_to='posts/', blank=True)
    likers = models.ManyToManyField(User, blank=True, related_name='likes')
    savers = models.ManyToManyField(User, blank=True, related_name='saved')
    comment_count = models.IntegerField(default=0)
    average_rating = models.FloatField(default=0)  # Novo campo para a média das avaliações
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')

    def __str__(self):
        return f"Post ID: {self.id} (creater: {self.creater})"

    def img_url(self):
        return self.content_image.url

    def append(self, name, value):
        setattr(self, name, value)

###########################


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    commenter = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='commenters')
    comment_content = models.TextField(max_length=90)
    comment_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Post: {self.post} | Commenter: {self.commenter}"

    def serialize(self):
        return {
            "id": self.id,
            "commenter": self.commenter.serialize(),
            "body": self.comment_content,
            "timestamp": self.comment_time.strftime("%b %d %Y, %I:%M %p")
        }


class Follower(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='followers')
    followers = models.ManyToManyField(
        User, blank=True, related_name='following')

    def __str__(self):
        return f"User: {self.user}"


User = get_user_model()


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    rating_value = models.FloatField()

    def __str__(self):
        return f"Rating for post {self.post_id} by user {self.user_id}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Recalculate average rating for the post
        total_ratings = Rating.objects.filter(post=self.post).count()
        sum_ratings = Rating.objects.filter(
            post=self.post).aggregate(Sum('rating_value'))
        average_rating = sum_ratings['rating_value__sum'] / \
            total_ratings if total_ratings else 0

        # Update the average_rating field in the related Post model
        self.post.average_rating = average_rating
        self.post.total_ratings = total_ratings
        self.post.save()


