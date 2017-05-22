from django.db import models
from userprofile.models import Doctor


class Post(models.Model):
    post_content = models.TextField()
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    doctor = models.ForeignKey(Doctor, models.DO_NOTHING, blank=False, null=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Medical Cases"

    @classmethod
    def list_posts(cls):
        return cls.objects.all()


class Photo(models.Model):
    image = models.ImageField(upload_to="posts", height_field=None, width_field=None)
    post = models.ForeignKey(Post, default=None)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)


class Comment(models.Model):
    comment_content = models.TextField()
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    post = models.ForeignKey(Post)
    doctor = models.ForeignKey(Doctor)


class Reply(models.Model):
    reply_content = models.TextField()
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    parent_comment_id = models.ForeignKey(Comment)
    post = models.ForeignKey(Post)
    doctor = models.ForeignKey(Doctor)




