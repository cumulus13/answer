from django import forms
from answer.models import Categories


class CheckForm(forms.ModelForm):
	name = forms.CharField(
		required=True,
		widget=forms.widgets.Textarea(
			attrs={
				"placeholder": "Something ....",
				"class": "textarea is-success is-medium",
			}
		),
		label = "",
	)

	class Meta:
		model = "Categories"
		exclude = ("url", )
