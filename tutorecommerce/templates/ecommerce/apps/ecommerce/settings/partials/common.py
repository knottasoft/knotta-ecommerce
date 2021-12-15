import json

SECRET_KEY = "{{ ECOMMERCE_SECRET_KEY }}"
ALLOWED_HOSTS = [
    "{{ ECOMMERCE_HOST }}",
    "ecommerce",
]
PLATFORM_NAME = "{{ PLATFORM_NAME }}"
PROTOCOL = "{% if ENABLE_HTTPS %}https{% else %}http{% endif %}"

CORS_ALLOW_CREDENTIALS = True

OSCAR_DEFAULT_CURRENCY = "{{ ECOMMERCE_CURRENCY }}"

{% if MFE_ENTERPRISE_MFE_APP %}
CORS_ORIGIN_WHITELIST.append("{% if ENABLE_HTTPS %}https://{% else %}http://{% endif %}{{ MFE_ENTERPRISE_MFE_APP["name"] }}.{{ MAIN_DOMAIN }}")
{% endif %}

{% if MFE_LEARNER_MFE_APP %}
CORS_ORIGIN_WHITELIST.append("{% if ENABLE_HTTPS %}https://{% else %}http://{% endif %}{{ MFE_LEARNER_MFE_APP["name"] }}.{{ MAIN_DOMAIN }}")
{% endif %}

EDX_API_KEY = "{{ ECOMMERCE_API_KEY }}"
{% set jwt_rsa_key = rsa_import_key(JWT_RSA_PRIVATE_KEY) %}
JWT_AUTH["JWT_ISSUER"] = "{{ JWT_COMMON_ISSUER }}"
JWT_AUTH["JWT_AUDIENCE"] = "{{ JWT_COMMON_AUDIENCE }}"
JWT_AUTH["JWT_SECRET_KEY"] = "{{ JWT_COMMON_SECRET_KEY }}"
JWT_AUTH["JWT_PUBLIC_SIGNING_JWK_SET"] = json.dumps(
    {
        "keys": [
            {
                "kid": "openedx",
                "kty": "RSA",
                "e": "{{ jwt_rsa_key.e|long_to_base64 }}",
                "n": "{{ jwt_rsa_key.n|long_to_base64 }}",
            }
        ]
    }
)
JWT_AUTH["JWT_ISSUERS"] = [
    {
        "ISSUER": "{{ JWT_COMMON_ISSUER }}",
        "AUDIENCE": "{{ JWT_COMMON_AUDIENCE }}",
        "SECRET_KEY": "{{ OPENEDX_SECRET_KEY }}"
    }
]

SOCIAL_AUTH_REDIRECT_IS_HTTPS = {% if ENABLE_HTTPS %}True{% else %}False{% endif %}
SOCIAL_AUTH_EDX_OAUTH2_ISSUER = "{% if ENABLE_HTTPS %}https{% else %}http{% endif %}://{{ LMS_HOST }}"
SOCIAL_AUTH_EDX_OAUTH2_URL_ROOT = "http://lms:8000"

BACKEND_SERVICE_EDX_OAUTH2_SECRET = "{{ ECOMMERCE_OAUTH2_SECRET }}"
BACKEND_SERVICE_EDX_OAUTH2_PROVIDER_URL = "http://lms:8000/oauth2"

EDX_DRF_EXTENSIONS = {
    'OAUTH2_USER_INFO_URL': '{% if ENABLE_HTTPS %}https{% else %}http{% endif %}://{{ LMS_HOST }}/oauth2/user_info',
}

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "{{ ECOMMERCE_MYSQL_DATABASE }}",
        "USER": "{{ ECOMMERCE_MYSQL_USERNAME }}",
        "PASSWORD": "{{ ECOMMERCE_MYSQL_PASSWORD }}",
        "HOST": "{{ MYSQL_HOST }}",
        "PORT": "{{ MYSQL_PORT }}",
        "OPTIONS": {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "{{ SMTP_HOST }}"
EMAIL_PORT = "{{ SMTP_PORT }}"
EMAIL_HOST_USER = "{{ SMTP_USERNAME }}"
EMAIL_HOST_PASSWORD = "{{ SMTP_PASSWORD }}"
EMAIL_USE_TLS = {{SMTP_USE_TLS}}

COURSE_CATALOG_API_URL='{% if ENABLE_HTTPS %}https{% else %}http{% endif %}://{{ DISCOVERY_HOST }}/api/v1/'

ENTERPRISE_CATALOG_SERVICE_URL = '{% if ENABLE_HTTPS %}https{% else %}http{% endif %}://{{ ENTERPRISE_CATALOG_HOST }}/'
ENTERPRISE_SERVICE_URL = '{% if ENABLE_HTTPS %}https{% else %}http{% endif %}://{{ LMS_HOST }}/enterprise/'
ENTERPRISE_API_URL = urljoin(ENTERPRISE_SERVICE_URL, 'api/v1/')

ENTERPRISE_LEARNER_PORTAL_HOSTNAME = '{% if ENABLE_HTTPS %}https://{% else %}http://{% endif %}{{ MFE_LEARNER_MFE_APP["name"] }}.{{ MAIN_DOMAIN }}'

LOGGING["handlers"]["local"] = {
    "class": "logging.handlers.WatchedFileHandler",
    "filename": "/var/log/ecommerce.log",
    "formatter": "standard",
}

PAYMENT_PROCESSOR_CONFIG = {
    "openedx": json.loads("""{{ ECOMMERCE_PAYMENT_PROCESSORS|tojson(indent=4) }}"""),
}
PAYMENT_PROCESSOR_CONFIG["dev"] = PAYMENT_PROCESSOR_CONFIG["openedx"]
PAYMENT_PROCESSORS = list(PAYMENT_PROCESSORS) + {{ ECOMMERCE_EXTRA_PAYMENT_PROCESSOR_CLASSES }}

{% for payment_processor, urls_module in ECOMMERCE_EXTRA_PAYMENT_PROCESSOR_URLS.items() %}
EXTRA_PAYMENT_PROCESSOR_URLS["{{ payment_processor }}"] = "{{ urls_module }}"

OFFER_ASSIGNMENT_EMAIL_TEMPLATE = '''
Вы можете использовать этот код для {REDEMPTIONS_REMAINING} курса(ов).
Аккаунт: {USER_EMAIL}
Код доступа: {CODE}
Срок действия кода: {EXPIRATION_DATE}
'''

OFFER_REVOKE_EMAIL_TEMPLATE = '''
Ваш менеджер по обучению отозвал код доступа {CODE}, и он больше не присвоен вашей учетной записи edX {USER_EMAIL}.
'''

OFFER_REMINDER_EMAIL_TEMPLATE = '''
Этот код был использован вами {REDEEMED_OFFER_COUNT} раз(ы) из {TOTAL_OFFER_COUNT} доступных для применения.
Аккаунт: {USER_EMAIL}
Код доступа: {CODE}
Срок действия кода: {EXPIRATION_DATE}
'''

ECOMMERCE_URL_ROOT='{% if ENABLE_HTTPS %}https{% else %}http{% endif %}://{{ ECOMMERCE_HOST }}/'

OSCAR_FROM_EMAIL='info@knotta.ru'

OFFER_ASSIGNMEN_EMAIL_TEMPLATE_BODY_MAP = {
    'assign': OFFER_ASSIGNMENT_EMAIL_TEMPLATE,
    'revoke': OFFER_REVOKE_EMAIL_TEMPLATE,
    'remind': OFFER_REMINDER_EMAIL_TEMPLATE,
}
{% endfor %}
