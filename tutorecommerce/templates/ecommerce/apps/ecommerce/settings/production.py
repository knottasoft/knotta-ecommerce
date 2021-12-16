from ..production import *

{% include "ecommerce/apps/ecommerce/settings/partials/common.py" %}

CORS_ORIGIN_WHITELIST = list(CORS_ORIGIN_WHITELIST) + [
    '{% if ENABLE_HTTPS %}https://{% else %}http://{% endif %}{{ MFE_CART_MFE_APP["name"] }}.{{ MAIN_DOMAIN }}',
    '{% if ENABLE_HTTPS %}https://{% else %}http://{% endif %}{{ MFE_PAYMENT_MFE_APP["name"] }}.{{ MAIN_DOMAIN }}'
]
CSRF_TRUSTED_ORIGINS = [
    '{% if ENABLE_HTTPS %}https://{% else %}http://{% endif %}{{ MFE_CART_MFE_APP["name"] }}.{{ MAIN_DOMAIN }}',
    '{% if ENABLE_HTTPS %}https://{% else %}http://{% endif %}{{ MFE_PAYMENT_MFE_APP["name"] }}.{{ MAIN_DOMAIN }}'
]

SOCIAL_AUTH_EDX_OAUTH2_PUBLIC_URL_ROOT = "{% if ENABLE_HTTPS %}https{% else %}http{% endif %}://{{ LMS_HOST }}"

BACKEND_SERVICE_EDX_OAUTH2_KEY = "{{ ECOMMERCE_OAUTH2_KEY }}"
