from django.core.management.base import BaseCommand
from django.db.models import Count
from django.db.models.functions import Lower

from fridasnippits.apps.frontend.models import User


class Command(BaseCommand):
    help = "Delete users whose nickname collides with an earlier user's nickname."

    def handle(self, *args, **options):
        duplicate_nicknames = (
            User.objects.exclude(nickname__isnull=True)
            .annotate(nickname_lower=Lower("nickname"))
            .values("nickname_lower")
            .annotate(count=Count("id"))
            .filter(count__gt=1)
            .values_list("nickname_lower", flat=True)
        )

        for nickname_lower in duplicate_nicknames:
            collisions = list(
                User.objects.filter(nickname__iexact=nickname_lower).order_by("date_joined", "id")
            )
            keeper = collisions[0]
            for loser in collisions[1:]:
                self.stdout.write(
                    f"Deleting {loser.username} (nickname={loser.nickname!r}); kept {keeper.username}"
                )
                loser.delete()
