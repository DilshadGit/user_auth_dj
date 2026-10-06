from io import BytesIO

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core import mail
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, SimpleTestCase, override_settings
from django.urls import reverse
from PIL import Image

User = get_user_model()


class SecuritySettingsTests(SimpleTestCase):
    def test_custom_user_model_is_used(self):
        self.assertEqual(settings.AUTH_USER_MODEL, 'accounts.CustomUser')

    def test_session_and_csrf_security_flags(self):
        self.assertTrue(settings.SESSION_COOKIE_HTTPONLY)
        self.assertEqual(settings.SESSION_COOKIE_SAMESITE, 'Lax')
        self.assertTrue(settings.CSRF_COOKIE_HTTPONLY)
        self.assertTrue(settings.SECURE_CONTENT_TYPE_NOSNIFF)
        self.assertEqual(settings.SECURE_REFERRER_POLICY, 'strict-origin-when-cross-origin')


class DashboardAccessTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            email='admin@example.com',
            password='StrongPass123!',
            is_staff=True,
            is_superuser=True,
        )
        self.staff = User.objects.create_user(
            email='staff@example.com',
            password='StrongPass123!',
            is_staff=True,
        )
        self.member = User.objects.create_user(
            email='member@example.com',
            password='StrongPass123!',
        )

    def test_admin_and_staff_can_access_dashboard(self):
        self.client.force_login(self.admin)
        response = self.client.get(reverse('accounts:dashboard'))
        self.assertEqual(response.status_code, 200)

        self.client.force_login(self.staff)
        response = self.client.get(reverse('accounts:dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_member_is_blocked_from_dashboard(self):
        self.client.force_login(self.member)
        response = self.client.get(reverse('accounts:dashboard'))
        self.assertIn(response.status_code, (302, 403))

    def test_users_receive_unique_barcode_numbers_on_create(self):
        first = User.objects.create_user(email='barcode-one@example.com', password='StrongPass123!')
        second = User.objects.create_user(email='barcode-two@example.com', password='StrongPass123!')

        self.assertTrue(first.barcode_number)
        self.assertTrue(second.barcode_number)
        self.assertNotEqual(first.barcode_number, second.barcode_number)

    def test_admin_can_block_and_unblock_user(self):
        self.client.force_login(self.admin)
        response = self.client.post(reverse('accounts:block_user', args=[self.member.pk]))

        self.member.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertFalse(self.member.is_active)

        unblock_response = self.client.post(reverse('accounts:block_user', args=[self.member.pk]))
        self.member.refresh_from_db()
        self.assertEqual(unblock_response.status_code, 302)
        self.assertTrue(self.member.is_active)

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_signup_sends_email_notification(self):
        response = self.client.post(
            reverse('accounts:signup'),
            {
                'first_name': 'New',
                'last_name': 'User',
                'email': 'newuser@example.com',
                'password1': 'StrongPassword123!',
                'password2': 'StrongPassword123!',
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Welcome to AccountCMS', mail.outbox[0].subject)
        self.assertIn('newuser@example.com', mail.outbox[0].to)

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_password_reset_sends_email(self):
        response = self.client.post(
            reverse('accounts:password_reset'),
            {'email': self.member.email},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Password reset', mail.outbox[0].subject)
        self.assertIn(self.member.email, mail.outbox[0].to)

    def test_user_can_update_own_profile_and_upload_picture(self):
        self.client.force_login(self.member)
        image = BytesIO()
        Image.new('RGB', (50, 50), color='blue').save(image, format='PNG')
        image.seek(0)

        response = self.client.post(
            reverse('accounts:profile_update'),
            {
                'first_name': 'Updated',
                'last_name': 'Member',
                'mobile_number': '+111222333',
                'address': 'Route 42',
                'postcode': 'W1A 1AA',
                'date_of_birth': '1995-12-05',
                'bio': 'Updated profile',
                'profile_image': SimpleUploadedFile('avatar.png', image.read(), content_type='image/png'),
            },
            follow=True,
        )

        self.member.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.member.first_name, 'Updated')
        self.assertEqual(self.member.mobile_number, '+111222333')
        self.assertTrue(self.member.profile_image)

    def test_user_can_delete_own_account_without_hard_delete(self):
        self.client.force_login(self.member)
        response = self.client.post(reverse('accounts:profile_delete'), follow=True)

        self.member.refresh_from_db()
        self.assertEqual(response.redirect_chain[-1][0], reverse('accounts:login'))
        self.assertFalse(self.member.is_active)
        self.assertTrue(self.member.is_deleted)
        self.assertTrue(User.objects.filter(pk=self.member.pk).exists())

    def test_profile_update_creates_audit_record(self):
        self.client.force_login(self.member)
        response = self.client.post(
            reverse('accounts:profile_update'),
            {
                'first_name': 'Audit',
                'last_name': 'User',
                'mobile_number': '+1010101010',
                'address': 'Audit Street',
                'postcode': 'A1 1AA',
                'date_of_birth': '1998-01-02',
                'bio': 'Audit trail test',
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.member.profile_updates.exists())

    def test_admin_can_access_docs_index_and_search_users(self):
        self.client.force_login(self.admin)
        user = User.objects.create_user(
            email='search-target@example.com',
            password='StrongPass123!',
            first_name='Aisha',
            last_name='Khan',
            barcode_number='BC-123',
            date_of_birth='1990-05-15',
            mobile_number='+1234567890',
            address='123 Main Street',
            postcode='AB12 3CD',
        )

        docs_response = self.client.get(reverse('docs_index'))
        self.assertEqual(docs_response.status_code, 200)

        nested_dir_response = self.client.get('/docs/db/')
        self.assertEqual(nested_dir_response.status_code, 200)
        self.assertContains(nested_dir_response, 'FINAL_AUTH_PROJECT_STATUS_AND_FIX_LOG.md')

        file_response = self.client.get('/docs/db/FINAL_AUTH_PROJECT_STATUS_AND_FIX_LOG.md/')
        self.assertEqual(file_response.status_code, 200)
        self.assertContains(file_response, 'FINAL AUTH')

        search_response = self.client.get(reverse('accounts:dashboard'), {'q': 'Aisha'})
        self.assertEqual(search_response.status_code, 200)
        self.assertContains(search_response, 'Aisha')
        self.assertContains(search_response, user.email)

        detail_response = self.client.get(reverse('accounts:user_detail', args=[user.pk]))
        self.assertEqual(detail_response.status_code, 200)
        self.assertContains(detail_response, 'Aisha')
        self.assertContains(detail_response, 'BC-123')
        self.assertContains(detail_response, 'AB12 3CD')

    def test_mermaid_block_is_rendered_as_browser_valid_div(self):
        self.client.force_login(self.admin)
        response = self.client.get('/docs/USER_AUTHENTICATION_FLOWCHART.md/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<div class="mermaid">')
        self.assertContains(response, 'flowchart LR')
        self.assertNotContains(response, '<pre><code class="language-mermaid">')
