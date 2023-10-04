import SelectBand from './SelectBand';

interface Options {
  parent: string;
  valueToShow: string;
  children: Array<String>;
  form: any;
}

export default (options: Options) => {

  return new SelectBand(options.form, options.parent, options.children, options.valueToShow)
}