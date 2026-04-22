# Services

::: app.services.user_service
    options:
      members:
        - EmailAlreadyRegisteredError
        - UsernameTakenError
        - InvalidCredentialsError
        - create_user
        - authenticate_user
