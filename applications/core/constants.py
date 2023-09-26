DOCUMENTS_DESCRIPTION = {
  'study_certificate': 'Справка с места учебы для регистрации',
  'study_certificate_embassy': 'Справка с места учебы для посольства',
  'study_certificate_translate_embassy': 'Перевод справки с места учебы для посольства',
  'photo_for_schengen': 'Фото на шенген 3.5x4.5',
  'zagranpassport_copy': 'Загранпаспорт',
  'passport_copy': 'Копия паспорта',
  'fluorography_express': 'Флюорография экспресс',
  'fluorography': 'Флюорография',
  'immatrikulation': 'Иммат',
  'transcript': 'Транскрипт оригинал',
  'transcript_translate': 'Перевод транскрипта',
  'bank_statement': 'Выписка с банка с подтверждением наличия минимум 500$',
  'conduct_certificate': 'Справка о несудимости, заверенная нотариусом',
  'mentaldispanser_certificate': 'Справка с психдиспансера о нормальном состоянии психического здоровья',
  'drugdispanser_certificate': 'Справка об отсутствии наркотических веществ в крови',
  'parental_permission': 'Разрешение родителей, заверенное нотариусом',
  'bank_details': 'Реквизиты банка',
}

DOCUMENT_TYPE_CHOICES = (
  ('training_agreement', 'Договор на Тренинг'),
  ('employment_agreement', 'Договор на Трудоустройство'),
  ('training_stable', 'Договор на Тренинг 6000'),
  ('acts', 'Акты'),
  ('closures', 'Расторжения'),
)


EMPLOYMENT_DOCUMENT_TYPE_CHOICES = (
  ('1000', 'Трудоустройство 1000'),
  ('2000', 'Трудоустройство 2000'),
)

AGREEMENT_ACT_TYPE_CHOICES = (
  ('training_agreement_act', 'Акт на тренинг'),
  ('employment_agreement_act', 'Акт на трудоустройство'),
  ('training_stable_act', 'Акт на тренинг 6000')
)

CLOSURE_DOC_TYPE_CHOICES = (
  ('training_closure', 'Расторжение на тренинг'),
  ('employment_closure', 'Расторжение на трудоустройство'),
  ('training_stable_closure', 'Расторжение на тренинг 6000'),
)
