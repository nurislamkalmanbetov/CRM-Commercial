export default class Checkbox {
  wrapper: HTMLDivElement;
  input: HTMLInputElement;
  label: HTMLLabelElement;

  constructor(wrapper: HTMLDivElement) {
    const input = wrapper.querySelector('.checkbox-wrapper__check') as HTMLInputElement;
    const label = wrapper.querySelector('.checkbox-wrapper__label') as HTMLLabelElement;
    this.wrapper = wrapper;
    this.input = input;
    this.label = label;

    this.init();
  }

  init() {
    this.input.addEventListener('change', this.toggle.bind(this));
    if(this.input.checked) this.toggle()
  }

  toggle() {
    if (this.input.checked) {
      this.label.classList.add('checkbox-wrapper__label_checked');
      return;
    }
    this.label.classList.remove('checkbox-wrapper__label_checked');
  }

}