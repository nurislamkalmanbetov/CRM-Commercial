// import * as Inputmask from "inputmask";

export default class MaskedInput {
  input: HTMLInputElement;
  mask: any;

  constructor(input: HTMLInputElement) {
    this.input = input;

    this.init();
  }

  init() {
    // console.log(Inputmask);
    // this.mask = new Inputmask("+999 (999)-99-99-99");
    // this.mask.mask(this.input);
  }
}