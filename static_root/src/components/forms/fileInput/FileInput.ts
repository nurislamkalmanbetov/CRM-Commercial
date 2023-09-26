export default class FileInput {
  wrapper: HTMLDivElement;
  input: HTMLInputElement;
  label: HTMLLabelElement;

  constructor(wrapper: HTMLDivElement) {
    const input = wrapper.querySelector('.file-input-wrapper__input') as HTMLInputElement;
    const label = wrapper.querySelector('.file-input-wrapper__label') as HTMLLabelElement;
    this.input = input;
    this.wrapper = wrapper;
    this.label = label;

    this.init();
  }

  init() {
    this.input.addEventListener('change', this.handleChange.bind(this));
  }

  handleChange(ev: any) {
    if (ev.target.files && ev.target.files.length) {
      this.label.textContent = ev.target.files[0].name || '';
    }
  }
}