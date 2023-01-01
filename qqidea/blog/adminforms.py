from django import forms
# 修改admin默认form组件
class PostAdminForm(forms.ModelForm):
    # 摘要字段的控件显示为Textarea
    description = forms.CharField(widget=forms.Textarea(
        attrs={'rows':3,'cols':80,'class':'form-control'}
    ),label='摘要',required=False)
