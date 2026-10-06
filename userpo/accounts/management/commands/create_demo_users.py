from datetime import timedelta
from typing import cast

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from accounts.models import CustomUser

User = cast(type[CustomUser], get_user_model())


class Command(BaseCommand):
    help = 'Create 100 demo users with the requested admin/staff/member split and include the real admin emails.'

    def handle(self, *args, **options):
        User.objects.all().delete()

        admin_emails = [
            'dilshad.a73@gmail.com',
            'dilshad.abdulla@icloud.com',
        ]
        staff_emails = [
            'staff01@example.com',
            'staff02@example.com',
            'staff03@example.com',
            'staff04@example.com',
        ]

        for email in admin_emails:
            user = User.objects.create_user(
                email=email,
                password='AdminPass!2026',
                first_name='Admin',
                last_name='User',
                mobile_number='+1234567890',
                is_staff=True,
                is_superuser=True,
                is_verified=True,
            )
            user.last_login = timezone.now() - timedelta(days=1)
            user.last_logout_at = timezone.now() - timedelta(days=2)
            user.last_login_ip = '127.0.0.1'
            user.save(update_fields=['last_login', 'last_logout_at', 'last_login_ip'])

        for index, email in enumerate(staff_emails, start=1):
            user = User.objects.create_user(
                email=email,
                password='StaffPass!2026',
                first_name='Staff',
                last_name=f'{index}',
                mobile_number=f'+1555000{index:02d}',
                is_staff=True,
                is_superuser=False,
                is_verified=True,
            )
            user.last_login = timezone.now() - timedelta(days=index + 5)
            user.last_logout_at = timezone.now() - timedelta(days=index + 7)
            user.last_login_ip = '127.0.0.1'
            user.save(update_fields=['last_login', 'last_logout_at', 'last_login_ip'])

        for index in range(1, 95):
            user = User.objects.create_user(
                email=f'member{index:03d}@example.com',
                password='MemberPass!2026',
                first_name='Member',
                last_name=f'{index}',
                mobile_number=f'+1555{index:05d}',
                is_staff=False,
                is_superuser=False,
                is_verified=True,
            )
            user.last_login = timezone.now() - timedelta(days=index + 11)
            user.last_logout_at = timezone.now() - timedelta(days=index + 13)
            user.last_login_ip = '127.0.0.1'
            user.save(update_fields=['last_login', 'last_logout_at', 'last_login_ip'])

        admin_count = User.objects.filter(is_superuser=True).count()
        staff_count = User.objects.filter(is_staff=True, is_superuser=False).count()
        member_count = User.objects.filter(is_staff=False, is_superuser=False).count()
        total_users = User.objects.count()

        self.stdout.write(self.style.SUCCESS(
            f'Created {total_users} users. Admins={admin_count}, Staff={staff_count}, Members={member_count}.'
        ))
