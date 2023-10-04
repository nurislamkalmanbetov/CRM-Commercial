import PhotoLoader from './PhotoLoader';

export default () => {
  const PHOTO_LOADER_QUERY = '.basic-questionnaire-page__photo-wrapper';

  const loader = document.querySelector(PHOTO_LOADER_QUERY) as HTMLDivElement;
  if (!loader) return;
  
  return new PhotoLoader(loader);
}