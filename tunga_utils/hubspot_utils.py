from copy import copy

import datetime
import requests
from django.utils import six

from tunga.settings import HUBSPOT_API_KEY, TUNGA_URL, HUBSPOT_DEFAULT_DEAL_STAGE_MEMBER, HUBSPOT_DEFAULT_DEAL_STAGE_NEW_USER
from tunga_utils.constants import TASK_SOURCE_NEW_USER, PROJECT_STAGE_OPPORTUNITY

HUBSPOT_API_BASE_URL = 'https://api.hubapi.com'
HUBSPOT_ENDPOINT_CREATE_UPDATE_CONTACT = '/contacts/v1/contact/createOrUpdate/email/{contact_email}/'
HUBSPOT_ENDPOINT_CREATE_DEAL = '/deals/v1/deal'
HUBSPOT_ENDPOINT_CREATE_DEAL_PROPERTY = '/properties/v1/deals/properties/'
HUBSPOT_ENDPOINT_CREATE_TAG_PROPERTY = '/contacts/v1/properties/tag'
HUBSPOT_ENDPOINT_CREATE_ENGAGEMENT = '/engagements/v1/engagements'
HUBSPOT_ENDPOINT_GET_OWNER = '/owners/v2/owners'
HUBSPOT_ENDPOINT_GET_DEAL = '/deals/v1/deal/{deal_id}'
HUBSPOT_ENDPOINT_GET_DEAL_PROPERTIES = '/properties/v1/deals/properties/'
HUBSPOT_ENDPOINT_GET_DEAL_PROPERTY = '/properties/v1/deals/properties/named/{property_name}'
HUBSPOT_ENDPOINT_GET_PIPELINES = '/deals/v1/pipelines'

KEY_VID = 'vid'
KEY_NAME = 'name'
KEY_LABEL = 'label'
KEY_DESCRIPTION = 'description'
KEY_TYPE = 'type'
KEY_FIELDTYPE = 'fieldType'
KEY_GROUPNAME = 'groupName'
KEY_DEALNAME = 'dealname'
KEY_DEALSTAGE = 'dealstage'
KEY_DEALTYPE = 'dealtype'
KEY_PIPELINE = 'pipeline'
KEY_AMOUNT = 'amount'
KEY_VALUE = 'value'
KEY_PIPELINE_ID = 'pipelineId'
KEY_STAGE_ID = 'stageId'
KEY_STAGES = 'stages'
KEY_HUBSPOT_OWNER_ID = 'hubspot_owner_id'
KEY_OWNERID = 'ownerId'
KEY_FIRSTNAME = 'firstName'
KEY_LASTNAME = 'lastName'

KEY_DEALURL = 'dealurl'
KEY_SCHEDULE_CALL_START = 'schedulecallstart'
KEY_SCHEDULE_CALL_END = 'schedulecallend'

KEY_VALUE_DEFAULT = 'default'
KEY_VALUE_NEWBUSINESS = 'newbusiness'
KEY_VALUE_EXISTINGBUSINESS = 'existingbusiness'
KEY_VALUE_APPOINTMENT_SCHEDULED = 'appointmentscheduled'
KEY_VALUE_QUALIFIEDTOBUY = 'qualifiedtobuy'
KEY_VALUE_PRESENTATION_SCHEDULED = 'presentationscheduled'
KEY_VALUE_DECISION_MAKER_BOUGHTIN = 'decisionmakerboughtin'
KEY_VALUE_CONTRACT_SENT = 'contractsent'
KEY_VALUE_CLOSED_WON = 'closedwon'
KEY_VALUE_CLOSED_LOST = 'closedlost'

KEY_EVENT_ID = 'eventId'
KEY_SUBSCRIPTION_ID = 'subscriptionId'
KEY_PORTAL_ID = 'portalId'
KEY_OBJECT_ID = 'objectId'
KEY_APP_ID = 'appId'
KEY_SUBSCRIPTION_TYPE = 'subscriptionType'
KEY_CHANGE_SOURCE = 'changeSource'
KEY_CHANGE_FLAG = 'changeFlag'
KEY_OCCURRED_AT = 'occurredAt'
KEY_PROPERTY_NAME = 'propertyName'
KEY_PROPERTY_VALUE = 'propertyValue'
KEY_OPTIONS = 'options'

KEY_VALUE_DEAL_CREATED = 'deal.creation'
KEY_VALUE_DEAL_DELETION = 'deal.deletion'
KEY_VALUE_DEAL_PROPERTY_CHANGE = 'deal.propertyChange'
KEY_VALUE_PROPERTY_TYPE_DATETIME = 'datetime'

HEADER_SIGNATURE = 'HTTP_X_HUBSPOT_SIGNATURE'


def get_hubspot_endpoint_url(endpoint):
    return '{}{}'.format(HUBSPOT_API_BASE_URL, endpoint)


def get_authed_hubspot_endpoint_url(endpoint, api_key):
    return '{}?hapikey={}'.format(get_hubspot_endpoint_url(endpoint), api_key)


def create_hubspot_contact(email=None, **kwargs):
    if not email:
        return None

    properties = [
        dict(property='email', value=email)
    ]
    if kwargs:
        for key, value in six.iteritems(kwargs):
            properties.append(
                dict(property=key, value=value)
            )

    r = requests.post(
        get_authed_hubspot_endpoint_url(
            HUBSPOT_ENDPOINT_CREATE_UPDATE_CONTACT.format(contact_email=email), HUBSPOT_API_KEY
        ),
        json=dict(properties=properties),
        verify=False
    )

    if r.status_code in [200, 201]:
        response = r.json()
        return response
    return None


def get_hubspot_contact_vid(email, **kwargs):
    response = create_hubspot_contact(email, **kwargs)
    if response and 'vid' in response:
        return response['vid']
    return


def create_hubspot_deal_property(name, label, description, group_name, property_type, field_type, trials=0):
    r = requests.post(
        get_authed_hubspot_endpoint_url(
            HUBSPOT_ENDPOINT_CREATE_DEAL_PROPERTY, HUBSPOT_API_KEY
        ),
        json={
            KEY_NAME: name,
            KEY_LABEL: label,
            KEY_DESCRIPTION: description,
            KEY_GROUPNAME: group_name,
            KEY_TYPE: property_type,
            KEY_FIELDTYPE: field_type
        },
        verify=False
    )

    if r.status_code in [200, 201]:
        return r.json()
    return None


def create_or_update_hubspot_deal(task, trials=0, **kwargs):
    if task.archived:
        return None

    properties = []
    associatedVids = []

    client_vid = get_hubspot_contact_vid(task.user.email)
    associatedVids.append(client_vid)

    properties.extend(
        [
            dict(
                name=KEY_DEALNAME,
                value=task.detailed_summary
            ),
            dict(
                name=KEY_DEALURL,
                value='{}/{}'.format(TUNGA_URL, task.id)
            )
        ]
    )

    if not task.hubspot_deal_id:
        properties.extend(
            [
                dict(
                    name=KEY_PIPELINE,
                    value=KEY_VALUE_DEFAULT
                ),
                dict(
                    name=KEY_DEALTYPE,
                    value=KEY_VALUE_NEWBUSINESS
                )
            ]
        )

    if KEY_DEALSTAGE in kwargs or not task.hubspot_deal_id:
        deal_stage = kwargs.get(
            KEY_DEALSTAGE,
            task.source == TASK_SOURCE_NEW_USER and HUBSPOT_DEFAULT_DEAL_STAGE_NEW_USER or HUBSPOT_DEFAULT_DEAL_STAGE_MEMBER
        )
        properties.append(
            dict(
                name=KEY_DEALSTAGE,
                value=deal_stage or KEY_VALUE_APPOINTMENT_SCHEDULED
            )
        )

    if task.pay:
        properties.append(
            dict(
                name=KEY_AMOUNT,
                value=str(task.pay)
            )
        )
    if task.schedule_call_start:
        properties.append(
            dict(
                name=KEY_SCHEDULE_CALL_START,
                value=task.schedule_call_start.isoformat()
            )
        )
    if task.schedule_call_end:
        properties.append(
            dict(
                name=KEY_SCHEDULE_CALL_END,
                value=task.schedule_call_end.isoformat()
            )
        )
    if 'createdate' in kwargs:
        properties.append(
            dict(
                name='createdate',
                value=kwargs['createdate']
            )
        )

    payload = dict(
        associations=dict(
            associatedCompanyIds=[],
            associatedVids=associatedVids
        ),
        properties=properties
    )

    if task.hubspot_deal_id:
        r = requests.put(
            get_authed_hubspot_endpoint_url(
                '{}/{}'.format(HUBSPOT_ENDPOINT_CREATE_DEAL, task.hubspot_deal_id), HUBSPOT_API_KEY
            ), json=payload, verify=False
        )
    else:
        r = requests.post(
            get_authed_hubspot_endpoint_url(
                HUBSPOT_ENDPOINT_CREATE_DEAL, HUBSPOT_API_KEY
            ), json=payload, verify=False
        )

    if r.status_code in [200, 201]:
        response = r.json()
        task.hubspot_deal_id = response['dealId']
        task.save()
        return response
    elif r.status_code >= 300 and trials < 3:
        # Create properties
        create_hubspot_deal_property(
            name=KEY_DEALURL, label='Deal URL', description='URL of the deal',
            group_name='dealinformation', property_type='string', field_type='text'
        )
        create_hubspot_deal_property(
            name=KEY_SCHEDULE_CALL_START, label='Availability Window Starts',
            description='Start of availability window',
            group_name='dealinformation', property_type='datetime', field_type='date'
        )
        create_hubspot_deal_property(
            name=KEY_SCHEDULE_CALL_END, label='Availability Window Ends',
            description='End of availability window',
            group_name='dealinformation', property_type='datetime', field_type='date'
        )
        # Try again
        return create_or_update_hubspot_deal(task, trials=trials + 1)
    return None


def create_or_update_project_hubspot_deal(project, trials=0, **kwargs):
    if project.archived or project.legacy_id or project.stage == PROJECT_STAGE_OPPORTUNITY:
        # Don't sync archived, legacy projects and opportunities
        return None

    properties = []
    associatedVids = []

    client_vid = get_hubspot_contact_vid(project.owner and project.owner.email or project.user.email)
    associatedVids.append(client_vid)

    properties.extend(
        [
            dict(
                name=KEY_DEALNAME,
                value=project.title
            ),
            dict(
                name=KEY_DEALURL,
                value='{}/projects/{}'.format(TUNGA_URL, project.id)
            )
        ]
    )

    if not project.hubspot_deal_id:
        properties.extend(
            [
                dict(
                    name=KEY_PIPELINE,
                    value=KEY_VALUE_DEFAULT
                ),
                dict(
                    name=KEY_DEALTYPE,
                    value=KEY_VALUE_NEWBUSINESS
                )
            ]
        )

    if KEY_DEALSTAGE in kwargs or not project.hubspot_deal_id:
        deal_stage = kwargs.get(
            KEY_DEALSTAGE,
            project.stage == PROJECT_STAGE_OPPORTUNITY and HUBSPOT_DEFAULT_DEAL_STAGE_NEW_USER or HUBSPOT_DEFAULT_DEAL_STAGE_MEMBER
        )
        properties.append(
            dict(
                name=KEY_DEALSTAGE,
                value=deal_stage or KEY_VALUE_APPOINTMENT_SCHEDULED
            )
        )

    if project.budget:
        properties.append(
            dict(
                name=KEY_AMOUNT,
                value=str(project.budget)
            )
        )
    if 'createdate' in kwargs:
        properties.append(
            dict(
                name='createdate',
                value=kwargs['createdate']
            )
        )

    payload = dict(
        associations=dict(
            associatedCompanyIds=[],
            associatedVids=associatedVids
        ),
        properties=properties
    )

    if project.hubspot_deal_id:
        r = requests.put(
            get_authed_hubspot_endpoint_url(
                '{}/{}'.format(HUBSPOT_ENDPOINT_CREATE_DEAL, project.hubspot_deal_id), HUBSPOT_API_KEY
            ), json=payload, verify=False
        )
    else:
        r = requests.post(
            get_authed_hubspot_endpoint_url(
                HUBSPOT_ENDPOINT_CREATE_DEAL, HUBSPOT_API_KEY
            ), json=payload, verify=False
        )

    if r.status_code in [200, 201]:
        response = r.json()
        project.hubspot_deal_id = response['dealId']
        project.save()
        return response
    elif r.status_code >= 300 and trials < 3:
        # Create properties
        create_hubspot_deal_property(
            name=KEY_DEALURL, label='Deal URL', description='URL of the deal',
            group_name='dealinformation', property_type='string', field_type='text'
        )
        # Try again
        return create_or_update_project_hubspot_deal(project, trials=trials + 1)
    return None


def create_hubspot_engagement(from_email, to_emails, subject, body, **kwargs):
    contact_vids = []
    for email in to_emails:
        vid = get_hubspot_contact_vid(email)
        if vid:
            contact_vids.append(vid)

    alternatives = kwargs.get('alternatives', ())
    html = kwargs.get('html', '')
    deal_ids = []
    for deal_id in kwargs.get('deal_ids', []) or []:
        if deal_id:
            deal_ids.append(deal_id)

    payload = {
        "engagement": {
            "active": True,
            KEY_TYPE: "EMAIL"
        },
        "associations": {
            "contactIds": contact_vids,
            "companyIds": [],
            "dealIds": deal_ids
        },
        "metadata": {
            "from": {
                "email": from_email,
                KEY_FIRSTNAME: "Tunga"  # , "lastName": "Support"
            },
            "to": [{"email": email} for email in to_emails],
            "cc": [{"email": email} for email in kwargs.get('cc', []) or []],
            "bcc": [{"email": email} for email in kwargs.get('bcc', []) or []],
            "subject": subject,
            "html": alternatives and alternatives[0] or html,
            "text": body
        }
    }
    r = requests.post(
        get_authed_hubspot_endpoint_url(
            HUBSPOT_ENDPOINT_CREATE_ENGAGEMENT, HUBSPOT_API_KEY
        ), json=payload, verify=False
    )

    if r.status_code in [200, 201]:
        response = r.json()
        return response
    return


def get_deal(deal_id):
    r = requests.get(
        get_authed_hubspot_endpoint_url(
            HUBSPOT_ENDPOINT_GET_DEAL.format(deal_id=deal_id), HUBSPOT_API_KEY
        ), verify=False
    )

    if r.status_code in [200, 201]:
        response = r.json()
        return response
    return


def get_deal_properties():
    r = requests.get(
        get_authed_hubspot_endpoint_url(
            HUBSPOT_ENDPOINT_GET_DEAL_PROPERTIES, HUBSPOT_API_KEY
        ), verify=False
    )

    if r.status_code in [200, 201]:
        response = r.json()
        return response
    return


def get_deal_property(property_name):
    r = requests.get(
        get_authed_hubspot_endpoint_url(
            HUBSPOT_ENDPOINT_GET_DEAL_PROPERTY.format(property_name=property_name), HUBSPOT_API_KEY
        ), verify=False
    )

    if r.status_code in [200, 201]:
        response = r.json()
        return response
    return


def get_deal_pipelines():
    r = requests.get(
        get_authed_hubspot_endpoint_url(
            HUBSPOT_ENDPOINT_GET_PIPELINES, HUBSPOT_API_KEY
        ), verify=False
    )

    if r.status_code in [200, 201]:
        response = r.json()
        return response
    return


def get_owners():
    r = requests.get(
        get_authed_hubspot_endpoint_url(
            HUBSPOT_ENDPOINT_GET_OWNER, HUBSPOT_API_KEY
        ), verify=False
    )

    if r.status_code in [200, 201]:
        response = r.json()
        return response
    return


def clean_property(internal_name, internal_value, deal_details, property_details, pipelines):
    current_property_details = None
    if property_details:
        for item in property_details:
            if item.get(KEY_NAME) == internal_name:
                current_property_details = item

    final_name = copy(internal_name)
    final_value = copy(internal_value)

    if current_property_details:
        final_name = current_property_details.get(KEY_LABEL, internal_name)
        value_options = current_property_details.get(KEY_OPTIONS, None)

        if value_options:
            for item in value_options:
                if internal_value and str(item.get(KEY_VALUE, '') or '') == str(internal_value or ''):
                    final_value = item.get(KEY_LABEL)
        else:
            if internal_name in [KEY_PIPELINE, KEY_DEALSTAGE] and pipelines:
                deal_properties = deal_details['properties']
                pipeline_internal_value = internal_name == KEY_PIPELINE and internal_value or \
                                          (deal_properties.get(KEY_PIPELINE, {})['value'] or '')

                current_pipeline = dict()
                for pipeline in pipelines:
                    if pipeline_internal_value and str(pipeline.get(KEY_PIPELINE_ID, None) or '') == str(pipeline_internal_value or ''):
                        current_pipeline = pipeline

                if internal_name == KEY_PIPELINE:
                    final_value = current_pipeline.get(KEY_LABEL, internal_value)
                elif internal_name == KEY_DEALSTAGE:
                    stages = current_pipeline.get(KEY_STAGES, [])
                    if stages:
                        for stage in stages:
                            if stage.get(KEY_STAGE_ID, None) == internal_value:
                                final_value = stage.get(KEY_LABEL, internal_value)
            else:
                if internal_name == KEY_AMOUNT:
                    final_value = 'EUR {}'.format(internal_value)
                elif internal_name == KEY_HUBSPOT_OWNER_ID:
                    owners = get_owners()
                    if owners:
                        for owner in owners:
                            if internal_value and str(owner.get(KEY_OWNERID, '') or '') == str(internal_value or ''):
                                owner_names = []
                                for name_key in [KEY_FIRSTNAME, KEY_LASTNAME]:
                                    if owner.get(name_key, None):
                                        owner_names.append(owner.get(name_key, ''))
                                final_value = (' '.join(owner_names)).strip() or internal_value
                elif current_property_details.get(KEY_TYPE, None) == KEY_VALUE_PROPERTY_TYPE_DATETIME:
                    # Divide by 1000 because HS timestamps are in milliseconds
                    final_value = datetime.datetime.utcfromtimestamp(int(internal_value)/1000).strftime('%d/%b/%Y')
    return final_name, final_value


def create_custom_hubspot_engagement(payload):
    r = requests.post(
        get_authed_hubspot_endpoint_url(
            HUBSPOT_ENDPOINT_CREATE_ENGAGEMENT, HUBSPOT_API_KEY
        ), json=payload, verify=False
    )

    if r.status_code in [200, 201]:
        response = r.json()
        return response
    return
