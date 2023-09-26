import FileInput from './FileInput';

export default () => {
  const FILE_INPUT_QUERY = '.file-input-wrapper';
  const inputs = document.querySelectorAll(FILE_INPUT_QUERY) as NodeListOf<HTMLDivElement>;
  inputs.forEach(input => new FileInput(input));
}