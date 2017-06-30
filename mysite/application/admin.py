# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.utils.html import format_html
from .models import UploadLicense
from . import image_handler
from django.conf import settings

import re
import json


class AdminUploadLicense(admin.ModelAdmin):

    list_display = ('file_link', 'download', 'papers',)

    def file_link(self, obj):
        if obj.file:
            return format_html("<a href='%s'>%s</a>" % \
                               (obj.file.url, obj.file.url.split('/')[-1]))
        else:
            return "No Attachment"

    def download(self,obj):
        if obj.file:
            return format_html("<a href='%s' download>Download</a>" % \
                               (obj.file.url))
        else:
            return "No Attachment"
    download.short_description = 'Image Download'


    def papers(self, obj):

        with open(dict_d, "r") as f_json:
            dd = json.load(f_json)

        if str(obj.file) not in dd:
            info_doc = dd[str(obj.file.url)]

            path = ['/media/upload_license/'+s for s in info_doc]

            a = info_doc[0].split('_')[-1][:-5]
            if a in str(obj.file):
                dd[str(obj.file)] = path

        html_hyperlink = ''
        for i in dd[str(obj.file)]:
            html_hyperlink += ("<a href='{}' download>{}</a><br>"
                               .format(i,i.split('/')[-1]))

        with open(dict_d, 'w') as f_json:
            json.dump(dd, f_json, sort_keys=True,
                      indent=4, separators=(',', ': '))

        return format_html(html_hyperlink)
    papers.short_description = 'Download Insurance Papers'


    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()
        info_doc = image_handler.handle(obj.file)

        with open(dict_d, "r") as f_json:
            dd = json.load(f_json)
        dd[str(obj.file.url)] = info_doc
        with open(dict_d, 'w') as f_json:
            json.dump(dd, f_json, sort_keys=True,
                      indent=4, separators=(',', ': '))

    global dict_d
    dict_d = ('{}/application/media/dict_documents.json'
              .format(settings.BASE_DIR))


admin.site.register(UploadLicense, AdminUploadLicense)
