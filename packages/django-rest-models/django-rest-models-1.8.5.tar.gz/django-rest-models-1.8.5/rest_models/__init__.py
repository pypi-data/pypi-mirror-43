__VERSION__ = '1.8.5'

try:
    from rest_models.checks import register_checks
    register_checks()
except ImportError:  # pragma: no cover
    pass
