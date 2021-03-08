from django.conf import settings
from django.db import models

# Create your models here.


class Quiz(models.Model):
    name = models.CharField(max_length=120, default="Name of the quiz")
    topic = models.CharField(max_length=120,  default="Topic of the quiz")
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    time_allowed = models.IntegerField(default=0, help_text="duration of the quiz in seconds")
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return f"Quiz-{self.name}-({self.topic})"

    def get_question(self):
        return self.question_set.all()


class Questions(models.Model):
    question = models.TextField(default="Questions")
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)


    def __str__(self):
        return self.question

    def get_answer(self):
        return self.answer_set.all()

    class Meta:
        verbose_name_plural = "Questions"


class Answer(models.Model):
    text = models.CharField(max_length=200, default="Answer")
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)


    def __str__(self):
        return f"Question:{self.question.question}|Answer:{self.text}|correct:{self.correct}"


class Result(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # profile = models.ImageField(upload_to=settings.MEDIA_ROOT, default='/static/img/profile.svg', blank =True)
    score = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username