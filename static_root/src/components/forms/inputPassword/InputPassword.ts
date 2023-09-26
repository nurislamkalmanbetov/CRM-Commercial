export default class InputPassword {
  wrapper: HTMLDivElement;
  input: HTMLInputElement;
  toggler: HTMLElement;

  constructor(wrapper: HTMLDivElement) {
    const input = wrapper.querySelector('.input-wrapper__input') as HTMLInputElement;
    const toggler = wrapper.querySelector('.input-wrapper__show-password') as HTMLElement;
    this.wrapper = wrapper;
    this.input = input;
    this.toggler = toggler;

    this.init();
  }

  init() {
    this.toggler.addEventListener('click', this.toggle.bind(this));
  }

  toggle() {
    this.input.focus();
    this.input.type = this.input.type === 'password' ? 'text' : 'password';
  }
}