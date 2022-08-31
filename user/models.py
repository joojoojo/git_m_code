from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

class User(AbstractBaseUser):
    """
        유저 이름      -> 실제 사용자 이름
        유저 이메일 주소 -> 회원가입할때 사용하는 아이디
        유저 비밀번호    -> 디폴트 쓰자
    """

    name = models.CharField(max_length=10)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.email

    class Meta:
        db_table = "User"
