
#!/usr/bin/python
# -*- encoding: utf-8 -*-
from django.db import models
from apps.register.models import Campus, User

# Grau
class SchoolLevel(models.Model):
    pk_school_level = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(null=False, max_length=25)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "tb_school_level"

# Serie
class SchoolGrade(models.Model):
    pk_school_grade = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(null=False, max_length=25)
    fk_school_level = models.ForeignKey(
        SchoolLevel, db_column='fk_school_level', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "tb_school_grade"

# turno
class Shift(models.Model):
    pk_shift = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(null=False, max_length=15)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "tb_shift"


class NoteType(models.Model):
    pk_note_type = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(null=False, max_length=15)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "tb_note_type"


class AbsenceType(models.Model):
    pk_absence_type = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(null=False, max_length=15)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "tb_absence_type"

# Tipo Etapa
class TermType(models.Model):
    pk_term_type = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(null=False, max_length=15)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "tb_term_type"

# Etapa
class Term(models.Model):
    pk_term_type = models.AutoField(primary_key=True, unique=True)
    fk_term_type = models.ForeignKey(
        TermType, db_column='fk_term_type', on_delete=models.CASCADE)
    name = models.CharField(null=False, max_length=15)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "tb_term"


class SchoolYear(models.Model):
    pk_school_year = models.AutoField(primary_key=True, unique=True)
    fk_campus = models.ForeignKey(
        Campus, db_column='fk_campus', on_delete=models.DO_NOTHING)
    fk_term_type = models.ForeignKey(
        TermType, db_column='fk_term_type', on_delete=models.DO_NOTHING)
    year = models.CharField(null=False, max_length=4)
    created = models.DateTimeField(auto_now_add=True, editable=True)
    edited = models.DateTimeField(editable=True)
    skill = models.IntegerField(null=False)
    total_grade = models.FloatField(null=False)
    average_grade = models.FloatField(null=False)
    status = models.IntegerField(null=False)

    def __str__(self):
        return self.year

    class Meta:
        db_table = "tb_school_year"


class SchoolYearDate(models.Model):
    pk_school_year_date = models.AutoField(primary_key=True, unique=True)
    fk_school_year = models.ForeignKey(
        SchoolYear, db_column='fk_school_year', on_delete=models.CASCADE)
    fk_term = models.ForeignKey(
        Term, db_column='fk_term', on_delete=models.DO_NOTHING)
    init_date = models.DateField(editable=True)
    final_date = models.DateField(editable=True)
    grade = models.FloatField(null=False)

    def __str__(self):
        return str(self.fk_school_year.year) + ' ' + str(self.fk_term)

    class Meta:
        db_table = "tb_school_year_date"


class ClassSetting(models.Model):
    pk_class_setting = models.AutoField(primary_key=True, unique=True)
    fk_campus = models.ForeignKey(
        Campus, db_column='fk_campus', on_delete=models.DO_NOTHING)
    fk_school_grade = models.ForeignKey(
        SchoolGrade, db_column='fk_school_grade', on_delete=models.DO_NOTHING)
    fk_shift = models.ForeignKey(
        Shift, db_column='fk_shift', on_delete=models.DO_NOTHING)
    fk_school_year = models.ForeignKey(
        SchoolYear, db_column='fk_school_year', on_delete=models.DO_NOTHING)
    name = models.CharField(null=False, max_length=25)
    edited = models.DateTimeField(editable=True)
    status = models.IntegerField(null=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "tb_class_setting"


class SubjectArea(models.Model):
    pk_subject_area = models.AutoField(primary_key=True, unique=True)
    fk_campus = models.ForeignKey(
        Campus, db_column='fk_campus', on_delete=models.DO_NOTHING)
    name = models.CharField(null=False, max_length=50)
    created = models.DateTimeField(auto_now_add=True, editable=True)
    edited = models.DateTimeField(editable=True)
    status = models.IntegerField(null=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "tb_subject_area"


class Subject(models.Model):
    pk_subject = models.AutoField(primary_key=True, unique=True)
    fk_campus = models.ForeignKey(
        Campus, db_column='fk_campus', on_delete=models.DO_NOTHING)
    fk_subject_area = models.ForeignKey(
        SubjectArea, db_column='fk_subject_area', on_delete=models.DO_NOTHING)
    subject_code = models.IntegerField(unique=True, null=False)
    subject_name = models.CharField(null=False, max_length=25)
    created = models.DateTimeField(auto_now_add=True, editable=True)
    edited = models.DateTimeField(editable=True)
    status = models.IntegerField(null=False)

    def __str__(self):
        return self.subject_name

    class Meta:
        db_table = "tb_subject"


class PedagogicalSetting(models.Model):
    pk_pedagogical_setting = models.AutoField(primary_key=True, unique=True)
    fk_class_setting = models.ForeignKey(
        ClassSetting, db_column='fk_class_setting', on_delete=models.CASCADE)
    fk_subject = models.ForeignKey(
        Subject, db_column='fk_subject', on_delete=models.DO_NOTHING)
    fk_employee_user = models.ForeignKey(
        User, db_column='fk_employee_user', on_delete=models.DO_NOTHING)
    edited = models.DateTimeField(editable=True)
    status = models.IntegerField(null=False)

    def __str__(self):
        return self.fk_employee_user.username

    class Meta:
        db_table = "tb_pedagogical_setting"


class StudentClass(models.Model):
    pk_student_class = models.AutoField(primary_key=True, unique=True)
    fk_class_setting = models.ForeignKey(
        ClassSetting, db_column='fk_class_setting', on_delete=models.CASCADE)
    fk_student_user = models.ForeignKey(
        User, db_column='fk_student_user', on_delete=models.DO_NOTHING)
    status = models.IntegerField(null=False)

    def __str__(self):
        return self.fk_student_user.username

    class Meta:
        db_table = "tb_student_class"


class SkillSettings(models.Model):
    pk_skill_setting = models.AutoField(primary_key=True, unique=True)
    fk_campus = models.ForeignKey(
        Campus, db_column='fk_campus', on_delete=models.DO_NOTHING)
    label_name = models.CharField(null=False, max_length=15)
    description = models.CharField(null=False, max_length=255)
    status = models.IntegerField(null=False)

    def __str__(self):
        return self.label_name

    class Meta:
        db_table = "tb_skill"


class SchoolYearSkill(models.Model):
    pk_school_year_skill = models.AutoField(primary_key=True, unique=True)
    fk_skill = models.ForeignKey(
        SkillSettings, db_column='fk_skill', on_delete=models.DO_NOTHING)
    fk_school_year = models.ForeignKey(
        SchoolYear, db_column='fk_school_year', on_delete=models.CASCADE)

    def __str__(self):
        return self.fk_skill.label_name

    class Meta:
        db_table = "tb_school_level_skill"


class SubjectGrade(models.Model):
    pk_subject_grade = models.AutoField(primary_key=True, unique=True)
    fk_class = models.ForeignKey(
        ClassSetting, db_column='fk_class', on_delete=models.CASCADE)
    fk_term = models.ForeignKey(
        Term, db_column='fk_term', on_delete=models.DO_NOTHING)
    fk_subject = models.ForeignKey(
        Subject, db_column='fk_subject', on_delete=models.DO_NOTHING)
    fk_student_user = models.ForeignKey(
        User, db_column='fk_student_user', on_delete=models.DO_NOTHING)
    grade_1 = models.FloatField(default=0.0)
    grade_2 = models.FloatField(default=0.0)
    grade_3 = models.FloatField(default=0.0)
    grade_4 = models.FloatField(default=0.0)
    grade_5 = models.FloatField(default=0.0)
    edited = models.DateTimeField(editable=True)
    status = models.IntegerField(null=False)

    def __str__(self):
        return self.fk_student_user.username

    class Meta:
        db_table = "tb_subject_grade"


class SkillGrade(models.Model):
    pk_skill_grade = models.AutoField(primary_key=True, unique=True)
    fk_class = models.ForeignKey(
        ClassSetting, db_column='fk_class', on_delete=models.CASCADE)
    fk_term = models.ForeignKey(
        Term, db_column='fk_term', on_delete=models.DO_NOTHING)
    fk_subject = models.ForeignKey(
        Subject, db_column='fk_subject', on_delete=models.DO_NOTHING)
    fk_skill = models.ForeignKey(
        SkillSettings, db_column='fk_skill', on_delete=models.DO_NOTHING)
    fk_student_user = models.ForeignKey(
        User, db_column='fk_student_user', on_delete=models.DO_NOTHING)
    grade_1 = models.FloatField(default=0.0)
    grade_2 = models.FloatField(default=0.0)
    grade_3 = models.FloatField(default=0.0)
    grade_4 = models.FloatField(default=0.0)
    grade_5 = models.FloatField(default=0.0)
    edited = models.DateTimeField(editable=True)
    status = models.IntegerField(null=False)

    def __str__(self):
        return self.fk_student_user.username

    class Meta:
        db_table = "tb_skill_grade"


class StudentPresence(models.Model):
    pk_student_presence = models.AutoField(primary_key=True, unique=True)
    fk_class = models.ForeignKey(
        ClassSetting, db_column='fk_class', on_delete=models.CASCADE)
    fk_term = models.ForeignKey(
        Term, db_column='fk_term', on_delete=models.DO_NOTHING)
    fk_subject = models.ForeignKey(
        Subject, db_column='fk_subject', on_delete=models.DO_NOTHING)
    fk_student_user = models.ForeignKey(
        User, db_column='fk_student_user', on_delete=models.DO_NOTHING)
    presence = models.IntegerField(default=100)
    date_presence = models.DateField(editable=True)

    def __str__(self):
        return self.fk_student_user.username + ' - ' + \
            str(self.presence) + '% - ' + str(self.date_presence) \
            + ' - ' + self.fk_subject.subject_name

    class Meta:
        db_table = "tb_student_presence"