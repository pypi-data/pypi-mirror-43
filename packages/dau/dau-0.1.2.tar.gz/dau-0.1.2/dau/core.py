
import warnings
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db.models import signals
from django.apps import apps
from django.db import DEFAULT_DB_ALIAS

def tag(msg:str):
    return "{} {}{}"('[DJANGO AUTO USER]',msg,'.')

def err_set(err_msg:str):
    raise ImproperlyConfigured(tag(err_msg))

def err_cre(err_msg:str):
    raise RuntimeError(err_msg)

def wrn(warn_msg:str):
    warnings.warn(tag(warn_msg))
class DjangoAutoUser():

    def __init__(self):        
        from django.contrib.auth import get_user_model
        self.auto_user = getattr(settings,'DJANGO_AUTO_USER')
        self.user_model = get_user_model()
        self.USERNAME_FIELD = self.user_model.USERNAME_FIELD
        self.__validate()
        self.__create_users()
        
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
            err_set('DJANGO_AUTO_USER settings under Django settings must be of type list but instead is of type {}'.format(str(type(self.auto_user))))

    def __users_validation(self):
        for idx, user_entry in enumerate(self.auto_user):
            self.__is_valid_user(idx,user_entry)

    def __is_valid_user(self,idx,user_entry):
        if not self.__is_valid(user_entry,dict):
            err_set('User entry at index {} in DJANGO_AUTO_USER settings must be a non empty dictionary'.format(str(idx)))
        elif not self.__is_valid(getattr(user_entry,'password'),str):
            err_set('User entry at index {} in DJANGO_AUTO_USER settings must contain a non empty "password" field of type {}'.format(str(idx),str(type(str))))
        elif not self.__is_valid(getattr(user_entry,self.USERNAME_FIELD),str): 
            err_set('User entry at index {} in DJANGO_AUTO_USER settings must contain a non empty "{}" field of type {}'.format(str(idx),self.USERNAME_FIELD,str(type(str))))

    def __create_users(self):
        for idx, user_entry in enumerate(self.auto_user):
            try:
                user, created = self.user_model.objects.get_or_create({self.USERNAME_FIELD:getattr(user_entry,self.USERNAME_FIELD)})
                user.set_password(getattr(user_entry,"password"))
                for field, value in user_entry.items():
                    if field not in [self.USERNAME_FIELD, "password"]:
                        if hasattr(user,field):
                            setattr(user,field,value)
                        else:
                            wrn('User model does not have attribute {} defined in user entry at index {} in DJANGO_AUTO_USER settings')
                user.save()

            except Exception as error:
                err_cre('Could not create user entry at index {} in DJANGO_AUTO_USER settings. {}'.format(str(idx),str(error)))
        
def post_migrate_receiver(app_config, verbosity=2, interactive=False, using=DEFAULT_DB_ALIAS, **kwargs):
    """
    Finalize the website loading.
    """
    DjangoAutoUser()