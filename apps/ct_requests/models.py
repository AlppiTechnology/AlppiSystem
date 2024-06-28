
#!/usr/bin/python
# -*- encoding: utf-8 -*-
from django.db import models

from apps.register.models import Campus, User


class CTCIInternalNote(models.Model):
    pk_ct_ci_internal_note = models.AutoField(primary_key=True, unique=True)
    title = models.CharField(null=False, max_length=128)
    fk_reporter = models.ForeignKey(
        User, db_column='fk_reporter', on_delete=models.DO_NOTHING)
    fk_campus = models.ForeignKey(
        Campus, db_column='fk_campus', on_delete=models.DO_NOTHING)
    ct_ci_single_attach = models.CharField(null=False, max_length=30)
    ct_ci_deadline = models.DateField(null=False)
    ct_ci_student_deadline  = models.DateField(null=False)
    ct_ci_cal_statement = models.IntegerField(null=True)
    ct_ci_cmdt_statement = models.IntegerField(null=True)
    ct_ci_cmdt_answer = models.IntegerField(null=True)
    created = models.DateTimeField(auto_now_add=True, null=False)
    updated = models.DateTimeField(null=False)
    status = models.IntegerField(null=False)


    def __str__(self):
        return self.title

    class Meta:
        db_table = "tb_ct_ci_internal_note"


class CTCIStudentInternalNote(models.Model):
    pk_ct_ci_student_internal_note = models.AutoField(primary_key=True, unique=True)
    fk_ct_ci_internal_note = models.ForeignKey(
        CTCIInternalNote, db_column='fk_ct_ci_internal_note', on_delete=models.CASCADE)
    fk_student = models.ForeignKey(
        User, db_column='fk_student', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.fk_ct_ci_internal_note

    class Meta:
        db_table = "tb_ct_ci_student_internal_note"


class CTCIComment(models.Model):
    pk_ct_ci_comment = models.AutoField(primary_key=True, unique=True)
    fk_ct_ci_internal_note = models.ForeignKey(
        CTCIInternalNote, db_column='fk_ct_ci_internal_note', on_delete=models.CASCADE)
    fk_user = models.ForeignKey(
        User, db_column='fk_user', on_delete=models.DO_NOTHING)
    date = models.DateTimeField(auto_now_add=True,  null=False)
    comment = models.TextField()


    def __str__(self):
        return self.fk_ct_ci_internal_note

    class Meta:
        db_table = "tb_ct_ci_comment"

class CTCIRegulament(models.Model):
    pk_ct_ci_regulament = models.AutoField(primary_key=True, unique=True)
    fk_ct_ci_internal_note = models.ForeignKey(
        CTCIInternalNote, db_column='fk_ct_ci_internal_note', on_delete=models.CASCADE)
    regulament = models.CharField(null=False, max_length=30)

    def __str__(self):
        return self.regulament

    class Meta:
        db_table = "tb_ct_ci_regulament"