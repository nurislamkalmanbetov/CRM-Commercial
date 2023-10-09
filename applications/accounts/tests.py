from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal
from datetime import timedelta

from .models import Profile, Payment

User = get_user_model()


class IwexTestCase(TestCase):

    def test_user_create(self):
        User.objects.create_user(email='test@test.asd', password='Qwerty123')
        self.assertEqual(User.objects.get(id=1).email, 'test@test.asd')



class UserModelTest(TestCase):

    def setUp(self):
        # Этот метод будет автоматически вызван перед каждым тестовым методом,
        # чтобы установить начальные условия для тестов.
        self.user = User.objects.create(
            email="testuser@example.com",
            phone="1234567890",
            whatsapp_phone="0987654321",
            is_employer=True,
            is_staff=False,
            is_student=False,
            is_active=True,
        )

    def test_create_user(self):
        user_count = User.objects.all().count()
        self.assertEqual(user_count, 1)
        self.assertEqual(self.user.email, "testuser@example.com")

    def test_save_user(self):
        self.user.phone = "1112223333"
        self.user.save()

        updated_user = User.objects.get(email="testuser@example.com")
        self.assertEqual(updated_user.phone, "1112223333")

    def delete(self, *args, **kwargs):
        if not self.is_superuser:
            self.is_delete = True
            self.save()
        else:
            super(User, self).delete(*args, **kwargs)

    def test_model_fields(self):
        self.assertIsInstance(self.user.email, str)
        self.assertIsInstance(self.user.phone, str)
        self.assertIsInstance(self.user.is_employer, bool)
        # Продолжайте проверять другие поля по аналогии...



class PaymentModelTest(TestCase):

    def setUp(self):
        # Создаем тестового пользователя
        self.user = User.objects.create(email="testuser@example.com")

        # Создаем тестового администратора, который принимает платежи
        self.admin = User.objects.create(email="admin@example.com", is_staff=True)

    def test_create_payment(self):
        payment = Payment.objects.create(user=self.user, who_created=self.admin, amount_paid=Decimal('5000.00'))
        self.assertEqual(payment.remaining_amount, Decimal('30000.00'))
        self.assertFalse(payment.is_fully_paid)
        self.assertIsNotNone(payment.due_date)

    def test_update_payment(self):
        payment = Payment.objects.create(user=self.user, who_created=self.admin, amount_paid=Decimal('5000.00'))
        payment.amount_paid += Decimal('30000.00')
        payment.save()
        self.assertEqual(payment.remaining_amount, Decimal('0.00'))
        self.assertTrue(payment.is_fully_paid)

    def test_payment_date(self):
        payment = Payment.objects.create(user=self.user, who_created=self.admin, amount_paid=Decimal('5000.00'))
        self.assertIsNotNone(payment.payment_date)

    def test_due_date(self):
        payment = Payment.objects.create(user=self.user, who_created=self.admin, amount_paid=Decimal('5000.00'))
        expected_due_date = payment.payment_date + timedelta(days=60)
        self.assertEqual(payment.due_date, expected_due_date)


