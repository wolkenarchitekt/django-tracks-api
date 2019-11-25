import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_admin_list(client, tracks):
    url = reverse('admin:tracks_track_changelist')
    response = client.get(url)
    assert response.status_code == 200
