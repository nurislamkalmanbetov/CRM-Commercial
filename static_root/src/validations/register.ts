
export default {
  email: {
    type: 'text',
    reg: /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/,
    msg: 'Укажите корректный email',
    required: true,
  },
  password: {
    type: 'text',
    reg: /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]{8,}$/,
    msg: 'Пароль должен состоять минимум из 8 символов и не содержать кириллицу',
    required: true,
  },
  password2: {
    type: 'text',
    reg: /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]{8,}$/,
    msg: 'Пароль должен состоять минимум из 8 символов и не содержать кириллицу',
    required: true,
  },
  first_name: {
    type: 'text',
    msg: 'Укажите имя(используйте латиницу)',
    reg: /^[a-zA-Z" "-]{2,}$/,
    required: true,
  },
  last_name: {
    type: 'text',
    msg: 'Укажите фамилию(используйте латиницу)',
    reg: /^[a-zA-Z" "-]{2,}$/,
    required: true,
  },
  birthday: {
    type: 'text',
    msg: 'Укажите дату рождения',
    reg: /^(0[1-9]|[12]\d|3[01])-(0[1-9]|1[0-2])-([12]\d{3})$/,
    required: true,
  },
  phone: {
    type: 'text',
    msg: 'Укажите номер телефона(996xxxxxxxxx)',
    reg: /^(996)([0-9]{9,9})$/, // Todo: Need to write phone reg
    required: true,
  },
  university: {
    type: 'select',
    msg: 'Укажите университет',
    required: true,
  },
  faculty: {
    type: 'select',
    msg: 'Укажите направление',
    required: true,
  },
}