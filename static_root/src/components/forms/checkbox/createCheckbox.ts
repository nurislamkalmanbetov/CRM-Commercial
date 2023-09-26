import Checkbox from './Checkbox';

export default () => {
  const CHECKBOX_QUERY = '.checkbox-wrapper';
  const checkboxes = document.querySelectorAll(CHECKBOX_QUERY) as NodeListOf<HTMLDivElement>;
  checkboxes.forEach(checkbox => new Checkbox(checkbox));
}
