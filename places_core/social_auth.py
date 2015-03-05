# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
from django.core.urlresolvers import reverse
from social.pipeline.partial import partial
from social.exceptions import AuthException
from userspace.models import UserProfile
from userspace.helpers import random_string, create_username


def obtain_user_social_profile(response):
    """
    Funkcja zwraca url profilu dla odpowiedniego social-backendu.
    """
    if 'link' in response: return response['link']
    if 'url' in response: return response['url']
    return u''


def obtain_user_gender(response):
    """
    Pobranie płci w odpowiednim formacie.
    """
    if not 'gender' in response:
        return None
    else:
        if response['gender'] == 'female': return 'F'
        elif response['gender'] == 'male': return 'M'
    return 'U'


def set_user_profile_birth_date(date_string):
    """
    Funkcja formatująca datę z ciągu JSON-a do natywnej pythonowej postaci.
    Zwraca `datetime` obiekt albo None jeżeli nie może przekonwertować daty,
    bo jest w złym formacie albo co.
    """
    birth_date = None
    try:
        birth_date = date_string.split(' ')[0]
    except Exception:
        pass
    return birth_date


def validate_email(strategy, details, user=None, social=None, *args, **kwargs):
    """
    Funkcja sprawdza, czy użytkownik o adresie email pobranym od dostawcy
    usługi uwierzytelniającej istnieje już w systemie. Jeżeli tak, konto
    social auth zostanie przypisane do tego użytkownika.
    """
    system_user = None
    try:
        system_user = User.objects.get(email=details.get('email'))
    except User.DoesNotExist:
        pass
    if user is None and system_user != None:
        return {'social': social,
                'user': system_user,
                'new_association': True}


@partial
def set_twitter_email(strategy, details, user=None, is_new=False, *args, **kwargs):
    """
    Ustawienie adresu email dla użytkowników, którzy tworzą konto przez
    API Twittera.
    """
    if kwargs['backend'].name == 'twitter' and is_new:
        email = strategy.session_pop('account_email')
        if email:
            details['email'] = email
        else:
            return strategy.redirect(reverse('user:twitter_email'))


def update_user_social_profile(strategy, details, response, user, *args, **kwargs):
    """
    Funkcja sprawdza, czy w odpowiedzi serwera zawarty jest adres profilu do
    któregokolwiek konta. Jeżeli tak, a w profilu użytkownika nie ma jeszcze
    tej informacji, zostanie ona zapisana.
    """
    changed = False
    profile = UserProfile.objects.get(user=user)
    
    if kwargs['backend'].name == 'facebook' and not profile.fb_url:
        profile.fb_url = obtain_user_social_profile(response)
        changed = True
    elif kwargs['backend'].name == 'google-plus' and not profile.gplus_url:
        profile.gplus_url = obtain_user_social_profile(response)
        changed = True
    if 'gender' in response and not profile.gender:
        profile.gender = obtain_user_gender(response)
        changed = True
    if 'birthday' in response and not profile.birth_date:
        profile.birth_date = set_user_profile_birth_date(response['birthday'])
        changed = True
    if kwargs['backend'].name == 'twitter' and not profile.twt_url:
        try:
            screen_name = response['access_token']['screen_name']
            profile.twt_url = 'https://twitter.com/' + screen_name
            changed = True
        except KeyError, TypeError:
            pass
    if kwargs['backend'].name == 'linkedin' and not profile.linkedin_url:
        try:
            profile.linkedin_url = response['publicProfileUrl']
            changed = True
        except KeyError:
            pass
    if changed: profile.save()


def create_user_profile(strategy, details, response, user=None, *args, **kwargs):
    """
    Tworzenie tokenu uwierzytalniającego dla aplikacji mobilnej. Tutaj uzupełniamy
    także dodatkowe informacje do profilu użytkownika.
    """
    from rest_framework.authtoken.models import Token
    from userspace.models import UserProfile
    token = None
    if user:
        try: token = user.auth_token
        except Token.DoesNotExist:
            token = Token.objects.create(user=user)
            token.save()
        try:
            profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            profile = UserProfile(user=user)
            if 'gender' in response:
                profile.gender = obtain_user_gender(response)
            profile.save()


def get_username(strategy, details, user=None, *args, **kwargs):
    """ Ustawiamy losową nazwę użytkownika, wg naszego schematu. """
    storage = strategy.storage
    if user:
        final_username = storage.user.get_username(user)
    else:
        import json
        print json.dumps(details)
        final_username = random_string(30)
        while storage.user.user_exists(username=final_username):
            final_username = random_string(30)
    return {'username': final_username}
