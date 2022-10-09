import re
from django.core.exceptions import ValidationError


def hex_color_valid(value):
    valid_color = re.compile(r"#([a-fA-F0-9]{6}|[a-fA-F0-9]{3})$")
    if valid_color.match(value):
        return value
    raise ValidationError("Please enter a valid HEX color")
