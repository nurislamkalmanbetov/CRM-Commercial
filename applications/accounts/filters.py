from django.db.models import Q
from django.contrib.admin import SimpleListFilter
from rangefilter.filter import DateRangeFilter


class CustomDateFilter(DateRangeFilter):
    template = 'admin/date_filter.html'


class ZagranPassportCopy(SimpleListFilter):
    title = 'Копия загран ID'
    parameter_name = 'int_pass_id'

    def lookups(self, request, model_admin):
        return [
            ('copy_confirm', 'Наличие электронной копии'),
            ('paper_copy_confirm', 'Наличие бумажной копии'),
            ('twice_confirm', 'Наличие обеих копий'),
            ('not_confirm', 'Нет копий'),
        ]

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'copy_confirm':
            return queryset.filter(zagranpassport_copy_confirm=True)
        if value == 'paper_copy_confirm':
            return queryset.filter(zagranpassport_copy_paper_confirm=True)
        if value == 'twice_confirm':
            return queryset.filter(zagranpassport_copy_confirm=True, zagranpassport_copy_paper_confirm=True)
        if value == 'not_confirm':
            return queryset.filter(zagranpassport_copy_confirm=False, zagranpassport_copy_paper_confirm=False)
        if value:
            return queryset


class PassportCopy(SimpleListFilter):
    title = 'Копия ID'
    parameter_name = 'passport_copy'

    def lookups(self, request, model_admin):
        return [
            ('copy_confirm', 'Наличие электронной копии'),
            ('paper_copy_confirm', 'Наличие бумажной копии'),
            ('twice_confirm', 'Наличие обеих копий'),
            ('not_confirm', 'Нет копий'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'copy_confirm':
            return queryset.filter(passport_copy_confirm=True)
        if self.value() == 'paper_copy_confirm':
            return queryset.filter(passport_copy_paper_confirm=True)
        if self.value() == 'twice_confirm':
            return queryset.filter(passport_copy_confirm=True, passport_copy_paper_confirm=True)
        if self.value() == 'not_confirm':
            return queryset.filter(passport_copy_confirm=False, passport_copy_paper_confirm=False)
        if self.value():
            return queryset


class JIPLConfirm(SimpleListFilter):
    title = 'JIPL'
    parameter_name = 'JIPL'

    def lookups(self, request, model_admin):
        return [
            ('paper_copy_confirm', 'Наличие бумажной версии'),
            ('not_paper_copy_confirm', 'Нет бумажной версии'),

        ]

    def queryset(self, request, queryset):
        if self.value() == 'paper_copy_confirm':
            return queryset.filter(jipl_paper_confirm=True)
        if self.value() == 'not_paper_copy_confirm':
            return queryset.filter(jipl_paper_confirm=False)
        if self.value():
            return queryset


class WorkContractConfirm(SimpleListFilter):
    title = 'Договор труда'
    parameter_name = 'labor_agreement'

    def lookups(self, request, model_admin):
        return [
            ('paper_copy_confirm', 'Наличие бумажной версии'),
            ('not_paper_copy_confirm', 'Нет бумажной версии'),

        ]

    def queryset(self, request, queryset):
        if self.value() == 'paper_copy_confirm':
            return queryset.filter(work_contract_paper_confirm=True)
        if self.value() == 'not_paper_copy_confirm':
            return queryset.filter(work_contract_paper_confirm=False)
        if self.value():
            return queryset


class ReceiptConfirm(SimpleListFilter):
    title = 'Расписка'
    parameter_name = 'raspiska'

    def lookups(self, request, model_admin):
        return [
            ('paper_copy_confirm', 'Наличие бумажной версии'),
            ('not_paper_copy_confirm', 'Нет бумажной версии'),

        ]

    def queryset(self, request, queryset):
        if self.value() == 'paper_copy_confirm':
            return queryset.filter(receipt_paper_confirm=True)
        if self.value() == 'not_paper_copy_confirm':
            return queryset.filter(receipt_paper_confirm=False)
        if self.value():
            return queryset


class TrainingContractConfirm(SimpleListFilter):
    title = 'Договор тренинга'
    parameter_name = 'training_agreement'

    def lookups(self, request, model_admin):
        return [
            ('paper_copy_confirm', 'Наличие бумажной версии'),
            ('not_paper_copy_confirm', 'Нет бумажной версии'),

        ]

    def queryset(self, request, queryset):
        if self.value() == 'paper_copy_confirm':
            return queryset.filter(traning_contract_paper_confirm=True)
        if self.value() == 'not_paper_copy_confirm':
            return queryset.filter(traning_contract_paper_confirm=False)
        if self.value():
            return queryset


class PhotoConfirm(SimpleListFilter):
    title = 'Фото на шенген'
    parameter_name = 'shengen_photo'

    def lookups(self, request, model_admin):
        return [
            ('copy_confirm', 'Наличие электронной версии'),
            ('paper_copy_confirm', 'Наличие бумажной копии'),
            ('twice_confirm', 'Наличие обеих копий'),
            ('not_confirm', 'Нет копий'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'paper_copy_confirm':
            return queryset.filter(photo_for_schengen_paper_confirm=True)
        if self.value() == 'copy_confirm':
            return queryset.filter(photo_for_schengen_confirm=True)
        if self.value() == 'twice_confirm':
            return queryset.filter(photo_for_schengen_paper_confirm=True, photo_for_schengen_confirm=True)
        if self.value() == 'not_confirm':
            return queryset.filter(photo_for_schengen_paper_confirm=False, photo_for_schengen_confirm=False)
        if self.value():
            return queryset


class StudyCertificateConfirm(SimpleListFilter):
    title = 'Справка с места учебы'
    parameter_name = 'student_note'

    def lookups(self, request, model_admin):
        return [
            ('copy_confirm', 'Наличие электронной версии'),
            ('paper_copy_confirm', 'Наличие бумажной копии'),
            ('twice_confirm', 'Наличие обеих копий'),
            ('not_confirm', 'Нет копий'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'paper_copy_confirm':
            return queryset.filter(study_certificate_paper_confirm=True)
        if self.value() == 'copy_confirm':
            return queryset.filter(study_certificate_confirm=True)
        if self.value() == 'twice_confirm':
            return queryset.filter(study_certificate_paper_confirm=True, study_certificate_confirm=True)
        if self.value() == 'not_confirm':
            return queryset.filter(study_certificate_paper_confirm=False, study_certificate_confirm=False)
        if self.value():
            return queryset


class FluorographyConfirm(SimpleListFilter):
    title = 'Флюорография'
    parameter_name = 'chest_xray'

    def lookups(self, request, model_admin):
        return [
            ('copy_confirm', 'Наличие электронной версии'),
            ('paper_copy_confirm', 'Наличие бумажной копии'),
            ('twice_confirm', 'Наличие обеих копий'),
            ('not_confirm', 'Нет копий'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'paper_copy_confirm':
            return queryset.filter(fluorography_paper_confirm=True)
        if self.value() == 'copy_confirm':
            return queryset.filter(fluorography_confirm=True)
        if self.value() == 'twice_confirm':
            return queryset.filter(fluorography_paper_confirm=True, fluorography_confirm=True)
        if self.value() == 'not_confirm':
            return queryset.filter(fluorography_paper_confirm=False, fluorography_confirm=False)
        if self.value():
            return queryset


class ResumeConfirm(SimpleListFilter):
    title = 'Резюме'
    parameter_name = 'resume'

    def lookups(self, request, model_admin):
        return [
            ('confirmed', 'Подтверждено'),
            ('not_confirmed', 'Не подтверждено'),

        ]

    def queryset(self, request, queryset):
        if self.value() == 'confirmed':
            return queryset.filter(resume_paper_confirm=True)
        if self.value() == 'not_confirmed':
            return queryset.filter(resume_paper_confirm=False)
        if self.value():
            return queryset


class IMMATConfirm(SimpleListFilter):
    title = 'IMMAT'
    parameter_name = 'IMMAT'

    def lookups(self, request, model_admin):
        return [
            ('immatrikulation', 'Электронная версии'),
            ('immatrikulation_confirm', 'Подтверждено наличие'),
            ('immatrikulation_paper_confirm', 'Бумажной копия'),
            ('twice_confirm', 'Наличие обеих копий'),
            ('not_confirm', 'Нет копий'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'immatrikulation':
            return queryset.exclude(immatrikulation__isnull=False)
        if self.value() == 'immatrikulation_confirm':
            return queryset.filter(immatrikulation_confirm=True)
        if self.value() == 'immatrikulation_paper_confirm':
            return queryset.filter(immatrikulation_paper_confirm=True)
        if self.value() == 'twice_confirm':
            return queryset.filter(immatrikulation_confirm=True, immatrikulation_paper_confirm=True)
        if self.value() == 'not_confirm':
            return queryset.filter(immatrikulation_confirm=False, immatrikulation_paper_confirm=False)
        if self.value():
            return queryset


class GermanyExperience(SimpleListFilter):
    title = 'Опыт в Германии'
    parameter_name = 'experience_in_germany'

    def lookups(self, request, model_admin):
        return [
            ('yes', 'Да'),
            ('no', 'Нет'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(Q(country1='Deutschland') | Q(country2='Deutschland') | Q(country3='Deutschland'))
        if self.value() == 'no':
            return queryset.exclude(Q(country1='Deutschland') | Q(country2='Deutschland') | Q(country3='Deutschland'))
        if self.value():
            return queryset


class GermanyInvitation(SimpleListFilter):
    title = 'Приглашение'
    parameter_name = 'invitation'

    def lookups(self, request, model_admin):
        return [
            ('yes', 'Да'),
            ('no', 'Нет'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.exclude(work_invitation_date__isnull=True)
        if self.value() == 'no':
            return queryset.filter(work_invitation_date__isnull=True)
        if self.value():
            return queryset



class GermanyInsurance(SimpleListFilter):
    title = 'Нем страховка'
    parameter_name = 'german_insurance'

    def lookups(self, request, model_admin):
        return [
            ('yes', 'Да'),
            ('no', 'Нет'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(german_insurance=True)
        if self.value() == 'no':
            return queryset.filter(german_insurance=False)
        if self.value():
            return queryset


class LocalInsurance(SimpleListFilter):
    title = 'Мест страховка'
    parameter_name = 'local_insurance'

    def lookups(self, request, model_admin):
        return [
            ('yes', 'Да'),
            ('no', 'Нет'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(local_insurance=True)
        if self.value() == 'no':
            return queryset.filter(local_insurance=False)
        if self.value():
            return queryset


class Accomodation(SimpleListFilter):
    title = 'Подтверждение жилья'
    parameter_name = 'accomodation'

    def lookups(self, request, model_admin):
        return [
            ('yes', 'Да'),
            ('no', 'Нет'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(accomodation=True)
        if self.value() == 'no':
            return queryset.filter(accomodation=False)
        if self.value():
            return queryset


class UniversityDocumentEmbassy(SimpleListFilter):
    title = 'Справка с универа'
    parameter_name = 'study_certificate_paper_embassy_confirm'

    def lookups(self, request, model_admin):
        return [
            ('yes', 'Да'),
            ('no', 'Нет'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(study_certificate_paper_embassy_confirm=True)
        if self.value() == 'no':
            return queryset.filter(study_certificate_paper_embassy_confirm=False)
        if self.value():
            return queryset


class UniversityDocumentTranslationEmbassy(SimpleListFilter):
    title = 'Перевод справки с универа'
    parameter_name = 'study_certificate_translate_paper_embassy_confirm'

    def lookups(self, request, model_admin):
        return [
            ('yes', 'Да'),
            ('no', 'Нет'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(study_certificate_translate_paper_embassy_confirm=True)
        if self.value() == 'no':
            return queryset.filter(study_certificate_translate_paper_embassy_confirm=False)
        if self.value():
            return queryset


class UniversityTranscript(SimpleListFilter):
    title = 'Транскрипт'
    parameter_name = 'transcript_paper_confirm'

    def lookups(self, request, model_admin):
        return [
            ('yes', 'Да'),
            ('no', 'Нет'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(transcript_paper_confirm=True)
        if self.value() == 'no':
            return queryset.filter(transcript_paper_confirm=False)
        if self.value():
            return queryset


class UniversityTranscriptTranslation(SimpleListFilter):
    title = 'Перевод транскрипта'
    parameter_name = 'transcript_translate_paper_confirm'

    def lookups(self, request, model_admin):
        return [
            ('yes', 'Да'),
            ('no', 'Нет'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(transcript_translate_paper_confirm=True)
        if self.value() == 'no':
            return queryset.filter(transcript_translate_paper_confirm=False)
        if self.value():
            return queryset


class BankStatement(SimpleListFilter):
    title = 'Выписка с банка'
    parameter_name = 'bank_statement_paper_confirm'

    def lookups(self, request, model_admin):
        return [
            ('yes', 'Да'),
            ('no', 'Нет'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(bank_statement_paper_confirm=True)
        if self.value() == 'no':
            return queryset.filter(bank_statement_paper_confirm=False)
        if self.value():
            return queryset


class PhotoFile(SimpleListFilter):
    title = 'Фото эл версия'
    parameter_name = 'photo_for_schengen'

    def lookups(self, request, model_admin):
        return [
            ('yes', 'Да'),
            ('no', 'Нет'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.exclude(Q(photo_for_schengen__isnull=True) | Q(photo_for_schengen=''))
        if self.value() == 'no':
            return queryset.filter(Q(photo_for_schengen__isnull=True) | Q(photo_for_schengen=''))
        if self.value():
            return queryset


class PhotoPaper(SimpleListFilter):
    title = 'Фото бум версия'
    parameter_name = 'photo_for_schengen_paper_confirm'

    def lookups(self, request, model_admin):
        return [
            ('yes', 'Да'),
            ('no', 'Нет'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(photo_for_schengen_paper_confirm=True)
        if self.value() == 'no':
            return queryset.filter(photo_for_schengen_paper_confirm=False)
        if self.value():
            return queryset


class EmbassyAnketa(SimpleListFilter):
    title = 'Анкета для посольства'
    parameter_name = 'embassy_anketa'

    def lookups(self, request, model_admin):
        return [
            ('yes', 'Да'),
            ('no', 'Нет'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(embassy_anketa=True)
        if self.value() == 'no':
            return queryset.filter(embassy_anketa=False)
        if self.value():
            return queryset


class ZagranPassport(SimpleListFilter):
    title = 'Загран бум'
    parameter_name = 'zagranpassport_copy_paper_confirm'

    def lookups(self, request, model_admin):
        return [
            ('yes', 'Да'),
            ('no', 'Нет'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(zagranpassport_copy_paper_confirm=True)
        if self.value() == 'no':
            return queryset.filter(zagranpassport_copy_paper_confirm=False)
        if self.value():
            return queryset


class MVD(SimpleListFilter):
    title = 'Справка с МВД'
    parameter_name = 'conduct_certificate_paper_confirm'

    def lookups(self, request, model_admin):
        return [
            ('yes', 'Да'),
            ('no', 'Нет'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(conduct_certificate_paper_confirm=True)
        if self.value() == 'no':
            return queryset.filter(conduct_certificate_paper_confirm=False)
        if self.value():
            return queryset


class Narkodispanser(SimpleListFilter):
    title = 'Наркодиспансер'
    parameter_name = 'drugdispanser_certificate_paper_confirm'

    def lookups(self, request, model_admin):
        return [
            ('yes', 'Да'),
            ('no', 'Нет'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(drugdispanser_certificate_paper_confirm=True)
        if self.value() == 'no':
            return queryset.filter(drugdispanser_certificate_paper_confirm=False)
        if self.value():
            return queryset


class Psihdispanser(SimpleListFilter):
    title = 'Психдиспансер'
    parameter_name = 'mentaldispanser_certificate_paper_confirm'

    def lookups(self, request, model_admin):
        return [
            ('yes', 'Да'),
            ('no', 'Нет'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(mentaldispanser_certificate_paper_confirm=True)
        if self.value() == 'no':
            return queryset.filter(mentaldispanser_certificate_paper_confirm=False)
        if self.value():
            return queryset


class ParentsPermission(SimpleListFilter):
    title = 'Разрешение от родителей'
    parameter_name = 'parental_permission_paper_confirm'

    def lookups(self, request, model_admin):
        return [
            ('yes', 'Да'),
            ('no', 'Нет'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(parental_permission_paper_confirm=True)
        if self.value() == 'no':
            return queryset.filter(parental_permission_paper_confirm=False)
        if self.value():
            return queryset


class WorkContract(SimpleListFilter):
    title = 'Рабочий договор'
    parameter_name = 'german_work_contract'

    def lookups(self, request, model_admin):
        return [
            ('yes', 'Да'),
            ('no', 'Нет'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(german_work_contract=True)
        if self.value() == 'no':
            return queryset.filter(german_work_contract=False)
        if self.value():
            return queryset


class BankAccountDetails(SimpleListFilter):
    title = 'Реквизиты с банка'
    parameter_name = 'bank_details_paper_confirm'

    def lookups(self, request, model_admin):
        return [
            ('yes', 'Да'),
            ('no', 'Нет'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(bank_details_paper_confirm=True)
        if self.value() == 'no':
            return queryset.filter(bank_details_paper_confirm=False)
        if self.value():
            return queryset


class FluorographyEmbassy(SimpleListFilter):
    title = 'Реквизиты с банка'
    parameter_name = 'fluorography_paper_confirm'

    def lookups(self, request, model_admin):
        return [
            ('yes', 'Да'),
            ('no', 'Нет'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(fluorography_paper_confirm=True)
        if self.value() == 'no':
            return queryset.filter(fluorography_paper_confirm=False)
        if self.value():
            return queryset


class Marshrut(SimpleListFilter):
    title = 'Маршрут'
    parameter_name = 'marshrut'

    def lookups(self, request, model_admin):
        return [
            ('not_exist', 'Нет маршрута'),
            ('doubtful', 'Сомнительно'),
            ('created', 'Маршрут был составлен'),
            ('received', 'Маршрут был получен'),
        ]

    def queryset(self, request, queryset):
        value = self.value()
        if value in ['not_exist', 'doubtful', 'created', 'received']:
            return queryset.filter(marshrut=value)
        return queryset


class ImatGiven(SimpleListFilter):
    title = 'Imat выдан на руки'
    parameter_name = 'immatrikulation_received'

    def lookups(self, request, model_admin):
        return [
            ('yes', 'Да'),
            ('no', 'Нет'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(immatrikulation_received=True)
        if self.value() == 'no':
            return queryset.filter(immatrikulation_received=False)
        if self.value():
            return queryset


class Domkom(SimpleListFilter):
    title = 'Справка от домкома'
    parameter_name = 'domkom_document'

    def lookups(self, request, model_admin):
        return [
            ('not_exist', 'Нет'),
            ('brought', 'Принес'),
            ('sent', 'Отправили в Германию'),
            ('not_given', 'Не дали'),
        ]

    def queryset(self, request, queryset):
        value = self.value()
        if value in ['not_exist', 'brought', 'sent', 'not_given']:
            return queryset.filter(domkom_document=value)
        return queryset


class BiletSending(SimpleListFilter):
    title = 'Билет'
    parameter_name = 'bilet_document'

    def lookups(self, request, model_admin):
        return [
            ('not_exist', 'Нет'),
            ('brought', 'Принес'),
            ('sent', 'Отправили в Германию'),
            ('not_given', 'Не смог получить (сомнительно)'),
        ]

    def queryset(self, request, queryset):
        value = self.value()
        if value in ['not_exist', 'brought', 'sent', 'not_given']:
            return queryset.filter(bilet_document=value)
        return queryset


class AktTrainings(SimpleListFilter):
    title = 'Акт тренинги'
    parameter_name = 'akt_trainings'

    def lookups(self, request, model_admin):
        return [
            ('yes', 'Да'),
            ('no', 'Нет'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(akt_trainings=True)
        if self.value() == 'no':
            return queryset.filter(akt_trainings=False)
        if self.value():
            return queryset


class AktIwex(SimpleListFilter):
    title = 'Акт IWEX'
    parameter_name = 'akt_iwex'

    def lookups(self, request, model_admin):
        return [
            ('yes', 'Да'),
            ('no', 'Нет'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(akt_iwex=True)
        if self.value() == 'no':
            return queryset.filter(akt_iwex=False)
        if self.value():
            return queryset


class InReview(SimpleListFilter):
    title = 'На рассмотрении'
    parameter_name = 'in_review'

    def lookups(self, request, model_admin):
        return [
            ('yes', 'Да'),
            ('no', 'Нет'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(in_review=True)
        if self.value() == 'no':
            return queryset.filter(in_review=False)
        if self.value():
            return queryset


class VisaFileFilter(SimpleListFilter):
    title = 'Скан визы'
    parameter_name = 'visa_file'

    def lookups(self, request, model_admin):
        return [
            ('yes', 'Да'),
            ('no', 'Нет'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.exclude(Q(visa_file__isnull=True) | Q(visa_file=''))
        if self.value() == 'no':
            return queryset.filter(Q(visa_file__isnull=True) | Q(visa_file=''))
        if self.value():
            return queryset

class NvksFilter(SimpleListFilter):
    title = 'НВКС'
    parameter_name = 'nvks'

    def lookups(self, request, model_admin):
        return [
            ('yes', 'Да'),
            ('no', 'Нет'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(nvks=True)
        if self.value() == 'no':
            return queryset.filter(nvks=False)
        if self.value():
            return queryset


class DirectionFilter(SimpleListFilter):
    title = 'Направление'
    parameter_name = 'direction'

    def lookups(self, request, model_admin):
        return [
            ('nord', 'Nord'),
            ('sud', 'Süd'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'nord':
            return queryset.filter(direction='nord')
        if self.value() == 'sud':
            return queryset.filter(direction='sud')
        if self.value():
            return queryset
