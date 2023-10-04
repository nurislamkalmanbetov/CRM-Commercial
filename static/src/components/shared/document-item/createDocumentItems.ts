import DocumentItem from './DocumentItem';


export default () => {
  const DOCUMENT_ITEMS_QUERY = '.document-item';

  const documentItems = document.querySelectorAll(DOCUMENT_ITEMS_QUERY) as NodeListOf<HTMLDivElement>;

  documentItems.forEach(document => new DocumentItem(document));

}