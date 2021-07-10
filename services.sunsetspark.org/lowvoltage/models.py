import uuid
from datetime import datetime, timedelta

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class AccountManager(UserManager):
    def create_user_from_email(
        self, name, email, email_nfkc, email_nfc, **extra_fields
    ):
        """
        Creates a user with just email address and name
        """
        return self.create_user(
            name=name,
            email=email,
            email_nfkc=email_nfkc,
            email_nfc=email_nfc,
            **extra_fields
        )

    def create_user_from_phone(self, name, phone, **extra_fields):
        return self.create_user(name=name, phone=phone)

    def create_user(self, email=None, password=None, name=None, **extra_fields):
        return super().create_user(
            username=uuid.uuid4(),
            email=email,
            password=password,
            name=name,
            **extra_fields
        )

    def create_superuser(self, email=None, password=None, name=None, **extra_fields):
        return super().create_superuser(
            username=uuid.uuid4(),
            email=email,
            password=password,
            name=name,
            **extra_fields
        )


class AbstractAccount(AbstractBaseUser, PermissionsMixin):
    """
    This model is copied from django's default user to retain admin-compliant
    permissions. First name and last name were removed, email is no longer
    required, and username is a uuid.

    Password are required. Other fields are optional.

    Do not change this code unless it is to reflect a change made in
    django's AbstractUser.
    """

    username = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_("email address"), blank=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = AccountManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"

    class Meta:
        verbose_name = _("account")
        verbose_name_plural = _("accounts")
        abstract = True

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Account(AbstractAccount):
    """
    This is the primary account model. Do not modify the abstract account model.
    """

    username = models.CharField(max_length=50, blank=True, null=True, unique=True)
    name = models.CharField(_("email address"), blank=False, max_length=100)

    email = models.EmailField(_("email address"), unique=True)
    email_verified = models.BooleanField(default=False)
    email_nfkc = models.EmailField(unique=True, null=True, blank=True)
    email_nfc = models.EmailField(unique=True, null=True, blank=True)

    phone = PhoneNumberField(unique=True, null=True, blank=True)
    phone_verified = models.BooleanField(default=False)

    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return "{}".format(self.name)

    def get_absolute_url(self):
        return reverse("account-detail")


# class AccountProfile(models.Model):
#     account = models.ForeignKey(Account, on_delete=models.CASCADE)


class RelationshipType(models.TextChoices):
    CAREGIVER = "CG", _("caregiver")
    PARENT = "P", _("parent")
    GRAND_PARENT = "GP", _("grand parent")
    SIBLING = "S", _("sibling")
    COUSIN = "CZ", _("cousin")
    AUNTUNCLE = "AU", _("aunt / uncle")


class FamilyMember(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    account_relationship = models.CharField(max_length=4, choices=RelationshipType.choices)
    name = models.CharField(blank=False, max_length=48)
    born_on = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} ({}'s {})".format(
            self.name, self.account.name, self.reverse_relationship
        )

    @property
    def reverse_relationship(self):
        """
        Returns a string with the expressing the relationship
        in terms of the account owner.
        """
        if self.account_relationship == RelationshipType.CAREGIVER:
            return _("child")
        elif self.account_relationship == RelationshipType.PARENT:
            return _("child")
        elif self.account_relationship == RelationshipType.GRAND_PARENT:
            return _("grandchild")
        elif self.account_relationship == RelationshipType.SIBLING:
            return _("sibling")
        elif self.account_relationship == RelationshipType.COUSIN:
            return _("cousin")
        elif self.account_relationship == RelationshipType.AUNTUNCLE:
            return _("niece / nephew")


class WorkshopType(models.TextChoices):
    EDUCATOR = "ED", _("educator")
    FAMILY = "FAM", _("family")
    KID = "KID", _("kid")
    TEEN = "TEEN", _("teen")


class WorkshopManager(models.Manager):
    def upcoming_workshops(self):
        return self.filter(is_published=False, starts_at__gte=datetime.now()).order_by('starts_at')


class Workshop(models.Model):
    title = models.CharField(blank=False, max_length=100)
    slug = models.SlugField(blank=False)
    description = models.CharField(blank=False, max_length=1000)
    starts_at = models.DateTimeField()
    workshop_type = models.CharField(max_length=5, choices=WorkshopType.choices)
    duration = models.DurationField()
    max_sign_up = models.PositiveSmallIntegerField(null=True)
    is_published = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = WorkshopManager()

    def __str__(self):
        return "{}".format(self.title)

    def get_absolute_url(self):
        return reverse("workshop-detail", kwargs={"slug": self.slug})

    @property
    def week(self):
        start_of_week = self.starts_at - timedelta(days=self.starts_at.weekday(), hours=self.starts_at.hour, minutes=self.starts_at.minute)
        return start_of_week

    @property
    def ends_at(self):
        return self.starts_at + self.duration


class WorkshopSignUp(models.Model):
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE)
    attending_acct = models.ForeignKey(Account, on_delete=models.CASCADE)
    spots_requested = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} spots for {}".format(self.spots_requested, self.attending_acct.name)


class WorkshopWaitingList(models.Model):
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE)
    waiting_acct = models.ForeignKey(Account, on_delete=models.CASCADE)
    spots_requested = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} spots for {}".format(self.spots_requested, self.attenting_acct.name)
