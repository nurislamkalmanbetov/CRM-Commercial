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
    msg: 'Пароль должен состоять минимум из 8 символов и без кириллицы',
    required: true,
  }
}