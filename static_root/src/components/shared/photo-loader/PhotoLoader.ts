import snackbar from '../snackbar/index';
import Loader from '../loader/index';
import Cookies from 'js-cookie';

export default class PhotoLoader {
  wrapper: HTMLDivElement;
  input: HTMLInputElement;
  image: HTMLDivElement;
  label: HTMLLabelElement;
  rotateInput: HTMLInputElement;
  helper: HTMLSpanElement;

  constructor(wrapper: HTMLDivElement) {

    const input = wrapper.querySelector('.basic-questionnaire-page__photo-wrapper-input') as HTMLInputElement;
    const image = wrapper.querySelector('.basic-questionnaire-page__photo-wrapper-photo') as HTMLDivElement;
    const label = wrapper.querySelector('.basic-questionnaire-page__photo-wrapper-label') as HTMLLabelElement;
    const rotateInput = wrapper.querySelector('#rotate') as HTMLInputElement;
    const helper = wrapper.querySelector('.basic-questionnaire-page__photo-wrapper-helper') as HTMLSpanElement;

    this.wrapper = wrapper;
    this.input = input;
    this.image = image;
    this.label = label;
    this.rotateInput = rotateInput;
    this.helper = helper;

    this.init();
  }

  init() {
    this.input.addEventListener('change', this.handleInputChange.bind(this));

    const status = this.image.getAttribute('data-status');
    if(status) {
      this.changeStyles();
    }
  }

  handleInputChange(e: any) {
    const headers = new Headers();
    headers.append('X-CSRFToken', Cookies.get('csrftoken'));
    const formData = new FormData();
    formData.append('photo', e.target.files[0]);
    const loader = new Loader();
    loader.show();
    fetch('/api/v1/upload/', {
      method: 'POST',
      body: formData,
      headers: headers,
      credentials: "same-origin",
    })
      .then((res: any) => res.json())
      .then((res: any) => {
        loader.remove();
        if (res.code === 200) {
          this.successFileLoad(res.photo);
        } else {
          this.failFileLoad(res.error);
        }
      })
      .catch((err: any) => {
        console.warn(`Error with send photo, info: ${err}`)
        loader.remove();
        snackbar('Что-то пошло не так :(', 'danger', 3000);
      })
  }

  failFileLoad(err: string) {
    snackbar(err, 'danger', 3000);
    this.input.value = '';
    this.input.type = '';
    this.input.type = 'file';
  }

  successFileLoad(url: string) {
    snackbar('Фото успешно добавлено', 'success', 3000);
    this.image.style.backgroundImage = `url(${url})`;
    this.changeStyles();
  }

  changeStyles() {
    this.label.style.display = 'none';
    this.image.classList.add('basic-questionnaire-page__photo-wrapper-photo_success');
    this.helper.classList.add('basic-questionnaire-page__photo-wrapper-helper_show');
    this.image.addEventListener('click', this.rotate.bind(this));
  }

  rotate() {
    this.rotateInput.value = `${Number(this.rotateInput.value) + 90}`;
    if (Number(this.rotateInput.value) >= 360) this.rotateInput.value = '0';
    this.image.style.transform = `rotate(${this.rotateInput.value}deg)`;
  }
}
