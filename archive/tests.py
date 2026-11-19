from django.contrib.auth import get_user_model
from django.test import TestCase
from .models import Work, Discipline, Keyword

class WorkModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username="testuser")
        self.discipline = Discipline.objects.create(name="Математика")
        self.keyword = Keyword.objects.create(name="тест")
        self.work = Work.objects.create(
            title="Тестовая работа",
            content="Описание",
            year=2025,
            supervisor="Иванов",
            grade=4,
            author=self.user,
            discipline=self.discipline,
        )
        self.work.keywords.add(self.keyword)

    def test_work_creation(self):
        self.assertEqual(self.work.title, "Тестовая работа")
        self.assertEqual(self.work.discipline.name, "Математика")
        self.assertEqual(self.work.author.username, "testuser")
        self.assertEqual(self.work.keywords.count(), 1)

    def test_str_method(self):
        self.assertEqual(str(self.work), "Тестовая работа")

class IndexQueriesTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username="u")
        self.discipline = Discipline.objects.create(name="c")
        self.keyword = Keyword.objects.create(name="t")
        for i in range(10):
            work = Work.objects.create(
                title=f"w{i}", content="text", year=2025, supervisor="sup",
                grade=5, author=self.user, discipline=self.discipline
            )
            work.keywords.add(self.keyword)

    def test_query_count_does_not_grow(self):
        with self.assertNumQueries(2):
            self.client.get("/")