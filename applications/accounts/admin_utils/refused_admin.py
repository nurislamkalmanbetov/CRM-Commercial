from django.contrib import admin
from django.http import HttpResponse


class ProfileInRefusedAdmin(admin.ModelAdmin):

    fields = ['first_name', 'last_name', 'is_refused', ]

    list_display = ['first_name', 'last_name', 'is_refused', ]

    def changelist_view(self, request, extra_context=None):

        if request.GET.get('get_xls', None):
            return self.export_xls(request)

        extra_context = extra_context or {}
        extra_context['table_classname'] = 'confirmed'
        return super(ProfileInRefusedAdmin, self).changelist_view(request, extra_context=extra_context)

    def export_xls(self, request):
        import xlwt

        queryset = self.get_queryset(request=request).order_by('last_name', 'first_name')

        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename=report.xls'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet("Профили")

        row_num = 0

        columns = [
            'Имя',
            'Фамилия'
        ]

        fields = [
            'first_name',
            'last_name'
        ]

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)
            # ws.col(col_num).width = columns[col_num][1]

        font_style = xlwt.XFStyle()
        font_style.alignment.wrap = 1

        for obj in queryset:
            row_num += 1
            row = []
            for field in fields:
                if hasattr(obj, field):
                    if field == 'bday':
                        value = obj.bday.strftime('%d.%m.%Y') if obj.bday else '-'
                    elif field == 'gender':
                        value = obj.get_gender_display() if obj.gender else '-'
                    elif field == 'summer_holidays_start':
                        value = obj.summer_holidays_start.strftime('%d.%m.%Y') if obj.summer_holidays_start else '-'
                    elif field == 'summer_holidays_end':
                        value = obj.summer_holidays_end.strftime('%d.%m.%Y') if obj.summer_holidays_end else '-'
                    elif field == 'zagranpassport_end_time':
                        value = obj.zagranpassport_end_time.strftime('%d.%m.%Y') if obj.zagranpassport_end_time else '-'
                    else:
                        value = getattr(obj, field)

                    if type(value) != int or type(value) != float or not value:
                        value = str(value)
                    row.append(value)
                else:
                    row.append(getattr(self, field)(obj, True))
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)

        wb.save(response)
        return response

    export_xls.short_description = u"Export XLS"
