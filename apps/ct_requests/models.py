
#!/usr/bin/python
# -*- encoding: utf-8 -*-
from django.db import models

from apps.register.models import Campus, User


class CTRDSeverity(models.Model):
    pk_ctrd_severity = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(null=False, max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "tb_ctrd_severity"


class CTRDPenalty(models.Model):
    pk_ctrd_penalty = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(null=False, max_length=320)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "tb_ctrd_penalty"


class CTRDChapter(models.Model):
    pk_ctrd_chapter = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(null=False, max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "tb_ctrd_chapter"


class CTRDSection(models.Model):
    pk_ctrd_section = models.AutoField(primary_key=True, unique=True)
    fk_ctrd_chapter = models.ForeignKey(
        CTRDChapter, db_column='fk_ctrd_chapter', on_delete=models.DO_NOTHING)
    name = models.CharField(null=False, max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "tb_ctrd_section"

class CTRDParagraph(models.Model):
    pk_ctrd_paragraph = models.AutoField(primary_key=True, unique=True)
    fk_ctrd_section = models.ForeignKey(
        CTRDSection, db_column='fk_ctrd_section', on_delete=models.DO_NOTHING)
    name = models.CharField(null=False, max_length=100)
    value = models.FloatField(default= 0.0)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "tb_ctrd_paragraph"


class CTRDRequest(models.Model):
    pk_ctrd_request = models.AutoField(primary_key=True, unique=True)
    title = models.CharField(null=False, max_length=128)
    fk_reporter = models.ForeignKey(
        User, db_column='fk_reporter', on_delete=models.DO_NOTHING)
    fk_campus = models.ForeignKey(
        Campus, db_column='fk_campus', on_delete=models.DO_NOTHING)
    fk_ctrd_severity = models.ForeignKey(
        CTRDSeverity, db_column='fk_ctrd_severity', on_delete=models.DO_NOTHING)
    fk_ctrd_penalty = models.ForeignKey(
        CTRDPenalty, db_column='fk_ctrd_penalty', on_delete=models.DO_NOTHING)
    fk_ctrd_chapter  = models.ForeignKey(
        CTRDChapter, db_column='fk_ctrd_chapter', on_delete=models.DO_NOTHING)
    fk_ctrd_section = models.ForeignKey(
        CTRDSection, db_column='fk_ctrd_section', on_delete=models.DO_NOTHING)
    fk_ctrd_paragraph = models.ForeignKey(
        CTRDParagraph, db_column='fk_ctrd_paragraph', on_delete=models.DO_NOTHING)
    date = models.DateField(null=False)
    status = models.IntegerField(null=False)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "tb_ctrd_request"



class CTRDStudentRequest(models.Model):
    pk_ctrd_student_request = models.AutoField(primary_key=True, unique=True)
    fk_ctrd_request = models.ForeignKey(
        CTRDRequest, db_column='fk_ctrd_request', on_delete=models.DO_NOTHING)
    fk_student = models.ForeignKey(
        User, db_column='fk_student', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.fk_ctrd_request

    class Meta:
        db_table = "tb_ctrd_student_request"


class CTRDComment(models.Model):
    pk_ctrd_comment = models.AutoField(primary_key=True, unique=True)
    fk_ctrd_request = models.ForeignKey(
        CTRDRequest, db_column='fk_ctrd_request', on_delete=models.DO_NOTHING)
    fk_user = models.ForeignKey(
        User, db_column='fk_user', on_delete=models.DO_NOTHING)
    date = models.DateField(null=False)
    comment = models.TextField()


    def __str__(self):
        return self.fk_ctrd_request

    class Meta:
        db_table = "tb_ctrd_comment"