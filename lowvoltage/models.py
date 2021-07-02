import uuid
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class AccountManager(UserManager):
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
    permissions. First name and last name were removed, email is no long
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
    username = models.CharField(max_length=50, blank=True, null=True, unique=True)
    name = models.CharField(blank=False, max_length=100)
    email = models.EmailField(_("email address"), unique=True)
    email_verified = models.BooleanField(default=False)
    phone = PhoneNumberField(blank=False, unique=True)
    phone_verified = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "name"]

    def __str__(self):
        return "{}".format(self.name)


# class AccountProfile(models.Model):
#     account = models.ForeignKey(Account, on_delete=models.CASCADE)


class RelativeType(models.TextChoices):
    CAREGIVER = "CG", _("caregiver")
    PARENT = "P", _("parent")
    GRAND_PARENT = "GP", _("grand parent")
    SIBLING = "S", _("sibling")
    COUSIN = "CZ", _("cousin")
    CHILD = "CH", _("child")


class FamilyMember(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    relationship = models.CharField(max_length=4, choices=RelativeType.choices)
    name = models.CharField(blank=False, max_length=48)
    born_on = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)


class WorkshopType(models.TextChoices):
    EDUCATOR = "ED", _("educator")
    FAMILY = "FAM", _("family")
    KID = "KID", _("kid")
    TEEN = "TEEN", _("teen")


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


class WorkshopSignUp(models.Model):
    event = models.ForeignKey(Workshop, on_delete=models.CASCADE)
    attending_acct = models.ForeignKey(Account, on_delete=models.CASCADE)
    spots_requests = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


class WorkshopWaitingList(models.Model):
    event = models.ForeignKey(Workshop, on_delete=models.CASCADE)
    waiting_acct = models.ForeignKey(Account, on_delete=models.CASCADE)
    spots_requests = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
