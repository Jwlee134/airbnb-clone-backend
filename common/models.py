from django.db import models

# Create your models here.


class Common(models.Model):

    """Common Model Definition"""

    created = models.DateTimeField(auto_now_add=True)  # model이 처음 생성될 때 갱신
    updated = models.DateTimeField(auto_now=True)  # model이 저장될때마다 갱신

    """ 
        아래 코드를 보는 순간 django는 Common이 db나 admin panel이 포함되는 것이 아닌
        재사용하기 위한 blueprint class라는 것을 알게 된다.
    """

    class Meta:
        abstract = True
