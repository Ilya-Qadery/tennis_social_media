import environ

env = environ.Env(
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, []),
    CORS_ALLOWED_ORIGINS=(list, []),
    KAVENEGAR_API_KEY=(str, ""),
    REDIS_URL=(str, "redis://localhost:6379/0"),
)
