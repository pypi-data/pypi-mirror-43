from django.urls import reverse

import mock
from bitbucket.exceptions import BitbucketBaseAPIException
from requests import HTTPError
from rest_framework.exceptions import PermissionDenied


@mock.patch('requests.sessions.Session.request')
@mock.patch('bitbucket.credentials.KatkaCredentialsService.client')
class TestGetProjects:
    def test_existing_projects(self, mock_credentials_client, mock_bitbucket_request, load_json_fixture, client):
        mock_credentials_client.return_value = mock.PropertyMock()
        credentials_response = mock.Mock()
        credentials_response.json.return_value = load_json_fixture('katka_credentials.json')
        mock_credentials_client.get.return_value = credentials_response

        bitbucket_response = mock.Mock()
        bitbucket_response.json.return_value = load_json_fixture('bitbucket_projects.json')
        mock_bitbucket_request.return_value = bitbucket_response

        endpoint = reverse('projects')
        response = client.get(
            endpoint,
            content_type='application/json',
            data={'credential': '4cb432f5-0def-48b6-ad05-f1c082b1f1b8', 'limit': 10, 'start': 2}
        )

        assert len(response.data['values']) == 2
        assert response.data['start'] == 0
        assert response.data['limit'] == 2
        assert response.data['size'] == 2
        assert response.data['is_last_page'] is False
        assert response.data['next_page_start'] == 2
        assert response.data['values'][0]['key'] == 'MSAP'
        assert response.data['values'][0]['description'] == 'My super awesome project'
        assert response.data['values'][1]['name'] == 'Not so awesome project'

    def test_no_projects(self, mock_credentials_client, mock_bitbucket_request, load_json_fixture, client):
        mock_credentials_client.return_value = mock.PropertyMock()
        credentials_response = mock.Mock()
        credentials_response.json.return_value = load_json_fixture('katka_credentials.json')
        mock_credentials_client.get.return_value = credentials_response

        bitbucket_response = mock.Mock()
        bitbucket_response.json.return_value = load_json_fixture('bitbucket_no_projects.json')
        mock_bitbucket_request.return_value = bitbucket_response

        endpoint = reverse('projects')
        response = client.get(
            endpoint,
            content_type='application/json',
            data={'credential': '4cb432f5-0def-48b6-ad05-f1c082b1f1b8', 'limit': 10, 'start': 2}
        )

        assert response.status_code == 200
        assert len(response.data['values']) == 0
        assert response.data['start'] == 0
        assert response.data['limit'] == 0
        assert response.data['size'] == 0
        assert response.data['is_last_page'] is True
        assert response.data['next_page_start'] == 0

    def test_bitbucket_exception(self, mock_credentials_client, mock_bitbucket_request, load_json_fixture, client):
        """ If the token is not valid bitbucket will retrieve an empty list of projects """
        mock_credentials_client.return_value = mock.PropertyMock()
        credentials_response = mock.Mock()
        credentials_response.json.return_value = load_json_fixture('katka_credentials.json')
        mock_credentials_client.get.return_value = credentials_response

        bitbucket_response = mock.Mock()
        bitbucket_response.raise_for_status.side_effect = HTTPError(
            'test exception', response=mock.Mock(content=None, status_code=500)
        )
        mock_bitbucket_request.return_value = bitbucket_response

        endpoint = reverse('projects')
        response = client.get(
            endpoint,
            content_type='application/json',
            data={'credential': '4cb432f5-0def-48b6-ad05-f1c082b1f1b9', 'limit': 10, 'start': 2}
        )

        assert response.status_code == BitbucketBaseAPIException.status_code


class TestGetProjectsNoCredentials:
    @mock.patch('requests.sessions.Session.request')
    def test_no_credential(self, mock_bitbucket_request, load_json_fixture, client):
        bitbucket_response = mock.Mock()
        bitbucket_response.json.return_value = load_json_fixture('bitbucket_no_projects.json')
        mock_bitbucket_request.return_value = bitbucket_response

        endpoint = reverse('projects')
        response = client.get(
            endpoint,
            content_type='application/json',
            data={'limit': 10, 'start': 2}
        )

        assert response.status_code == 200
        assert len(response.data['values']) == 0

    @mock.patch('bitbucket.credentials.KatkaCredentialsService.client')
    def test_no_credential_found(self, mock_credentials_client, load_json_fixture, client):
        mock_credentials_client.return_value = mock.PropertyMock()
        credentials_response = mock.Mock()
        credentials_response.raise_for_status.side_effect = HTTPError(
            'test exception', response=mock.Mock(content=None, status_code=404)
        )
        mock_credentials_client.get.return_value = credentials_response

        endpoint = reverse('projects')
        response = client.get(
            endpoint,
            content_type='application/json',
            data={'credential': '4cb432f5-0def-48b6-ad05-f1c082b1f1b9', 'limit': 10, 'start': 2}
        )

        assert response.status_code == PermissionDenied.status_code
