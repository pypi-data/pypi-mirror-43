
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured

def pre(msg:str):
    return "".join(" ".join('[DJANGO AUTO USER]',msg),'.')

def err(err_msg:str):
    raise ImproperlyConfigured(pre(err_msg))

class DjangoAutoUser():

    def __init__(self):
        self.auto_user = settings['AUTO_USER']
        self.all_fields = [f for f in User._meta.get_fields()]
        self.required_fields =  [f for f in self.all_fields() if not getattr(f, 'blank', False) is True]
        self.unique_fields = [f for f in self.all_fields() if getattr(f, 'unique', False) is True]
        self.__validate()
        self.__automate()

    def __is_valid(self,obj,typ:type):
        if obj and isinstance(obj,typ):
            return True
        else:
            return False

    def __validate(self):
        self.__settings_validation()
        self.__users_validation()

    def __settings_validation(self):
        if not self.__is_valid(self.auto_user,list):
            err('AUTO_USER settings under Django settings must be of type list but instead is of type {}'.format(str(type(self.auto_user))))

    def __users_validation(self):
        for idx, user in self.auto_user:
            self.__is_valid_user(idx,user)
            self.__has_required_fields(idx,user)
            self.__has_all_fields(idx,user)

        self.__has_unique_users()

    def __is_valid_user(self,idx,user):
        if not self.__is__valid(user,dict):
            err('User entry at index {} in AUTO_USER settings must contain a non empty dictionary'.format(str(idx)))

    def __has_required_fields(self,idx,user):
        for f in self.required_fields:
            if not self.__is_valid(user[f.name],f.get_internal_type):
                err('User entry at index {} in AUTO_USER settings must have a the required field {} of type {}'.format(str(idx),f.name,str(f.get_internal_type)))

    def __has_all_fields(self,idx,user):
        for key in list(user.keys()):
            if not key in [f.name for f in self.all_fields]:
                err('User entry at index {} in AUTO_USER settings contains field {} which is not in User model'.format(str(idx),key))

    def __has_unique_users(self):
        for unique_field in self.unique_fields:
            users_unique_fields = [user[unique_field.name] for user in self.auto_user]
            if len(users_unique_fields) != len(set(users_unique_fields)):
                err('Uniqueness of field {} for User model is not respected in user entries of AUTO_USER settings'.format(unique_field.name))

    def __automate(self):
        for user in self.auto_users:
            u = User()
            for k,v in user:
                if k == 'password':
                    u.set_password(v)
                else:
                    u[k] = v
            u.save()

