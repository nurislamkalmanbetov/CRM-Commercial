import ReturnBtn from './ReturnBtn';

export default () => {
  const RETURN_BTN_QUERY = '.return-btn';
  const btns = document.querySelectorAll(RETURN_BTN_QUERY) as NodeListOf<HTMLLinkElement>;
  btns.forEach(btn => new ReturnBtn(btn));
}