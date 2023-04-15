from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
import datetime

class Avthor(models.Model):
    avthorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAvthor = models.SmallIntegerField(default=0)

    def update_rating(self):
     postRat = self.post_set.all().aggregate(postrating=Sum('rating'))
     pRat = 0
     pRat += postRat.get('postrating')

     commentRat =self.avthorUser.comment_set.all().aggregate(commentRating=Sum('rating'))
     cRat = 0
     cRat += commentRat.get('commentRating')
     self.ratingAvthor = pRat*3 +cRat
     self.save()

class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

class Post(models.Model):
  avthor = models.ForeignKey(Avthor, on_delete=models.CASCADE)

  NEWS ='NW'
  ARTICLE = 'AR'
  CATEGORY_CHOICES=(
      (NEWS, 'Новости'),
      (ARTICLE, 'Статьи'),
  )
  categoryType = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=ARTICLE)
  dateCreation = models.DateTimeField(auto_now_add=True)
  dateCreation.editable = True
  postCategory = models.ManyToManyField(Category, through='PostCategory')
  title = models.CharField(max_length=128)
  text = models.TextField()
  rating = models.SmallIntegerField(default=0)


  def like(self):
      self.rating += 1
      self.save()

  def dislike(self):
      self.rating -= 1
      self.save()

  def preview(self):
      return self.text[0:123]+'...'

  def get_absolute_url(self):
      return f'/article/{self.id}'

  #def __str__(self):
      #return f'{self.name.title()}'

class PostCategory(models.Model):
   postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
   categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dateCration = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)


    def __str__(self):

        return self.commentUser.username

    def like(self):
        self.rating+=1
        self.save()

    def dislike(self):
        self.rating-=1
        self.save()








