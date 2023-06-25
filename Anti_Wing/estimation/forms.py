from django import forms


class TestForm(forms.Form):
    horse_id = forms.CharField()
    distance = forms.IntegerField()
    ground_type = forms.ChoiceField(
        choices=(
            (0, 'option1'),
            (1, 'option2'),
        )
    )
    ground_condition = forms.ChoiceField(
        choices=(
            (0, 'option3'),
            (1, 'option4'),
        )
    )