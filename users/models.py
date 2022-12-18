from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    """
    아래는 enum type으로 모델 생성하는 방법
    models.TextChoices 상속하는 class 생성 후 models.*field의 choices 인자에 넣어준다.

    MALE = ("male", "Male")
    0번 인덱스는 실제 DB에 들어갈 텍스트, 1번 인덱스는 admin panel에 보여질 텍스트
    """

    class GenderChoices(models.TextChoices):
        MALE = ("male", "Male")
        FEMALE = ("female", "Female")

    class LanguageChoices(models.TextChoices):
        KR = ("kr", "Korean")
        EN = ("en", "English")

    class CurrencyChoices(models.TextChoices):
        KRW = "krw", "Korean won"
        USD = "usd", "Dollar"

    first_name = models.CharField(max_length=150, editable=False)
    last_name = models.CharField(max_length=150, editable=False)
    name = models.CharField(max_length=120, default="")
    is_host = models.BooleanField(default=False)
    ### blank=True => not required(can be empty)
    avatar = models.URLField(blank=True)
    gender = models.CharField(max_length=10, choices=GenderChoices.choices)
    language = models.CharField(max_length=2, choices=LanguageChoices.choices)
    currency = models.CharField(max_length=3, choices=CurrencyChoices.choices)
