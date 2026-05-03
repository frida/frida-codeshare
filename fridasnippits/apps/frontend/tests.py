from django.test import TestCase
from django.urls import reverse

from fridasnippits.apps.frontend.models import Project, User


class NicknameUrlTests(TestCase):
    """Regression tests for issue #13: search 500s when an owner's Auth0
    nickname contains a dot (e.g. ``melanie.valentetransp``)."""

    def test_reverse_project_view_allows_dot_in_nickname(self):
        url = reverse(
            "project_view",
            kwargs={"nickname": "@melanie.valentetransp", "project_slug": "foo-bar"},
        )
        self.assertEqual(url, "/@melanie.valentetransp/foo-bar/")

    def test_reverse_user_info_view_allows_dot_in_nickname(self):
        url = reverse("user_info_view", kwargs={"nickname": "@lorenzo.difuccia"})
        self.assertEqual(url, "/@lorenzo.difuccia")


class SearchEndpointTests(TestCase):
    def test_search_with_dotted_nickname_owner(self):
        owner = User.objects.create(
            username="melanie.valentetransp", nickname="melanie.valentetransp"
        )
        Project.objects.create(
            owner=owner,
            project_name="Android SSL Bypass",
            project_source="// android",
            description="bypasses ssl on android",
            project_slug="android-ssl-bypass",
            hash="",
            latest_version="",
        )

        response = self.client.get("/search/", {"query": "android"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "/@melanie.valentetransp/android-ssl-bypass/")


class BrowsePaginationTests(TestCase):
    """Regression test for issue #9: browse paginated by ``-count`` only,
    so projects with tied like counts could appear on multiple pages on
    Postgres (which gives no ordering guarantee for ties under LIMIT/
    OFFSET). SQLite happens to be deterministic for ties so a behavioral
    test wouldn't catch it — instead, assert the queryset's ``ORDER BY``
    includes a unique tiebreaker."""

    def _browse_queryset(self):
        owner = User.objects.create(username="alice", nickname="alice")
        Project.objects.create(
            owner=owner,
            project_name="p",
            project_source="",
            description="",
            project_slug="p",
            hash="",
            latest_version="",
        )
        response = self.client.get("/browse")
        return response.context["projects"].paginator.object_list

    def test_browse_orders_by_unique_tiebreaker(self):
        order_by = self._browse_queryset().query.order_by
        self.assertIn(
            "id", [field.lstrip("-") for field in order_by],
            f"browse ORDER BY {order_by!r} lacks a unique tiebreaker; "
            "tied rows can appear on multiple pages on Postgres",
        )
