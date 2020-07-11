from django.contrib.auth import get_user_model

from ..users.setupnewuser import setup_new_user

User = get_user_model()


def get_or_create_user(request, user_data):
    try:
        user = User.objects.get(sso_id=user_data["id"])
        if user_needs_updating(user, user_data):
            update_user(user, user_data)
        return user
    except User.DoesNotExist:
        user = User.objects.create_user(
            user_data["username"],
            user_data["email"],
            is_active=user_data.get("is_active", True),
            sso_id=user_data["id"],
        )
        if is_more_user_data(user_data):
            update_profile_fields(user, user_data)
        user.update_acl_key()
        setup_new_user(request.settings, user)
        return user


def user_needs_updating(user, user_data):
    return any(
        (
            user.username != user_data["username"],
            user.email != user_data["email"],
            user.is_active != user_data.get("is_active", user.is_active),
        )
    )


def update_user(user, user_data):
    if user.username != user_data["username"]:
        user.set_username(user_data["username"])
    if user.email != user_data["email"]:
        user.set_email(user_data["email"])
    if user.is_active != user_data.get("is_active", user.is_active):
        user.is_active = user_data["is_active"]
    user.save()


def is_more_user_data(user_data):
    return any(
        (
            'real_name' in user_data,
            'gender' in user_data,
            'location' in user_data,
        )
    )


def update_profile_fields(user, user_data):
    if "real_name" in user_data:
        user.profile_fields['real_name'] = user_data['real_name']
    if "gender" in user_data:
        user.profile_fields['gender'] = user_data['gender']
    if "location" in user_data:
        user.profile_fields['location'] = user_data['location']

    user.save(update_fields=["profile_fields"])
