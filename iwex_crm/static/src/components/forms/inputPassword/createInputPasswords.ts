import InputPassword from './InputPassword';

export default () => {
  const INPUT_PASSWORD_QUERY = '.input-wrapper_type_password';
  const inputs = document.querySelectorAll(INPUT_PASSWORD_QUERY) as NodeListOf<HTMLDivElement>;
  inputs.forEach(input => new InputPassword(input));
}