from typing import Dict, List, Type

from ariadne import MutationType, convert_kwargs_to_snake_case
from graphql import GraphQLResolveInfo
from pydantic import BaseModel, EmailStr, create_model, constr

from ...auth import create_user_token
from ...conf.cache import clear_settings_cache
from ...conf.update import update_settings
from ...errors import SiteWizardDisabledError
from ...hooks import create_user_hook, create_user_token_hook
from ...types import AsyncValidator, GraphQLContext
from ...users.create import create_user
from ...validation import (
    EmailIsAvailableValidator,
    UsernameIsAvailableValidator,
    passwordstr,
    usernamestr,
    validate_data,
    validate_model,
)
from ..errorhandler import error_handler


setup_site_mutation = MutationType()


@setup_site_mutation.field("setupSite")
@convert_kwargs_to_snake_case
@error_handler
async def resolve_setup_site(
    _, info: GraphQLResolveInfo, *, input: dict  # pylint: disable=redefined-builtin
):
    if not info.context["settings"]["enable_site_wizard"]:
        raise SiteWizardDisabledError()

    input_model = create_input_model(info.context)
    cleaned_data, errors = validate_model(input_model, input)

    if cleaned_data:
        validators: Dict[str, List[AsyncValidator]] = {
            "name": [UsernameIsAvailableValidator(),],
            "email": [EmailIsAvailableValidator(),],
        }
        cleaned_data, errors = await validate_data(cleaned_data, validators, errors)

    if errors:
        return {"errors": errors}

    await update_settings(
        {
            "enable_site_wizard": False,
            "forum_name": cleaned_data["forum_name"],
            "forum_index_threads": cleaned_data["forum_index_threads"],
        }
    )
    await clear_settings_cache()

    user = await create_user_hook.call_action(
        create_user,
        cleaned_data["name"],
        cleaned_data["email"],
        password=cleaned_data["password"],
        is_administrator=True,
        is_moderator=True,
        extra={},
        context=info.context,
    )
    token = await create_user_token_hook.call_action(
        create_user_token, info.context, user, in_admin=False
    )

    return {"user": user, "token": token}


def create_input_model(context: GraphQLContext) -> Type[BaseModel]:
    return create_model(
        "SetupSiteInputModel",
        forum_name=(constr(strip_whitespace=True, min_length=1, max_length=150), ...),
        forum_index_threads=(bool, ...),
        name=(usernamestr(context["settings"]), ...),
        email=(EmailStr, ...),
        password=(passwordstr(context["settings"]), ...),
    )
