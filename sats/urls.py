from django.conf.urls import url

import views

urlpatterns = [
    # views
    url(r'dashboard$', views.dashboard, name="dashboard"),
    url(r'dashboard/children$', views.children, name="children"),
    url(r'dashboard/administrators$', views.administrators, name="administrators"),
    url(r'dashboard/schools$', views.schools, name="schools"),
    url(r'dashboard/guardians$', views.guardians, name="guardians"),
    url(r'snifferupdate$', views.sniffer_update, name="sniffer_update"),

	# CRUD functionality
	url(r'guardianadd$', views.guardian_add, name="guardian_add"),
	url(r'guardianedit$', views.guardian_edit, name="guardian_edit"),
	url(r'guardiandelete$', views.guardian_delete, name="guardian_delete"),

    url(r'childadd$', views.child_add, name="child_add"),
	url(r'childedit$', views.child_edit, name="child_edit"),
	url(r'childdelete$', views.child_delete, name="child_delete"),

    url(r'schooladd$', views.school_add, name="school_add"),
	url(r'schooledit$', views.school_edit, name="school_edit"),
	url(r'schooldelete$', views.school_delete, name="school_delete"),

    url(r'adminadd$', views.admin_add, name="admin_add"),
	url(r'adminedit$', views.admin_edit, name="admin_edit"),
	url(r'admindelete$', views.admin_delete, name="admin_delete"),

    url(r'fetch_and_update$', views.fetch_and_update, name="fetch_and_update"),
    url(r'start_autoload$', views.start_autoload, name="start_autoload"),

    # AJAX and forms
    url(r'refreshabsentlatechildren$', views.refresh_absent_late_children,
        name="refresh_absent_late_children"),
	url(r'refreshchildren$', views.refresh_children, name="refresh_children"),
    url(r'changeschoolstarttime$', views.change_school_start_time,
        name="change_school_start_time"),

    # authentication
    url(r'signin$', views.signin, name="signin"),
    url(r'signout$', views.signout, name="signout"),

    # catch all index
    url(r'index$', views.index, name="index"),
    url(r'$', views.redirect, name="redirect"),
]
