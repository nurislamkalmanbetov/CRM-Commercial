import Form from "../form/Form";

const DATA = {
  personal: ['firstname', 'lastname', 'birthday', 'sex', 'country'],
};



export default class FormStatus {
  form: Form;
  listItems = [];
  constructor(form: Form) {
    this.form = form;
    this.init();
    this.createMenuIdList();
  }

  init() {
    this.form.form.addEventListener('change', this.checkChange.bind(this));
  }

  checkChange(e) {
    this.listItems.forEach(({ item }) => {
      const isSuccess = item.elements.every((key: string) =>
        (this.form.valids[key] && !this.form.errors[key]) || !this.form.validations[key].required);
      
      if (isSuccess) item.setStatus('success');
      
      const isError = item.elements.every((key: string) =>
        !this.form.valids[key] && this.form.errors[key]);
      
      if (isError || !isSuccess) item.setStatus('error');
    })
  }

  createMenuIdList() {
    Object.keys(DATA).forEach((key: string) => {
      const item = new ListItem(key, DATA[key]);
      this.listItems.push({
        id: key,
        item,
      });
    })
  }
}

class ListItem {
  id: string;
  elements: Array<string>;
  status: string;
  wrapper: HTMLLinkElement;
  /*
    We have a 3 statuses:
    -success - when field is successed
    -default - when field isn't touched
    -error - when field isn't successed
  */

  constructor(id: string, elements: Array<string>) {
    const wrapper = document.getElementById(`menu-${id}`) as HTMLLinkElement;
    this.wrapper = wrapper;
    this.id = id;
    this.elements = elements;
  }

  setStatus(status: string) {
    this.status = status;
    this.wrapper.className = `basic-questionnaire-page__menu-item basic-questionnaire-page__menu-item_${status}`;
  }

  getStatus() {
    return this.status;
  }
}