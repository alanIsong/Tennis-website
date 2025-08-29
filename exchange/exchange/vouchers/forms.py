from django import forms


class VoucherApplyForm(forms.Form):
    code = forms.CharField(
        label="Voucher Code",
        max_length=50,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your voucher code",
            }
        ),
    )
