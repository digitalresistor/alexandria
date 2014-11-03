from pyramid.session import SignedCookieSessionFactory

def includeme(config):
    # Create the session factory, we are using the stock one
    _session_factory = SignedCookieSessionFactory(
            config.registry.settings['pyramid.secret.session'],
            httponly=True,
            max_age=864000,
            timeout=864000,
            reissue_time=1200,
            )

    config.set_session_factory(_session_factory)

