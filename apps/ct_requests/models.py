
#!/usr/bin/python
# -*- encoding: utf-8 -*-
from django.db import models

from apps.register.models import Campus, User


class DRCTSeverity(models.Model):
    pk_drct_severity = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(null=False, max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "tb_drct_severity"


class DRCTPenalty(models.Model):
    pk_drct_penalty = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(null=False, max_length=320)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "tb_drct_penalty"


class DRCTChapter(models.Model):
    pk_drct_chapter = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(null=False, max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "tb_drct_chapter"


class DRCTSection(models.Model):
    pk_drct_section = models.AutoField(primary_key=True, unique=True)
    fk_drct_chapter = models.ForeignKey(
        DRCTChapter, db_column='fk_drct_chapter', on_delete=models.DO_NOTHING)
    name = models.CharField(null=False, max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "tb_drct_section"


class DRCTParagraph(models.Model):
    pk_drct_paragraph = models.AutoField(primary_key=True, unique=True)
    fk_drct_section = models.ForeignKey(
        DRCTSection, db_column='fk_drct_section', on_delete=models.DO_NOTHING)
    name = models.CharField(null=False, max_length=100)
    value = models.FloatField(default= 0.0)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "tb_drct_paragraph"


class DRCTRequest(models.Model):
    pk_drct_request = models.AutoField(primary_key=True, unique=True)
    title = models.CharField(null=False, max_length=128)
    fk_reporter = models.ForeignKey(
        User, db_column='fk_reporter', on_delete=models.DO_NOTHING)
    fk_campus = models.ForeignKey(
        Campus, db_column='fk_campus', on_delete=models.DO_NOTHING)
    fk_drct_severity = models.ForeignKey(
        DRCTSeverity, db_column='fk_drct_severity', on_delete=models.DO_NOTHING)
    fk_drct_penalty = models.ForeignKey(
        DRCTPenalty, db_column='fk_drct_penalty', on_delete=models.DO_NOTHING)
    fk_drct_chapter  = models.ForeignKey(
        DRCTChapter, db_column='fk_drct_chapter', on_delete=models.DO_NOTHING)
    fk_drct_section = models.ForeignKey(
        DRCTSection, db_column='fk_drct_section', on_delete=models.DO_NOTHING)
    fk_drct_paragraph = models.ForeignKey(
        DRCTParagraph, db_column='fk_drct_paragraph', on_delete=models.DO_NOTHING)
    date = models.DateField(null=False)
    status = models.IntegerField(null=False)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "tb_drct_request"


class DRCTStudentRequest(models.Model):
    pk_drct_student_request = models.AutoField(primary_key=True, unique=True)
    fk_drct_request = models.ForeignKey(
        DRCTRequest, db_column='fk_drct_request', on_delete=models.DO_NOTHING)
    fk_student = models.ForeignKey(
        User, db_column='fk_student', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.fk_drct_request

    class Meta:
        db_table = "tb_drct_student_request"


class DRCTComment(models.Model):
    pk_drct_comment = models.AutoField(primary_key=True, unique=True)
    fk_drct_request = models.ForeignKey(
        DRCTRequest, db_column='fk_drct_request', on_delete=models.DO_NOTHING)
    fk_user = models.ForeignKey(
        User, db_column='fk_user', on_delete=models.DO_NOTHING)
    date = models.DateField(null=False)
    comment = models.TextField()


    def __str__(self):
        return self.fk_drct_request

    class Meta:
        db_table = "tb_drct_comment"