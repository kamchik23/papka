# cafe/management/commands/add_sample_tours.py
from django.core.management.base import BaseCommand
from cafe.models import Tour

class Command(BaseCommand):
    help = 'Добавляет тестовые туры в базу данных'

    def handle(self, *args, **options):
        tours_data = [
            {
                'title': 'Отдых в Сочи',
                'description': 'Прекрасный отдых на черноморском побережье. Включает проживание в отеле 4*, питание по системе "всё включено", экскурсии по достопримечательностям Сочи.',
                'price': 45000,
                'duration_days': 7,
                'destination': 'Сочи, Россия',
                'image': '/static/images/sochi.jpg'
            },
            {
                'title': 'Горнолыжный курорт в Красной Поляне',
                'description': 'Незабываемый горнолыжный отдых в горах Кавказа. Прокат оборудования, инструктаж для начинающих, комфортабельные шале у подножия гор.',
                'price': 65000,
                'duration_days': 5,
                'destination': 'Красная Поляна, Россия',
                'image': '/static/images/krasnaya_polyana.jpg'
            },
            {
                'title': 'Экскурсионный тур по Золотому Кольцу',
                'description': 'Путешествие по древним городам России: Сергиев Посад, Переславль-Залесский, Ростов Великий, Ярославль, Кострома, Иваново, Суздаль, Владимир.',
                'price': 35000,
                'duration_days': 8,
                'destination': 'Золотое Кольцо, Россия',
                'image': '/static/images/golden_ring.jpg'
            },
            {
                'title': 'Пляжный отдых в Турции',
                'description': 'Все включено на берегу Средиземного моря. Шикарные пляжи, бассейны, анимация, экскурсии в древние города и дегустация местной кухни.',
                'price': 75000,
                'duration_days': 10,
                'destination': 'Анталья, Турция',
                'image': '/static/images/turkey.jpg'
            },
            {
                'title': 'Горный треккинг на Алтае',
                'description': 'Активный отдых для любителей природы. Походы по горным тропам, ночевки в палатках, сплавы по горным рекам, знакомство с местной культурой.',
                'price': 28000,
                'duration_days': 6,
                'destination': 'Алтай, Россия',
                'image': '/static/images/altai.jpg'
            },
            {
                'title': 'Культурный тур в Санкт-Петербург',
                'description': 'Знакомство с культурной столицей России. Экскурсии по Эрмитажу, Петергофу, Царскому Селу, речные прогулки по каналам и ночные разводы мостов.',
                'price': 40000,
                'duration_days': 5,
                'destination': 'Санкт-Петербург, Россия',
                'image': '/static/images/spb.jpg'
            },
            {
                'title': 'Сафари в Кении',
                'description': 'Уникальное сафари в национальных парках Кении. Наблюдение за дикими животными в естественной среде, проживание в лоджах, знакомство с культурой масаи.',
                'price': 120000,
                'duration_days': 12,
                'destination': 'Найроби, Кения',
                'image': '/static/images/kenya.jpg'
            },
            {
                'title': 'Гастрономический тур в Италию',
                'description': 'Путешествие для гурманов: дегустации вин в Тоскане, кулинарные мастер-классы, посещение сыроварен и оливковых рощ, экскурсии по историческим местам.',
                'price': 89000,
                'duration_days': 9,
                'destination': 'Флоренция, Италия',
                'image': '/static/images/italy.jpg'
            },
            {
                'title': 'Экзотический отдых в Таиланде',
                'description': 'Отдых на тропических островах: дайвинг, сноркелинг, экскурсии к буддийским храмам, тайский массаж, знакомство с местной кухней и культурой.',
                'price': 68000,
                'duration_days': 14,
                'destination': 'Пхукет, Таиланд',
                'image': '/static/images/thailand.jpg'
            },
            {
                'title': 'Зимняя сказка в Карелии',
                'description': 'Зимнее приключение в карельских лесах: катание на хаски, снегоходах, подледная рыбалка, баня по-черному, северное сияние и уютные деревянные домики.',
                'price': 32000,
                'duration_days': 4,
                'destination': 'Карелия, Россия',
                'image': '/static/images/karelia.jpg'
            }
        ]

        created_count = 0
        for tour_data in tours_data:
            tour, created = Tour.objects.get_or_create(
                title=tour_data['title'],
                defaults=tour_data
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Добавлен тур: {tour.title}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Тур уже существует: {tour.title}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'Успешно добавлено {created_count} туров!')
        )