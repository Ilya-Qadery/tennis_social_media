"""
URL configuration for trainings app.
"""
from django.urls import path

from .apis.drill import DrillCreateApi, DrillDetailApi, DrillListApi
from .apis.goal import (
    TrainingGoalCreateApi,
    TrainingGoalDetailApi,
    TrainingGoalListApi,
    TrainingGoalProgressApi,
)
from .apis.session import (
    TrainingSessionAddDrillApi,
    TrainingSessionCreateApi,
    TrainingSessionDetailApi,
    TrainingSessionListApi,
    TrainingSessionRemoveDrillApi,
    TrainingStatsApi,
)

urlpatterns = [
    # Drills
    path("drills/", DrillListApi.as_view(), name="drill-list"),
    path("drills/create/", DrillCreateApi.as_view(), name="drill-create"),
    path("drills/<uuid:drill_id>/", DrillDetailApi.as_view(), name="drill-detail"),
    
    # Sessions
    path("sessions/", TrainingSessionListApi.as_view(), name="session-list"),
    path("sessions/create/", TrainingSessionCreateApi.as_view(), name="session-create"),
    path("sessions/stats/", TrainingStatsApi.as_view(), name="training-stats"),
    path("sessions/<uuid:session_id>/", TrainingSessionDetailApi.as_view(), name="session-detail"),
    path(
        "sessions/<uuid:session_id>/drills/",
        TrainingSessionAddDrillApi.as_view(),
        name="session-add-drill"
    ),
    path(
        "sessions/<uuid:session_id>/drills/<uuid:drill_instance_id>/",
        TrainingSessionRemoveDrillApi.as_view(),
        name="session-remove-drill"
    ),
    
    # Goals
    path("goals/", TrainingGoalListApi.as_view(), name="goal-list"),
    path("goals/create/", TrainingGoalCreateApi.as_view(), name="goal-create"),
    path("goals/<uuid:goal_id>/", TrainingGoalDetailApi.as_view(), name="goal-detail"),
    path(
        "goals/<uuid:goal_id>/progress/",
        TrainingGoalProgressApi.as_view(),
        name="goal-progress"
    ),
]
