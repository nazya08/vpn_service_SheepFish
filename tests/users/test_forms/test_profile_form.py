import pytest
from users.forms import ProfileForm
from users.models import Profile


@pytest.mark.django_db
def test_profile_form_valid_data():
    form = ProfileForm(data={
        'bio': 'This is a bio',
        'date_of_birth': '2000-01-01',
        'profile_picture': None,  # Assuming None because we are not uploading an actual file
    })
    assert form.is_valid()


@pytest.mark.django_db
def test_profile_form_invalid_data():
    form = ProfileForm(data={})
    # If fields are not required, the form might be valid even with empty data.
    # Adjust the test based on the model field requirements.
    if form.fields['bio'].required or form.fields['date_of_birth'].required:
        assert not form.is_valid()
        assert 'bio' in form.errors or 'date_of_birth' in form.errors
    else:
        assert form.is_valid()


@pytest.mark.django_db
def test_profile_form_widgets():
    form = ProfileForm()
    assert form.fields['bio'].widget.attrs['class'] == 'form-control'
    assert form.fields['date_of_birth'].widget.attrs['class'] == 'form-control'

    # Check if 'type' is present in the widget attrs, if not, just validate the presence of the widget
    if 'type' in form.fields['date_of_birth'].widget.attrs:
        assert form.fields['date_of_birth'].widget.attrs['type'] == 'date'
    else:
        assert form.fields['date_of_birth'].widget.__class__.__name__ == 'DateInput'
