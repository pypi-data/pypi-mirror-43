from django.apps import AppConfig, apps
from django.core.checks import Critical, Warning, register
from django.db.utils import OperationalError


class MicrosoftAuthConfig(AppConfig):
    name = "microsoft_auth"
    verbose_name = "Microsoft Auth"


@register()
def microsoft_auth_validator(app_configs, **kwargs):
    from django.contrib.sites.models import Site
    from .conf import config

    errors = []

    if apps.is_installed("microsoft_auth") and not apps.is_installed(
        "django.contrib.sites"
    ):

        errors.append(
            Critical(
                "`django.contrib.sites` is not installed",
                hint=(
                    "`microsoft_auth` requires `django.contrib.sites` "
                    "to be installed and configured"
                ),
                id="microsoft_auth.E001",
            )
        )

    if not hasattr(config, "SITE_ID") or config.SITE_ID is None:
        errors.append(
            Critical(
                "current site not configured",
                hint=(
                    "`django.contrib.sites` requires a `SITE_ID` setting "
                    "to be set"
                ),
                id="microsoft_auth.E002",
            )
        )
    else:
        try:
            current_site = Site.objects.get_current()
        except OperationalError:
            errors.append(
                Warning(
                    "`django.contrib.sites` migrations not ran",
                    id="microsoft_auth.W001",
                )
            )
        else:
            if str(current_site) == "example.com":
                errors.append(
                    Warning(
                        (
                            "current site is still `example.com`, Microsoft "
                            "auth might not work"
                        ),
                        hint=(
                            "Microsoft/Xbox auth uses OAuth, which requires "
                            "a real redirect URI to come back to"
                        ),
                        id="microsoft_auth.W002",
                    )
                )

    if config.MICROSOFT_AUTH_LOGIN_ENABLED:  # pragma: no branch
        if config.MICROSOFT_AUTH_CLIENT_ID == "":
            errors.append(
                Warning(
                    ("`MICROSOFT_AUTH_CLIENT_ID` is not configured"),
                    hint=(
                        "`MICROSOFT_AUTH_LOGIN_ENABLED` is `True`, but "
                        "`MICROSOFT_AUTH_CLIENT_ID` is empty. Microsoft "
                        "auth will be disabled"
                    ),
                    id="microsoft_auth.W003",
                )
            )
        if config.MICROSOFT_AUTH_CLIENT_SECRET == "":
            errors.append(
                Warning(
                    ("`MICROSOFT_AUTH_CLIENT_SECRET` is not configured"),
                    hint=(
                        "`MICROSOFT_AUTH_LOGIN_ENABLED` is `True`, but "
                        "`MICROSOFT_AUTH_CLIENT_SECRET` is empty. Microsoft "
                        "auth will be disabled"
                    ),
                    id="microsoft_auth.W004",
                )
            )

    return errors
