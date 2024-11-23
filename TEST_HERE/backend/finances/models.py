from django.db import models

# Create your models here.
class DepositProduct(models.Model):
    # 금융상품 코드
    fin_prdt_cd = models.CharField(max_length=100)
    # 상품명
    fin_prdt_nm = models.CharField(max_length=100)
    # 금융회사 명
    kor_co_nm = models.CharField(max_length=100)
    # 금융회사 코드
    fin_co_no = models.CharField(max_length=100)
    # 가입방법
    join_way = models.CharField(max_length=100, default='', null=True)
    # 최고한도
    max_limit = models.CharField(max_length=100, default='', null=True)
    # 만기 후 이자율
    mtrt_int = models.CharField(max_length=100, null=True)
    # 가입대상
    join_member = models.CharField(max_length=100, default='', null=True)
    # 기타 유의사항
    etc_note = models.CharField(max_length=100, default='', null=True)


class SavingProduct(models.Model):
    # 금융상품 코드
    fin_prdt_cd = models.CharField(max_length=100)
    # 상품명
    fin_prdt_nm = models.CharField(max_length=100)
    # 금융회사 명
    kor_co_nm = models.CharField(max_length=100)
    # 금융회사 코드
    fin_co_no = models.CharField(max_length=100)
    # 가입방법
    join_way = models.CharField(max_length=100, default='', null=True)
    # 최고한도
    max_limit = models.CharField(max_length=100, default='', null=True)
    # 만기 후 이자율
    mtrt_int = models.CharField(max_length=100, default='', null=True)
    # 가입대상
    join_member = models.CharField(max_length=100, default='', null=True)
    # 기타 유의사항
    etc_note = models.CharField(max_length=100, default='', null=True)

