from django.views.generic import TemplateView, ListView

from home.models import TeamMember, MissionContent


class HomePageView(TemplateView):
    template_name = 'components/pages/home.html'


class EmergencyGuidelineView(TemplateView):
    template_name = 'components/pages/emergency_contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['steps'] = [
            {"step": 1, "title": "Call Emergency Services",
             "description": "Dial 911 or your local emergency number immediately."},
            {"step": 2, "title": "Provide First Aid",
             "description": "If trained, provide first aid to the injured person until help arrives."},
            {"step": 3, "title": "Stay Calm",
             "description": "Keep yourself and others calm to avoid further panic or injury."},
            {"step": 4, "title": "Gather Information",
             "description": "Collect important information such as the nature of the emergency and any injuries sustained."},
            {"step": 5, "title": "Follow Instructions",
             "description": "Follow the instructions given by emergency personnel over the phone."},
            {"step": 6, "title": "Wait for Help",
             "description": "Stay with the injured person and wait for emergency services to arrive."},
        ]
        return context


class Scanner(TemplateView):
    template_name = 'components/pages/Scanner.html'
    pass


class PrescriptionPageView(TemplateView):
    template_name = 'components/pages/prescription.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dosing_schedule'] = [
            (1, "65 mg/m²"), (2, "65 mg/m²"), (3, "235 mg/m²"), (4, "515 mg/m²"), (5 - 14, "1030 mg/m²")
        ]
        context['admin_instructions'] = [
            ("Tzield is administered by intravenous infusion (IV) over a minimum duration of 30 minutes.", "icon1.png"),
            (
                "Dosage form and strength: Injection: 2 mg/2 mL (1 mg/mL) clear, colorless to slightly opalescent solution.",
                "icon2.png"),
            ("Do not administer 2 doses on the same day.", "icon3.png"),
            ("If an infusion is missed, resume as soon as possible at the next scheduled time.", "icon4.png")
        ]
        return context


class AboutUsView(TemplateView):
    template_name = 'components/pages/about_us.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['team_members'] = TeamMember.objects.all()
        return context


class MissionView(ListView):
    model = MissionContent
    template_name = 'components/pages/mission.html'
    context_object_name = 'mission_contents'
