import os
import re
import shutil
import tempfile
import unittest


_TEMP_DIR = tempfile.mkdtemp(prefix='doctor_security_test_')
os.environ['DATABASE_URL'] = 'sqlite:///' + os.path.join(_TEMP_DIR, 'doctor.db')
os.environ['SECRET_KEY'] = 'test-only-secret-key'
os.environ['ADMIN_PASSWORD'] = 'test-admin-password'
os.environ['USER_PASSWORD'] = 'test-user-password'
os.environ.pop('RENDER', None)

from app import Doctor, app, db  # noqa: E402


class SecurityRegressionTests(unittest.TestCase):
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(_TEMP_DIR, ignore_errors=True)

    def setUp(self):
        app.config.update(TESTING=True, RATELIMIT_ENABLED=False)
        with app.app_context():
            db.drop_all()
            db.create_all()
        self.client = app.test_client()

    @staticmethod
    def _csrf_from_html(response):
        match = re.search(rb'<meta name="csrf-token" content="([^"]+)"', response.data)
        if not match:
            raise AssertionError('CSRF meta token missing')
        return match.group(1).decode()

    def _login(self, username='admin', password='test-admin-password'):
        response = self.client.post('/login', json={
            'username': username,
            'password': password,
        })
        self.assertEqual(response.status_code, 200)
        return response.get_json()['csrf_token']

    def test_sensitive_api_routes_require_login(self):
        for path in ('/api/doctors', '/api/stats', '/api/export'):
            with self.subTest(path=path):
                self.assertEqual(self.client.get(path).status_code, 401)

    def test_page_and_security_headers_remain_available(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self._csrf_from_html(response)
        self.assertEqual(response.headers['X-Frame-Options'], 'DENY')
        self.assertEqual(response.headers['X-Content-Type-Options'], 'nosniff')
        self.assertIn("frame-ancestors 'none'", response.headers['Content-Security-Policy'])

    def test_csrf_blocks_write_but_valid_flow_still_works(self):
        token = self._login()
        payload = {'name': '安全測試醫師', 'specialty': '家醫科'}
        blocked = self.client.post('/api/doctors', json=payload)
        self.assertEqual(blocked.status_code, 403)

        created = self.client.post(
            '/api/doctors',
            json=payload,
            headers={'X-CSRF-Token': token},
        )
        self.assertEqual(created.status_code, 201)
        listing = self.client.get('/api/doctors')
        self.assertEqual(listing.status_code, 200)
        self.assertEqual(len(listing.get_json()), 1)
        self.assertEqual(listing.headers['Cache-Control'], 'no-store')

    def test_non_admin_cannot_delete(self):
        with app.app_context():
            doctor = Doctor(name='保留醫師', email='保留醫師')
            db.session.add(doctor)
            db.session.commit()
            doctor_id = doctor.id

        token = self._login('user', 'test-user-password')
        response = self.client.delete(
            f'/api/doctors/{doctor_id}',
            headers={'X-CSRF-Token': token},
        )
        self.assertEqual(response.status_code, 403)

    def test_logout_then_login_returns_fresh_csrf_token(self):
        first_token = self._login()
        logout = self.client.post('/logout', headers={'X-CSRF-Token': first_token})
        self.assertEqual(logout.status_code, 200)
        second_token = self._login()
        self.assertTrue(second_token)
        created = self.client.post(
            '/api/doctors',
            json={'name': '重新登入後仍可新增'},
            headers={'X-CSRF-Token': second_token},
        )
        self.assertEqual(created.status_code, 201)

    def test_existing_crud_and_export_flows_still_work(self):
        token = self._login()
        headers = {'X-CSRF-Token': token}
        created = self.client.post('/api/doctors', json={
            'name': '回歸測試醫師',
            'specialty': '家醫科',
            'status': '未聯繫',
        }, headers=headers)
        self.assertEqual(created.status_code, 201)
        doctor_id = created.get_json()['id']
        updated = self.client.put(f'/api/doctors/{doctor_id}', json={
            'name': '回歸測試醫師更新',
            'specialty': '內科',
            'status': '聯繫過',
        }, headers=headers)
        self.assertEqual(updated.status_code, 200)
        self.assertEqual(updated.get_json()['specialty'], '內科')

        exported = self.client.get('/api/export')
        self.assertEqual(exported.status_code, 200)
        self.assertIn('attachment', exported.headers.get('Content-Disposition', ''))
        self.assertEqual(
            self.client.delete(f'/api/doctors/{doctor_id}', headers=headers).status_code,
            200,
        )


if __name__ == '__main__':
    unittest.main()
