from django.contrib import admin
from .models import UserProfile
from .models import Pand, TypeHuis, Fase, Status
from .models import Criteria, PandCriteria
from .models import Eigenschap, PandEigenschap
from .models import VerbruiksType, PandVerbruiksType
from .models import Wettelijk, PandWettelijk
from .models import Review, PandReview
from .models import Bezichtiging, PandBezichtiging
from .models import Supportticket
from django.shortcuts import get_object_or_404
from master.models import Image



class ImageInlineAdmin(admin.TabularInline):
    model = Image

class CriteriaInlineAdmin(admin.TabularInline):
        model = PandCriteria


class EigenschapInlineAdmin(admin.TabularInline):
    model = PandEigenschap


class VerbruikInlineAdmin(admin.TabularInline):
    model = PandVerbruiksType


class WettelijkInlineAdmin(admin.TabularInline):
     model = PandWettelijk


class ReviewInlineAdmin(admin.TabularInline):
    model = PandReview


class ImageAdmin(admin.ModelAdmin):
    list_display = ('file', 'pand')
    fields = ('file', 'pand')





# Panden opties

class PandAdmin(admin.ModelAdmin):
    list_display = ('user', 'fase', 'straat', 'postcode', 'stad', 'prijs', 'profiel_foto')
    fields = ('user', ('straat_naam', 'huis_nummer'), ('postcode', 'stad'), 'status', 'type', 'fase', 'prijs', 'beschrijving', 'profiel_foto')
    search_fields = ('fase__naam', 'postcode', 'stad')
    inlines = [ImageInlineAdmin, CriteriaInlineAdmin, EigenschapInlineAdmin, VerbruikInlineAdmin, WettelijkInlineAdmin, ReviewInlineAdmin]
    multiupload_form = True
    multiupload_list = False

    def admin_image(self):
        return '<img src="%s"/>' % self.img

    admin_image.allow_tags = True


class PandCriteriaAdmin(admin.ModelAdmin):
    list_display = ('pand', 'aantal', 'criteria')
    fields = ('pand', ('aantal', 'criteria'))
    search_fields = ('pand__postcode', 'pand__stad', 'criteria__naam')


class EigenschapAdmin(admin.ModelAdmin):
    list_display = ('naam', 'oppervlakte')
    fields = ('naam', ('oppervlakte', 'eenheid'))
    search_fields = ('naam', 'oppervlakte')


class PandEigenschapAdmin(admin.ModelAdmin):
    list_display = ('pand', 'eigenschap')
    search_fields = ('pand__postcode', 'pand__stad', 'eigenschap__naam')


class PandVerbruiksTypeAdmin(admin.ModelAdmin):
    list_display = ('pand', 'verbruik')
    search_fields = ('pand__postcode', 'pand__stad', 'verbruik__naam')


class PandWettelijkAdmin(admin.ModelAdmin):
    list_display = ('pand', 'wettelijk', 'jaartal')
    fields = ('pand', 'wettelijk', ('oppervlakte', 'eenheid'))
    search_fields = ('pand__postcode', 'pand__stad', 'wettelijk__naam')


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('review_naam', 'review_text')
    search_fields = ('review_naam',)


class PandReviewAdmin(admin.ModelAdmin):
    list_display = ('pand', 'review')
    search_fields = ('pand__postcode', 'pand__stad', 'review__review_naam')


class BezichtigingAdmin(admin.ModelAdmin):
    list_display = ('voornaam_bezoeker', 'achternaam_bezoeker')
    search_fields = ('voornaam_bezoeker', 'achternaam_bezoeker')


class PandBezichtigingAdmin(admin.ModelAdmin):
    list_display = ('pand', 'bezichtiging', 'bezichtigd')
    search_fields = (
    'pand__postcode', 'pand__stad', 'bezichtiging__voornaam_bezoeker', 'bezichtiging__achternaam_bezoeker')


class SupportticketAdmin(admin.ModelAdmin):
    list_display = ('user', 'titel', 'beschrijving', 'gemaakt')
    search_fields = ('titel',)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'locatie', 'geslacht')
    search_fields = ('locatie',)


# Register your models here.


admin.site.register(Image, ImageAdmin)

# ________USER( GURU )___________
admin.site.register(UserProfile, UserProfileAdmin)

# _________PAND___________
admin.site.register(Pand, PandAdmin)
admin.site.register(TypeHuis)
admin.site.register(Fase)
admin.site.register(Status)

# _______CRITERIAS_________
admin.site.register(Criteria)
admin.site.register(PandCriteria, PandCriteriaAdmin)

# ______EIGENSCAPPEN________
admin.site.register(Eigenschap, EigenschapAdmin)
admin.site.register(PandEigenschap, PandEigenschapAdmin)

# _________VERBRUIK______________
admin.site.register(VerbruiksType)
admin.site.register(PandVerbruiksType, PandVerbruiksTypeAdmin)

# ________WETTELIJK____________
admin.site.register(Wettelijk)
admin.site.register(PandWettelijk, PandWettelijkAdmin)

# _________REVIEWS______________
admin.site.register(Review, ReviewAdmin)
admin.site.register(PandReview, PandReviewAdmin)

# _______BEZICHTIGING__________
admin.site.register(Bezichtiging, BezichtigingAdmin)
admin.site.register(PandBezichtiging, PandBezichtigingAdmin)

# __________SUPPORT__________
admin.site.register(Supportticket, SupportticketAdmin)
