from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class RegisterUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = [
			'username',
			'email',
			'password1',
			'password2'
		]