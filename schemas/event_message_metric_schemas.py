from datetime import datetime

from configs.orjson.orjson_config import ORJSONModel
from enum import Enum

class SumRedEnum(str, Enum):
    SUM = "SUM"
    RED = "RED"

class ColumnsVacancyMetricEnum(str, Enum):
    shortlists_count = "shortlists_count"
    shares_count = "shares_count"
    views_count = "views_count"
    applications_count = "applications_count"
    interview_count = "interview_count"

class ColumnUserMetricEnum(str, Enum):
    post_count = "post_count"
    favorite_post_count = "favorite_post_count"
    comment_count = "comment_count"
    favorite_comment_count = "favorite_comment_count"
    follower_count = "follower_count"
    followed_count = "followed_count"
    share_count = "share_count"
    connection_count = "connection_count"
    blocked_count = "blocked_count"
    reaction_comment_given_count = "reaction_comment_given_count"
    reaction_comment_received_count = "reaction_comment_received_count"
    enterprise_follow_count = "enterprise_follow_count"
    enterprise_follower_count = "enterprise_follower_count"
    profile_view_count = "profile_view_count"
    vacancy_application_count = "vacancy_application_count"

class ColumnEnterpriseMetricEnum(str, Enum):
    followed_count = "followed_count"
    follower_count = "follower_count"
    vacancies_count = "vacancies_count"
    post_count = "post_count"
    comment_post = "comment_post"
    view_count = "view_count"
    review_count = "review_count"
    employments_count = "employments_count"

class EntityEnum(str, Enum):
    USER_METRIC = "USER_METRIC"
    VACANCY_METRIC = "VACANCY_METRIC"
    ENTERPRISE_METRIC = "ENTERPRISE_METRIC"
    POST_ENTERPRISE_METRIC = "POST_ENTERPRISE_METRIC"
    POST_USER_METRIC = "POST_USER_METRIC"
    COMMENT_POST_ENTERPRISE_METRIC = "COMMENT_POST_ENTERPRISE_METRIC"

class ColumnsPostEnterpriseMetricEnum(str, Enum):
    views_count = "views_count"
    shares_count = "shares_count"
    reactions_like_count = "reactions_like_count"
    reactions_dislike_count = "reactions_dislike_count"
    favorites_count = "favorites_count"
    comments_count = "comments_count"

class ColumnsPostUserMetricEnum(str, Enum):
    views_count = "views_count"
    shares_count = "shares_count"
    reactions_like_count = "reactions_like_count"
    reactions_dislike_count = "reactions_dislike_count"
    favorites_count = "favorites_count"
    comments_count = "comments_count"

class ColumnsCommentPostEnterpriseMetricEnum(str, Enum):
    replies_count = "replies_count"
    edited_count = "edited_count"
    views_count = "views_count"
    shares_count = "shares_count"
    reactions_like_count = "reactions_like_count"
    reactions_dislike_count = "reactions_dislike_count"
    favorites_count = "favorites_count"

class EventMessageMetric(ORJSONModel):
    event_id: str
    metric_id: int
    column: str
    action: SumRedEnum
    entity: EntityEnum
    created_at: datetime
    source: str
    metadata: dict