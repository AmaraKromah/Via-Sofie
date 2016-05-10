from __future__ import unicode_literals
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

decimal = RegexValidator(r'^[0-9]+(\.[0-9]{1,5})?$', 'Enkel decimalen toegelaten bv. 0.1')
alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Enkel alphanumerische waarden toegtelaten bv. abc123  .')
alphaChar = RegexValidator(r'^[a-zA-Z_ ]*$', 'Enkel letters toegelaten bv a-z,A-Z')



# _________________BEGIN GURU DOMEIN________________________

class UserProfile(models.Model):
    MY_CHOICES = (
        ('a', 'Man'),
        ('b', 'Vrouw'),
        ('c', 'Anders'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    locatie = models.CharField(max_length=140, blank=True)
    geslacht = models.CharField(max_length=1, choices=MY_CHOICES, blank=True)

    def __str__(self):
        return 'Naam : ' + str(self.user.username) + ' email: ' + str(self.user.email) + ' Locatie: ' + str(
            self.locatie) + ' Geslacht: ' + str(self.geslacht)

    def get_absolute_url(self):
        return '/profile/' + str(self.user.pk)

    @classmethod
    def create(cls, user, locatie, geslacht):
        profile = cls(user=user, locatie=locatie, geslacht=geslacht)
        profile.save()
        return profile


# ________________EINDE GURU DOMEIN ________________________

class TypeHuis(models.Model):
    class Meta:
        verbose_name_plural = "Type huizen"

    naam = models.CharField(max_length=65, validators=[alphaChar])

    def __str__(self):
        return self.naam


class Fase(models.Model):
    class Meta:
        verbose_name_plural = "Fases"

    naam = models.CharField(max_length=15)

    def __str__(self):
        return self.naam


class Status(models.Model):
    class Meta:
        verbose_name_plural = "Statussen"

    naam = models.CharField(max_length=65, validators=[alphaChar])

    def __str__(self):
        return self.naam


class Pand(models.Model):
    class Meta:
        verbose_name_plural = "Pand"
        ordering = ["user"]  # sorteren op users

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.ForeignKey(TypeHuis, on_delete=models.CASCADE)
    fase = models.ForeignKey(Fase, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    straat_naam = models.CharField(max_length=255, validators=[alphaChar])
    huis_nummer = models.IntegerField()
    stad = models.CharField(max_length=255, validators=[alphaChar])
    postcode = models.IntegerField()
    prijs = models.DecimalField(max_digits=16, decimal_places=2)
    beschrijving = models.TextField()
    hits = models.IntegerField(default=0)
    profiel_foto = models.FileField('Profiel_foto', upload_to='media/', default='')

    def straat(self):
        return u'%s %s' % (self.straat_naam, self.huis_nummer)
    straat.short_description = "straat"


    def fotos(self):
        alle_fotos = Image.objects.filter(pand=self)
        return alle_fotos

    def criteria(self):
        pand_criterias = PandCriteria.objects.filter(pand=self)
        return pand_criterias

    def eigenschappen(self):
        pand_eigenschappen = PandEigenschap.objects.filter(pand=self)
        return pand_eigenschappen

    def verbruiks_type(self):
        pand_verbruiks_type = PandVerbruiksType.objects.filter(pand=self)
        return pand_verbruiks_type

    def wettelijk(self):
        pand_wettelijk = PandWettelijk.objects.filter(pand=self)
        return pand_wettelijk

    def review(self):
        pand_review = PandReview.objects.filter(pand=self)
        return pand_review

    def __str__(self):
        return self.straat_naam + ' ' + str(self.huis_nummer) + ' ' + self.stad + ' ' + str(self.postcode) + '<img src="%s"/>' % self.profiel_foto


class Image(models.Model):
    file = models.FileField('File', upload_to='media/')
    pand = models.ForeignKey('Pand', related_name='images', blank=True, null=True)

    def __str__(self):
        return self.file.url


class Criteria(models.Model):
    class Meta:
        verbose_name_plural = "Criteria's"

    naam = models.CharField(max_length=255, validators=[alphaChar])

    def __str__(self):
        return self.naam


class PandCriteria(models.Model):
    class Meta:
        unique_together = ("pand", "criteria")
        verbose_name_plural = "Pand criteria's"

    pand = models.ForeignKey(Pand, on_delete=models.CASCADE)
    criteria = models.ForeignKey(Criteria, on_delete=models.CASCADE)
    aantal = models.SmallIntegerField(default=1)

    def __str__(self):
        return str(self.criteria)


class Eigenschap(models.Model):
    class Meta:
        verbose_name_plural = "Eigenschappen"

    naam = models.CharField(max_length=255, validators=[alphaChar])
    oppervlakte = models.CharField(blank=True, max_length=32, validators=[alphanumeric], default='0')
    eenheid = models.CharField(blank=True, max_length=10, default="M")

    def __str__(self):
        return self.naam


class PandEigenschap(models.Model):
    class Meta:
        verbose_name_plural = "Pand eigenschappen"

    pand = models.ForeignKey(Pand, on_delete=models.CASCADE)
    eigenschap = models.ForeignKey(Eigenschap, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.pand) + ' ' + str(self.eigenschap)


class VerbruiksType(models.Model):
    class Meta:
        verbose_name_plural = "Verbruikstypen"

    naam = models.CharField(max_length=255, validators=[alphaChar])

    def __str__(self):
        return self.naam


class PandVerbruiksType(models.Model):
    class Meta:
        verbose_name_plural = "Pand verbruikstypen"

    pand = models.ForeignKey(Pand, on_delete=models.CASCADE)
    verbruik = models.ForeignKey(VerbruiksType, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.pand) + ' met energievorm ' + str(self.verbruik)


class Wettelijk(models.Model):
    class Meta:
        verbose_name="wettelijke informatie"
        verbose_name_plural = "Wettelijke informaties"

    naam = models.CharField(max_length=255, validators=[alphaChar])

    def __str__(self):
        return self.naam


class PandWettelijk(models.Model):
    class Meta:
        verbose_name_plural = "Wettelijke informaties van panden"

    pand = models.ForeignKey(Pand, on_delete=models.CASCADE)
    wettelijk = models.ForeignKey(Wettelijk, on_delete=models.CASCADE, verbose_name="wettelijke informatie")
    oppervlakte = models.CharField(blank=True, max_length=32, validators=[decimal])
    eenheid = models.CharField(blank=True, max_length=10, default="M")
    jaartal = models.DateField()

    def __str__(self):
        return str(self.pand) + ' ' + str(self.wettelijk) + ' ' + str(self.jaartal)


class Review(models.Model):
    class Meta:
        verbose_name_plural = "Reviews"

    review_naam = models.CharField(max_length=255, validators=[alphaChar], verbose_name="Auteur")
    review_text = models.TextField(verbose_name="review")

    def __str__(self):
        return self.review_text+' |review door: '+self.review_naam


class PandReview(models.Model):
    class Meta:
        verbose_name_plural = "Pand reviews"

    pand = models.ForeignKey(Pand, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.pand) + ' ' + str(self.review)


class Bezichtiging(models.Model):
    class Meta:
        verbose_name_plural = "Bezichtigingen"

    voornaam_bezoeker = models.CharField(max_length=255, validators=[alphaChar], verbose_name="Voornaam")
    achternaam_bezoeker = models.CharField(max_length=255, validators=[alphaChar], verbose_name="Achternaam")

    def __str__(self):
        return self.achternaam_bezoeker + ' ' + self.voornaam_bezoeker


class PandBezichtiging(models.Model):
    class Meta:
        verbose_name_plural = "Pand bezichtigingen"
        unique_together = ("pand", "bezichtiging", "datum")  # kan toch niet dat een persoon dezelfde pand meermaals op dezelfde dag bezichtig ofwel?

    pand = models.ForeignKey(Pand, on_delete=models.CASCADE)
    bezichtiging = models.ForeignKey(Bezichtiging, on_delete=models.CASCADE)
    datum = models.DateField()

    def bezichtigd(self):
        return u'%s' % self.datum
    bezichtigd.short_description = "Bezichtigd op"

    def __str__(self):
        return str(self.bezichtiging) + ' ' + str(self.pand) + ' ' + str(self.datum)


class Supportticket(models.Model):
    class Meta:
        verbose_name_plural = "Supporttickets"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    titel = models.CharField(max_length=255)
    beschrijving = models.TextField()
    datum = models.DateField()

    def gemaakt(self):
        return u'%s' % self.datum
    gemaakt.short_description = "Gemaakt op"

    def __str__(self):
        return self.titel + ' ' + self.beschrijving + ' ' + str(self.datum)
