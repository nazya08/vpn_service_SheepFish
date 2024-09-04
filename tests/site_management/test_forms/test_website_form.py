import pytest
from django import forms

from site_management.forms.website import WebsiteForm
from tests.conftest import user


@pytest.mark.django_db
def test_website_form_valid_data(user):
    form_data = {
        'name': 'Test Website',
        'original_url': 'https://www.testwebsite.com'
    }
    form = WebsiteForm(data=form_data)
    assert form.is_valid()
    assert form.cleaned_data['name'] == 'Test Website'
    assert form.cleaned_data['original_url'] == 'https://www.testwebsite.com'


@pytest.mark.django_db
def test_website_form_invalid_data():
    form_data = {
        'name': '',  # Invalid data
        'original_url': 'not-a-url'  # Invalid URL
    }
    form = WebsiteForm(data=form_data)
    assert not form.is_valid()
    assert 'name' in form.errors
    assert 'original_url' in form.errors


@pytest.mark.django_db
def test_website_form_field_widgets():
    form = WebsiteForm()
    name_widget = form.fields['name'].widget
    original_url_widget = form.fields['original_url'].widget

    assert isinstance(name_widget, forms.TextInput)
    assert name_widget.attrs['class'] == 'form-control'

    assert isinstance(original_url_widget, forms.URLInput)
    assert original_url_widget.attrs['class'] == 'form-control'
