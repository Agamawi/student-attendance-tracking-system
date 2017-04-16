# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from models import *

# Register your models here.

admin.site.register(Admin)
admin.site.register(Guardian)
admin.site.register(Tag)
admin.site.register(School)
admin.site.register(ChildGuardian)
admin.site.register(Child)
admin.site.register(Sniffer)
admin.site.register(TagUpdate)