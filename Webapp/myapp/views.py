from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from myapp.models import *


def login(request):
    request.session['lid'] = ''
    return render(request, 'index login.html')
def login_post(request):
    username = request.POST['username']
    password = request.POST['password']
    res = Login.objects.filter(username=username, password=password)
    if res.exists():
        ress = Login.objects.get(username = username, password=password)
        request.session['lid']=ress.id

        if ress.type == 'Admin':
            return redirect('/myapp/adminhome/')
        elif ress.type == 'Authority':
            return redirect('/myapp/authority_home/')
        elif ress.type== 'Staff':
            return redirect('/myapp/staff_home/')
        else:
            return HttpResponse('''<script>alert('User not found');window.location='/myapp/login/'</script>''')

    else:
        return HttpResponse('''<script>alert('User not found');window.location='/myapp/login/'</script>''')



def adminhome(request):
    if request.session['lid'] == '':
        return redirect('/')
    return render(request,'Admin/home index.html')

def admin_addauthority(request):
    if request.session['lid'] == '':
        return redirect('/')
    return render(request, 'Admin/Add Authority.html')

def admin_addauthority_post(request):
    if request.session['lid'] == '':
        return redirect('/')
    name=request.POST['textfield']
    place=request.POST['textfield2']
    email=request.POST['textfield3']
    phone=request.POST['textfield4']
    post=request.POST['textfield5']
    district=request.POST['textfield6']
    pincode=request.POST['textfield7']

    l=Login()
    l.username=email
    import random
    ps=random.randint(0000,9999)
    l.password = str(ps)
    l.type = 'Authority'
    l.save()

    a=Authority()
    a.LOGIN=l
    a.name = name
    a.place = place
    a.email = email
    a.phone = phone
    a.post = post
    a.district = district
    a.pincode = pincode
    a.save()

    return HttpResponse('''<script>alert('Added Successfully');window.location='/myapp/admin_addauthority/'</script>''')


def admin_viewauthority(request):
    if request.session['lid'] == '':
        return redirect('/')
    res = Authority.objects.all()
    return render(request, 'Admin/View Authority.html',{'data':res})

def admin_viewauthority_post(request):
    if request.session['lid'] == '':
        return redirect('/')
    search=request.POST['textfield']
    ab = Authority.objects.filter(name__icontains=search)
    return render(request, 'Admin/View Authority.html', {'data':ab})


def admin_deleteauthority(request,id):
    if request.session['lid'] == '':
        return redirect('/')
    res = Authority.objects.filter(id = id).delete()
    return HttpResponse('''<script>alert('Deleted Successfully');window.location='/myapp/admin_viewauthority/'</script>''')

def admin_editauthority(request,id):
    if request.session['lid'] == '':
        return redirect('/')
    res = Authority.objects.get(id = id)
    return render(request, 'Admin/Edit Authority.html', {"data":res})

def admin_editauthority_post(request):
    if request.session['lid'] == '':
        return redirect('/')
    name = request.POST['textfield']
    place = request.POST['textfield2']
    Email = request.POST['textfield3']
    phone = request.POST['textfield4']
    post = request.POST['textfield5']
    district = request.POST['textfield6']
    pincode = request.POST['textfield7']
    id = request.POST['id']

    a = Authority.objects.get(id = id)
    a.name = name
    a.place = place
    a.email = Email
    a.phone = phone
    a.post = post
    a.district = district
    a.pincode = pincode
    a.save()
    return HttpResponse('''<script>alert('Edited Successfully');window.location='/myapp/admin_viewauthority/'</script>''')


def admin_addstaff(request):
    if request.session['lid'] == '':
        return redirect('/')
    return render(request, 'Admin/Add Staff.html')

def admin_addstaff_post(request):
    if request.session['lid'] == '':
        return redirect('/')
    name = request.POST['textfield']
    department = request.POST['textfield8']
    photo = request.FILES['textfield9']
    gender = request.POST['textfield10']
    place = request.POST['textfield2']
    email = request.POST['textfield3']
    phone = request.POST['textfield4']
    post = request.POST['textfield5']
    district = request.POST['textfield6']
    pincode = request.POST['textfield7']
    from datetime import datetime
    date = datetime.now().strftime('%Y%m%d_%H%M%S')+".jpg"
    fs = FileSystemStorage()
    fs.save(date,photo)
    path = fs.url(date)


    l = Login()
    l.username = email
    import random
    ps = random.randint(0000, 9999)
    l.password = str(ps)
    l.type = 'Staff'
    l.save()

    s = Staff()
    s.LOGIN = l
    s.name = name
    s.department = department
    s.photo = path
    s.gender = gender
    s.place = place
    s.email = email
    s.phone = phone
    s.post = post
    s.district = district
    s.pincode = pincode
    s.save()

    return HttpResponse('''<script>alert('Added Successfully');window.location='/myapp/admin_addstaff/'</script>''')




def admin_viewstaff(request):
    if request.session['lid'] == '':
        return redirect('/')
    res=Staff.objects.all()
    return render(request, 'Admin/View Staff.html',{'data':res})

def admin_viewstaff_post(request):
    if request.session['lid'] == '':
        return redirect('/')
    search = request.POST['textfield']
    ab = Staff.objects.filter(name__icontains=search)
    return render(request, 'Admin/View Staff.html', {'data':ab})

def admin_deletestaff(request,id):
    if request.session['lid'] == '':
        return redirect('/')
    res = Staff.objects.filter(id = id).delete()
    return HttpResponse('''<script>alert('Deleted Successfully');window.location='/myapp/admin_viewstaff/'</script>''')

def admin_editstaff(request, id):
    if request.session['lid'] == '':
        return redirect('/')
    res = Staff.objects.get(id=id)
    return render(request, 'Admin/Edit Staff.html', {"data":res})

def admin_editstaff_post(request):
    if request.session['lid'] == '':
        return redirect('/')
    name = request.POST['textfield']
    department = request.POST['textfield8']
    gender = request.POST['textfield10']
    place = request.POST['textfield2']
    Email = request.POST['textfield11']
    phone = request.POST['textfield3']
    post = request.POST['textfield5']
    district = request.POST['textfield6']
    pincode = request.POST['textfield7']
    id = request.POST['id']
    s = Staff.objects.get(id = id)

    if 'textfield9' in request.FILES:
        photo = request.FILES['textfield9']

        from datetime import datetime
        date = datetime.now().strftime('%Y%m%d_%H%M%S') + ".jpg"
        fs = FileSystemStorage()
        fs.save(date, photo)
        path = fs.url(date)
        s.photo = path
        s.save()

    s.name = name
    s.department = department
    s.gender = gender
    s.place = place
    s.email = Email
    s.phone = phone
    s.post = post
    s.district = district
    s.pincode = pincode
    s.save()
    return HttpResponse('''<script>alert('Edited Successfully');window.location='/myapp/admin_viewstaff/'</script>''')

def admin_addstudent(request):
    if request.session['lid'] == '':
        return redirect('/')
    return render(request, 'Admin/Add Student.html')

def admin_addstudent_post(request):
    if request.session['lid'] == '':
        return redirect('/')
    name = request.POST['textfield']
    admissionno = request.POST['textfield2']
    dob = request.POST['textfield3']
    department = request.POST['textfield4']
    course = request.POST['textfield5']
    email = request.POST['textfield6']
    gender = request.POST['textfield7']
    place = request.POST['textfield8']
    photo = request.FILES['fileField']
    from datetime import datetime
    date = datetime.now().strftime('%Y%m%d_%H%M%S') + ".jpg"
    fs = FileSystemStorage()
    fs.save(date, photo)
    path = fs.url(date)

    s = Student()
    s.name = name
    s.admissionno = admissionno
    s.dob = dob
    s.department = department
    s.course = course
    s.photo = path
    s.gender = gender
    s.place = place
    s.email = email
    s.save()

    return HttpResponse('''<script>alert('Added Successfully');window.location='/myapp/admin_addstudent/'</script>''')


def admin_viewstudent(request):
    if request.session['lid'] == '':
        return redirect('/')
    ab = Student.objects.all()
    return render(request, 'Admin/View Student.html', {'data':ab})

def admin_viewstudent_post(request):
    if request.session['lid'] == '':
        return redirect('/')
    search = request.POST['textfield']
    ab = Student.objects.filter(name__icontains=search)

    return render(request, 'Admin/View Student.html',{'data':ab})   ############//


def admin_editstudent(request, id):
    if request.session['lid'] == '':
        return redirect('/')
    res = Student.objects.get(id = id)
    return render(request, 'Admin/Edit Student.html', {"data":res})

def admin_editstudent_post(request):
    if request.session['lid'] == '':
        return redirect('/')
    name = request.POST['textfield']
    admissionno = request.POST['textfield2']
    dob = request.POST['textfield3']
    department = request.POST['textfield4']
    course = request.POST['textfield5']
    email = request.POST['textfield6']
    gender = request.POST['textfield7']
    place = request.POST['textfield8']
    photo = request.FILES['fileField']
    id = request.POST['id']
    s = Student.objects.get(id=id)

    if 'fileField' in request.FILES:
        photo = request.FILES['fileField']

        from datetime import datetime
        date = datetime.now().strftime('%Y%m%d_%H%M%S') + ".jpg"
        fs = FileSystemStorage()
        fs.save(date, photo)
        path = fs.url(date)
        s.photo = path
        s.save()
    s.name = name
    s.admissionno = admissionno
    s.dob = dob
    s.department = department
    s.course = course
    s.gender = gender
    s.place = place
    s.email = email
    s.save()
    return HttpResponse('''<script>alert('Edited Successfully');window.location='/myapp/admin_viewstudent/'</script>''')

def admin_deletestudent(request,id):
    if request.session['lid'] == '':
        return redirect('/')
    res = Student.objects.filter(id = id).delete()
    return HttpResponse('''<script>alert('Deleted Successfully');window.location='/myapp/admin_viewstudent/'</script>''')

def admin_addexam(request):
    if request.session['lid'] == '':
        return redirect('/')
    return render(request, 'Admin/Add Exam.html')

def admin_addexam_post(request):
    if request.session['lid'] == '':
        return redirect('/')
    examname = request.POST['textfield']
    examcode = request.POST['textfield2']
    date = request.POST['textfield3']
    type = request.POST['select']

    e = Exam()
    e.examname = examname
    e.examcode = examcode
    e.date = date
    e.type = type
    e.save()
    # Submit button available in html page   #############################
    return HttpResponse('''<script>alert('Added Successfully');window.location='/myapp/admin_addexam/'</script>''')


def admin_viewexam(request):
    if request.session['lid'] == '':
        return redirect('/')
    res=Exam.objects.all()
    return render(request, 'Admin/View Exam.html',{'data':res})

def admin_viewexam_post(request):
    if request.session['lid'] == '':
        return redirect('/')
    fromdate = request.POST['textfield']
    todate = request.POST['textfield2']
    res = Exam.objects.filter(date__range=[fromdate,todate])
    return render(request, 'Admin/View Exam.html',{'data':res})


def admin_editexam(request, id):
    if request.session['lid'] == '':
        return redirect('/')
    res = Exam.objects.get(id = id)
    return render(request, 'Admin/Edit Exam.html', {"data":res})

def admin_deleteexam(request,id):
    if request.session['lid'] == '':
        return redirect('/')
    res = Exam.objects.filter(id = id).delete()
    return HttpResponse('''<script>alert('Deleted Successfully');window.location='/myapp/admin_viewexam/'</script>''')

def admin_editexam_post(request):
    if request.session['lid'] == '':
        return redirect('/')
    examname = request.POST['textfield']
    examcode = request.POST['textfield2']
    date = request.POST['textfield3']
    type = request.POST['select']
    id = request.POST['id']

    e = Exam.objects.get(id = id)
    e.examname = examname
    e.examcode = examcode
    e.date = date
    e.type = type
    e.save()
    # Submit button available in html page   #############################
    return HttpResponse('''<script>alert('Added Successfully');window.location='/myapp/admin_viewexam/'</script>''')


def admin_addschedule(request):
    if request.session['lid'] == '':
        return redirect('/')
    a = Exam.objects.all()
    return render(request, 'Admin/Add Schedule.html', {'data':a})

def admin_addschedule_post(request):
    if request.session['lid'] == '':
        return redirect('/')

    date = request.POST['textfield']
    fromtime = request.POST['textfield2']
    totime = request.POST['textfield3']
    exam = request.POST['select']

    s = Schedule()
    s.EXAM_id = exam
    s.date = date
    s.fromtime = fromtime
    s.totime = totime
    s.exam = exam
    s.save()

    return HttpResponse('''<script>alert('Added Successfully');window.location='/myapp/admin_addschedule/'</script>''')


def admin_viewschedule(request):
    if request.session['lid'] == '':
        return redirect('/')
    res = Schedule.objects.all()
    return render (request, 'Admin/View Schedule.html', {'data':res})

def admin_viewschedule_post(request):
    if request.session['lid'] == '':
        return redirect('/')
    fromdate = request.POST['textfield']
    todate = request.POST['textfield2']
    res = Schedule.objects.filter(date__range=[fromdate,todate])

    return render (request, 'Admin/View Schedule.html', {'data':res})


def admin_editschedule(request, id):
    if request.session['lid'] == '':
        return redirect('/')
    a = Exam.objects.all()
    res = Schedule.objects.get(id=id)
    return render(request, 'Admin/Edit Schedule.html',{"data":res, "data2":a})

def admin_editschedule_post(request):
    if request.session['lid'] == '':
        return redirect('/')
    date = request.POST['textfield']
    fromtime = request.POST['textfield2']
    totime = request.POST['textfield3']
    exam = request.POST['select']
    id = request.POST['id']


    s = Schedule.objects.get(id = id)
    s.date = date
    s.fromtime = fromtime
    s.totime = totime
    s.exam = exam    # Value is not given in the HTML page
    s.save()
    return HttpResponse('''<script>alert('Edited Successfully');window.location='/myapp/admin_viewschedule/'</script>''')

def admin_deleteschedule(request,id):
    if request.session['lid'] == '':
        return redirect('/')
    res = Schedule.objects.filter(id = id).delete()
    return HttpResponse('''<script>alert('Deleted Successfully');window.location='/myapp/admin_viewschedule/'</script>''')

def admin_addstaffallocation(request,id):
    if request.session['lid'] == '':
        return redirect('/')
    res1 = Staff.objects.all()
    return render(request, 'Admin/Add Staff Allocation.html',{'data1':id,'data':res1})

def admin_addstaffallocation_post(request):
    if request.session['lid'] == '':
        return redirect('/')
    hdid=request.POST['id1']
    # date = request.POST['textfield']
    staff = request.POST['select2']
    # hh=Hallallocation.objects.get(id=hallallocation)


    s = Staffallocation()
    from datetime import datetime
    date = datetime.now().strftime('%Y-%m-%d')
    s.date = date
    s.HALLALLOCATION_id = hdid
    s.STAFF_id=staff
    s.status = 'Allocated'
    s.save()

    return HttpResponse('''<script>alert('Added Successfully');window.location='/myapp/admin_viewhallallocation/'</script>''')


def admin_viewstaffallocation(request,id):
    if request.session['lid'] == '':
        return redirect('/')
    res = Staffallocation.objects.filter(HALLALLOCATION_id=id)
    return render(request, 'Admin/View Staff Allocation.html',{'data':res})

def admin_viewstaffallocation_post(request):
    if request.session['lid'] == '':
        return redirect('/')
    fromdate = request.POST['textfield']
    todate = request.POST['textfield2']
    return render(request, 'Admin/View Staff Allocation.html')
    #href edit&delete ###################################################




def admin_editstaffallocation(request, id):
    if request.session['lid'] == '':
        return redirect('/')
    res2 = Staff.objects.all()
    res = Staffallocation.objects.get(id=id)
    return render(request, 'Admin/Edit Staff Allocation.html', {"data":res, "data2":res2})

def admin_editstaffallocation_post(request):
    if request.session['lid'] == '':
        return redirect('/')
    id = request.POST['id']
    staff = request.POST['select']
    #date = request.POST['textfield']
    # hallallocation = request.POST['select2']  # Value for the hall allocation is not given in the HTML Page
    # Submit button######################################

    s = Staffallocation.objects.get(id=id)
    s.STAFF_id = staff
    s.save()
    return HttpResponse('''<script>alert('Edited Successfully');window.location='/myapp/admin_viewhallallocation/'</script>''')

def admin_deletestaffallocation(request,id):
    if request.session['lid'] == '':
        return redirect('/')
    res = Staffallocation.objects.filter(id = id).delete()
    return HttpResponse('''<script>alert('Deleted Successfully');window.location='/myapp/admin_viewhallallocation/'</script>''')


def admin_addstudentallocation(request):
    if request.session['lid'] == '':
        return redirect('/')
    var = Student.objects.all()
    va = Hallallocation.objects.all()
    return render(request, 'Admin/Add Student Allocation.html',{'data1':var, 'data2':va})

def admin_addstudentallocation_post(request):
    if request.session['lid'] == '':
        return redirect('/')
    student = request.POST['select2']
    # date = request.POST['textfield2']
    hallallocation = request.POST['select']################
    # Submit Button ##########################################

    s = Studentallocation()
    s.STUDENT_id = student
    from datetime import datetime
    s.date = datetime.now().strftime('%Y-%m-%d')
    s.HALLALLOCATION_id = hallallocation
    s.status = 'Allocated'
    s.save()

    return HttpResponse('''<script>alert('Added Successfully');window.location='/myapp/admin_addstudentallocation/'</script>''')


def admin_viewstudentallocation(request):
    if request.session['lid'] == '':
        return redirect('/')
    res = Studentallocation.objects.all()
    return render(request, 'Admin/View Student Allocation.html', {'data':res})

def admin_viewstudentallocation_post(request):
    if request.session['lid'] == '':
        return redirect('/')
    return render(request, 'Admin/View Student Allocation.html')
    # Edit and Delete hyperlink available ##########################


def admin_editstudentallocation(request, id):
    if request.session['lid'] == '':
        return redirect('/')
    res = Studentallocation.objects.get(id = id)
    var = Student.objects.all()
    va = Hallallocation.objects.all()
    return render(request, 'Admin/Edit Student Allocation.html', {"data":res, "data1":var, "data2":va})

def admin_editstudentallocation_post(request):
    if request.session['lid'] == '':
        return redirect('/')
    student = request.POST['select2']
    # date = request.POST['textfield2']
    hallallocation = request.POST['select']
    id = request.POST['id']

    s = Studentallocation.objects.get(id=id)
    s.STUDENT_id = student
    from datetime import datetime
    s.date = datetime.now().strftime('%Y-%m-%d')
    s.HALLALLOCATION_id = hallallocation
    s.status = 'Allocated'

    s.save()

    return HttpResponse('''<script>alert('Edited Successfully');window.location='/myapp/admin_viewstudentallocation/'</script>''')

def admin_deletestudentallocation(request,id): ##########Last class
    if request.session['lid'] == '':
        return redirect('/')
    res = Studentallocation.objects.filter(id = id).delete()
    return HttpResponse('''<script>alert('Deleted Successfully');window.location='/myapp/admin_viewstudentallocation/'</script>''')

def admin_addhall(request):
    if request.session['lid'] == '':
        return redirect('/')
    return render(request, 'Admin/Add Hall.html')


def admin_addhall_post(request):
    if request.session['lid'] == '':
        return redirect('/')
    rno = request.POST['textfield']
    floor = request.POST['textfield2']


    a = Hall()
    a.roomno = rno
    a.floor = floor
    a.save()
    return HttpResponse('''<script>alert('Added Successfully');window.location='/myapp/admin_addhall/'</script>''')


def admin_viewhall(request):
    if request.session['lid'] == '':
        return redirect('/')
    res=Hall.objects.all()
    return render(request, 'Admin/View Hall.html',{'data':res})

def admin_viewhall_post(request):
    if request.session['lid'] == '':
        return redirect('/')
    return render(request, 'Admin/View Hall.html')
    #Edit n Delete hyperlink available##########################


def admin_edithall(request, id):
    if request.session['lid'] == '':
        return redirect('/')
    res = Hall.objects.get(id=id)
    return render(request, 'Admin/Edit Hall.html', {"data":res})

def admin_edithall_post(request):
    if request.session['lid'] == '':
        return redirect('/')
    roomno = request.POST['textfield']
    id = request.POST['id']
    floor = request.POST['textfield2']

    a = Hall.objects.get(id=id)
    a.roomno = roomno
    a.floor = floor
    a.save()
    # Edit n delete hyperlink ####################################
    # Submit button
    return HttpResponse('''<script>alert('Edited Successfully');window.location='/myapp/admin_viewhall/'</script>''')

def admin_deletehall(request,id):
    if request.session['lid'] == '':
        return redirect('/')
    res = Hall.objects.filter(id = id).delete()
    return HttpResponse('''<script>alert('Deleted Successfully');window.location='/myapp/admin_viewhall/'</script>''')

def admin_viewcomplaint(request):
    if request.session['lid'] == '':
        return redirect('/')
    res = Complaint.objects.all()
    return render(request, 'Admin/View Complaint.html',{'data':res})

def admin_viewcomplaint_post(request):
    if request.session['lid'] == '':
        return redirect('/')
    fromdate = request.POST['textfield']
    todate = request.POST['textfield2']
    res = Complaint.objects.filter(date__range=[fromdate,todate])
    return render(request, 'Admin/View Complaint.html',{'data':res})


def admin_reply(request,id):
    if request.session['lid'] == '':
        return redirect('/')
    return render(request, 'Admin/Reply.html',{'id':id})

def admin_reply_post(request):
    if request.session['lid'] == '':
        return redirect('/')
    reply = request.POST['textfield']
    id = request.POST['id']
    Complaint.objects.filter(id=id).update(status="Replied",reply=reply)
    # Submit button
    return HttpResponse('''<script>alert('Replied Successfully');window.location='/myapp/admin_viewcomplaint/'</script>''')


def admin_addhallallocation(request, id):
    if request.session['lid'] == '':
        return redirect('/')
    res=Exam.objects.all()
    #rr=Hall.objects.all()
    return render(request, 'Admin/Add Hall Allocation.html',{'id':id,'data1':res})

def admin_addhallallocation_post(request):
    if request.session['lid'] == '':
        return redirect('/')
    exam = request.POST['select'] #######################################
    hall = request.POST['id']
    ex=Exam.objects.get(id=exam)
    date = request.POST['textfield']
    #did=request.POST['id1']
    # Submit Button

    s = Hallallocation()
    s.EXAM = ex
    s.HALL_id=hall
    s.date = date
    s.status = 'Allocated'
    s.save()
    return HttpResponse('''<script>alert('Added Successfully');window.location='/myapp/admin_viewhallallocation/'</script>''')


def admin_viewhallallocation(request):
    if request.session['lid'] == '':
        return redirect('/')
    res=Hallallocation.objects.all()
    return render(request, 'Admin/View Hall Allocation.html',{'data':res})

def admin_viewhallallocation_post(request):
    if request.session['lid'] == '':
        return redirect('/')
    fromdate = request.POST['textfield']
    todate = request.POST['textfield2']
    res = Hallallocation.objects.filter(date__range=[fromdate,todate])

    # Submit button
    return render(request, 'Admin/View Hall Allocation.html', {'data':res})


def admin_edithallallocation(request, id):
    if request.session['lid'] == '':
        return redirect('/')
    res = Hallallocation.objects.get(id = id)
    res1 = Exam.objects.all()
    res2 = Hall.objects.all()
    return render(request, 'Admin/Edit Hall Allocation.html', {"data":res, "data2":res2, "data1":res1})

def admin_edithallallocation_post(request):
    if request.session['lid'] == '':
        return redirect('/')
    id = request.POST['id']
    exam = request.POST['select']  ############################
    hall = request.POST['select2']
    date = request.POST['textfield']

    s = Hallallocation.objects.get(id=id)
    s.EXAM_id = exam
    s.HALL_id = hall
    s.date = date
    s.save()
    return HttpResponse('''<script>alert('Edited Successfully');window.location='/myapp/admin_viewhallallocation/'</script>''')

def admin_deletehallallocation(request,id):
    if request.session['lid'] == '':
        return redirect('/')
    res = Hallallocation.objects.filter(id = id).delete()
    return HttpResponse('''<script>alert('Deleted Successfully');window.location='/myapp/admin_viewhallallocation/'</script>''')


#######################################################################################################################
########################################################################################################################
###################      AUTHORITY Module     ############################################################################
########################################################################################################################
###########################################################################################################################

def authority_changepassword(request):
    if request.session['lid'] == '':
        return redirect('/')
    return render(request, 'Authority/Change Password.html')

def authority_changepassword_post(request):
    if request.session['lid'] == '':
        return redirect('/')
    oldpassword = request.POST['textfield']
    newpassword = request.POST['textfield2']
    confirmpassword = request.POST['textfield3']
    var = Login.objects.filter(id=request.session['lid'], password = oldpassword)
    if var.exists():
        var2 = Login.objects.get(id=request.session['lid'], password = oldpassword)
        if newpassword==confirmpassword:
            var3 = Login.objects.filter(id = request.session['lid']).update(password = confirmpassword)
            return HttpResponse('''<script>alert('Changed Successfully');window.location='/myapp/login/'</script>''')
        else:
            return HttpResponse('''<script>alert('Password mismatch');window.location='/myapp/authority_changepassword/'</script>''')
    else:
        return HttpResponse('''<script>alert('Password mismatch');window.location='/myapp/authority_changepassword/'</script>''')

        # Submit button
def authority_home(request):
    if request.session['lid'] == '':
        return redirect('/')
    return render(request,'Authority/home index.html')

def authority_viewexam(request):
    if request.session['lid'] == '':
        return redirect('/')
    var = Exam.objects.all()
    return render(request, 'Authority/View Exam.html', {'data':var})

def authority_viewexam_post(request):
    if request.session['lid'] == '':
        return redirect('/')
    fromdate = request.POST['textfield']
    todate = request.POST['textfield2']
    var = Exam.objects.filter(date__range=[fromdate, todate])
    return render(request, 'Authority/View Exam.html', {'data':var})


def authority_viewallocatedstudent(request):
    if request.session['lid'] == '':
        return redirect('/')
    var = Studentallocation.objects.all()
    return render(request, 'Authority/View Allocated Student.html',{'data':var})

def authority_viewallocatedstudent_post(request):
    if request.session['lid'] == '':
        return redirect('/')
    fromdate = request.POST['textfield']
    todate = request.POST['textfield2']
    var = Studentallocation.objects.filter(date__range=[fromdate, todate])
    return render(request, 'Authority/View Allocated Student.html', {'data': var})


def authority_viewallocatedstaff(request):
    if request.session['lid'] == '':
        return redirect('/')
    var = Staffallocation.objects.all()
    return render(request, 'Authority/View Allocated staff.html', {'data':var})

def authority_viewallocatedstaff_post(request):
    if request.session['lid'] == '':
        return redirect('/')
    fromdate = request.POST['textfield']
    todate = request.POST['textfield2']
    var = Staffallocation.objects.filter(date__range=[fromdate, todate])
    return render(request, 'Authority/View Allocated staff.html', {'data': var})


def authority_viewexamhall(request):
    if request.session['lid'] == '':
        return redirect('/')
    var = Hallallocation.objects.all()
    return render(request, 'Authority/View Exam Hall.html', {'data':var})

def authority_viewexamhall_post(request):
    if request.session['lid'] == '':
        return redirect('/')
    fromdate = request.POST['textfield']
    todate = request.POST['textfield2']
    var = Hallallocation.objects.filter(date__range=[fromdate, todate])
    return render(request, 'Authority/View Exam Hall.html', {'data':var})


def authority_viewprofile(request):
    if request.session['lid'] == '':
        return redirect('/')
    var = Authority.objects.get(LOGIN=request.session['lid'])
    return render(request, 'Authority/View Profile.html', {'data':var})

def authority_viewprofile_post(request):
    if request.session['lid'] == '':
        return redirect('/')
    return render(request, 'Authority/View Profile.html')

def authority_viewdetectedanomalies(request):
    if request.session['lid'] == '':
        return redirect('/')
    var=Abnormalactivity.objects.all()
    return render(request, 'Authority/View Detected Anomalies.html', {'data':var})

def authority_viewdetectedanomalies_post(request):
    if request.session['lid'] == '':
        return redirect('/')
    fromdate=request.POST['textfield']
    todate=request.POST['textfield2']
    var=Abnormalactivity.objects.filter(date__range=[fromdate, todate])
    return render(request, 'Authority/View Detected Anomalies.html', {'data':var})


#######################################################################################################################
########################################################################################################################
###################      STAFF Module     ############################################################################
########################################################################################################################
###########################################################################################################################

def staff_sendcomplaint(request):
    if request.session['lid'] == '':
        return redirect('/')
    return render(request, 'Staff/Send Complaint.html')

def staff_sendcomplaint_post(request):
    if request.session['lid'] == '':
        return redirect('/')
    complaint = request.POST['textfield']
    var = Complaint()
    from datetime import datetime
    var.date=datetime.now().strftime('%Y-%m-%d')
    var.complaint = complaint
    var.reply = 'Pending'
    var.status='Pending'
    var.STAFF =  Staff.objects.get(LOGIN=request.session['lid'])
    var.save()
    # Submit button
    return HttpResponse('''<script>alert('Submitted Successfully');window.location='/myapp/staff_sendcomplaint/'</script>''')

def staff_home(request):
    if request.session['lid'] == '':
        return redirect('/')
    return render(request,'Staff/home index.html')


def staff_viewallocatedexamhall(request):
    if request.session['lid'] == '':
        return redirect('/')
    var = Staffallocation.objects.filter(STAFF__LOGIN_id = request.session['lid'])
    return render(request, 'Staff/View Allocated Exam Hall.html', {'data':var})

def staff_viewallocatedexamhall_post(request):
    if request.session['lid'] == '':
        return redirect('/')
    return render(request, 'Staff/View Allocated Exam Hall.html')


def staff_viewallocatedexam(request,id):
    if request.session['lid'] == '':
        return redirect('/')
    sta=Staff.objects.get(LOGIN_id=request.session['lid']).id
    hall=Staffallocation.objects.get(STAFF_id=sta).HALLALLOCATION.id
    exm=Hallallocation.objects.get(id=hall).EXAM.id


    var = Exam.objects.filter(id=exm)
    return render(request, 'Staff/View Allocated Exam.html',{'data':var})

def staff_viewallocatedexam_post(request):
    if request.session['lid'] == '':
        return redirect('/')
    fromdate = request.POST['textfield']
    todate = request.POST['textfield2']
    sta = Staff.objects.get(LOGIN_id=request.session['lid']).id
    hall = Staffallocation.objects.get(STAFF_id=sta).HALLALLOCATION.id
    exm = Hallallocation.objects.get(id=hall).EXAM.id

    var = Exam.objects.filter(id=exm,date__range=[fromdate, todate])
    return render(request, 'Staff/View Allocated Exam.html', {'data': var})

def staff_viewexamschedule(request):
    if request.session['lid'] == '':
        return redirect('/')
    var = Schedule.objects.all()
    return render(request, 'Staff/View Exam Schedule.html', {'data':var})

def staff_viewexamschedule_post(request):
    if request.session['lid'] == '':
        return redirect('/')
    fromdate = request.POST['textfield2']
    todate = request.POST['textfield']
    var = Schedule.objects.filter(date__range=[fromdate, todate])
    return render(request, 'Staff/View Exam Schedule.html',{'data':var})


def staff_viewprofile(request):
    if request.session['lid'] == '':
        return redirect('/')
    var = Staff.objects.get(LOGIN=request.session['lid'])
    return render(request, 'Staff/View Profile.html', {'data':var})

def staff_viewprofile_post(request):
    if request.session['lid'] == '':
        return redirect('/')
    return render(request, 'Staff/View Profile.html')


def staff_viewreply(request):
    if request.session['lid'] == '':
        return redirect('/')
    var= Complaint.objects.filter(STAFF__LOGIN_id=request.session['lid'])
    return render(request, 'Staff/View Reply.html', {'data':var})

def staff_viewreply_post(request):
    if request.session['lid'] == '':
        return redirect('/')
    fromdate = request.POST['textfield']
    todate = request.POST['textfield2']
    var = Complaint.objects.filter(STAFF__LOGIN_id=request.session['lid'], date__range=[fromdate, todate])
    return render(request, 'Staff/View Reply.html', {'data': var})


def staff_viewstudentinexamhall(request):
    if request.session['lid'] == '':
        return redirect('/')

    SS=Studentallocation.objects.filter(HALLALLOCATION__staffallocation__STAFF__LOGIN_id=request.session['lid'])
    return render(request,'Staff/View Student in Exam hall.html',{'data':SS})

def staff_viewstudentinexamhall_post(request):
    if request.session['lid'] == '':
        return redirect('/')
    fromdate = request.POST['textfield']
    todate = request.POST['textfield2']
    SS=Studentallocation.objects.filter(HALLALLOCATION__staffallocation__STAFF__LOGIN_id=request.session['lid'], date__range=[fromdate,todate])
    return render(request,'Staff/View Student in Exam hall.html',{'data':SS})

def staff_viewdetectedanomalies(request):
    if request.session['lid'] == '':
        return redirect('/')
    var=Abnormalactivity.objects.all()
    return render(request, 'Staff/View Detected Anomalies.html', {'data':var})

def staff_viewdetectedanomalies_post(request):
    if request.session['lid'] == '':
        return redirect('/')
    fromdate=request.POST['textfield']
    todate=request.POST['textfield2']
    var=Abnormalactivity.objects.filter(date__range=[fromdate, todate])
    return render(request, 'Staff/View Detected Anomalies.html', {'data':var})






