from urllib import parse

from directory_client_core.authentication import SessionSSOAuthenticator

from directory_api_client.base import AbstractAPIClient


class CompanyAPIClient(AbstractAPIClient):

    endpoints = {
        'profile': '/supplier/company/',
        'case-study-detail': '/supplier/company/case-study/{id}/',
        'case-study-list': '/supplier/company/case-study/',
        'validate-company-number': '/validate/company-number/',
        'verify': '/supplier/company/verify/',
        'verify-companies-house': '/supplier/company/verify/companies-house/',
        'public-case-study-detail': '/public/case-study/{id}/',
        'public-profile-detail': '/public/company/{number}/',
        'public-profile-list': '/public/company/',
        'search-companies': '/company/search/',
        'search-case-studies': '/case-study/search/',
        'transfer-invite': '/supplier/company/transfer-ownership-invite/',
        'transfer-invite-detail': (
            '/supplier/company/transfer-ownership-invite/{invite_key}/'
        ),
        'collaboration-invite': '/supplier/company/collaboration-invite/',
        'collaboration-invite-detail': (
            '/supplier/company/collaboration-invite/{invite_key}/'
        ),
        'remove-collaborators': '/supplier/company/remove-collaborators/',
        'collaborators': '/supplier/company/collaborators/',
        'request-collaboration': '/supplier/company/collaborator-request/',
    }
    authenticator = SessionSSOAuthenticator

    def update_profile(self, sso_session_id, data):
        files = {}
        if 'logo' in data:
            files['logo'] = data.pop('logo')
        return self.patch(
            url=self.endpoints['profile'],
            data=data,
            files=files,
            authenticator=self.authenticator(sso_session_id),
        )

    def retrieve_private_profile(self, sso_session_id):
        return self.get(
            url=self.endpoints['profile'],
            authenticator=self.authenticator(sso_session_id),
            use_fallback_cache=True,
        )

    def retrieve_public_profile(self, number):
        return self.get(
            url=self.endpoints['public-profile-detail'].format(number=number),
            use_fallback_cache=True,
        )

    def list_public_profiles(self, **kwargs):
        url = '{path}?{querystring}'.format(
            path=self.endpoints['public-profile-list'],
            querystring=parse.urlencode(kwargs, doseq=True),
        )
        return self.get(url=url, use_fallback_cache=True)

    def validate_company_number(self, number):
        url = self.endpoints['validate-company-number']
        params = {'number': number}
        return self.get(url, params=params)

    def create_case_study(self, data, sso_session_id):
        files = {}
        for field in ['image_one', 'image_two', 'image_three', 'video_one']:
            if data.get(field):
                files[field] = data.pop(field)
        url = self.endpoints['case-study-list']
        return self.post(
            url,
            data=data,
            files=files,
            authenticator=self.authenticator(sso_session_id),
        )

    def update_case_study(self, data, sso_session_id, case_study_id):
        files = {}
        for field in ['image_one', 'image_two', 'image_three', 'video_one']:
            if data.get(field):
                files[field] = data.pop(field)
        url = self.endpoints['case-study-detail'].format(id=case_study_id)
        return self.patch(
            url,
            data=data,
            files=files,
            authenticator=self.authenticator(sso_session_id),
        )

    def retrieve_private_case_study(self, sso_session_id, case_study_id):
        return self.get(
            url=self.endpoints['case-study-detail'].format(id=case_study_id),
            authenticator=self.authenticator(sso_session_id),
            use_fallback_cache=True,
        )

    def retrieve_public_case_study(self, case_study_id):
        url = self.endpoints['public-case-study-detail'].format(
            id=case_study_id
        )
        return self.get(url=url, use_fallback_cache=True)

    def delete_case_study(self, sso_session_id, case_study_id):
        url = self.endpoints['case-study-detail'].format(id=case_study_id)
        return self.delete(
            url, authenticator=self.authenticator(sso_session_id)
        )

    def verify_with_code(self, sso_session_id, code):
        return self.post(
            self.endpoints['verify'],
            data={'code': code},
            authenticator=self.authenticator(sso_session_id),
        )

    def verify_with_companies_house(self, sso_session_id, access_token):
        data = {'access_token': access_token}
        url = self.endpoints['verify-companies-house']
        return self.post(
            url,
            data=data,
            authenticator=self.authenticator(sso_session_id),
        )

    def search_company(self, **kwargs):
        return self.get(
            url=self.endpoints['search-companies'],
            params=kwargs,
            use_fallback_cache=True,
        )

    def search_case_study(self, **kwargs):
        return self.get(
            url=self.endpoints['search-case-studies'],
            params=kwargs,
            use_fallback_cache=True,
        )

    def create_transfer_invite(self, sso_session_id, new_owner_email):
        return self.post(
            self.endpoints['transfer-invite'],
            data={'new_owner_email': new_owner_email},
            authenticator=self.authenticator(sso_session_id),
        )

    def retrieve_transfer_invite(self, sso_session_id, invite_key):
        url = self.endpoints['transfer-invite-detail'].format(
            invite_key=invite_key
        )
        return self.get(url, authenticator=self.authenticator(sso_session_id))

    def accept_transfer_invite(self, sso_session_id, invite_key):
        url = self.endpoints['transfer-invite-detail'].format(
            invite_key=invite_key
        )
        return self.patch(
            url,
            data={'accepted': True},
            authenticator=self.authenticator(sso_session_id),
        )

    def create_collaboration_invite(self, sso_session_id, collaborator_email):
        return self.post(
            self.endpoints['collaboration-invite'],
            data={'collaborator_email': collaborator_email},
            authenticator=self.authenticator(sso_session_id))

    def retrieve_collaboration_invite(self, sso_session_id, invite_key):
        url = self.endpoints['collaboration-invite-detail'].format(
            invite_key=invite_key
        )
        return self.get(url, authenticator=self.authenticator(sso_session_id))

    def accept_collaboration_invite(self, sso_session_id, invite_key):
        url = self.endpoints['collaboration-invite-detail'].format(
            invite_key=invite_key
        )
        return self.patch(
            url,
            data={'accepted': True},
            authenticator=self.authenticator(sso_session_id),
        )

    def remove_collaborators(self, sso_session_id, sso_ids):
        url = self.endpoints['remove-collaborators']
        return self.post(
            url,
            data={'sso_ids': sso_ids},
            authenticator=self.authenticator(sso_session_id),
        )

    def retrieve_collaborators(self, sso_session_id):
        url = self.endpoints['collaborators']
        return self.get(url, authenticator=self.authenticator(sso_session_id))

    def request_collaboration(self, company_number, collaborator_email):
        return self.post(
            self.endpoints['request-collaboration'],
            data={
                'company_number': company_number,
                'collaborator_email': collaborator_email
            },
        )
