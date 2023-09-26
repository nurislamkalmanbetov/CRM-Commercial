export default () => {
  const button = document.getElementById('submit-questionnaire') as HTMLButtonElement;

  if (!button) return;

  button.addEventListener('click', openQuestionnaireModal);
}

function openQuestionnaireModal() {
  const popup = document.getElementById('submit-popup') as HTMLDivElement;

  if (!popup) {
    console.warn('Popup questionnaire not found');
    return;
  }

  popup.classList.add('popup_show');
  document.body.classList.add('no-scroll');

  const cancel = popup.querySelector('#popup-cancel');
  const submit = popup.querySelector('#popup-submit');

  cancel.addEventListener('click', cancelQuestionnaireModal);
  submit.addEventListener('click', submitQuestionnaire);
}

function cancelQuestionnaireModal() {
  const popup = document.getElementById('submit-popup') as HTMLDivElement;

  if (!popup) {
    console.warn('Popup questionnaire not found');
    return;
  }

  popup.classList.remove('popup_show');
  document.body.classList.remove('no-scroll');
}

function submitQuestionnaire() {
  console.log('questionnaire is submitted');
}