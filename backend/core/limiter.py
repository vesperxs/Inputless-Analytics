from django_limits.limiter import Limiter
from django.contrib.auth.models import User
from django.db.models import Q


class UserLimiter(Limiter):
    rules = {
        User: [
            {
                'limit': 5,
                'message': "Only 5 active users allowed",
                'filterset': Q(is_active=True)
            },
            {
                'limit': 3,
                'message': "Only 10 staff members allowed",
                'filterset': Q(is_staff=True)
            }
        ]
    }