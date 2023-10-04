import Input from './Input';

export default () => {
  /* 
    For each inputs after create Input class use focus() and blur() method.
    So in this function use no - scroll class for body, that scroll did not create bug
  */
  document.body.classList.add('no-scroll');
  const INPUT_QUERY = '.input-wrapper';
  const inputs = document.querySelectorAll(INPUT_QUERY) as NodeListOf<HTMLDivElement>;
  inputs.forEach(input => new Input(input));
  document.body.classList.remove('no-scroll');
  window.scrollTo({
    top: 0,
    left: 0,
  })
}