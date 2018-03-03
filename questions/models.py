from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class ModelManager(models.Manager):
    def new(self):
        return self.order_by('-date')

    def hot(self):
        return self.order_by('-likes')


class Profile(models.Model):
    user = models.OneToOneField(User)
    # nickname = models.TextField()
    # avatar = models.ImageField(default=)

    def __str__(self):
        return self.user.username


class Question(models.Model):

    title = models.CharField(max_length=200)
    text = models.TextField()
    likes = models.IntegerField(blank=True, null=True)
    dislikes = models.IntegerField(blank=True, null=True)
    answer_count = models.IntegerField(default=0)
    date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(Profile, blank=True, null=True)
    objects = ModelManager()

    def like(self):
        self.likes += 1
        self.save()

    def dislike(self):
        self.dislikes += 1
        self.save()


    def make_tags(self, request):
        tags = request.POST["question_tags"].split(", ")

        for tag in tags:
            try:
                current_tag = Tag.objects.get(name=tag)

            except:
                current_tag = Tag(name=tag)
                current_tag.save()
            self.save()
            current_tag.question.add(self)


        # self.save()



class Answer(models.Model):

    text = models.TextField()
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, related_name="answers")
    user = models.ForeignKey(Profile, blank=True, null=True)


class Tag(models.Model):

    name = models.TextField()
    question = models.ManyToManyField(Question, related_name="tags", related_query_name="tag")