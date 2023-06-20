from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
import datetime

class Avthor(models.Model):
    avthorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAvthor = models.SmallIntegerField(default=0)

    def __str__(self):
     return f'{self.avthorUser}'

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
    subscriber = models.ManyToManyField(User, through='CategorySubscriber' )






class Post(models.Model):
  avthor = models.ForeignKey(Avthor, on_delete=models.CASCADE)

  NEWS ='NW'
  ARTICLE = 'AR'
  CATEGORY_CHOICES=(
      (NEWS, 'Новости'),
      (ARTICLE, 'Статьи'),
  )
  categoryType = models.CharField(Category,max_length=2, choices=CATEGORY_CHOICES, default=ARTICLE)
  dateCreation = models.DateTimeField(auto_now_add=True)
  dateCreation.editable = True
  PostCategory = models.ManyToManyField(Category, through='PostCategory')
  title = models.CharField(max_length=128)
  text = models.TextField()
  rating = models.SmallIntegerField(default=0)
  #user = models.ForeignKey(User, on_delete=models.CASCADE)





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
   PostCategory = models.ForeignKey(Post, on_delete=models.CASCADE)
   category = models.ForeignKey(Category, on_delete=models.CASCADE)





class CategorySubscriber(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} is subscribed to category {self.category}'

class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dateCreation= models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)


    def __str__(self):

        return self.commentUser.username

    def like(self):
        self.rating+=1
        self.save()

    def dislike(self):
        self.rating-=1
        self.save()


class Malling(models.Model):
    date = models.DateField(
        default=datetime,
    )
    user_name = models.CharField(
        max_length=200
    )
    message = models.TextField()

    def __str__(self):
        return f'{self.user_name}: {self.message}'




