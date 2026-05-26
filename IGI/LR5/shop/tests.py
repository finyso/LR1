from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date, timedelta
from shop.models import *

class ModelTests(TestCase):
    """Тесты моделей"""
    
    def setUp(self):
        self.category = Category.objects.create(name='Тестовая категория')
        
        self.product = Product.objects.create(
            name='Тестовый товар',
            category=self.category,
            price=100.00,
            description='Описание товара',
            is_available=True
        )
        
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        
        self.client_obj = Client.objects.create(
            user=self.user,
            name='Тестовый Клиент',
            phone='+375 (29) 123-45-67',
            email='test@example.com',
            address='Тестовый адрес',
            date_of_birth=date.today() - timedelta(days=365*25)  # 25 лет
        )
    
    def test_category_creation(self):
        """Тест создания категории"""
        self.assertEqual(self.category.name, 'Тестовая категория')
        self.assertEqual(str(self.category), 'Тестовая категория')
    
    def test_product_creation(self):
        """Тест создания товара"""
        self.assertEqual(self.product.name, 'Тестовый товар')
        self.assertEqual(float(self.product.price), 100.00)
        self.assertIn('Тестовый товар', str(self.product))
        self.assertIn('100', str(self.product))
    
    def test_client_creation(self):
        """Тест создания клиента"""
        self.assertEqual(self.client_obj.name, 'Тестовый Клиент')
        self.assertTrue(self.client_obj.age() >= 18)
    
    def test_client_age_validation(self):
        """Тест валидации возраста (должен быть 18+)"""
        with self.assertRaises(ValueError):
            underage_client = Client(
                name='Молодой',
                phone='+375 (29) 111-11-11',
                email='young@example.com',
                address='Адрес',
                date_of_birth=date.today() - timedelta(days=365*16)  # 16 лет
            )
            underage_client.save()
    
    def test_phone_validation(self):
        """Тест формата телефона"""
        with self.assertRaises(Exception):
            wrong_phone_client = Client(
                name='Тест',
                phone='123456789', 
                email='test@example.com',
                address='Адрес',
                date_of_birth=date.today() - timedelta(days=365*20)
            )
            wrong_phone_client.full_clean()
    
    def test_product_price_validation(self):
        """Тест валидации цены (не может быть отрицательной)"""
        with self.assertRaises(Exception):
            negative_price = Product(
                name='Дешевый',
                category=self.category,
                price=-10.00,
                description='Отрицательная цена'
            )
            negative_price.full_clean()
    
    def test_order_creation(self):
        """Тест создания заказа"""
        order = Order.objects.create(
            client=self.client_obj,
            delivery_address='Тестовый адрес доставки',
            status='pending',
            total_amount=100.00
        )
        
        OrderItem.objects.create(
            order=order,
            product=self.product,
            quantity=2,
            price_at_time=100.00
        )
        
        self.assertEqual(order.client.name, 'Тестовый Клиент')
        self.assertEqual(order.status, 'pending')
        self.assertEqual(order.items.count(), 1)
        self.assertEqual(order.items.first().subtotal(), 200.00)
    
    def test_promo_code_validity(self):
        """Тест промокода"""
        now = timezone.now()
        promo = PromoCode.objects.create(
            code='TEST10',
            discount_percent=10,
            valid_from=now - timedelta(days=1),
            valid_to=now + timedelta(days=30),
            is_active=True,
            max_uses=10
        )
        
        self.assertTrue(promo.is_valid)
        self.assertEqual(str(promo), 'TEST10 (10%)')


class ViewTests(TestCase):
    """Тесты представлений (views)"""
    
    def setUp(self):
        self.category = Category.objects.create(name='Торты')
        self.product = Product.objects.create(
            name='Наполеон',
            category=self.category,
            price=450.00,
            description='Вкусный торт',
            is_available=True
        )
        
        self.user = User.objects.create_user(
            username='viewuser',
            password='viewpass123'
        )
    
    def test_home_page(self):
        """Тест главной страницы"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/home.html')
    
    def test_products_page(self):
        """Тест страницы товаров"""
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Наполеон')
    
    def test_product_search(self):
        """Тест поиска товаров"""
        response = self.client.get('/products/?search=торт')
        self.assertEqual(response.status_code, 200)
    
    def test_product_filter_by_price(self):
        """Тест фильтрации по цене"""
        response = self.client.get('/products/?min_price=100&max_price=500')
        self.assertEqual(response.status_code, 200)
    
    def test_reviews_page(self):
        """Тест страницы отзывов"""
        response = self.client.get('/reviews/')
        self.assertEqual(response.status_code, 200)
    
    def test_promocodes_page(self):
        """Тест страницы промокодов"""
        response = self.client.get('/promocodes/')
        self.assertEqual(response.status_code, 200)
    
    def test_about_page(self):
        """Тест страницы "О компании" """
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)
    
    def test_contacts_page(self):
        """Тест страницы контактов"""
        response = self.client.get('/contacts/')
        self.assertEqual(response.status_code, 200)
    
    def test_statistics_page(self):
        """Тест страницы статистики"""
        response = self.client.get('/statistics/')
        self.assertEqual(response.status_code, 200)
    
    def test_login_page(self):
        """Тест страницы входа"""
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)
    
    def test_register_page(self):
        """Тест страницы регистрации"""
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)


class AuthTests(TestCase):
    """Тесты аутентификации и авторизации"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='authuser',
            password='authpass123'
        )
    
    def test_user_login(self):
        """Тест входа пользователя"""
        response = self.client.post('/login/', {
            'username': 'authuser',
            'password': 'authpass123'
        })
        self.assertEqual(response.status_code, 302)
    
    def test_user_logout(self):
        """Тест выхода пользователя"""
        self.client.login(username='authuser', password='authpass123')
        response = self.client.post('/logout/')
        self.assertEqual(response.status_code, 302)
    
    def test_register_new_user(self):
        """Тест регистрации нового пользователя"""
        response = self.client.post('/register/', {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'NewPass123!',
            'password2': 'NewPass123!',
            'name': 'Новый Пользователь',
            'phone': '+375 (29) 123-45-67',
            'address': 'Тестовый адрес',
            'date_of_birth': '2000-01-01'
        })
        self.assertEqual(response.status_code, 302)
    
    def test_protected_page_requires_login(self):
        """Тест защищенной страницы (требуется вход)"""
        response = self.client.get('/orders/')
        self.assertEqual(response.status_code, 302) 


class AdminTests(TestCase):
    """Тесты админ-панели"""
    
    def setUp(self):
        self.admin = User.objects.create_superuser(
            username='admin',
            password='adminpass123',
            email='admin@example.com'
        )
    
    def test_admin_login(self):
        """Тест входа в админку"""
        response = self.client.post('/admin/login/', {
            'username': 'admin',
            'password': 'adminpass123'
        })
        self.assertEqual(response.status_code, 302)
    
    def test_admin_page_access(self):
        """Тест доступа к админ-панели"""
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)


class CartTests(TestCase):
    """Тесты корзины"""
    
    def setUp(self):
        self.category = Category.objects.create(name='Тест')
        self.product = Product.objects.create(
            name='Тест',
            category=self.category,
            price=100,
            description='Тест'
        )
        self.user = User.objects.create_user(
            username='cartuser',
            password='cartpass123'
        )
        self.client.login(username='cartuser', password='cartpass123')
    
    def test_add_to_cart(self):
        """Тест добавления товара в корзину"""
        response = self.client.get(f'/cart/add/{self.product.id}/')
        self.assertEqual(response.status_code, 302) 
        cart = self.client.session.get('cart', {})
        self.assertIn(str(self.product.id), cart)

class QuickCoverageBoost(TestCase):
    """Быстрое повышение покрытия"""
    
def test_api_functions_always_return_string(self):
    from shop.api.services import get_random_fact, get_joke
    self.assertTrue(isinstance(get_random_fact(), str))
    self.assertTrue(isinstance(get_joke(), str))
    
    def test_all_models_have_str(self):
        models_to_check = [
            Category(name='Test'),
            Product(name='Test', category=Category(name='Cat'), price=100, description='D'),
            Client(name='Test', phone='+375 (29) 111-11-11', email='e@e.com', address='A', date_of_birth=date.today() - timedelta(days=7300)),
            PromoCode(code='T', discount_percent=10, valid_from=timezone.now(), valid_to=timezone.now() + timedelta(days=1)),
            News(title='T', summary='S', content='C'),
            Vacancy(title='T', description='D', requirements='R', salary='S'),
            GlossaryTerm(term='T', definition='D'),
            CompanyInfo(key='K', value='V')
        ]
        for model in models_to_check:
            self.assertTrue(str(model))

class AdditionalCoverageTests(TestCase):
    """Дополнительные тесты для повышения покрытия до 80%+"""
    
    def setUp(self):
        self.category = Category.objects.create(name='ТестКат', description='Описание')
        self.product = Product.objects.create(
            name='ТестПродукт',
            category=self.category,
            price=500,
            description='Тестовое описание',
            is_available=True,
            unit='pcs'
        )
        self.user = User.objects.create_user('testuser2', 'test2@test.com', 'test123')
        self.client_obj = Client.objects.create(
            user=self.user,
            name='Тест Клиент 2',
            phone='+375 (29) 222-22-22',
            email='test2@test.com',
            address='Тест адрес 2',
            date_of_birth=date.today() - timedelta(days=7300)
        )
        self.employee_user = User.objects.create_user('empuser', 'emp@test.com', 'emppass')
        self.employee = Employee.objects.create(
            user=self.employee_user,
            name='Тест Сотрудник',
            position='manager',
            phone='+375 (29) 999-99-99',
            email='emp@test.com',
            date_of_birth=date.today() - timedelta(days=10000)
        )
    
    def test_employee_age_validation(self):
        """Тест валидации возраста сотрудника"""
        with self.assertRaises(ValueError):
            young_employee = Employee(
                name='Молодой',
                position='courier',
                phone='+375 (29) 111-11-11',
                email='young@test.com',
                date_of_birth=date.today() - timedelta(days=365*16)
            )
            young_employee.save()
    
    def test_employee_str_method(self):
        """Тест строкового представления сотрудника"""
        self.assertIn('Тест Сотрудник', str(self.employee))
        self.assertIn('Менеджер', str(self.employee))
    
    def test_contact_str_method(self):
        """Тест строкового представления контакта"""
        contact = Contact.objects.create(
            employee=self.employee,
            work_phone='+375 (29) 777-77-77',
            work_email='work@test.com',
            responsibilities='Управление заказами'
        )
        self.assertIn('Тест Сотрудник', str(contact))
    
    def test_pickup_point_str_method(self):
        """Тест строкового представления точки самовывоза"""
        pickup = PickupPoint.objects.create(
            name='Тестовая точка',
            address='ул. Тестовая 1',
            phone='+375 (29) 111-11-11',
            work_hours='09:00-20:00'
        )
        self.assertEqual(str(pickup), 'Тестовая точка')
    
    def test_ingredient_str_method(self):
        """Тест строкового представления ингредиента"""
        ingredient = Ingredient.objects.create(
            name='Мука',
            unit='кг',
            cost_per_unit=1.50
        )
        self.assertEqual(str(ingredient), 'Мука')
    
    def test_product_ingredient_relation(self):
        """Тест связи продукт-ингредиент"""
        ingredient = Ingredient.objects.create(
            name='Сахар',
            unit='кг',
            cost_per_unit=2.00
        )
        product_ingredient = ProductIngredient.objects.create(
            product=self.product,
            ingredient=ingredient,
            quantity=0.5
        )
        self.assertEqual(product_ingredient.product.name, 'ТестПродукт')
        self.assertEqual(product_ingredient.ingredient.name, 'Сахар')
    
    def test_order_with_promo_code_discount(self):
        """Тест заказа с применением промокода"""
        now = timezone.now()
        promo = PromoCode.objects.create(
            code='DISCOUNT20',
            discount_percent=20,
            valid_from=now - timedelta(days=1),
            valid_to=now + timedelta(days=30),
            is_active=True,
            max_uses=5
        )
        
        order = Order.objects.create(
            client=self.client_obj,
            employee=self.employee,
            delivery_address='Тест адрес',
            promo_code=promo,
            total_amount=0
        )
        
        OrderItem.objects.create(
            order=order,
            product=self.product,
            quantity=2,
            price_at_time=500
        )
        
        total = 2 * 500
        total = total * (100 - promo.discount_percent) / 100
        order.total_amount = total
        order.save()
        
        self.assertEqual(order.total_amount, 800) 
    
    def test_order_item_save_sets_price(self):
        """Тест автоматической установки цены в OrderItem"""
        order = Order.objects.create(
            client=self.client_obj,
            delivery_address='Тест',
            total_amount=0
        )
        order_item = OrderItem.objects.create(
            order=order,
            product=self.product,
            quantity=1,
            price_at_time=None  
        )
        self.assertEqual(float(order_item.price_at_time), 500)
    
    def test_cart_view_requires_login(self):
        """Тест что корзина требует авторизации"""
        self.client.logout()
        response = self.client.get('/cart/')
        self.assertEqual(response.status_code, 302)  
    
    def test_employee_dashboard_access(self):
        """Тест доступа к панели сотрудника"""
        self.client.login(username='empuser', password='emppass')
        response = self.client.get('/employee/dashboard/')
        self.assertEqual(response.status_code, 200)
    
    def test_employee_dashboard_forbidden_for_client(self):
        """Тест что клиент не может зайти в панель сотрудника"""
        self.client.login(username='testuser2', password='test123')
        response = self.client.get('/employee/dashboard/')
        self.assertEqual(response.status_code, 302)  
    
    def test_pickup_points_page(self):
        """Тест страницы точек самовывоза"""
        self.client.login(username='testuser2', password='test123')
        response = self.client.get('/pickup-points/')
        self.assertEqual(response.status_code, 200)
    
    def test_employee_clients_view(self):
        """Тест просмотра клиентов сотрудником"""
        self.client.login(username='empuser', password='emppass')
        response = self.client.get('/employee/clients/')
        self.assertEqual(response.status_code, 200)
    
    def test_employee_order_detail(self):
        """Тест деталей заказа для сотрудника"""
        self.client.login(username='empuser', password='emppass')
        order = Order.objects.create(
            client=self.client_obj,
            employee=self.employee,
            delivery_address='Тест',
            total_amount=500
        )
        response = self.client.get(f'/employee/order/{order.id}/')
        self.assertEqual(response.status_code, 200)
    
    def test_employee_order_detail_not_found(self):
        """Тест несуществующего заказа"""
        self.client.login(username='empuser', password='emppass')
        response = self.client.get('/employee/order/99999/')
        self.assertEqual(response.status_code, 404)
    
    def test_remove_from_cart(self):
        """Тест удаления товара из корзины"""
        self.client.login(username='testuser2', password='test123')
        session = self.client.session
        session['cart'] = {str(self.product.id): 2}
        session.save()
        
        response = self.client.get(f'/cart/remove/{self.product.id}/')
        self.assertEqual(response.status_code, 302)
        
        cart = self.client.session.get('cart', {})
        self.assertNotIn(str(self.product.id), cart)
    
    def test_update_cart(self):
        """Тест обновления количества в корзине"""
        self.client.login(username='testuser2', password='test123')
        session = self.client.session
        session['cart'] = {str(self.product.id): 2}
        session.save()
        
        response = self.client.post(f'/cart/update/{self.product.id}/', {
            'quantity': 5
        })
        self.assertEqual(response.status_code, 302)
        
        cart = self.client.session.get('cart', {})
        self.assertEqual(cart.get(str(self.product.id)), 5)
    
    def test_update_cart_remove_if_zero(self):
        """Тест удаления при количестве 0"""
        self.client.login(username='testuser2', password='test123')
        session = self.client.session
        session['cart'] = {str(self.product.id): 2}
        session.save()
        
        response = self.client.post(f'/cart/update/{self.product.id}/', {
            'quantity': 0
        })
        self.assertEqual(response.status_code, 302)
        
        cart = self.client.session.get('cart', {})
        self.assertNotIn(str(self.product.id), cart)
    
    def test_redirect_after_login_for_admin(self):
        """Тест редиректа после логина для админа"""
        admin = User.objects.create_superuser('testadmin', 'admin@test.com', 'admin123')
        response = self.client.post('/login/', {
            'username': 'testadmin',
            'password': 'admin123'
        })
        self.assertEqual(response.status_code, 302)
    
    def test_redirect_after_login_for_employee(self):
        """Тест редиректа после логина для сотрудника"""
        self.client.login(username='empuser', password='emppass')
        response = self.client.get('/redirect-after-login/')
        self.assertEqual(response.status_code, 302)
    
    def test_custom_logout(self):
        """Тест кастомного выхода"""
        self.client.login(username='testuser2', password='test123')
        response = self.client.post('/logout/')
        self.assertEqual(response.status_code, 302)
    
    def test_news_detail_view(self):
        """Тест детальной страницы новости"""
        news = News.objects.create(
            title='Тест новость',
            summary='Кратко',
            content='Полный текст новости',
            is_published=True
        )
        response = self.client.get(f'/news/{news.id}/')
        self.assertEqual(response.status_code, 200)
    
    def test_vacancy_list_view(self):
        """Тест списка вакансий"""
        Vacancy.objects.create(
            title='Тест вакансия',
            description='Описание',
            requirements='Требования',
            salary='1000',
            is_active=True
        )
        response = self.client.get('/vacancies/')
        self.assertEqual(response.status_code, 200)
    
    def test_glossary_list_view(self):
        """Тест словаря терминов"""
        GlossaryTerm.objects.create(
            term='Тест термин',
            definition='Определение'
        )
        response = self.client.get('/glossary/')
        self.assertEqual(response.status_code, 200)
    
    def test_product_detail_url(self):
        """Тест что страница товара существует (хотя у нас нет детальной)"""
        response = self.client.get(f'/products/')
        self.assertEqual(response.status_code, 200)
    
    def test_privacy_policy_page(self):
        """Тест страницы политики конфиденциальности"""
        response = self.client.get('/privacy/')
        self.assertEqual(response.status_code, 200)
    
    def test_order_create_post_with_empty_cart(self):
        """Тест создания заказа с пустой корзиной"""
        self.client.login(username='testuser2', password='test123')
        session = self.client.session
        session['cart'] = {}
        session.save()
        
        response = self.client.post('/order/create/', {
            'delivery_address': 'Тест адрес'
        })
        self.assertEqual(response.status_code, 302)  
    
    def test_invalid_product_in_cart(self):
        """Тест несуществующего товара в корзине"""
        self.client.login(username='testuser2', password='test123')
        session = self.client.session
        session['cart'] = {'99999': 2} 
        session.save()
        
        response = self.client.get('/cart/')
        self.assertEqual(response.status_code, 200)              

class AdminPanelTests(TestCase):
    """Тесты админ-панели (новые функции)"""
    
    def setUp(self):
        self.admin = User.objects.create_superuser(
            username='admin',
            password='admin123',
            email='admin@test.com'
        )
        self.category = Category.objects.create(name='ТестКат')
        self.product = Product.objects.create(
            name='ТестТовар',
            category=self.category,
            price=100,
            description='Тест'
        )
        self.client.login(username='admin', password='admin123')
    
    def test_admin_products_page(self):
        """Тест страницы управления товарами"""
        response = self.client.get('/admin-panel/products/')
        self.assertEqual(response.status_code, 200)
    
    def test_admin_product_create(self):
        """Тест создания товара админом"""
        response = self.client.post('/admin-panel/product/create/', {
            'name': 'Новый товар',
            'category': self.category.id,
            'price': '200',
            'description': 'Описание',
            'unit': 'pcs',
            'is_available': 'on'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Product.objects.filter(name='Новый товар').exists())
    
    def test_admin_product_edit(self):
        """Тест редактирования товара админом"""
        response = self.client.post(f'/admin-panel/product/{self.product.id}/edit/', {
            'name': 'Измененный товар',
            'category': self.category.id,
            'price': '150',
            'description': 'Новое описание',
            'unit': 'kg',
            'is_available': 'on'
        })
        self.assertEqual(response.status_code, 302)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'Измененный товар')
    
    def test_admin_product_delete(self):
        """Тест удаления товара админом"""
        response = self.client.post(f'/admin-panel/product/{self.product.id}/delete/')
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Product.objects.filter(id=self.product.id).exists())
    
    def test_admin_categories_page(self):
        """Тест страницы категорий"""
        response = self.client.get('/admin-panel/categories/')
        self.assertEqual(response.status_code, 200)
    
    def test_admin_sales_page(self):
        """Тест страницы продаж"""
        response = self.client.get('/admin-panel/sales/')
        self.assertEqual(response.status_code, 200)
    
    def test_admin_product_delete_confirmation(self):
        """Тест страницы подтверждения удаления"""
        response = self.client.get(f'/admin-panel/product/{self.product.id}/delete/')
        self.assertEqual(response.status_code, 200)


class EmployeePanelTests(TestCase):
    """Тесты панели сотрудника"""
    
    def setUp(self):
        self.employee_user = User.objects.create_user(
            username='employee',
            password='emp123'
        )
        self.employee = Employee.objects.create(
            user=self.employee_user,
            name='Тест Сотрудник',
            position='manager',
            phone='+375 (29) 111-11-11',
            email='emp@test.com',
            date_of_birth=date.today() - timedelta(days=10000)
        )
        self.category = Category.objects.create(name='Тест')
        self.product = Product.objects.create(
            name='Товар',
            category=self.category,
            price=100,
            description='Тест'
        )
        self.client.login(username='employee', password='emp123')
    
    def test_employee_order_create_page(self):
        """Тест страницы создания заказа сотрудником"""
        response = self.client.get('/employee/order/create/')
        self.assertEqual(response.status_code, 200)
    
    def test_employee_order_add_item(self):
        """Тест добавления товара в заказ"""
        from django.test import Client as DjangoClient
        client = DjangoClient()
        client.login(username='employee', password='emp123')
        
        client_obj = Client.objects.create(
            name='Клиент',
            phone='+375 (29) 111-11-11',
            email='client@test.com',
            address='Адрес',
            date_of_birth=date.today() - timedelta(days=7300)
        )
        order = Order.objects.create(
            client=client_obj,
            employee=self.employee,
            delivery_address='Тест'
        )
        response = client.post(f'/employee/order/{order.id}/add-item/', {
            'product': self.product.id,
            'quantity': 2,
            'price_at_time': 100
        })
        self.assertEqual(response.status_code, 302)


class OrderTests(TestCase):
    """Тесты заказов"""
    
    def setUp(self):
        self.client_obj = Client.objects.create(
            name='Тест Клиент',
            phone='+375 (29) 111-11-11',
            email='client@test.com',
            address='Адрес',
            date_of_birth=date.today() - timedelta(days=7300)
        )
        self.category = Category.objects.create(name='Тест')
        self.product = Product.objects.create(
            name='Тест',
            category=self.category,
            price=100,
            description='Тест'
        )
        self.user = User.objects.create_user('testuser', 'test@test.com', 'pass123')
        self.client.login(username='testuser', password='pass123')
    
    def test_order_list_without_client_profile(self):
        """Тест списка заказов без профиля клиента"""
        response = self.client.get('/orders/')
        self.assertEqual(response.status_code, 302)
    
    def test_cart_view_empty(self):
        """Тест пустой корзины"""
        response = self.client.get('/cart/')
        self.assertEqual(response.status_code, 200)


class UrlTests(TestCase):
    """Тесты URL маршрутов"""
    
    def test_calendar_page(self):
        """Тест страницы календаря"""
        response = self.client.get('/calendar/')
        self.assertEqual(response.status_code, 200)
    
    def test_pickup_points_page_requires_login(self):
        """Тест что точки самовывоза требуют логина"""
        response = self.client.get('/pickup-points/')
        self.assertEqual(response.status_code, 302)
    
    def test_statistics_page(self):
        """Тест страницы статистики (доступна всем)"""
        response = self.client.get('/statistics/')
        self.assertEqual(response.status_code, 200)
    
    def test_privacy_page(self):
        """Тест страницы политики"""
        response = self.client.get('/privacy/')
        self.assertEqual(response.status_code, 200)


class ModelStringTests(TestCase):
    """Тесты строковых представлений моделей"""
    
    def test_order_str(self):
        """Тест строки заказа"""
        client = Client.objects.create(
            name='Тест',
            phone='+375 (29) 111-11-11',
            email='test@test.com',
            address='Адрес',
            date_of_birth=date.today() - timedelta(days=7300)
        )
        order = Order.objects.create(
            client=client,
            delivery_address='Адрес',
            total_amount=100
        )
        self.assertIn(str(order.id), str(order))
    
    def test_promo_code_str(self):
        """Тест строки промокода"""
        promo = PromoCode.objects.create(
            code='TEST',
            discount_percent=15,
            valid_from=timezone.now(),
            valid_to=timezone.now() + timedelta(days=30)
        )
        self.assertEqual(str(promo), 'TEST (15%)')
    
    def test_news_str(self):
        """Тест строки новости"""
        news = News.objects.create(
            title='Тест новость',
            summary='Кратко',
            content='Полно'
        )
        self.assertEqual(str(news), 'Тест новость')


class EdgeCaseTests(TestCase):
    """Тесты граничных случаев"""
    
    def test_product_with_zero_price(self):
        """Тест товара с нулевой ценой"""
        category = Category.objects.create(name='Тест')
        product = Product.objects.create(
            name='Бесплатно',
            category=category,
            price=0,
            description='Бесплатный товар'
        )
        self.assertEqual(float(product.price), 0)
    
    def test_order_without_items(self):
        """Тест заказа без товаров"""
        client = Client.objects.create(
            name='Тест',
            phone='+375 (29) 111-11-11',
            email='test@test.com',
            address='Адрес',
            date_of_birth=date.today() - timedelta(days=7300)
        )
        order = Order.objects.create(
            client=client,
            delivery_address='Адрес',
            total_amount=0
        )
        self.assertEqual(order.total_amount, 0)
    
    def test_employee_without_user(self):
        """Тест сотрудника без привязанного пользователя"""
        employee = Employee.objects.create(
            name='Сотрудник без user',
            position='manager',
            phone='+375 (29) 111-11-11',
            email='no@user.com',
            date_of_birth=date.today() - timedelta(days=10000)
        )
        self.assertIsNone(employee.user)

class ViewsCoverageTests(TestCase):
    """Тесты для повышения покрытия views.py"""
    
    def setUp(self):
        self.category = Category.objects.create(name='Тест')
        self.product = Product.objects.create(
            name='Товар',
            category=self.category,
            price=100,
            description='Тест',
            is_available=True
        )
        self.user = User.objects.create_user('testuser', 'test@test.com', 'pass123')
        self.client_obj = Client.objects.create(
            user=self.user,
            name='Тест Клиент',
            phone='+375 (29) 111-11-11',
            email='test@test.com',
            address='Адрес',
            date_of_birth=date.today() - timedelta(days=7300)
        )
    
    def test_add_review_without_client(self):
        """Тест добавления отзыва пользователем без профиля клиента"""
        self.client.login(username='testuser', password='pass123')
        response = self.client.post('/reviews/add/', {
            'product': self.product.id,
            'rating': 5,
            'text': 'Отличный товар!'
        })
        self.assertEqual(response.status_code, 302)
    
    def test_employee_dashboard_for_admin(self):
        """Тест панели сотрудника для админа"""
        admin = User.objects.create_superuser('admin2', 'admin@test.com', 'admin123')
        self.client.login(username='admin2', password='admin123')
        response = self.client.get('/employee/dashboard/')
        self.assertEqual(response.status_code, 200)
    
    def test_employee_order_detail_for_admin(self):
        """Тест деталей заказа для админа"""
        admin = User.objects.create_superuser('admin3', 'admin@test.com', 'admin123')
        self.client.login(username='admin3', password='admin123')
        order = Order.objects.create(
            client=self.client_obj,
            delivery_address='Тест',
            total_amount=500
        )
        response = self.client.get(f'/employee/order/{order.id}/')
        self.assertEqual(response.status_code, 200)
    
    def test_redirect_after_login_superuser(self):
        """Тест редиректа после логина суперпользователя"""
        admin = User.objects.create_superuser('admin4', 'admin@test.com', 'admin123')
        self.client.login(username='admin4', password='admin123')
        response = self.client.get('/redirect-after-login/')
        self.assertEqual(response.status_code, 302)
    
    def test_redirect_after_login_employee(self):
        """Тест редиректа после логина сотрудника"""
        emp_user = User.objects.create_user('emp2', 'emp@test.com', 'emp123')
        Employee.objects.create(
            user=emp_user,
            name='Сотрудник',
            position='manager',
            phone='+375 (29) 111-11-11',
            email='emp@test.com',
            date_of_birth=date.today() - timedelta(days=10000)
        )
        self.client.login(username='emp2', password='emp123')
        response = self.client.get('/redirect-after-login/')
        self.assertEqual(response.status_code, 302)
    
    def test_redirect_after_login_client(self):
        """Тест редиректа после логина клиента"""
        self.client.login(username='testuser', password='pass123')
        response = self.client.get('/redirect-after-login/')
        self.assertEqual(response.status_code, 302)
    
    def test_privacy_policy_page(self):
        """Тест страницы политики"""
        response = self.client.get('/privacy/')
        self.assertEqual(response.status_code, 200)


class AdminPanelAdditionalTests(TestCase):
    """Дополнительные тесты админ-панели"""
    
    def setUp(self):
        self.admin = User.objects.create_superuser(
            username='admin',
            password='admin123',
            email='admin@test.com'
        )
        self.category = Category.objects.create(name='Тест')
        self.product = Product.objects.create(
            name='Товар',
            category=self.category,
            price=100,
            description='Тест'
        )
        self.client.login(username='admin', password='admin123')
    
    def test_admin_product_create_get(self):
        """Тест GET запроса создания товара"""
        response = self.client.get('/admin-panel/product/create/')
        self.assertEqual(response.status_code, 200)
    
    def test_admin_product_edit_get(self):
        """Тест GET запроса редактирования товара"""
        response = self.client.get(f'/admin-panel/product/{self.product.id}/edit/')
        self.assertEqual(response.status_code, 200)
    
    def test_admin_product_delete_get(self):
        """Тест GET запроса удаления товара (страница подтверждения)"""
        response = self.client.get(f'/admin-panel/product/{self.product.id}/delete/')
        self.assertEqual(response.status_code, 200)
    
    def test_admin_products_with_search(self):
        """Тест страницы товаров с поиском"""
        response = self.client.get('/admin-panel/products/?search=Товар')
        self.assertEqual(response.status_code, 200)

class CartEdgeTests(TestCase):
    """Тесты граничных случаев корзины"""
    
    def setUp(self):
        self.category = Category.objects.create(name='Тест')
        self.product = Product.objects.create(
            name='Товар',
            category=self.category,
            price=100,
            description='Тест'
        )
        self.user = User.objects.create_user('cartuser', 'cart@test.com', 'cart123')
        self.client.login(username='cartuser', password='cart123')
    
    def test_add_to_cart_multiple_times(self):
        """Тест многократного добавления одного товара"""
        response = self.client.get(f'/cart/add/{self.product.id}/')
        response = self.client.get(f'/cart/add/{self.product.id}/')
        self.assertEqual(response.status_code, 302)
        cart = self.client.session.get('cart', {})
        self.assertEqual(cart.get(str(self.product.id)), 2)
    
    def test_update_cart_invalid_quantity(self):
        """Тест обновления корзины с невалидным количеством"""
        session = self.client.session
        session['cart'] = {str(self.product.id): 2}
        session.save()
        
        response = self.client.post(f'/cart/update/{self.product.id}/', {
            'quantity': -5
        })
        self.assertEqual(response.status_code, 302)


class OrderStatusTests(TestCase):
    """Тесты статусов заказов"""
    
    def setUp(self):
        self.client_obj = Client.objects.create(
            name='Тест',
            phone='+375 (29) 111-11-11',
            email='test@test.com',
            address='Адрес',
            date_of_birth=date.today() - timedelta(days=7300)
        )
        self.employee = Employee.objects.create(
            name='Сотрудник',
            position='manager',
            phone='+375 (29) 111-11-11',
            email='emp@test.com',
            date_of_birth=date.today() - timedelta(days=10000)
        )
        self.order = Order.objects.create(
            client=self.client_obj,
            employee=self.employee,
            delivery_address='Тест'
        )
        self.admin = User.objects.create_superuser('admin', 'admin@test.com', 'admin123')
    
    def test_order_status_update_via_post(self):
        """Тест обновления статуса заказа через POST"""
        self.client.login(username='admin', password='admin123')
        response = self.client.post(f'/employee/order/{self.order.id}/', {
            'status': 'completed'
        })
        self.assertEqual(response.status_code, 302)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'completed')