from django.core.management.base import BaseCommand
from drugs.models import Route

class Command(BaseCommand):
    help = 'Populate the Route model with common medicine routes'

    def handle(self, *args, **options):
        routes = [
            ('Oral', 'Taken by mouth. This includes tablets, capsules, liquids, and chewable forms.'),
            ('Sublingual', 'Placed under the tongue to dissolve and be absorbed into the bloodstream.'),
            ('Buccal', 'Placed between the gum and cheek to be absorbed through the oral mucosa.'),
            ('Topical', 'Applied directly to the skin or mucous membranes.'),
            ('Transdermal', 'Absorbed through the skin via a patch or gel.'),
            ('Intravenous (IV)', 'Injected directly into a vein for immediate absorption into the bloodstream.'),
            ('Intramuscular (IM)', 'Injected into muscle tissue for slower absorption than IV.'),
            ('Subcutaneous (SC)', 'Injected into the fatty tissue just beneath the skin.'),
            ('Inhalation', 'Breathed in through the mouth or nose, typically used for respiratory conditions.'),
            ('Nasal', 'Administered through the nose, often as a spray or drops.'),
            ('Ophthalmic', 'Applied directly to the eye, usually as drops or ointment.'),
            ('Otic', 'Administered into the ear canal.'),
            ('Rectal', 'Inserted into the rectum, often as suppositories or enemas.'),
            ('Vaginal', 'Inserted into the vagina, often as creams, tablets, or suppositories.'),
            ('Intradermal', 'Injected into the dermis, the layer of skin between the epidermis and subcutaneous tissues.'),
            ('Epidural', 'Injected into the space around the spinal cord.'),
            ('Intrathecal', 'Injected directly into the fluid surrounding the brain and spinal cord.'),
            ('Intra-articular', 'Injected directly into a joint space.'),
            ('Intralesional', 'Injected directly into a lesion or affected area of tissue.'),
            ('Intravesical', 'Administered directly into the bladder.'),
        ]

        for name, description in routes:
            Route.objects.get_or_create(name=name, description=description)

        self.stdout.write(self.style.SUCCESS('Successfully populated Route model'))