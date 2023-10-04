export default class Select {
  wrapper: HTMLDivElement;
  select: HTMLSelectElement;
  label: HTMLLabelElement;
  constructor(wrapper: HTMLDivElement) {
    const select = wrapper.querySelector('.select-wrapper__select') as HTMLSelectElement;
    const label = wrapper.querySelector('.select-wrapper__label') as HTMLLabelElement;
    this.wrapper = wrapper;
    this.select = select;
    this.label = label;
    this.init();
  }
  init() {
    this.select.addEventListener('change', this.handleChange.bind(this));
    this.checkSelect();
  }
  checkSelect() {
    if (this.select.selectedOptions[0].value !== '') {
      this.label.classList.add('select-wrapper__label_small');
    } else {
      this.label.classList.remove('select-wrapper__label_small');
    }
  }
  handleChange(e: any) {
    if (e.target.value !== '') {
      this.label.classList.add('select-wrapper__label_small');
    } else {
      this.label.classList.remove('select-wrapper__label_small');
    }
  }
}