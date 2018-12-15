# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from passlib.hash import pbkdf2_sha256

class Clnts(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=30)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    ddate_created = models.DateTimeField()

    class Meta:
        db_table = 'clients'

    @classmethod
    def create(cls, name, ddate_created):
        client_new = cls(name=name,user=Users.objects.filter(ddate_created= ddate_created).values('id'),
                         ddate_created=ddate_created)
        client_new.save()
        return client_new


class Logusers(models.Model):
    id = models.BigAutoField(primary_key=True)
    uid = models.ForeignKey('Users', models.DO_NOTHING, db_column='uid')
    mail = models.EmailField(max_length=30)
    pass_field = models.CharField(db_column='pass', max_length=30)  # Field renamed because it was a Python reserved word.
    ddate_created = models.DateTimeField()

    class Meta:
        db_table = 'logusers'


class Permissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=30)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    perm = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        db_table = 'permissions'


class Test1(models.Model):
    id = models.IntegerField(primary_key=True)

    class Meta:
        db_table = 'test1'


class Testt(models.Model):
    id = models.BigIntegerField(primary_key=True)

    class Meta:
        db_table = 'testt'


class Users(models.Model):
    id = models.BigAutoField(primary_key=True)
    mail = models.CharField(max_length=30)
    pass_field = models.CharField(db_column='pass', max_length=256)  # Field renamed because it was a Python reserved word.
    ddate_created = models.DateTimeField()
    img = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'users'

    @classmethod
    def create(cls,mail,pass_field,ddate_created):
        user_new = cls(mail=mail,pass_field=pass_field,ddate_created=ddate_created)
        user_new.save()
        return user_new

    def verify_password(self, raw_pass):
        return pbkdf2_sha256.verify(raw_pass, self.pass_field)


class Tours(models.Model):
    id = models.BigAutoField(primary_key=True)
    country = models.CharField(max_length=15)
    place = models.CharField(max_length=15)
    description = models.CharField(max_length=300)

    class Meta:
        db_table = 'tours'
