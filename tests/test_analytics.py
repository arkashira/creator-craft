from analytics import Analytics, EngagementMetrics, AnalyticsSettings

def test_update_metrics():
    settings = AnalyticsSettings(True, True)
    analytics = Analytics(settings)
    analytics.update_metrics(10, 20, 100.0)
    assert analytics.get_metrics() == EngagementMetrics(10, 20, 100.0)

def test_customize_settings():
    settings = AnalyticsSettings(True, True)
    analytics = Analytics(settings)
    analytics.customize_settings(False, True)
    assert analytics.settings.track_engagement == False
    assert analytics.settings.track_revenue == True

def test_get_data():
    settings = AnalyticsSettings(True, True)
    analytics = Analytics(settings)
    analytics.update_metrics(10, 20, 100.0)
    data = analytics.get_data()
    assert len(data) == 1
    assert data[0]['users'] == 10
    assert data[0]['sessions'] == 20
    assert data[0]['revenue'] == 100.0

def test_edge_case_no_tracking():
    settings = AnalyticsSettings(False, False)
    analytics = Analytics(settings)
    analytics.update_metrics(10, 20, 100.0)
    assert analytics.get_metrics() == EngagementMetrics(0, 0, 0.0)
