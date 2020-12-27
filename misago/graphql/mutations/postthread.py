from asyncio import gather
from typing import Dict, List, Optional, Tuple

from ariadne import MutationType, convert_kwargs_to_snake_case
from graphql import GraphQLResolveInfo
from pydantic import PositiveInt, constr, create_model

from ...auth import get_authenticated_user
from ...categories.update import update_category
from ...database import database
from ...errors import ErrorsList
from ...hooks import (
    create_post_hook,
    create_thread_hook,
    post_thread_hook,
    post_thread_input_hook,
    post_thread_input_model_hook,
)
from ...loaders import store_category, store_post, store_thread
from ...pubsub.threads import publish_thread_update
from ...richtext import parse_markup
from ...threads.create import create_post, create_thread
from ...threads.update import update_thread
from ...types import (
    AsyncValidator,
    GraphQLContext,
    ParsedMarkupMetadata,
    Post,
    PostThreadInput,
    PostThreadInputModel,
    Thread,
)
from ...validation import (
    CategoryExistsValidator,
    CategoryIsOpenValidator,
    NewThreadIsClosedValidator,
    UserIsAuthorizedRootValidator,
    threadtitlestr,
    validate_data,
    validate_model,
)
from ..errorhandler import error_handler


post_thread_mutation = MutationType()


@post_thread_mutation.field("postThread")
@convert_kwargs_to_snake_case
@error_handler
async def resolve_post_thread(
    _, info: GraphQLResolveInfo, *, input: dict  # pylint: disable=redefined-builtin
):
    input_model = await post_thread_input_model_hook.call_action(
        create_input_model, info.context
    )
    cleaned_data, errors = validate_model(input_model, input)

    if cleaned_data:
        validators: Dict[str, List[AsyncValidator]] = {
            "category": [
                CategoryExistsValidator(info.context),
                CategoryIsOpenValidator(info.context),
            ],
            ErrorsList.ROOT_LOCATION: [UserIsAuthorizedRootValidator(info.context),],
        }

        if cleaned_data.get("is_closed") and cleaned_data.get("category"):
            validators["is_closed"] = [
                NewThreadIsClosedValidator(info.context, cleaned_data["category"])
            ]

        cleaned_data, errors = await post_thread_input_hook.call_action(
            validate_input_data, info.context, validators, cleaned_data, errors
        )

    if errors:
        return {"errors": errors}

    thread, post, _ = await post_thread_hook.call_action(
        post_thread, info.context, cleaned_data
    )

    return {"thread": thread, "post": post}


async def create_input_model(context: GraphQLContext) -> PostThreadInputModel:
    return create_model(
        "PostThreadInputModel",
        category=(PositiveInt, ...),
        title=(threadtitlestr(context["settings"]), ...),
        markup=(
            constr(
                strip_whitespace=True, min_length=context["settings"]["post_min_length"]
            ),
            ...,
        ),
        is_closed=(Optional[bool], False),
    )


async def validate_input_data(
    context: GraphQLContext,
    validators: Dict[str, List[AsyncValidator]],
    data: PostThreadInput,
    errors: ErrorsList,
) -> Tuple[PostThreadInput, ErrorsList]:
    return await validate_data(data, validators, errors)


async def post_thread(
    context: GraphQLContext, cleaned_data: PostThreadInput
) -> Tuple[Thread, Post, ParsedMarkupMetadata]:
    user = await get_authenticated_user(context)
    rich_text, metadata = await parse_markup(context, cleaned_data["markup"])

    async with database.transaction():
        thread = await create_thread_hook.call_action(
            create_thread,
            cleaned_data["category"],
            cleaned_data["title"],
            starter=user,
            is_closed=cleaned_data.get("is_closed") or False,
            context=context,
        )
        post = await create_post_hook.call_action(
            create_post,
            thread,
            cleaned_data["markup"],
            rich_text,
            poster=user,
            context=context,
        )
        category = cleaned_data["category"]
        thread, category = await gather(
            update_thread(thread, first_post=post, last_post=post),
            update_category(category, increment_threads=True, increment_posts=True),
        )

    store_thread(context, thread)
    store_category(context, category)
    store_post(context, post)

    await publish_thread_update(thread)

    return thread, post, metadata
