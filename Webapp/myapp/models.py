from django.db import models

# Create your models here.
class Login(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    type = models.CharField(max_length=20)

class Authority(models.Model):
    LOGIN = models.ForeignKey(Login, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    place = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    phone = models.CharField(max_length=10)
    post = models.CharField(max_length=30)
    district = models.CharField(max_length=30)
    pincode = models.CharField(max_length=30)

class Staff(models.Model):
    LOGIN = models.ForeignKey(Login, on_delete=models.CASCADE,default='')
    name = models.CharField(max_length=30)
    department = models.CharField(max_length=30)
    photo = models.CharField(max_length=480)
    gender = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    phone = models.CharField(max_length=30)
    place = models.CharField(max_length=30)
    post = models.CharField(max_length=30,default="")
    district = models.CharField(max_length=30)
    pincode = models.CharField(max_length=30)

class Student(models.Model):
    name = models.CharField(max_length=30)
    admissionno = models.CharField(max_length=30)
    photo = models.CharField(max_length=480)
    dob = models.CharField(max_length=30)
    place = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    department = models.CharField(max_length=30)
    course = models.CharField(max_length=30)
    gender = models.CharField(max_length=30)

class Exam(models.Model):
    examname = models.CharField(max_length=30)
    examcode = models.CharField(max_length=30)
    date = models.CharField(max_length=30)
    type = models.CharField(max_length=30)

class Schedule(models.Model):
    date = models.CharField(max_length=30)
    fromtime = models.CharField(max_length=30)
    totime = models.CharField(max_length=30)
    EXAM = models.ForeignKey(Exam, on_delete=models.CASCADE)

class Hall(models.Model):
    roomno = models.CharField(max_length=30)
    floor = models.CharField(max_length=30)

class Hallallocation(models.Model):
    EXAM = models.ForeignKey(Exam, on_delete=models.CASCADE)
    HALL = models.ForeignKey(Hall, on_delete=models.CASCADE)
    date = models.CharField(max_length=30)
    status = models.CharField(max_length=30)

class Staffallocation(models.Model):
    STAFF = models.ForeignKey(Staff, on_delete=models.CASCADE)
    date = models.CharField(max_length=30)
    HALLALLOCATION = models.ForeignKey(Hallallocation, on_delete=models.CASCADE)
    status = models.CharField(max_length=30)

class Studentallocation(models.Model):
    STUDENT = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.CharField(max_length=30)
    HALLALLOCATION = models.ForeignKey(Hallallocation, on_delete=models.CASCADE)
    status = models.CharField(max_length=30)

class Complaint(models.Model):
    date = models.CharField(max_length=30)
    complaint = models.CharField(max_length=2000)
    reply = models.CharField(max_length=2000)
    status = models.CharField(max_length=30)
    STAFF = models.ForeignKey(Staff, on_delete=models.CASCADE)

class Abnormalactivity(models.Model):
    date = models.DateField()
    time = models.TimeField()
    type = models.CharField(max_length=100)
    content = models.CharField(max_length=300)
    photo = models.CharField(max_length=500)
    HALL = models.ForeignKey(Hall,on_delete=models.CASCADE)


