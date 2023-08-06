import requests

try:
    from django.contrib.auth.views import logout
except ImportError:
    try:
        from django.contrib.auth.views import logout_view as logout
    except ImportError:
        from django.contrib.auth import logout

from django.shortcuts import redirect, render
from django.conf import settings
from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2CallbackView,
    OAuth2LoginView,
)

from .provider import OrfiumOAuth2Provider
from django.conf import settings

PRODUCTION_ORFIUM_ENDPOINT = 'https://api.orfium.com'

try:
    API_ORFIUM_ENDPOINT = settings.API_ORFIUM_ENDPOINT.split('/v1')[0]
except AttributeError:
    # use the production endpoint by default
    API_ORFIUM_ENDPOINT = PRODUCTION_ORFIUM_ENDPOINT


# on production, we use auth.orfium.com for login
if API_ORFIUM_ENDPOINT == PRODUCTION_ORFIUM_ENDPOINT:
    LOGIN_BASE_URL = 'https://auth.orfium.com'
else:
    LOGIN_BASE_URL = API_ORFIUM_ENDPOINT

# get the session cookie from the api endpoint
SESSION_COOKIE_DOMAIN = '.'.join(
        [''] +
        API_ORFIUM_ENDPOINT.
        replace('https://', '').
        replace('http://', '').
        split('.')[1:]
    ). \
    split(':')[0]


class OrfiumOAuth2CallbackView(OAuth2CallbackView):

    def dispatch(self, request):
        result = super(OrfiumOAuth2CallbackView, self).dispatch(request)

        # check if logged in
        is_authenticated = request.user.is_authenticated

        # Django >= 1.10 (?)
        if is_authenticated not in [True, False]:
            is_authenticated = is_authenticated()

        # ignore errors if we're already logged in
        # error here is a 200 since the error page of allauth is rendered
        # success would be 302
        if result.status_code == 200 and is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)

        # redirect to the default redirect page instead of connections
        try:
            if result.url.endswith('/social/connections/'):
                return redirect(settings.LOGIN_REDIRECT_URL)
        except AttributeError:
            pass

        return result


class OrfiumOAuth2Adapter(OAuth2Adapter):
    provider_id = OrfiumOAuth2Provider.id
    access_token_url = '%s/oauth/token/' % LOGIN_BASE_URL
    authorize_url = '%s/oauth/authorize/' % LOGIN_BASE_URL
    profile_url = '%s/v1/my/info/' % API_ORFIUM_ENDPOINT
    # See:
    # http://developer.linkedin.com/forum/unauthorized-invalid-or-expired-token-immediately-after-receiving-oauth2-token?page=1 # noqa
    access_token_method = 'POST'

    def complete_login(self, request, app, token, **kwargs):
        extra_data = self.get_user_info(token)
        return self.get_provider().sociallogin_from_response(
            request, extra_data)

    def get_user_info(self, token):
        resp = requests.get(self.profile_url,
                            headers={'Authorization': 'Bearer %s' % token.token})
        return resp.json()['user_info']


oauth2_login = OAuth2LoginView.adapter_view(OrfiumOAuth2Adapter)
oauth2_callback = OrfiumOAuth2CallbackView.adapter_view(OrfiumOAuth2Adapter)


def logout_view(request):
    # logout from the dashboard
    logout(request)

    # we need an intermediate page in order to first delete the sessionid cookie
    response = render(request, 'api-logout-redirect.html', {
        'API_LOGOUT_URL': '%s/accounts/logout/' % LOGIN_BASE_URL
    })

    # logout from the main website as well
    # temporarily, until all authentications is handled by api.orfium.com
    response.delete_cookie('sessionid', domain=SESSION_COOKIE_DOMAIN)

    return response
