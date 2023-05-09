from django.db import models


class CourseTab(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=100, blank=True, null=True)
    course_number = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'course_tab'
