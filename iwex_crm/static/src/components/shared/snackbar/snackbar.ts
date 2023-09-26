let timeout: any;

export default (text: string, type: 'success' | 'danger' | 'warning', ms: number) => {
  
  const classes = `snackbar snackbar_${type}`;

  const snackbar = document.createElement('div');
  snackbar.className = classes;
  snackbar.innerHTML = `
    <div class="snackbar__text">${text}</div>
    <span class="snackbar__action"></span>
  `;
  const action = snackbar.querySelector('.snackbar__action') as HTMLDivElement;
  action.addEventListener('click', closeSnackbar.bind(null, snackbar));

  document.body.appendChild(snackbar);
  snackbar.classList.add('snackbar_show');
  timeout = setTimeout(closeSnackbar.bind(null, snackbar), ms);
}

function closeSnackbar(snackbar: HTMLDivElement) {
  snackbar.classList.remove('snackbar_show');
}