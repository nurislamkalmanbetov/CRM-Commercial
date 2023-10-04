export default () => {
  const button = document.getElementById('submit-questionnaire-warning') as HTMLButtonElement;

  if (!button) return;

  button.addEventListener('click', openModal);
}

function openModal(e: any) {
  e.preventDefault();
  const popup = document.getElementById('warning') as HTMLDivElement;
  popup.classList.add('popup_show');
  document.body.classList.add('no-scroll');

  const button = popup.querySelector('.warning-popup__button') as HTMLButtonElement;

  button.addEventListener('click', () => {
    popup.classList.remove('popup_show');
    document.body.classList.remove('no-scroll');

    const form = e.target.closest('form');
    
    if (!form) return;

    form.submit();

  })

}