from applications.core.constants import DOCUMENTS_DESCRIPTION


def get_documents_list(key_list, request):
    documents = []

    for key in key_list:
        doc = getattr(request.user.profile, key)
        is_confirm = getattr(request.user.profile, f'{key}_confirm')
        description = DOCUMENTS_DESCRIPTION[key]
        filename = ''
        url = f'/media/{doc.name}' if doc.name else None
        if doc.name:
            filename = doc.name.replace(f'documents/profile_{request.user.profile.id}/', '')
            filename = (filename[:24] + '...') if len(filename) > 25 else filename
        else:
            filename = doc.field._verbose_name
            
        documents.append({
            'name': key,
            'title': doc.field._verbose_name,
            'default_title': doc.field._verbose_name,
            'status': doc.name != '',
            'is_confirm': is_confirm,
            'description': description,
            'url': url,
            'filename': filename,
        })

    return documents
