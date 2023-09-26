import FormStatus from './FormStatus';
import Form from '../form/Form';

export default (form: Form) => {
  const formStatus = new FormStatus(form);
  return formStatus;
}