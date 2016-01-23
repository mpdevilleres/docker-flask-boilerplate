from wtforms.validators import ValidationError, Optional, Required


class RequiredIfFieldOneGreaterThanFieldTwo(object):
    """
    Compares the value of two fields if field1 is greater than field2 allow and validate.

    :param field1:
        The name of the greater field.
    :param field2:
        The name of the lesser field.
    :param message:
        Error message to raise in case of a validation error. Can be
        interpolated with `%(other_label)s` and `%(other_name)s` to provide a
        more helpful error.
    """
    def __init__(self, field1=None, field2=None, message=None):

        self.field1 = field1
        self.field2 = field2
        self.message = message

    def __call__(self, form, field):
        try:
            greater = form[self.field1]
            lesser = form[self.field2]
        except KeyError:
            raise ValidationError(field.gettext(u"Invalid field name '%s' or '%s'.") % self.field1, self.field2)

        if field.data == '' and (greater.data < lesser.data):
            if self.message is None:
                self.message = field.gettext(u"'{}' must be greater than '{}'".format(self.field1, self.field2))

            raise ValidationError(self.message)

class RequiredIfNotZero(object):
    """
    Required if field has zero Value

    :param field1:
        The name of the greater field.
    :param field2:
        The name of the lesser field.
    :param message:
        Error message to raise in case of a validation error. Can be
        interpolated with `%(other_label)s` and `%(other_name)s` to provide a
        more helpful error.
    """
    def __init__(self, other_field=None, message=None):

        self.other_field = other_field
        self.message = message

    def __call__(self, form, field):
        try:
            other_field = form[self.other_field]
        except KeyError:
            raise ValidationError(field.gettext(u"Invalid field name '%s' or '%s'.") % self.field1, self.field2)

        if field.data != '' and (other_field != 0):
            if self.message is None:
                self.message = field.gettext(u"{} is required".format(field))

            raise ValidationError(self.message)

class RequiredIf(Required):
    # a validator which makes a field required if
    # another field is set and has a truthy value

    def __init__(self, other_field_name, *args, **kwargs):
        self.other_field_name = other_field_name
        super(RequiredIf, self).__init__(*args, **kwargs)

    def __call__(self, form, field):
        other_field = form._fields.get(self.other_field_name)
        if other_field is None:
            raise Exception('no field named "%s" in form' % self.other_field_name)
        if bool(other_field.data):
            super(RequiredIf, self).__call__(form, field)

class RequiredIfValue(object):
    """Validates field conditionally.
    Usage::
        login_method = StringField('', [AnyOf(['email', 'facebook'])])
        email = StringField('', [RequiredIf(login_method='email')])
        password = StringField('', [RequiredIf(login_method='email')])
        facebook_token = StringField('', [RequiredIf(login_method='facebook')])
    """
    def __init__(self, *args, **kwargs):
        self.conditions = kwargs

    def __call__(self, form, field):
        for name, data in self.conditions.items():
            if name not in form._fields:
                Optional(form, field)
            else:
                condition_field = form._fields.get(name)
                if condition_field.data == data and not field.data:
                    Required()(form, field)
        Optional()(form, field)