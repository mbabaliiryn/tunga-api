from django.core.exceptions import ObjectDoesNotExist
from django.db.models.aggregates import Count, Sum
from django.db.models.expressions import When, Case, F
from django.db.models.fields import IntegerField
from django.db.models.query_utils import Q
from dry_rest_permissions.generics import DRYPermissionFiltersBase

from tunga_auth.models import USER_TYPE_DEVELOPER, USER_TYPE_PROJECT_OWNER
from tunga_profiles.models import UserProfile
from tunga_utils.constants import USER_TYPE_PROJECT_MANAGER, STATUS_INITIAL, STATUS_ACCEPTED


def my_connections_q_filter(user):
    return (
        (
            Q(connections_initiated__to_user=user) &
            Q(connections_initiated__status=STATUS_ACCEPTED)
           
        ) |
        (
            Q(connection_requests__from_user=user) &
            Q(connection_requests__status=STATUS_ACCEPTED)
        )   
       
    )   

class UserFilterBackend(DRYPermissionFiltersBase):
    def filter_list_queryset(self, request, queryset, view):
        if view.action == 'list':
            queryset = queryset.exclude(id=request.user.id)
        queryset = queryset.exclude(pending=True)
        user_filter = request.query_params.get('filter', None)
        project_id = request.query_params.get('project', None)
        if project_id:
            queryset = queryset.filter(
                Q(projects_created__id = project_id) |
                Q(projects_managed__id = project_id) |
                Q(projects_owned__id = project_id) |

                (
                    Q(project_participation__project__id = project_id) &
                    Q(project_participation__status = STATUS_ACCEPTED)

                )
            )
        if user_filter in ['developers', 'project-owners', 'clients', 'project-managers', 'pms']:
            if user_filter == 'developers':
                queryset = queryset.filter(type=USER_TYPE_DEVELOPER)
            elif user_filter in ['project-managers', 'pms']:
                queryset = queryset.filter(type=USER_TYPE_PROJECT_MANAGER)
            else:
                queryset = queryset.filter(type=USER_TYPE_PROJECT_OWNER)
            queryset = queryset.annotate(
                skills_count=Count('userprofile__skills')
            ).annotate(
                skills_rank=Case(
                    When(
                        skills_count__gte=3,
                        then=3
                    ),
                    default='skills_count',
                    output_field=IntegerField()
                )
            ).annotate(
                task_count=Count('task_participants')
            ).annotate(
                task_rank=Case(
                    When(
                        task_count__gt=3,
                        then=3
                    ),
                    default='task_count',
                    output_field=IntegerField()
                )
            ).annotate(
                total_rank=F('skills_rank') + F('task_rank')
            ).annotate(
                profile_rank=Case(
                    When(
                        ~Q(userprofile__bio='') &
                        Q(userprofile__bio__isnull=False),
                        then=2 + F('total_rank')
                    ),
                    default='total_rank',
                    output_field=IntegerField()
                )
            ).order_by('-profile_rank', 'first_name', 'last_name')
        elif user_filter in ['team', 'my-project-owners', 'my-clients']:
            if user_filter in ['my-project-owners', 'my-clients']:
                user_type = USER_TYPE_PROJECT_OWNER
            
            else:
                user_type = USER_TYPE_DEVELOPER
            queryset = queryset.filter(type=user_type).filter(
                my_connections_q_filter(request.user)
            )
        elif user_filter == 'requests':
            queryset = queryset.filter(
                connections_initiated__to_user=request.user, connections_initiated__status=STATUS_INITIAL) 
        elif user_filter == 'relevant':
            queryset = queryset.filter(type=USER_TYPE_DEVELOPER)
            try:
                user_skills = request.user.userprofile.skills.all()
                queryset = queryset.filter(userprofile__skills__in=user_skills)
                when = []
                for skill in user_skills:
                    new_when = When(
                            userprofile__skills=skill,
                            then=1
                        )
                    when.append(new_when)
                queryset = queryset.annotate(matches=Sum(
                    Case(
                        *when,
                        default=0,
                        output_field=IntegerField()
                    )
                )).order_by('-matches', 'first_name', 'last_name', '-date_joined')
            except (ObjectDoesNotExist, UserProfile.DoesNotExist):
                return queryset.none()
        return queryset






    
