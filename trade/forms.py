from django.forms import ModelForm
from .models import TradePost
from django import forms

class TradePostForm(ModelForm):
    '''ModelFormのサブクラス
    '''
    class Meta:
        '''ModelFormのインナークラス
        
        Attributes:
        model: モデルのクラス
        fields: フォームで使用するモデルのフィールドを指定
        '''
        # 作成するビューで入力されたデータをモデルに反映
        model = TradePost
        fields = ['category', 'title', 'comment','price', 'image1', 'image2']

class ContactForm(forms.Form):
    name = forms.CharField(label = 'お名前')
    email = forms.EmailField(label = 'メールアドレス')
    message = forms.CharField(label = 'メッセージ',widget=forms.Textarea)

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'お名前を入力してください'
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'メールアドレス'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['message'].widget.attrs['placeholder'] = 'メッセージを入力'
        self.fields['message'].widget.attrs['class'] = 'form-control'
