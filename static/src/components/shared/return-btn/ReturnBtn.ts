export default class ReturnBtn {
  btn: HTMLLinkElement;

  constructor(btn: HTMLLinkElement) {
    this.btn = btn;

    this.init()
  }

  private init() {
    this.btn.addEventListener('click', this.goBack);
  }

  private goBack() {
    window.history.back();
  }
}