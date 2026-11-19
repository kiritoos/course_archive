import random
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker
from archive.models import Discipline, Keyword, Work

class Command(BaseCommand):
    help = "Заполняет базу тестовыми данными"

    def add_arguments(self, parser):
        parser.add_argument("--works", type=int, default=100_000)

    @transaction.atomic
    def handle(self, *args, **options):
        fake = Faker("ru_RU")
        User = get_user_model()

        users = [User.objects.get_or_create(username=f"student_{i}")[0] for i in range(20)]
        Discipline.objects.bulk_create([Discipline(name=f"Дисциплина {i}") for i in range(50)], ignore_conflicts=True)
        Keyword.objects.bulk_create([Keyword(name=f"ключ_{i}") for i in range(200)], ignore_conflicts=True)

        disciplines = list(Discipline.objects.all())
        keywords = list(Keyword.objects.all())
        total = options["works"]
        batch_size = 5000
        Through = Work.keywords.through

        for start in range(0, total, batch_size):
            size = min(batch_size, total - start)
            works = Work.objects.bulk_create([
                Work(
                    title=fake.sentence(nb_words=5)[:200],
                    content=fake.text(max_nb_chars=400),
                    year=random.randint(2015, 2026),
                    supervisor=fake.name(),
                    grade=random.randint(2, 5),
                    is_defended=random.random() < 0.8,
                    author=random.choice(users),
                    discipline=random.choice(disciplines),
                )
                for _ in range(size)
            ])
            Through.objects.bulk_create([
                Through(work_id=work.pk, keyword_id=kw.pk)
                for work in works
                for kw in random.sample(keywords, 3)
            ])
            self.stdout.write(f"Создано {start + size} из {total}")

        self.stdout.write(self.style.SUCCESS("Готово! База заполнена."))