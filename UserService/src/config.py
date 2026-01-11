from supertokens_python.recipe import dashboard
from supertokens_python.recipe import userroles
from supertokens_python.recipe import thirdparty
from supertokens_python.recipe.thirdparty.provider import ProviderInput, ProviderConfig, ProviderClientConfig
from supertokens_python.recipe.emailpassword import InputFormField
from supertokens_python.recipe import emailpassword, session
from supertokens_python.recipe.emailpassword.interfaces import (
    APIInterface,
    APIOptions,
    SignUpPostOkResult,
)
from supertokens_python.recipe.emailpassword.types import FormField
from typing import List, Dict, Any, Union
from supertokens_python.recipe.session.interfaces import SessionContainer

#SQL BEGIN
from pydantic_settings import BaseSettings

from models.user_model import UserCreate


class Settings(BaseSettings):
    db_host: str = "localhost"
    db_user: str = "auth_service"
    db_password: str = "LivinOnLove"
    db_name: str = "user_service"
    jwt_secret: str = "supersecretkey"
    user_api_url: str = "http://localhost"
    website_url: str = "http://localhost"
    super_tokens_api_url: str = "https://try.supertokens.com"
    website_port: int = 3000
    service_port: int = 3001

    class Config:
        env_file = ".env"

settings = Settings()
#SQL END

#SuperTokens BEGIN
from supertokens_python import init, InputAppInfo, SupertokensConfig
import os

def get_api_domain() -> str:
    api_port = str(settings.service_port)
    api_url = f"{settings.user_api_url}:{api_port}"
    return api_url

def get_website_domain() -> str:
    website_port = str(settings.website_port)
    website_url = f"{settings.website_url}:{website_port}"
    return website_url

def get_form_value(form_fields: List[FormField], field_id: str) -> str | None:
    for field in form_fields:
        if field.id == field_id:
            return field.value
    return None

def override_email_password_apis(original_implementation: APIInterface):
    original_sign_up_post = original_implementation.sign_up_post

    async def sign_up_post(
        form_fields: List[FormField],
        tenant_id: str,
        session: Union[SessionContainer, None],
        should_try_linking_with_session_user: Union[bool, None],
        api_options: APIOptions,
        user_context: Dict[str, Any],
    ):
        # First we call the original implementation of sign_up_post.
        response = await original_sign_up_post(
            form_fields,
            tenant_id,
            session,
            should_try_linking_with_session_user,
            api_options,
            user_context,
        )

        # Post sign up response, we check if it was successful
        if isinstance(response, SignUpPostOkResult):
            from database import insert_user, create_tenant
            user_id = response.user.id
            email = response.user.emails[0]

            name = get_form_value(form_fields, "name")
            lastname = get_form_value(form_fields, "lastname")
            company_name = get_form_value(form_fields, "company")

            print(user_id)
            print(email)
            print(name)
            print(lastname)

            # Determine company_id
            if company_name:
                # Create tenant with default size (e.g., 1)
                tenant_id = create_tenant(company_name, size=10)
            else:
                # fallback default company_id
                tenant_id = 1

            user = UserCreate(
                email=email,
                name=name,
                lastname=lastname,
                company_id=tenant_id
            )

            insert_user(user_id, user)
            #TODO: Fix šumnike (custom field lastname ne dela, ce ma šumnike
        return response

    original_implementation.sign_up_post = sign_up_post
    return original_implementation

supertokens_config = SupertokensConfig(
    connection_uri=settings.super_tokens_api_url
)

app_info = InputAppInfo(
    app_name="SuperTokens Demo App",
    api_domain=get_api_domain(),
    website_domain=get_website_domain(),
    api_base_path="/auth",
    website_base_path="/auth"
)

recipe_list = [
    session.init(),
    dashboard.init(),
    userroles.init(),
    emailpassword.init(
        sign_up_feature=emailpassword.InputSignUpFeature(
            form_fields=[InputFormField(id='name'), InputFormField(id='lastname', optional=False), InputFormField(id='company', optional=True)]
        ),
        override=emailpassword.InputOverrideConfig(
                apis=override_email_password_apis
        )
    ),
    thirdparty.init(
        sign_in_and_up_feature=thirdparty.SignInAndUpFeature(
            providers=[
                ProviderInput(
                    config=ProviderConfig(
                        third_party_id="google",
                        clients=[
                            ProviderClientConfig(
                                client_id="1060725074195-kmeum4crr01uirfl2op9kd5acmi9jutn.apps.googleusercontent.com",
                                client_secret="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"
                            )
                        ]
                    )
                )
            ]
        )
    )
]

init(
    supertokens_config=supertokens_config,
    app_info=app_info,
    framework="fastapi",
    recipe_list=recipe_list,
    mode="asgi",
    telemetry=False
)
#SuperTokens END