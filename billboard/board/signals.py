import time

from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.conf import settings
from celery import shared_task
from datetime import datetime, timedelta

from board.models import Advertisement, Feedback, Author


@shared_task
def printer2():
    time.sleep(3)
    print("Hello from signals!")


def send_notifications_new_comment(preview, pk, author):
    html_content = render_to_string("comment_created_email.html",
                                    {
                                        "text": preview,
                                        "link": f"{settings.SITE_URL}/board/{pk}",
                                    })

    msg = EmailMultiAlternatives(subject=f"New comment to yor advertisement",
                                 body="",
                                 from_email=settings.DEFAULT_FROM_EMAIL,
                                 to=author)

    msg.attach_alternative(html_content, "text/html")
    msg.send()


def send_notifications_comment_accepted(text, pk, author):
    html_content = render_to_string("comment_accepted_email.html",
                                    {
                                        "text": text,
                                        "link": f"{settings.SITE_URL}/board/{pk}",
                                    })

    msg = EmailMultiAlternatives(subject=f"You comment '{text}' is accepted",
                                 body=f"{text}",
                                 from_email=settings.DEFAULT_FROM_EMAIL,
                                 to=author)

    msg.attach_alternative(html_content, "text/html")
    msg.send()


@shared_task
def notify_about_new_comment(comment_pk: int, ad_pk: int, **kwargs):
    advertisement = Advertisement.objects.get(id=ad_pk)
    comment = Feedback.objects.get(id=comment_pk)
    recipient_list = [advertisement.author.user.email]
    send_notifications_new_comment(comment.text, comment.pk,  recipient_list)
    return True


@shared_task
def notify_about_comment_accepted(comment_pk: int, **kwargs):
    comment = Feedback.objects.get(id=comment_pk)
    user = comment.user
    advertisement = comment.advertisement
    recipient_list = [user.email]
    send_notifications_comment_accepted(comment.text, advertisement.pk, recipient_list)
    return True


# @shared_task
# def notify_about_ads_mon_8am():
#     today = datetime.now()
#     last_week = today - timedelta(days=7)
#     advertisements = Advertisement.objects.filter(date_time__gte=last_week)
#     categories = set(advertisements.values_list("category__name", flat=True))
#     subscribers = set(Category.objects.filter(name__in=categories).values_list("subscribers__email", flat=True))
#
#     html_content = render_to_string("daily_advertisements.html", {"link": settings.SITE_URL,
#                                                                   "advertisements": advertisements
#                                                                   }
#                                     )
#     msg = EmailMultiAlternatives(subject="ADs for a week",
#                                  body="",
#                                  from_email=settings.DEFAULT_FROM_EMAIL,
#                                  to=subscribers)
#
#     msg.attach_alternative(html_content, "text/html")
#     msg.send()
#     return True
