from django.db import models
from django.contrib.auth.models import User

# ---- PROFILO CON AVATAR + COLORE SFONDoO ----
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    bg_color = models.CharField(max_length=7, blank=True, null=True) 
    # Colore esadecimale tipo #RRGGBB, persistito nel DB

    def __str__(self):
        return f"Profile({self.user.username})"


# ---- LINK ITEM (lasciato invariato) ----
class LinkItem(models.Model):
    YT = "youtube"
    IG = "instagram"
    TT = "tiktok"
    TW = "twitter"
    WB = "website"
    OT = "altro"
    TYPE_CHOICES = [
        (YT, "YouTube"),
        (IG, "Instagram"),
        (TT, "TikTok"),
        (TW, "Twitter/X"),
        (WB, "Sito Web"),
        (OT, "Altro"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="links")
    url = models.URLField()
    tipo = models.CharField(max_length=20, choices=TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.get_tipo_display()} → {self.url}"
