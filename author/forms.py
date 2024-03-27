from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Author

class AuthorSignUpForm(UserCreationForm):
    class Meta:
        model = Author
        fields = ('username','bio_detail',)
    
class AuthorChangeForm(UserChangeForm):
    class Meta:
        model = Author
        fields = ('username','bio_detail',)