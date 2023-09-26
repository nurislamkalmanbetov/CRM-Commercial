const RESET_EMAIL_VALIDATION_SCHEMA = {
  email: {
    type: 'text',
    reg: /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/,
    msg: 'Укажите корректный email',
    required: true,
  },
}

const RESET_CODE_VALIDATION_SCHEMA = {
  code: {
    type: 'text',
    msg: 'Укажите корректный код доступа',
    reg: /^.{6,6}$/,
    required: true,
  },
}

const RESET_PASSWORD_VALIDATION_SCHEMA = {
  pass: {
    type: 'text',
    reg: /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]{8,}$/,
    msg: 'Пароль должен состоять минимум из 8 символов',
    required: true,
  },
  repeatpass: {
    type: 'text',
    reg: /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]{8,}$/,
    msg: 'Пароль должен состоять минимум из 8 символов',
    required: true,
  },
}

export {
  RESET_EMAIL_VALIDATION_SCHEMA,
  RESET_CODE_VALIDATION_SCHEMA,
  RESET_PASSWORD_VALIDATION_SCHEMA,
}