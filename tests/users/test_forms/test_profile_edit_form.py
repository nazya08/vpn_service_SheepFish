import pytest
from users.forms import ProfileEditForm
from users.models import Profile


@pytest.mark.django_db
def test_profile_edit_form_valid_data():
    form = ProfileEditForm(data={
        'bio': 'This is an updated bio',
        'profile_picture': None,  # Assuming None because we are not uploading an actual file
    })
    assert form.is_valid()


@pytest.mark.django_db
def test_profile_edit_form_invalid_data():
    form = ProfileEditForm(data={})
    if form.fields['bio'].required:
        assert not form.is_valid()
        assert 'bio' in form.errors
    else:
        assert form.is_valid()


@pytest.mark.django_db
def test_profile_edit_form_widgets():
    form = ProfileEditForm()
    assert form.fields['bio'].widget.attrs['class'] == 'form-control'
    assert form.fields['profile_picture'].widget.attrs['class'] == 'form-control-file'
