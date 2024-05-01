#!/usr/bin/python
# -*- encoding: utf-8 -*-
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from apps.register.manager import CustomUserManager



class FederativeUnit(models.Model):
    pk_fu = models.AutoField(primary_key=True, unique=True)
    acronym = models.CharField(null=False, max_length=2)
    fu_name = models.CharField(null=False, max_length=50)
    fu_code = models.IntegerField(null=False)

    def __str__(self):
        return self.fu_name
    
    class Meta:
        db_table = "tb_federative_unit"

class City(models.Model):
    pk_city = models.AutoField(primary_key=True, unique=True)
    city_name = models.CharField(null=False, max_length=50)
    fk_fu = models.ForeignKey(FederativeUnit, db_column='fk_fu', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.city_name
    
    class Meta:
        db_table = "tb_city"

class Campus(models.Model):
    pk_campus = models.AutoField(primary_key=True, unique=True)
    cnpj = models.CharField(null=False,  max_length=14)
    campus_code = models.IntegerField(null=False, unique=True)
    campus_name = models.CharField(null=False, max_length=254)
    trading_name = models.CharField(null=False, max_length=100)
    company_name = models.CharField(null=False, max_length=100)
    public_place = models.CharField(null=False, max_length=50)
    fk_city = models.ForeignKey(City, db_column='fk_city', on_delete=models.DO_NOTHING)
    fk_fu = models.ForeignKey(FederativeUnit, db_column='fk_fu', on_delete=models.DO_NOTHING)
    email = models.EmailField(max_length=150, null=False)
    phone =  models.CharField(null=False, max_length=25)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    edited = models.DateTimeField(editable=True)
    status = models.IntegerField(null=False)

    def __str__(self):
        return self.campus_name
    
    class Meta:
        db_table = "tb_campus"


class User(AbstractUser, PermissionsMixin):
    first_name = False
    last_name = False


    # groups = models.ManyToManyField(Group, related_name='user_groups', null=True)
    # user_permissions = models.ManyToManyField(Permission, related_name='user_permissions', null=True)
    pk_user = models.AutoField(primary_key=True, unique=True)
    registration = models.CharField(unique=True, null=False, max_length=6)
    cpf = models.CharField(null=False,  max_length=14)
    password = models.TextField(null=False)
    fk_campus = models.ForeignKey(Campus, db_column='fk_campus', on_delete=models.DO_NOTHING, null=True)
    username = models.CharField(null=False, max_length=254)
    phone = models.CharField(null=False, max_length=100)
    email = models.CharField(null=False, max_length=50)
    fk_city = models.ForeignKey(City, db_column='fk_city', on_delete=models.DO_NOTHING, null=True)
    fk_fu = models.ForeignKey(FederativeUnit, db_column='fk_fu', on_delete=models.DO_NOTHING, null=True)
    sex = models.CharField(null=False, max_length=1)
    birth_date =  models.DateField(null=False)
    created = models.DateTimeField(auto_now_add=True, editable=True)
    edited = models.DateTimeField(editable=True)
    is_superuser =  models.BooleanField(null=False)
    is_staff = models.BooleanField(null=False)


    USERNAME_FIELD = 'registration'
    REQUIRED_FIELDS = []


    objects = CustomUserManager()

    def __str__(self):
        return self.username
    
    class Meta:
        db_table = "tb_user"
