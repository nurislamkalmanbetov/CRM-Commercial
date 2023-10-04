import Form from './Form';

export default (formId: string, validations: Object) => {
  const form = document.querySelector(formId) as HTMLFormElement;
  if (!form) return;
  return new Form(form, validations);
}