import pytest
import django
from django.urls import reverse


@pytest.mark.django_db
@pytest.mark.skip(reason="Admin tests disabled")
def test_admin_list(admin_client):
    url = reverse("admin:tracks_api_track_changelist")
    response = admin_client.get(url)
    assert response.status_code == 200
