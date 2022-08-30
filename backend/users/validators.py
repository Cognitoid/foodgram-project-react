from django.contrib.auth.validators import UnicodeUsernameValidator


class RegexUsernameValidator(UnicodeUsernameValidator):

    regex = r'^[\w.@+-]+\z'
