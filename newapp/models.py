from django.contrib.auth.models import User
from django.db import models


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    authorRating = models.SmallIntegerField(default=0)

    def update_rating(self):
        rating = 0
        for article in Post.objects.filter(postAuthor=self, postType='AR'):
            # суммарный рейтинг каждой статьи автора умножается на 3
            # Не поста, а статьи - значит, без новостей
            rating += article.postRating * 3
            for authorPostsRating in Comment.objects.filter(commentPost=article.id):
                # суммарный рейтинг всех комментариев к статьям автора
                # Не к постам, а к статьям - значит, без новостей
                rating += authorPostsRating.commentRating

        for authorComments in Comment.objects.filter(commentUser=self.authorUser):
            # суммарный рейтинг всех комментариев автора
            rating += authorComments.commentRating

        self.authorRating = rating
        self.save()


class Category(models.Model):
    categoryName = models.CharField(max_length=255, unique=True)


class Post(models.Model):
    postAuthor = models.ForeignKey(Author, on_delete=models.CASCADE)

    NEWS = 'NE'
    ARTICLE = 'AR'
    TYPE_CHOICES = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    )
    postType = models.CharField(max_length=2, choices=TYPE_CHOICES, default=ARTICLE)
    postDTCreate = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    postTitle = models.CharField(max_length=255)
    postText = models.TextField()
    postRating = models.SmallIntegerField(default=0)

    def like(self):
        self.postRating += 1
        self.save()

    def dislike(self):
        self.postRating -= 1
        self.save()

    def preview(self):
        return self.postText[:124] + '...'


class PostCategory(models.Model):
    pcPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    pcCategory = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    commentText = models.TextField()
    commentDTCreate = models.DateTimeField(auto_now_add=True)
    commentRating = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.commentUser.username

    def like(self):
        self.commentRating += 1
        self.save()

    def dislike(self):
        self.commentRating -= 1
        self.save()
