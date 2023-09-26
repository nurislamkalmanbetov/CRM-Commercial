export default class Input {
  wrapper: HTMLDivElement;
  input: HTMLInputElement;
  label: HTMLLabelElement;
  tip: HTMLSpanElement;

  constructor(wrapper: HTMLDivElement) {
    const input = wrapper.querySelector('.input-wrapper__input') as HTMLInputElement;
    const label = wrapper.querySelector('.input-wrapper__label') as HTMLLabelElement;
    const tip = wrapper.querySelector('.input-wrapper__tip') as HTMLSpanElement;
    this.wrapper = wrapper;
    this.input = input;
    this.label = label;
    this.tip = tip;

    this.init();
  }

  init() {
    this.input.focus();
    this.input.blur();
    this.focus();
    this.blur();
    this.input.addEventListener('focus', this.focus.bind(this));
    this.input.addEventListener('blur', this.blur.bind(this));
    const type = this.input.getAttribute('readonly');
    if (type === 'readonly') {
      this.wrapper.classList.add('input-wrapper_readonly');
    }
  }

  type() {
    return this.input.type;
  }

  focus() {

    this.input.classList.add('input-wrapper__input_focused');
    this.label.classList.add('input-wrapper__label_small');
    if (this.tip) {
      this.tip.classList.add('input-wrapper__tip_show');
    }
  }

  blur() {
    if (this.tip) {
      this.tip.classList.remove('input-wrapper__tip_show');
    }
    if (!this.input.value.length) {
      this.label.classList.remove('input-wrapper__label_small');
      this.input.classList.remove('input-wrapper__input_focused');
    }
  }

}