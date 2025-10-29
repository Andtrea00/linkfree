from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, CreateView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.db.models import Count
from .models import LinkItem, Profile
from .forms import LinkItemForm, AvatarUploadForm


class HomeView(TemplateView):
    template_name = "home.html"


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        profile, _ = Profile.objects.get_or_create(user=self.request.user)

        ctx["form"] = LinkItemForm()
        ctx["avatar_form"] = AvatarUploadForm(instance=profile)
        ctx["links"] = LinkItem.objects.filter(user=self.request.user)
        ctx["profile_user"] = self.request.user
        ctx["profile"] = profile
        ctx["is_owner"] = True

        public_path = reverse("public_profile", kwargs={"username": self.request.user.username})
        ctx["share_url"] = self.request.build_absolute_uri(public_path)

        # ⬇️ importante: leggi il colore con fallback
        ctx["bg_color"] = getattr(profile, "bg_color", None) or "#f7f7f8"
        return ctx

    def post(self, request, *args, **kwargs):
        action = request.POST.get("action")
        profile, _ = Profile.objects.get_or_create(user=request.user)

        if action == "create_link":
            form = LinkItemForm(request.POST)
            if form.is_valid():
                item = form.save(commit=False)
                item.user = request.user
                item.save()
                return redirect("dashboard")
            ctx = self.get_context_data()
            ctx["form"] = form
            return self.render_to_response(ctx)

        if action == "upload_avatar":
            form = AvatarUploadForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()
                return redirect("dashboard")
            ctx = self.get_context_data()
            ctx["avatar_form"] = form
            return self.render_to_response(ctx)

        if action == "set_bg_color":
            color = (request.POST.get("bg_color") or "").strip()
            # valida formato #RRGGBB molto semplice
            if len(color) == 7 and color.startswith("#"):
                profile.bg_color = color
            else:
                profile.bg_color = None
            profile.save()
            return redirect("dashboard")

        return redirect("dashboard")


class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")


class PublicProfileView(TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        username = kwargs.get("username")
        profile_user = get_object_or_404(User, username=username)
        profile, _ = Profile.objects.get_or_create(user=profile_user)

        ctx["profile_user"] = profile_user
        ctx["profile"] = profile
        ctx["links"] = LinkItem.objects.filter(user=profile_user)
        ctx["is_owner"] = self.request.user.is_authenticated and self.request.user == profile_user

        public_path = reverse("public_profile", kwargs={"username": profile_user.username})
        ctx["share_url"] = self.request.build_absolute_uri(public_path)

        # ⬇️ stesso fallback
        ctx["bg_color"] = getattr(profile, "bg_color", None) or "#f7f7f8"
        return ctx
    

class DeleteLinkView(LoginRequiredMixin, View):
    def post(self, request, pk):
        item = get_object_or_404(LinkItem, pk=pk)
        if item.user != request.user:
            return HttpResponseForbidden("Non autorizzato")
        item.delete()
        return redirect("dashboard")


class StatsView(LoginRequiredMixin, TemplateView):
    template_name = "stats.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        profile, _ = Profile.objects.get_or_create(user=self.request.user)

        # Colore sfondo uguale alla dashboard
        ctx["bg_color"] = getattr(profile, "bg_color", None) or "#f7f7f8"

        # Statistiche base
        qs = LinkItem.objects.filter(user=self.request.user)
        ctx["total_links"] = qs.count()

        # Per tipologia (YouTube, Instagram, ecc.)
        per_tipo = (
            qs.values("tipo")
              .annotate(cnt=Count("id"))
              .order_by("-cnt")
        )
        # Converte in lista di tuple (label leggibile, count)
        tipo_label = dict(LinkItem.TYPE_CHOICES)
        ctx["by_type"] = [(tipo_label.get(row["tipo"], row["tipo"]), row["cnt"]) for row in per_tipo]

        # Ultimi 10 link creati (per avere qualcosa di utile subito)
        ctx["latest"] = qs.order_by("-created_at")[:10]

        return ctx
