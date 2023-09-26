interface ValidationField {
  reg: RegExp,
  msg: string,
}

interface Validations {
  email?: ValidationField,
  password?: ValidationField,
}

export default class Form {
  form: HTMLFormElement;
  validations: Validations;
  errors: Object;
  valids: Object;
  
  constructor(form: HTMLFormElement, validations: Validations) {
    this.form = form;
    this.validations = validations;
    this.errors = {};
    this.valids = {};
    this.init();
  }

  init() {
    Object.keys(this.validations).forEach(fieldKey => {
      if(!this.form[fieldKey]) return new Error(`Form ${this.form.id} doesn't have input w name ${fieldKey}`)
      this.form[fieldKey].addEventListener('change', this.validate.bind(this, fieldKey));
      this.errors[fieldKey] = false; // need to inspect this
      this.valids[fieldKey] = false; // need to inspect this
    });
    this.submitDisable(true);
  }

  validate(name: string) {
    // @ts-ignore: Unreachable code error
    if (!this.validations[name].required) {
      this.setValid(name);
      return;
    }
    // @ts-ignore: Unreachable code error
    if (this.validations[name].type === 'file') {
      this.setValid(name);
    // @ts-ignore: Unreachable code error
    } else if (this.validations[name].type === 'select') {
      if (this.form[name].value !== '') {
        this.setValid(name);
      } else {
        // @ts-ignore: Unreachable code error
        this.setError(name, this.validations[name].msg)
      }
    } else {
      // @ts-ignore: Unreachable code error
      if (!this.validations[name].reg.test(this.form[name].value)) {
        // @ts-ignore: Unreachable code error
        this.setError(name, this.validations[name].msg);
      } else {
        this.setValid(name);
      }
    }
  }

  setError(name: string, msg: string) {
    // @ts-ignore: Unreachable code error
    this.errors[name] = msg;
    this.render();
  }

  setValid(name: string) {
    // @ts-ignore: Unreachable code error
    this.errors[name] = false;
    this.valids[name] = true;
    this.render();
  }
  

  render(errors: Object = this.errors) {
    this.clearAll();
    Object.keys(errors).forEach(field => {
      // @ts-ignore: Unreachable code error
      const fieldType = this.validations[field].type;
      if (fieldType === 'select') {
        const select = this.form.querySelector(`.select-wrapper__select[name="${field}"]`)
        const errorOutput = select.closest('.select-wrapper').querySelector('.select-wrapper__error') as HTMLSpanElement;
        // @ts-ignore: Unreachable code error
        if (errors[field]) {
          this.submitDisable(true);
          // @ts-ignore: Unreachable code error
          errorOutput.textContent = errors[field];
          errorOutput.classList.add('select-wrapper__error_show');
          select.classList.add('select-wrapper__select_error');
          select.classList.remove('select-wrapper__select_validated');
        } else if(this.valids[field]) {
          select.classList.remove('select-wrapper__select_error');
          select.classList.add('select-wrapper__select_validated');
          errorOutput.classList.remove('select-wrapper__error_show');
        }
      } else if (fieldType === 'file') {
        const wrapper = this.form.querySelector(`.file-input-wrapper__input[name="${field}"]`).closest('.file-input-wrapper');
        const label = wrapper.querySelector('.file-input-wrapper__label');
        // @ts-ignore: Unreachable code error      
        if (errors[field]) {
          this.submitDisable(true);
          const errorOutput = wrapper.querySelector('.file-input-wrapper__error') as HTMLSpanElement;
          // @ts-ignore: Unreachable code error      
          errorOutput.textContent = errors[field];
          errorOutput.classList.add('file-input-wrapper__error_show');
          label.classList.add('file-input-wrapper__label_error');
          label.classList.remove('file-input-wrapper__label_validated');
        } else if(this.valids[field]) {
          label.classList.remove('file-input-wrapper__label_error');
          label.classList.add('file-input-wrapper__label_validated');
        }
      } else if (fieldType === 'checkbox') {
      } else {
        const input = this.form.querySelector(`.input-wrapper__input[name="${field}"]`)
        // @ts-ignore: Unreachable code error      
        if (errors[field]) {
          this.submitDisable(true);
          const errorOutput = input.closest('.input-wrapper').querySelector('.input-wrapper__error') as HTMLSpanElement;
          // @ts-ignore: Unreachable code error
          errorOutput.textContent = errors[field];
          errorOutput.classList.add('input-wrapper__error_show');
          input.classList.add('input-wrapper__input_error');
          input.classList.remove('input-wrapper__input_validated');
        } else if(this.valids[field]) {
          input.classList.add('input-wrapper__input_validated');
          input.classList.remove('input-wrapper__input_error');
        }
      }
    })
  }

  clearAll() {
    const errors = this.form.querySelectorAll('.input-wrapper__error') as NodeListOf<HTMLSpanElement>;
    errors.forEach(err => {
      err.classList.remove('input-wrapper__error_show');
      const defaultError = err.getAttribute('data-default-error') as string;
      err.textContent = defaultError || 'Error';
    });

    const inputs = this.form.querySelectorAll('.input-wrapper__input') as NodeListOf<HTMLInputElement>;
    inputs.forEach(inpt => {
      inpt.classList.remove('input-wrapper__input_validated');
    });

    this.submitDisable(false);
  }

  submitDisable(value: boolean) {
    const submit = this.form.querySelector('button[type="submit"]') as HTMLButtonElement;
    submit.disabled = value;
  }
}
