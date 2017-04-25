# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils.html import escape
import datetime
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from models import *
from labeeb_wrapper import get_data
from time import sleep
from django.conf import settings

# Create your views here.
def redirect(request):
    return HttpResponseRedirect(reverse("index"))

@csrf_exempt
def index(request):
    if request.user.is_authenticated():
        try:
            guardian = Guardian.objects.get(user=request.user)
            children = list(map(lambda x: x.child,
                                ChildGuardian.objects.filter(guardian=guardian)))
            context = {"guardian": {
                            "first_name": guardian.user.first_name,
                            "last_name": guardian.user.last_name,
                            "email": guardian.user.email,
                            "relationship": guardian.relationship,
                            "occupation": guardian.occupation
            }}
            
            # get all the tags for the children of the guardian
            all_tags = map(lambda x: TagUpdate.objects.filter(tag=x.tag), children)
            new_all_tags = []
            for lst in all_tags:
                new_all_tags += lst
            # parse all the updates 
            tag_updates = []
            context['history'] = []
            for tag in new_all_tags:
                tag_updates.append({
                    "tag": tag.tag.mac_address,
                    "sniffer": tag.sniffer.name,
                    "time_stamp": str(tag.time_stamp)
                    })
            context['history'] = tag_updates

            guardian_children = {"children": []}
            for child in children:
                child_data = {"first_name": child.first_name,
                              "last_name": child.last_name,
                              "age": child.age,
                              "grade": child.grade,
                              "section": child.section,
                              "tag": child.tag.mac_address,
                              "school": child.school.name,
                              "id": child.id
                              }
                tag_updates = TagUpdate.objects.filter(tag=child.tag,
                                                       time_stamp__date=datetime.date.today()).order_by("-time_stamp")
                if len(tag_updates) == 0:
                    child_data["location"] = "Not at school"
                    child_data["last_seen"] = "n/a"
                else:
                    child_data["location"] = tag_updates[0].sniffer.name
                    child_data["last_seen"] = tag_updates[0].time_stamp
                guardian_children["children"].append(child_data)
                context["children"] = guardian_children
            return JsonResponse(context)
        except Exception as e:
            return HttpResponseRedirect(reverse("dashboard"))
 
    return HttpResponseRedirect(reverse("signin"))


@csrf_exempt
def signin(request):
    context = {}
    if request.method == "POST":
        try:
            email = escape(request.POST["email"])
            password = escape(request.POST["password"])

            csrf_token = request.POST.get("csrfmiddlewaretoken", None)

            user = authenticate(username=email, password=password)
            if user is None:
                if csrf_token is None:
                    return JsonResponse({"status":
                                         "Invalid email and password."})
                context["errors"] = "Invalid email and password."
                return render(request, "signin.html", context)
            else:
                login(request, user)
                if csrf_token is None:
                    return JsonResponse({"status": "Successful"})
                return HttpResponseRedirect(reverse("dashboard"))
        except:
            return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "signin.html", context)


def signout(request):
    if request.user.is_authenticated():
        logout(request)

    return HttpResponseRedirect(reverse("index"))


def dashboard(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse("index"))

    context = {"is_home": True}

    # check whether user is guardian or admin
    try:
        admin = Admin.objects.get(user=request.user)
        context["admin"] = admin
    except:
        context["admin"] = None

    try:
        guardian = Guardian.objects.get(user=request.user)
        context["guardian"] = guardian
    except:
        context["guardian"] = None

    # if user is guardian, get list of guardian's children
    if context["guardian"] is not None:
        children = ChildGuardian.objects.filter(guardian=guardian)
        print children
        context["children"] = []
        for child in children:
            # Child.objects.filter(id=child.id)
            context["children"].append(child)

    # if user is school admin, calculate list of absent students and
    # late students
    if context["admin"] is not None and context["admin"].super_admin == False:
        school_children = Child.objects.filter(school=context["admin"].school)
        late_children = []
        absent_children = []

        for child in school_children:
            tag_updates = TagUpdate.objects.filter(tag=child.tag,
                                                   time_stamp__date=datetime.date.today()).order_by("time_stamp")
            # if no sniffer has updated with child's tag, child did not come to
            # school
            if len(tag_updates) == 0:
                absent_children.append(child)

            # check if child was late or not
            else:
                if len(tag_updates.filter(time_stamp__time__lte=context["admin"
                                                                        ].school.start_time)) == 0:
                    # child was late, get time of arrival
                    child = child.__dict__
                    child["time_of_arrival"] = tag_updates[0].time_stamp
                    late_children.append(child)

        context["absent_children"] = absent_children
        context["late_children"] = late_children

    return render(request, "dashboard.html", context)


def children(request):
    try:
        if not request.user.is_authenticated():
            raise

        context = {"is_children": True}
        admin = Admin.objects.get(user=request.user)
        context["admin"] = admin
        if admin.super_admin:
            school_children = Child.objects.all()
        else:
            school_children = Child.objects.filter(school=admin.school)
        children = []
        for child in school_children:
            tag_updates = TagUpdate.objects.filter(tag=child.tag,
                                                   time_stamp__date=datetime.date.today()).order_by("-time_stamp")
            school_name = child.school.name
            school_id = child.school.id
            tag_mac_address = child.tag.mac_address
            child = child.__dict__
            child["school"] = school_name
            child["school_id"] = school_id
            child["tag"] = tag_mac_address
            if len(tag_updates) == 0:
                child["location"] = "Not present"
                child["last_seen"] = "n/a"
            else:
                child["location"] = tag_updates[0].sniffer.name
                child["last_seen"] = tag_updates[0].time_stamp
                if ((timezone.now() - tag_updates[0].time_stamp).total_seconds() >= 15):
                    child["in_out"] = "OUT"
                else:
                    child["in_out"] = "IN"
            children.append(child)
        context["children"] = children
        context["schools"] = School.objects.all()
        return render(request, "children.html", context)
    except:
        return HttpResponseRedirect(reverse("index"))


def schools(request):
    try:
        if not request.user.is_authenticated():
            raise

        context = {"is_schools": True}
        admin = Admin.objects.get(user=request.user)
        if not admin.super_admin:
            raise
        context["admin"] = admin
        context["schools"] = School.objects.all()
        return render(request, "schools.html", context)
    except:
        return HttpResponseRedirect(reverse("index"))


def guardians(request):
    try:
        if not request.user.is_authenticated():
            raise

        context = {"is_guardians": True}
        context["admin"] = Admin.objects.get(user=request.user)
        context["guardians"] = Guardian.objects.all()
        return render(request, "guardians.html", context)
    except:
        return HttpResponseRedirect(reverse("index"))


def administrators(request):
    try:
        if not request.user.is_authenticated():
            raise

        context = {"is_admins": True}
        context["admin"] = Admin.objects.get(user=request.user)
        context["admins"] = Admin.objects.all()
        context["schools"] = School.objects.all()
        return render(request, "admins.html", context)
    except:
        return HttpResponseRedirect(reverse("index"))


def refresh_children(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse("index"))

    response = {"errors": 0}
    context = {}

    # check user is school admin
    try:
        admin = Admin.objects.get(user=request.user)
        if admin.super_admin:
            response["errors"] = 1
            return JsonResponse(response)
        context["admin"] = admin
    except:
        response["errors"] = 2
        return JsonResponse(response)

    try:
        school_children = Child.objects.filter(school=admin.school)
        children = []
        for child1 in school_children:
            tag_updates = TagUpdate.objects.filter(tag=child1.tag, time_stamp__date=datetime.date.today()).order_by("-time_stamp")

            child = child1.__dict__
            child["school"] = child1.school.name
            child["school_id"] = child1.school.id
            child["tag"] = child1.tag.mac_address
            
            if len(tag_updates) == 0:
                child["location"] = "Not present"
                child["last_seen"] = "n/a"
            else:
                child["location"] = tag_updates[0].sniffer.name
                child["last_seen"] = tag_updates[0].time_stamp
                if ((timezone.now() - tag_updates[0].time_stamp).total_seconds() >= 15):
                    child["in_out"] = "OUT"
                else:
                    child["in_out"] = "IN"
            children.append(child)
        context["children"] = children
        response["children"] = render_to_string("children_table.html", context,
                                                request)
        return JsonResponse(response)
    except Exception as e:
        response["errors"] = 3
        return JsonResponse(response)


def refresh_absent_late_children(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse("index"))

    response = {"errors": 0}
    context = {}

    # check user is school admin
    try:
        admin = Admin.objects.get(user=request.user)
        if admin.super_admin:
            response["errors"] = 1
            return JsonResponse(response)
        context["admin"] = admin
    except:
        response["errors"] = 2
        return JsonResponse(response)

    try:
        school_children = Child.objects.filter(school=context["admin"].school)
        late_children = []
        absent_children = []

        for child in school_children:
            tag_updates = TagUpdate.objects.filter(tag=child.tag,
                                                   time_stamp__date=datetime.date.today()).order_by("time_stamp")
            # if no sniffer has updated with child's tag, child did not come to
            # school
            if len(tag_updates) == 0:
                absent_children.append(child)

            # check if child was late or not
            else:
                if len(tag_updates.filter(time_stamp__time__lte=context["admin"
                                                                        ].school.start_time)) == 0:
                    # child was late, get time of arrival
                    child = child.__dict__
                    child["time_of_arrival"] = tag_updates[0].time_stamp
                    late_children.append(child)

        context["absent_children"] = absent_children
        context["late_children"] = late_children

        response["absent_children"] = render_to_string(
            "absent_children_table.html", context, request)
        response["late_children"] = render_to_string(
            "late_children_table.html", context, request)
        return JsonResponse(response)
    except:
        response["errors"] = 3
        return JsonResponse


def change_school_start_time(request):
    try:
        if not request.user.is_authenticated():
            raise
        admin = Admin.objects.get(user=request.user)
        if admin.super_admin:
            raise
        new_start_time = escape(request.POST["school_start_time"])
        admin.school.start_time = new_start_time
        try:
            admin.school.save()
        except Exception as e:
            return HttpResponse(e)
        return HttpResponseRedirect(reverse("dashboard"))
    except:
        return HttpResponseRedirect(reverse("index"))

@csrf_exempt
def sniffer_update(request):
    if request.method == "GET":
        return render(request, "sniffer_update.html", {})
    try:
        mac_addresses = escape(request.POST["mac_addresses"])
        sniffer_no = escape(request.POST["sniffer_no"])
        sniffer = Sniffer.objects.get(number=sniffer_no)
        mac_addresses = mac_addresses.split('!')
        context = {}
        context["success_count"] = 0
        context["fail_count"] = 0
        for mac_address in mac_addresses:
            try:
                tag = Tag.objects.get(mac_address=mac_address)
                tag_update = TagUpdate(tag=tag, sniffer=sniffer)
                tag_update.save()
                context["success_count"] += 1
            except:
                context["fail_count"] += 1
                pass
        return render(request, "sniffer_update.html", context)
    except Exception as e:
        return HttpResponse(e)


@csrf_exempt
def child_add(request):
    try:
        first_name = escape(request.POST["first_name"])
        last_name = escape(request.POST["last_name"])
        age = escape(request.POST["age"])
        grade = escape(request.POST["grade"])
        section = escape(request.POST["section"])
        school_id = escape(request.POST["school"])
        school = School.objects.get(id=school_id)
        tag_mac_address = escape(request.POST["tag"])
        tag = None
        try:
            tag = Tag.objects.filter(mac_address=tag_mac_address)[0]
        except:
            tag = Tag(mac_address=tag_mac_address)
        tag.save()

        child = Child(first_name=first_name, last_name=last_name, tag=tag,
                      age=age, grade=grade, section=section, school=school)
        child.save()

        return JsonResponse({"success": True})
    except Exception as e:
        print e
        return JsonResponse({"success": False})


@csrf_exempt
def child_edit(request):
    try:
        child = Child.objects.get(id=escape(request.POST["user_id"]))
        child.first_name = escape(request.POST["first_name"])
        child.last_name = escape(request.POST["last_name"])
        child.age = escape(request.POST["age"])
        child.grade = escape(request.POST["grade"])
        child.section = escape(request.POST["section"])
        school_id = escape(request.POST["school"])
        child.school = School.objects.get(id=school_id)
        child.tag.mac_address = escape(request.POST["tag"])
        child.tag.save()
        child.save()

        return JsonResponse({"success": True})
    except:
        return JsonResponse({"success": False})


@csrf_exempt
def child_delete(request):
    try:
        child_id = escape(request.POST["id"])
        child = Child.objects.get(id=child_id)
        child.delete()
        return JsonResponse({"success": True})
    except:
        return JsonResponse({"success": False})


@csrf_exempt
def guardian_add(request):
    try:
        first_name = escape(request.POST["first_name"])
        last_name = escape(request.POST["last_name"])
        email = escape(request.POST["email"])
        relationship = escape(request.POST["relationship"])
        occupation = escape(request.POST["occupation"])

        user = User.objects.create_user(username=email, email=email,
                                        password='newpass')
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        guardian = Guardian(user=user, relationship=relationship,
                            occupation=occupation)
        guardian.save()

        return JsonResponse({"success": True})
    except:
        return JsonResponse({"success": False})


@csrf_exempt
def guardian_edit(request):
    try:
        guardian = Guardian.objects.get(id=escape(request.POST["user_id"]))
        guardian.user.first_name = escape(request.POST["first_name"])
        guardian.user.last_name = escape(request.POST["last_name"])
        guardian.relationship = escape(request.POST["relationship"])
        guardian.occupation = escape(request.POST["occupation"])
        guardian.user.save()
        guardian.save()

        return JsonResponse({"success": True})
    except:
        return JsonResponse({"success": False})


@csrf_exempt
def guardian_delete(request):
    try:
        guardian_id = escape(request.POST["id"])
        guardian = Guardian.objects.get(id=guardian_id)
        guardian.user.delete()
        guardian.delete()
        return JsonResponse({"success": True})
    except:
        return JsonResponse({"success": False})


@csrf_exempt
def school_add(request):
    try:
        name = escape(request.POST["name"])
        building_no = escape(request.POST["building_no"])
        street = escape(request.POST["street"])
        city = escape(request.POST["city"])
        zone = escape(request.POST["zone"])
        start_time = escape(request.POST["start_time"])

        school = School(name=name, building_no=building_no, street=street,
                        city=city, zone_no=zone, start_time=start_time)
        school.save()

        return JsonResponse({"success": True})
    except:
        return JsonResponse({"success": False})


@csrf_exempt
def school_edit(request):
    try:
        school = School.objects.get(id=escape(request.POST["school_id"]))
        school.name = escape(request.POST["name"])
        school.building_no = escape(request.POST["building_no"])
        school.street = escape(request.POST["street"])
        school.city = escape(request.POST["city"])
        school.zone = escape(request.POST["zone"])
        school.start_time = escape(request.POST["start_time"])
        school.save()

        return JsonResponse({"success": True})
    except Exception as e:
        print e
        return JsonResponse({"success": False})


@csrf_exempt
def school_delete(request):
    try:
        school_id = escape(request.POST["id"])
        school = School.objects.get(id=school_id)
        school.delete()
        return JsonResponse({"success": True})
    except:
        return JsonResponse({"success": False})


@csrf_exempt
def admin_add(request):
    try:
        first_name = escape(request.POST["first_name"])
        last_name = escape(request.POST["last_name"])
        email = escape(request.POST["email"])
        contact_number = escape(request.POST["contact_number"])
        super_admin = eval(escape(request.POST["super_admin"]))

        user = User.objects.create_user(username=email, email=email,
                                        password='newpass')
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        admin = Admin(user=user, contact_number=contact_number,
                      super_admin=super_admin)
        if not super_admin:
            school_id = escape(request.POST['school'])
            school = School.objects.get(id=school_id)
            admin.school = school
        admin.save()

        return JsonResponse({"success": True})
    except:
        return JsonResponse({"success": False})


@csrf_exempt
def admin_edit(request):
    try:
        admin = Admin.objects.get(id=escape(request.POST["admin_id"]))
        admin.user.first_name = escape(request.POST["first_name"])
        admin.user.last_name = escape(request.POST["last_name"])
        admin.user.email = escape(request.POST["email"])
        admin.contact_number = escape(request.POST["contact_number"])
        admin.super_admin = eval(escape(request.POST["super_admin"]))

        if not admin.super_admin:
            school_id = escape(request.POST['school'])
            admin.school = School.objects.get(id=school_id)

        admin.user.save()
        admin.save()

        return JsonResponse({"success": True})
    except:
        return JsonResponse({"success": False})


@csrf_exempt
def admin_delete(request):
    try:
        admin_id = escape(request.POST["id"])
        admin = Admin.objects.get(id=admin_id)
        admin.user.delete()
        admin.delete()
        return JsonResponse({"success": True})
    except:
        return JsonResponse({"success": False})


# function will be called every x seconds to fetch the new data 
def fetch_update():
    if not settings.LOADED_DATA:
        print "load the data first from the Labeeb IoT at /fetch_and_update"
        return 1

    new_time = datetime.datetime.today() - datetime.timedelta(seconds=10)
    data = get_data(new_time)
    # print "Data: ", data
    # create all the entries for the updates 
    for entry in data:
        all_tags = entry['stringValue'].split("!")
        sniffers = []
        # iterate over the tags 
        for tag in all_tags:
            if tag in sniffers:
                continue
            try:
                current_sniffer = Sniffer.objects.filter(name=entry['deviceId'])[0]
                current_tag = Tag.objects.filter(mac_address=tag)[0]
                new_tagupdate = TagUpdate(tag=current_tag, sniffer=current_sniffer)
                new_tagupdate.save()
                sniffers.append(tag)
            except Exception as e:
                pass

    print "updated the model..."
    sleep(10)

# populate the db 
@csrf_exempt
def fetch_and_update(request): 
    if not request.user.is_superuser:
        redirect(request)
    data = get_data()
    result = {}
    unique_tags = {}
    for row in data:
        key = row['deviceId']
        if key in result.keys():
            result[key].append(row)
        else:
            result[key] = [row]
        tags = row['stringValue'].split("!")
        # get all the unique tags 
        for tag in tags:
            if tag not in unique_tags.keys():
                unique_tags[tag] = 1

    # attach all sniffers to the same school 
    school = School.objects.all()[0]

    # create all the sniffers 
    for sniffer in result.keys():
        try:
            new_sniffer = Sniffer(name=sniffer, number=1234, school=school)
            new_sniffer.save()
        except:
            pass

    # create all the tags 
    for tag in unique_tags:
        try:
            new_tag = Tag(mac_address=tag)
            new_tag.save()
        except:
            pass

    # create all the entries for the updates 
    for entry in data:
        all_tags = entry['stringValue'].split("!")
        # iterate over the tags 
        for tag in all_tags:
            current_sniffer = Sniffer.objects.filter(name=entry['deviceId'])[0]
            current_tag = Tag.objects.filter(mac_address=tag)[0]
            new_tagupdate = TagUpdate(tag=current_tag, sniffer=current_sniffer, time_stamp=entry['storeTime'])
            new_tagupdate.save()

    settings.LOADED_DATA = True
    
    print "fetched and updated the db"
    return HttpResponseRedirect(reverse("start_autoload"))

@csrf_exempt
def start_autoload(request):
    if not request.user.is_superuser:
        redirect(request)
    settings.LOADED_DATA = True
    while True:
        fetch_update()

    return JsonResponse({"success": "The server is now autoloading"})


