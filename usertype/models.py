from django.db import models

class Course(models.Model):
    course_id = models.CharField(primary_key=True, max_length=8)
    title = models.CharField(max_length=32, blank=True, null=True)
    dept_name = models.ForeignKey('Department', models.DO_NOTHING, db_column='dept_name', blank=True, null=True)
    credits = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'course'
        managed = False


class Department(models.Model):
    dept_name = models.CharField(db_column='dept_Name', primary_key=True, max_length=32)  # Field name made lowercase.
    building = models.CharField(max_length=32, blank=True, null=True)
    budget = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'department'
        managed = False


class Instructor(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=32, blank=True, null=True)
    dept_name = models.ForeignKey(Department, models.DO_NOTHING, db_column='dept_name', blank=True, null=True)
    salary = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'instructor'
        managed = False


class Section(models.Model):
    course_id = models.CharField(db_column='course_ID', max_length=6, primary_key=True)  # Field name made lowercase.
    sec_id = models.CharField(db_column='sec_ID', max_length=6)  # Field name made lowercase.
    semester = models.IntegerField()
    year = models.IntegerField()
    building = models.CharField(max_length=32, blank=True, null=True)
    room = models.CharField(max_length=32, blank=True, null=True)
    capacity = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'section'
        unique_together = (('course_id', 'sec_id', 'semester', 'year'),)
        managed = False


class Student(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=32, blank=True, null=True)
    dept_name = models.ForeignKey(Department, models.DO_NOTHING, db_column='dept_name', blank=True, null=True)
    total_credits = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'student'
        managed = False


class Takes(models.Model):
    id = models.ForeignKey(Student, models.DO_NOTHING, db_column='ID', primary_key=True)  # Field name made lowercase.
    course = models.ForeignKey(Section, models.DO_NOTHING, db_column='course_ID', related_name='takes_section_course')  # Field name made lowercase.
    sec = models.ForeignKey(Section, models.DO_NOTHING, db_column='sec_ID', related_name = 'takes_section_sec')  # Field name made lowercase.
    semester = models.ForeignKey(Section, models.DO_NOTHING, db_column='semester', related_name = 'takes_section_semester')
    year = models.ForeignKey(Section, models.DO_NOTHING, db_column='year', related_name = 'takes_section_year')
    grade = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        db_table = 'takes'
        unique_together = (('id', 'course', 'sec', 'semester', 'year'),)
        managed = False


class Teaches(models.Model):
    course = models.ForeignKey(Section, models.DO_NOTHING, db_column='course_ID', primary_key = True, related_name = 'teaches_section_course')  # Field name made lowercase.
    sec = models.ForeignKey(Section, models.DO_NOTHING, db_column='sec_ID', related_name = 'teaches_section_sec')  # Field name made lowercase.
    semester = models.ForeignKey(Section, models.DO_NOTHING, db_column='semester', related_name = 'teaches_section_semester')
    year = models.ForeignKey(Section, models.DO_NOTHING, db_column='year', related_name = 'teaches_section_year')
    id = models.ForeignKey(Instructor, models.DO_NOTHING, db_column='ID')  # Field name made lowercase.

    class Meta:
        db_table = 'teaches'
        unique_together = (('course', 'sec', 'semester', 'year', 'id'),)
        managed = False
