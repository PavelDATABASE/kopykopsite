from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from kopykop.models import Profile


class Command(BaseCommand):
    help = 'Создаёт профили для пользователей, у которых их нет'

    def handle(self, *args, **options):
        users_without_profile = User.objects.filter(profile__isnull=True)
        
        if not users_without_profile.exists():
            self.stdout.write(self.style.SUCCESS('Все пользователи уже имеют профили'))
            return
        
        for user in users_without_profile:
            Profile.objects.create(user=user)
            self.stdout.write(f'Создан профиль для пользователя: {user.username}')
        
        self.stdout.write(self.style.SUCCESS(f'Создано профилей: {users_without_profile.count()}'))
