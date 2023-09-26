import Select from './Select';

export default () => {
  const SELECT_QUERY = '.select-wrapper';
  const selects = document.querySelectorAll(SELECT_QUERY) as NodeListOf<HTMLDivElement>;

  selects.forEach((select: HTMLDivElement) => {
    new Select(select);
  })
}