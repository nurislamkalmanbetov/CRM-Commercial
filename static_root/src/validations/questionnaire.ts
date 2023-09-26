export default {
  // Main info
  first_name: {
    type: "text",
    msg: "Укажите имя (латиницей)",
    reg: /^[a-zA-Z" "-]{2,}$/,
    required: true
  },
  last_name: {
    type: "text",
    msg: "Укажите фамилию (латиницей)",
    reg: /^[a-zA-Z" "-]{2,}$/,
    required: true
  },
  first_name_ru: {
    type: "text",
    msg: "Укажите имя (на русском)",
    reg: /^[а-яА-Я" "-]{2,}$/,
    required: true
  },
  last_name_ru: {
    type: "text",
    msg: "Укажите фамилию (на русском)",
    reg: /^[а-яА-Я" "-]{2,}$/,
    required: true
  },
  bday: {
    type: "text",
    msg: "Укажите дату рождения",
    reg: /^(0[1-9]|[12]\d|3[01])-(0[1-9]|1[0-2])-([12]\d{3})$/,
    required: true
  },
  gender: {
    type: "select",
    msg: "Укажите пол",
    required: true
  },
  nationality: {
    type: "select",
    msg: "Укажите гражданство",
    required: true
  },

  // Birth Place
  birth_country: {
    type: "select",
    msg: "Укажите страну",
    required: true
  },
  birth_region: {
    type: "select",
    msg: "Укажите регион",
    required: true
  },
  birth_city: {
    type: "text",
    msg: "Укажите город/село (используйте латиницу)",
    reg: /^[a-zA-Z" "-]{2,}$/,
    required: true
  },

  // Registration place info
  reg_region: {
    type: "select",
    msg: "Укажите область",
    required: true
  },
  reg_city: {
    type: "text",
    msg: "Укажите город/село (используйте русский язык)",
    reg: /^[а-яА-Я0-9\\./"\-*^:!@#() ]{1,}$/,
    required: true
  },
  reg_city_en: {
    type: "text",
    msg: "Укажите город/село (используйте латиницу)",
    reg: /^[a-zA-Z0-9\\./"\-*^:!@#() ]{1,}$/,
    required: true
  },
  reg_district: {
    type: "text",
    msg: "Укажите район (используйте русский язык)",
    reg: /^[а-яА-Я0-9\\./"\-*^:!@#() ]{1,}$/,
    required: true
  },
  reg_district_en: {
    type: "text",
    msg: "Укажите район (используйте латиницу)",
    reg: /^[a-zA-Z0-9\\./"\-*^:!@#() ]{1,}$/,
    required: true
  },
  reg_street: {
    type: "text",
    msg: "Укажите улицу (используйте русский язык)",
    reg: /^[а-яА-Я0-9\\./"\-*^:!@#() ]{1,}$/,
    required: true
  },
  reg_street_en: {
    type: "text",
    msg: "Укажите улицу (используйте латиницу)",
    reg: /^[a-zA-Z0-9\\./"\-*^:!@#() ]{1,}$/,
    required: true
  },
  reg_house: {
    type: "text",
    msg: "Укажите дом",
    reg: /^.{1,}$/,
    required: true
  },
  reg_apartment: {
    type: "text",
    msg: "Укажите квартиру",
    reg: /^.{1,}$/,
    required: false
  },

  // Residence place info
  live_region: {
    type: "select",
    msg: "Укажите область",
    required: true
  },
  live_city: {
    type: "text",
    msg: "Укажите город/село (используйте русский язык)",
    reg: /^[а-яА-Я0-9\\./"\-*^:!@#() ]{1,}$/,
    required: true
  },
  live_city_en: {
    type: "text",
    msg: "Укажите город/село (используйте латиницу)",
    reg: /^[a-zA-Z0-9\\./"\-*^:!@#() ]{1,}$/,
    required: true
  },
  live_district: {
    type: "text",
    msg: "Укажите район (используйте русский язык)",
    reg: /^[а-яА-Я0-9\\./"\-*^:!@#() ]{1,}$/,
    required: true
  },
  live_district_en: {
    type: "text",
    msg: "Укажите район (используйте латиницу)",
    reg: /^[a-zA-Z0-9\\./"\-*^:!@#() ]{1,}$/,
    required: true
  },
  live_street: {
    type: "text",
    msg: "Укажите улицу (используйте русский язык)",
    reg: /^[а-яА-Я0-9\\./"\-*^:!@#() ]{1,}$/,
    required: true
  },
  live_street_en: {
    type: "text",
    msg: "Укажите улицу (используйте латиницу)",
    reg: /^[a-zA-Z0-9\\./"\-*^:!@#() ]{1,}$/,
    required: true
  },
  live_house: {
    type: "text",
    msg: "Укажите дом",
    reg: /^.{1,}$/,
    required: true
  },
  live_apartment: {
    type: "text",
    msg: "Укажите квартиру",
    reg: /^.{1,}$/,
    required: false
  },

  // Passport data
  passport_number: {
    type: "text",
    msg: "Укажите ID паспорта (ANxxxxxxx или IDxxxxxxx)",
    reg: /^(AN|ID)([0-9]{6,7})$/,
    required: true
  },
  zagranpassport_number: {
    type: "text",
    msg: "Укажите ID Загранпаспорта (ACxxxxxx)",
    reg: /^(AC)([0-9]{6,7})$/, // Todo: Need to write passport reg
    required: true
  },
  zagranpassport_end_time: {
    type: "text",
    msg: "Укажите время окончания загранпаспорта",
    required: false,
    reg: /^(0[1-9]|[12]\d|3[01])-(0[1-9]|1[0-2])-([12]\d{3})$/
  },

  // Contacts data
  phone: {
    type: "text",
    msg: "Укажите номер телефона",
    reg: /^(996)([0-9]{9,9})$/, // Todo: Need to write phone reg
    required: true
  },
  whatsapp_phone: {
    type: "text",
    msg: "Укажите номер What`s App",
    reg: /^(996)([0-9]{9,9})$/, // Todo: Need to write phone reg
    required: true
  },
  email: {
    type: "text",
    msg: "Укажите email",
    reg: /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/,
    required: true
  },

  // Study data
  university: {
    type: "text",
    msg: "Укажите университет",
    reg: /^.{1,}$/,
    required: false
  },
  degree: {
    type: "select",
    msg: "Укажите степень",
    required: true
  },
  faculty: {
    type: "text",
    msg: "Укажите направление",
    reg: /^.{1,}$/,
    required: false
  },
  year: {
    type: "select",
    msg: "Укажите курс",
    required: true
  },
  study_start: {
    type: "text",
    reg: /^[0-9]{4}$/,
    msg: "Укажите дату поступления",
    required: true
  },
  study_end: {
    type: "text",
    reg: /^[0-9]{4}$/,
    msg: "Укажите дату окончания",
    required: true
  },

  // Parents info
  father_phone: {
    type: "text",
    msg: "Укажите телефон",
    reg: /^(996)([0-9]{9})$/,
    required: false
  },
  father_work_phone: {
    type: "text",
    msg: "Укажите телефон",
    reg: /^(996)([0-9]{9})$/,
    required: false
  },
  mother_phone: {
    type: "text",
    msg: "Укажите телефон",
    reg: /^(996)([0-9]{9})$/,
    required: false
  },
  mother_work_phone: {
    type: "text",
    msg: "Укажите телефон",
    reg: /^(996)([0-9]{9})$/,
    required: false
  },
  father_company: {
    type: "text",
    msg: "Укажите место работы",
    reg: /^.{1,}$/,
    required: true
  },
  mother_company: {
    type: "text",
    msg: "Укажите место работы",
    reg: /^.{1,}$/,
    required: true
  },
  // Work data
  company1: {
    type: "text",
    msg: "Укажите место работы (используйте латиницу)",
    reg: /^[a-zA-Z\s\d]+$/,
    required: true
  },
  position1: {
    type: "select",
    msg: "Укажите должность",
    required: true
  },
  start_date1: {
    type: "text",
    msg: "Укажите время начала работы",
    required: true,
    reg: /^(0[1-9]|[12]\d|3[01])-(0[1-9]|1[0-2])-([12]\d{3})$/
  },
  end_date1: {
    type: "text",
    msg: "Укажите время окончания работы",
    required: true,
    reg: /^(0[1-9]|[12]\d|3[01])-(0[1-9]|1[0-2])-([12]\d{3})$/
  },
  country1: {
    type: "select",
    msg: "Укажите страну",
    required: true
  },
  company2: {
    type: "text",
    msg: "Укажите место работы (используйте латиницу)",
    reg: /^[a-zA-Z\s\d]+$/,
    required: true
  },
  position2: {
    type: "select",
    msg: "Укажите должность",
    required: true
  },
  start_date2: {
    type: "text",
    msg: "Укажите время начала работы",
    required: true,
    reg: /^(0[1-9]|[12]\d|3[01])-(0[1-9]|1[0-2])-([12]\d{3})$/
  },
  end_date2: {
    type: "text",
    msg: "Укажите время окончания работы",
    required: true,
    reg: /^(0[1-9]|[12]\d|3[01])-(0[1-9]|1[0-2])-([12]\d{3})$/
  },
  country2: {
    type: "select",
    msg: "Укажите страну",
    required: true
  },
  company3: {
    type: "text",
    msg: "Укажите место работы (используйте латиницу)",
    reg: /^[a-zA-Z\s\d]+$/,
    required: false
  },
  position3: {
    type: "select",
    msg: "Укажите должность",
    required: false
  },
  start_date3: {
    type: "text",
    msg: "Укажите время начала работы",
    required: true,
    reg: /^(0[1-9]|[12]\d|3[01])-(0[1-9]|1[0-2])-([12]\d{3})$/
  },
  end_date3: {
    type: "text",
    msg: "Укажите время окончания работы",
    required: true,
    reg: /^(0[1-9]|[12]\d|3[01])-(0[1-9]|1[0-2])-([12]\d{3})$/
  },
  country3: {
    type: "select",
    msg: "Укажите страну",
    required: false
  },

  // Language data
  german: {
    type: "select",
    msg: "Укажите уровень владения",
    required: true
  },
  english: {
    type: "select",
    msg: "Укажите уровень владения",
    required: true
  },
  turkish: {
    type: "select",
    msg: "Укажите уровень владения",
    required: true
  },
  russian: {
    type: "select",
    msg: "Укажите уровень владения",
    required: true
  },
  chinese: {
    type: "select",
    msg: "Укажите уровень владения",
    required: true
  },

  // Additional data
  shirt_size: {
    type: "select",
    msg: "Укажите размер",
    required: true
  },
  pants_size: {
    type: "select",
    msg: "Укажите размер",
    required: true
  },
  shoe_size: {
    type: "select",
    msg: "Укажите размер",
    required: true
  },
  driver_license: {
    type: "select",
    msg: "Укажите данные",
    required: true
  },
  driving_experience: {
    type: "select",
    msg: "Укажите стаж",
    required: true
  },
  transmission: {
    type: "select",
    msg: "Укажите данные",
    required: true
  },
  cat_a: {
    type: "checkbox",
    required: false,
    msg: "Укажите категорию",
    reg: /^.{0,}$/
  },

  // Bicycle license

  bicycle_skill: {
    type: "select",
    msg: "Укажите умение езды на велосипеде",
    required: "true"
  }
};
