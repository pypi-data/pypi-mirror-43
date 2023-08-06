import urllib.parse
from typing import Iterable, Optional, Tuple
from urllib.parse import urljoin

from flask import (
    abort, current_app, redirect, render_template, request, session, url_for)

from flask_saml2.signing import Digester, RsaSha1Signer, Sha1Digester, Signer
from flask_saml2.types import X509, PKey
from flask_saml2.utils import certificate_to_string, import_string

from .idphandler import AuthData, IdPHandler


class ServiceProvider:

    session_auth_data_key = 'saml_auth_data'
    blueprint_name = 'flask_saml2_sp'

    def login_successful(
        self,
        auth_data: AuthData,
        relay_state: str,
    ):
        """
        Called when a user is successfully logged on. Subclasses should
        override this if they want to do more with the returned user data.
        Subclasses *must* call
        ``super().login_successful(auth_data, relay_state)``, but they can
        return a different response.
        """
        self.set_auth_data_in_session(auth_data)
        return redirect(relay_state)

    # Service provider configuration

    def get_sp_config(self) -> dict:
        """
        Get the basic configuration for this service provider. This should be
        a dict like the following:

        .. code-block:: python

            >>> sp.get_sp_config()
            {
                'issuer': 'My Service Provider',
                'certificate': certificate_from_file('certificate.pem'),
                'private_key': certificate_from_file('private-key.pem'),
            }
        """
        return current_app.config['SAML2_SP']

    def get_sp_entity_id(self) -> str:
        return self.get_metadata_url()

    def get_sp_certificate(self) -> Optional[X509]:
        """Get the public certificate for this SP."""
        return self.get_sp_config().get('certificate')

    def get_sp_private_key(self) -> Optional[PKey]:
        """Get the private key for this SP."""
        return self.get_sp_config().get('private_key')

    def get_sp_signer(self) -> Optional[Signer]:
        """Get the signing algorithm used by this SP."""
        private_key = self.get_sp_private_key()
        if private_key is not None:
            return RsaSha1Signer(private_key)

    def get_sp_digester(self) -> Digester:
        """Get the digest algorithm used by this SP."""
        return Sha1Digester()

    def should_sign_requests(self) -> bool:
        """
        Should this SP sign its SAML statements. Defaults to True if the SP is
        configured with both a certificate and a private key.
        """
        return self.get_sp_certificate() is not None \
            and self.get_sp_private_key() is not None

    # Identity provider configuration

    def get_identity_providers(self) -> Iterable[Tuple[str, dict]]:
        """
        Get an iterable of identity provider ``config`` dicts.``config`` should
        be a dict specifying an IdPHandler subclass and optionally any
        constructor arguments:

        .. code-block:: python

            >>> list(sp.get_identity_providers())
            [{
                'CLASS': 'my_app.identity_providers.MyIdPIdPHandler',
                'OPTIONS': {
                    'entity_id': 'https://idp.example.com/metadata.xml',
                },
            }]

        Defaults to ``current_app.config['SAML2_IDENTITY_PROVIDERS']``.
        """
        return current_app.config['SAML2_IDENTITY_PROVIDERS']

    def get_login_url(self):
        return url_for(self.blueprint_name + '.login')

    def get_acs_url(self):
        return url_for(self.blueprint_name + '.acs', _external=True)

    def get_sls_url(self):
        return url_for(self.blueprint_name + '.sls', _external=True)

    def get_metadata_url(self):
        return url_for(self.blueprint_name + '.metadata', _external=True)

    def get_default_login_return_url(self):
        return None

    def get_login_return_url(self):
        urls = [
            request.args.get('next'),
            self.get_default_login_return_url(),
        ]
        for url in urls:
            if url is None:
                continue
            url = self.make_absolute_url(url)
            if self.is_valid_redirect_url(url):
                return url

        return None

    def get_logout_return_url(self):
        return None

    def is_valid_redirect_url(self, url):
        """
        Is this URL valid and safe to redirect to? Defaults to only allowing
        URLs on the current server.
        """
        bits = urllib.parse.urlsplit(url)

        # Relative URLs are safe
        if not bits.scheme and not bits.netloc:
            return True

        # Otherwise the scheme and server name must match
        return bits.scheme == request.scheme \
            and bits.netloc == current_app.config['SERVER_NAME']

    # IdPHandlers

    def make_idp_handler(self, config) -> IdPHandler:
        cls = import_string(config['CLASS'])
        options = config.get('OPTIONS', {})
        return cls(self, **options)

    def get_idp_handlers(self) -> Iterable[IdPHandler]:
        """
        Get the IdPHandler for each service provider defined.
        """
        for config in self.get_identity_providers():
            yield self.make_idp_handler(config)

    def get_default_idp_handler(self) -> Optional[IdPHandler]:
        """
        Get the default IdP to sign in with. When logging in, if there is
        a default IdP, the user will be automatically logged in with that IdP.
        If there is no default, a list of IdPs to sign in with will be
        presented. Return ``None`` if there is no default IdP.
        """
        handlers = list(self.get_idp_handlers())
        if len(handlers) == 1:
            return handlers[0]
        return None

    def get_idp_handler_by_entity_id(self, entity_id) -> IdPHandler:
        """
        Find a IdPHandler instance that can handle the current request.
        """
        for handler in self.get_idp_handlers():
            if handler.entity_id == entity_id:
                return handler
        raise ValueError(f"No IdP handler with entity ID {entity_id}")

    def get_idp_handler_by_current_session(self):
        """
        Get the idphandler used to authenticate the currently logged in user.
        """
        auth_data = self.get_auth_data_in_session()
        return auth_data.handler

    # Authentication

    def login_required(self) -> None:
        """
        Check if a user is currently logged in to this session, and
        :method:`flask.abort` with a redirect to the login page if not. It is
        suggested to use :meth:`is_user_logged_in`.
        """
        if not self.is_user_logged_in():
            abort(redirect(self.get_login_url()))

    def is_user_logged_in(self) -> bool:
        return self.session_auth_data_key in session and \
            AuthData.is_valid(self, session[self.session_auth_data_key])

    def logout(self) -> None:
        """Terminate the session for a logged in user."""
        self.clear_auth_data_in_session()

    # Misc

    def render_template(self, template: str, **context) -> str:
        context = {
            'sp': self,
            **context,
        }
        return render_template(template, **context)

    def set_auth_data_in_session(self, auth_data: AuthData):
        session[self.session_auth_data_key] = auth_data.to_dict()

    def clear_auth_data_in_session(self):
        session.pop(self.session_auth_data_key, None)

    def get_auth_data_in_session(self) -> AuthData:
        """
        Get an AuthData instance from the data stored for the currently logged
        in user.
        """
        return AuthData.from_dict(self, session[self.session_auth_data_key])

    def make_absolute_url(self, url):
        # TODO is there a better way of doing this?
        base = '{}://{}'.format(
            request.scheme, current_app.config['SERVER_NAME'])
        return urljoin(base, url)

    def get_metadata_context(self) -> dict:
        """
        Get any extra context for the metadata template. Suggested extra
        context variables include 'org' and 'contacts'.
        """
        return {
            'sls_url': self.get_sls_url(),
            'acs_url': self.get_acs_url(),
            'entity_id': self.get_sp_entity_id(),
            'certificate': certificate_to_string(self.get_sp_certificate()),
            'org': None,
            'contacts': [],
        }
