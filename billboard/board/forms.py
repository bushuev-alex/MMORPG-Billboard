from django import forms
from board.models import Advertisement
from django.core.exceptions import ValidationError
from django.utils.translation import gettext


class FeedbackForm(forms.Form):
    text = forms.CharField(label="Leave a feedback", max_length=1024)


class AdvertisementForm(forms.ModelForm):
    title = forms.CharField(max_length=50)

    class Meta:
        model = Advertisement
        fields = ["author", "category", "title", "text"]

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        text = cleaned_data.get("text")
        # type = cleaned_data.get("type")

        if title == text:
            raise ValidationError(gettext("Title and text should be different."))

        return cleaned_data
