import json
from dataclasses import dataclass
from datetime import datetime

@dataclass
class EngagementMetrics:
    users: int
    sessions: int
    revenue: float

@dataclass
class AnalyticsSettings:
    track_engagement: bool
    track_revenue: bool

class Analytics:
    def __init__(self, settings: AnalyticsSettings):
        self.settings = settings
        self.metrics = EngagementMetrics(0, 0, 0.0)
        self.data = []

    def update_metrics(self, users: int, sessions: int, revenue: float):
        if self.settings.track_engagement:
            self.metrics.users = users
            self.metrics.sessions = sessions
        if self.settings.track_revenue:
            self.metrics.revenue = revenue
        self.data.append({
            'timestamp': datetime.now().isoformat(),
            'users': users,
            'sessions': sessions,
            'revenue': revenue
        })

    def get_metrics(self):
        return self.metrics

    def get_data(self):
        return self.data

    def customize_settings(self, track_engagement: bool, track_revenue: bool):
        self.settings.track_engagement = track_engagement
        self.settings.track_revenue = track_revenue
