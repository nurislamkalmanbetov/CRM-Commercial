export default class SelectBand {
  form: any;
  parent: HTMLSelectElement;
  children: Array<String>;
  valueToShow: string;

  constructor(form: any, parentId: string, children: Array<String>, valueToShow: string) {
    this.form = form;
    this.parent = document.getElementById(parentId) as HTMLSelectElement;
    this.children = children;
    this.valueToShow = valueToShow;
    if (this.parent) {
      this.init();
    }
  }

  init() {
    this.parent.addEventListener('change', this.handleChangeParent.bind(this));
    
    if (this.check(this.parent.value)) {
      this.showChildrens();
    } else {
      this.hideChildrens();
    }
  }

  check(value: string) {
    return value === this.valueToShow;
  }

  handleChangeParent(e) {
    const value = e.target.selectedOptions[0].value;
    if (this.check(value)) {
      this.showChildrens();
    } else {
      this.hideChildrens();
    }
  }

  showChildrens() {
    this.children.forEach((id: string) => {
      this.form.validations[id].required = true;
      const element = document.getElementById(id) as HTMLElement;
      let wrapper = element.closest('.select-wrapper') as HTMLElement;
      if(!wrapper) wrapper = element.closest('.input-wrapper') as HTMLElement;
      if(!wrapper) wrapper = element.closest('.checkbox-group') as HTMLElement;
      if (!wrapper) throw new Error('Error with find wrapper in SelectBand.js');
      wrapper.style.display = '';
    })
  }

  hideChildrens() {
    this.children.forEach((id: string) => {
      this.form.validations[id].required = false;
      const element = document.getElementById(id) as HTMLElement;
      let wrapper = element.closest('.select-wrapper') as HTMLElement;
      if(!wrapper) wrapper = element.closest('.input-wrapper') as HTMLElement;
      if (!wrapper) wrapper = element.closest('.checkbox-group') as HTMLElement;
      if (!wrapper) throw new Error('Error with find wrapper in SelectBand.js');
      wrapper.style.display = 'none';
    })
  }
}