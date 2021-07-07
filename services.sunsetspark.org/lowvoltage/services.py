import unicodedata

from . import custom_errors
from .models import (Account, FamilyMember, RelationshipType, Workshop,
                     WorkshopSignUp, WorkshopType, WorkshopWaitingList)


def create_account(name, email=None, phone=None):
    email_nfc = unicodedata.normalize("NFC", email)
    email_nfkc = unicodedata.normalize("NFKC", email)

    if Account.objects.filter(email_nfkc=email_nfkc).exists():
        raise custom_errors.EmailAlreadyExistsError()

    if phone and Account.objects.filter(phone=phone).exists():
        raise custom_errors.PhoneAlreadyExistsError()

    account = Account.objects.create_user_from_email(
        name=name, email=email, email_nfc=email_nfc, email_nfkc=email_nfkc
    )
    return account


def add_family_to_account(acct_model, name, rship, born_on):
    famm = FamilyMember(
        account=acct_model, name=name, account_relationship=rship, born_on=born_on
    )
    famm.save()
    return famm


def create_workshop(title, slug, description, starts_at, workshop_type, duration):
    wshop = Workshop(
        title=title,
        slug=slug,
        description=description,
        starts_at=starts_at,
        workshop_type=workshop_type,
        duration=duration,
    )
    wshop.save()
    return wshop


def signup_for_workshop(workshop_model, account_model, spots_req):
    signup = WorkshopSignUp(
        workshop=workshop_model,
        attending_acct=account_model,
        spots_requested=spots_req,
    )
    signup.save()
    return signup


def signup_for_workshop_waitlist(workshop_model, account_model, spots_req):
    waitlist = WorkshopWaitingList(
        workshop=workshop_model,
        waiting_acct=account_model,
        spots_requested=spots_req,
    )
    waitlist.save()
    return waitlist
