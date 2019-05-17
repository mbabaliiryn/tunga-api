import json

import requests
from django.core.exceptions import ObjectDoesNotExist
from slacker import Slacker

from tunga.settings import SLACK_STAFF_OUTGOING_WEBHOOK_TOKEN, SLACK_AUTHORIZE_URL, SLACK_SCOPES, SLACK_CLIENT_ID, \
    SLACK_ACCESS_TOKEN_URL, TUNGA_ICON_SQUARE_URL_150
from tunga_profiles.utils import get_app_integration
from tunga_utils.constants import APP_INTEGRATION_PROVIDER_SLACK

KEY_TOKEN = 'token'
KEY_TEAM_ID = 'team_id'
KEY_TEAM_DOMAIN = 'team_domain'
KEY_CHANNEL_ID = 'channel_id'
KEY_CHANNEL_NAME = 'channel_name'
KEY_USER_ID = 'user_id'
KEY_USER_NAME = 'user_name'
KEY_TEXT = 'text'
KEY_TRIGGER_WORD = 'trigger_word'
KEY_TIMESTAMP = 'timestamp'
KEY_BOT_ID = 'bot_id'
KEY_BOT_NAME = 'bot_name'
KEY_SERVICE_ID = 'service_id'
KEY_USERNAME = 'username'
KEY_ICON_URL = 'icon_url'
KEY_ICON_EMOJI = 'icon_emoji'
KEY_ATTACHMENTS = 'attachments'
KEY_COLOR = 'color'
KEY_FALLBACK = 'fallback'
KEY_PRETEXT = 'pretext'
KEY_AUTHOR_NAME = 'author_name'
KEY_AUTHOR_LINK = 'author_link'
KEY_AUTHOR_ICON = 'author_icon'
KEY_TITLE = 'title'
KEY_TITLE_LINK = 'title_link'
KEY_FIELDS = 'fields'
KEY_VALUE = 'value'
KEY_SHORT = 'short'
KEY_IMAGE_URL = 'image_url'
KEY_THUMB_URL = 'thumb_url'
KEY_FOOTER = 'footer'
KEY_FOOTER_ICON = 'footer_icon'
KEY_TS = 'ts'
KEY_MRKDWN = 'mrkdwn'
KEY_MRKDWN_IN = 'mrkdwn_in'
KEY_COMMAND = 'command'
KEY_LINK_NAMES = 'link_names'
KEY_ACTIONS = 'actions'
KEY_TYPE = 'type'
KEY_URL = 'url'

KEY_ID = 'id'
KEY_CHANNELS = 'channels'
KEY_CHANNEL = 'channel'
KEY_MEMBERS = 'members'
KEY_PROFILE = 'profile'
KEY_EMAIL = 'email'
KEY_NAME = 'name'
KEY_GROUPS = 'groups'

VALUE_TYPE_BUTTON = 'button'


def get_authorize_url(redirect_uri):
    return '%s?client_id=%s&scope=%s&redirect_uri=%s' % (
        SLACK_AUTHORIZE_URL, SLACK_CLIENT_ID, ','.join(SLACK_SCOPES), redirect_uri
    )


def get_token_url():
    return SLACK_ACCESS_TOKEN_URL


def get_webhook_url(user):
    app_integration = get_app_integration(user=user, provider=APP_INTEGRATION_PROVIDER_SLACK)
    if app_integration and app_integration.extra:
        extra = json.loads(app_integration.extra)
        incoming_webhook = extra.get('incoming_webhook', None)
        if incoming_webhook:
            return incoming_webhook.get('url', None)
    return None


def verify_webhook_token(token):
    return token == SLACK_STAFF_OUTGOING_WEBHOOK_TOKEN


def get_integration_task(task):
    target_task = task
    if task.parent:
        target_task = task.parent
    return target_task


def is_task_notification_enabled(task, event_id):
    target_task = get_integration_task(task)
    return target_task.integration_set.filter(provider=APP_INTEGRATION_PROVIDER_SLACK, events__id=event_id).count() > 0


def send_incoming_webhook(url, message):
    message[KEY_LINK_NAMES] = 1
    return requests.post(url, json=message)


def get_slack_token(user):
    app_integration = get_app_integration(user=user, provider=APP_INTEGRATION_PROVIDER_SLACK)
    if app_integration and app_integration.extra:
        return app_integration.token
    return None


def send_integration_message(task, message=None, attachments=None, author_name='tunga', author_icon=TUNGA_ICON_SQUARE_URL_150):
    try:
        target_task = get_integration_task(task)
        task_integration = target_task.integration_set.get(provider=APP_INTEGRATION_PROVIDER_SLACK)
    except:
        return
    webhook_url = get_webhook_url(task.user)
    if webhook_url:
        # Attempt to send via webhook in case of old tokens
        send_incoming_webhook(webhook_url, {
            KEY_TEXT: message,
            KEY_ATTACHMENTS: attachments
        })
    else:
        # token = get_slack_token(task.user)
        send_slack_message(
            task_integration.token, task_integration.channel_id,
            message=message, attachments=attachments, author_name=author_name, author_icon=author_icon
        )


def send_project_message(project, message=None, attachments=None, author_name='tunga', author_icon=TUNGA_ICON_SQUARE_URL_150):
    try:
        slack_token = project.projectmeta_set.get(meta_key='slack_token').meta_value
        slack_channel = project.projectmeta_set.get(meta_key='slack_channel_id').meta_value
    except ObjectDoesNotExist:
        slack_token = None
        slack_channel = None

    if slack_token and slack_channel:
        # token = get_slack_token(task.user)
        send_slack_message(
            slack_token, slack_channel,
            message=message, attachments=attachments, author_name=author_name, author_icon=author_icon
        )
    else:
        webhook_url = get_webhook_url(project.owner or project.user)
        if webhook_url:
            # Attempt to send via webhook in case of old tokens
            send_incoming_webhook(webhook_url, {
                KEY_TEXT: message,
                KEY_ATTACHMENTS: attachments
            })


def send_slack_message(token, channel, message=None, attachments=None, author_name='tunga', author_icon=TUNGA_ICON_SQUARE_URL_150):
    slack_client = Slacker(token)
    slack_client.chat.post_message(
        channel, message, attachments=attachments,
        as_user=False, username=author_name, icon_url=author_icon, link_names=1
    )


def upload_file(token, channel, upload, content=None, filetype=None, filename=None, title=None, initial_comment=None):
    slack_client = Slacker(token)
    slack_client.files.upload(
        upload, channels=[channel],
        content=content, filetype=filetype, filename=filename, title=title, initial_comment=initial_comment
    )


def get_user_id(email, token):
    slack_client = Slacker(token)
    try:
        response = slack_client.users.list()
        if response.successful:
            users = response.body.get(KEY_MEMBERS, None)
            if users:
                for user in users:
                    user_profile = user.get(KEY_PROFILE, None)
                    if user_profile:
                        if user_profile.get(KEY_EMAIL, None) == email:
                            return user.get(KEY_ID, None)
    except:
        pass
    return None


def get_username(email, token):
    slack_client = Slacker(token)
    try:
        response = slack_client.users.list()
        if response.successful:
            users = response.body.get(KEY_MEMBERS, None)
            if users:
                for user in users:
                    user_profile = user.get(KEY_PROFILE, None)
                    if user_profile:
                        if user_profile.get(KEY_EMAIL, None) == email:
                            return user.get(KEY_NAME, None)
    except:
        pass
    return None


def get_user_im_id(email, token):
    user_id = get_user_id(email, token)

    if user_id:
        slack_client = Slacker(token)

        try:
            im_response = slack_client.im.open(user_id)
            if im_response and im_response.successful:
                im_details = im_response.body.get(KEY_CHANNEL, None)
                return im_details.get(KEY_ID, None)
        except:
            pass
    return 


    {
    "ok": true,
    "channel": {
        "id": "D947RLWRX"
    }
}


