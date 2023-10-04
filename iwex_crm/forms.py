from django import forms

from applications.accounts.models import Profile


class RegistrationDocumentsForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['study_certificate', 'photo_for_schengen', 'zagranpassport_copy',
                  'passport_copy', 'fluorography_express', 'immatrikulation', ]

        widgets = {
            'study_certificate': forms.FileInput(attrs={'class': 'form-control__input'}),
            'photo_for_schengen': forms.FileInput(attrs={'class': 'form-control__input'}),
            'zagranpassport_copy': forms.FileInput(attrs={'class': 'form-control__input'}),
            'passport_copy': forms.FileInput(attrs={'class': 'form-control__input'}),
            'fluorography_express': forms.FileInput(attrs={'class': 'form-control__input'}),
            'immatrikulation': forms.FileInput(attrs={'class': 'form-control__input'}),
        }


class EmbassyDocumentsForm(forms.ModelForm):

    class Meta:
        model = Profile

        fields = ['study_certificate_embassy',
                  'study_certificate_translate_embassy',
                  'transcript',
                  'transcript_translate',
                  'fluorography',
                  'bank_statement',
                  'conduct_certificate',
                  'mentaldispanser_certificate',
                  'drugdispanser_certificate',
                  'parental_permission',
                  'bank_details',
                  ]

        widgets = {
            'study_certificate_embassy': forms.FileInput(attrs={'class': 'form-control__input'}),
            'study_certificate_translate_embassy': forms.FileInput(attrs={'class': 'form-control__input'}),
            'transcript': forms.FileInput(attrs={'class': 'form-control__input'}),
            'transcript_translate': forms.FileInput(attrs={'class': 'form-control__input'}),
            'fluorography': forms.FileInput(attrs={'class': 'form-control__input'}),
            'bank_statement': forms.FileInput(attrs={'class': 'form-control__input'}),
            'conduct_certificate': forms.FileInput(attrs={'class': 'form-control__input'}),
            'mentaldispanser_certificate': forms.FileInput(attrs={'class': 'form-control__input'}),
            'drugdispanser_certificate': forms.FileInput(attrs={'class': 'form-control__input'}),
            'parental_permission': forms.FileInput(attrs={'class': 'form-control__input'}),
            'bank_details': forms.FileInput(attrs={'class': 'form-control__input'}),
        }
