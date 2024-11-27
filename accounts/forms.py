from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class  Meta:
        # 連携するUserモデルを設定
        model = CustomUser
        # 使用するフィールドを設定
        fields = ('username', 'password1' ,'password2')