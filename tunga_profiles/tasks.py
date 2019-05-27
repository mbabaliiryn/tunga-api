from django_rq.decorators import job

from tunga_auth.models import TungaUser
from tunga_utils import algolia_utils
from tunga_utils.helpers import clean_instance
from tunga_utils.serializers import SearchUserSerializer


@job
def sync_algolia_user(user):
    user = clean_instance(user, TungaUser)
    algolia_utils.add_objects([SearchUserSerializer(user).data])
