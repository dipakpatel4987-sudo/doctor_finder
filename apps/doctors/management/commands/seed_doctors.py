from django.core.management.base import BaseCommand
from apps.doctors.models import Doctor

DATA = [
    ('Dr. Amit Shah', 'Cardiologist', 'Ahmedabad', 500, 15, 4.8, 23.0225, 72.5714, 'MBBS, MD, DM (Cardiology)'),
    ('Dr. Neha Patel', 'Dentist', 'Surat', 400, 8, 4.6, 21.1702, 72.8311, 'BDS, MDS'),
    ('Dr. Rohit Mehta', 'Neurologist', 'Vadodara', 700, 12, 4.9, 22.3072, 73.1812, 'MBBS, MD, DM (Neurology)'),
    ('Dr. Pooja Desai', 'Dermatologist', 'Rajkot', 450, 9, 4.7, 22.3039, 70.8022, 'MBBS, MD (Dermatology)'),
    ('Dr. Kiran Joshi', 'Cardiologist', 'Surat', 600, 11, 4.5, 21.1959, 72.8302, 'MBBS, MD, DM'),
    ('Dr. Vivek Trivedi', 'Dentist', 'Ahmedabad', 350, 6, 4.4, 23.0395, 72.5660, 'BDS'),
    ('Dr. Sneha Rao', 'Neurologist', 'Rajkot', 650, 10, 4.8, 22.2900, 70.7900, 'MBBS, MD, DM'),
    ('Dr. Manish Gupta', 'Dermatologist', 'Vadodara', 500, 7, 4.6, 22.3200, 73.1700, 'MBBS, DDVL'),
]


class Command(BaseCommand):
    help = 'Sample doctors add karta hai'

    def handle(self, *args, **opts):
        created = 0
        for n, s, c, f, e, r, la, lo, edu in DATA:
            _, new = Doctor.objects.get_or_create(
                name=n,
                defaults=dict(
                    specialty=s, city=c, fee=f, experience=e, rating=r,
                    latitude=la, longitude=lo, education=edu,
                    phone='+91 98250 00000',
                    about=f'{n} {s} specialist hain aur {e} saal ka anubhav rakhte hain.',
                ),
            )
            created += int(new)
        self.stdout.write(self.style.SUCCESS(f'{created} doctors add hue.'))