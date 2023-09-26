import MaskedInput from './MaskedInput';

export default () => {
  const maskedInputIds = [
    'contacts_phone',
    'parents_contacts_phone_father',
    'parents_work_phone_father',
    'parents_contacts_phone_mother',
    'parents_work_phone_mother',
  ];

  maskedInputIds.forEach((id: string) => {
    const input = document.getElementById(id) as HTMLInputElement;
    if (!input) return;
    new MaskedInput(input);
  })
}