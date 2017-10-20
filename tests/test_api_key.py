from sgbackend import SendGridBackend


def test_read_from_settings_by_default(settings):
    """API key should be read from settings if not provided in init."""
    settings.SENDGRID_API_KEY = 'somerandom key'
    sg = SendGridBackend()

    assert sg.api_key == settings.SENDGRID_API_KEY


def test_read_from_init_if_provided(settings):
    """Should pick up API key from init, if provided."""
    settings.SENDGRID_API_KEY = 'somerandom key'
    actual_key = 'another'

    sg = SendGridBackend(api_key=actual_key)

    assert sg.api_key == actual_key

""" Note: no API key configuration is tested in test_mail."""