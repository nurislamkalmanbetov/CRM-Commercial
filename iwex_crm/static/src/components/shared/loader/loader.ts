export default class Loader {
  wrapper: HTMLDivElement;
  text: string;


  constructor(text: string = 'Загрузка...') {
    this.text = text;
    this.init();
  }

  init() {
    const wrapper = document.createElement('div');
    wrapper.className = 'loader';
    wrapper.innerHTML = `
      <div class="loader__content">
        <div class="loader__logo"></div>
        <div class="loader__spinner"></div>
        <span class="loader__text">${this.text}</span>
      </div>
    `;
    document.body.appendChild(wrapper);
    this.wrapper = wrapper;
  }

  show() {
    document.body.classList.add('no-scroll');
    this.wrapper.classList.add('loader_show');
  }
  
  remove() {
    document.body.classList.remove('no-scroll');
    this.wrapper.classList.remove('loader_show');
  }
}