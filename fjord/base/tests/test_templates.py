from fjord.base.middleware import MOBILE_COOKIE

from fjord.base.tests import LocalizingClient, reverse
from fjord.search.tests import ElasticTestCase


# This is an ElasticTestCase instead of a normal one because the front
# page (which this queries) uses ElasticSearch. Being an
# ElasticTestCase makes sure that the testing index is properly set
# up, instead of trying to access a possibly missing index.
class TestMobileQueryStringOverride(ElasticTestCase):
    client_class = LocalizingClient

    def test_mobile_override(self):
        """Test mobile override and cookie behavior."""
        # Doing a request without specifying a mobile querystring
        # parameter should not set a cookie.
        resp = self.client.get('/')
        assert MOBILE_COOKIE not in resp.cookies

        # Doing a request and specifying the mobile querystring
        # parameter should persist that value in the MOBILE cookie.
        resp = self.client.get('/', {
            'mobile': 1
        })
        assert MOBILE_COOKIE in resp.cookies
        assert resp.cookies[MOBILE_COOKIE].value == 'yes'

        resp = self.client.get('/', {
            'mobile': 0
        })
        assert MOBILE_COOKIE in resp.cookies
        assert resp.cookies[MOBILE_COOKIE].value == 'no'


class TestGettextString(ElasticTestCase):
    client_class = LocalizingClient

    def test_gettext_in_templates(self):
        """Verify that _() returns a safe string in templates."""
        url = reverse('dashboard')
        r = self.client.get(url)
        assert r.status_code == 200

        # The & shouldn't get escaped to &amp;
        assert '&amp;raquo;' not in r.content
        assert '&raquo;' in r.content
