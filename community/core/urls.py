"""URL configuration for the core application."""

from django.urls import path

from . import views


app_name = "core"

urlpatterns = [
    # Home
    path(
        "",
        views.HomeView.as_view(),
        name="home",
    ),

    # Blog
    path(
        "blog/",
        views.BlogPostListView.as_view(),
        name="blog-list",
    ),
    path(
        "blog/<slug:slug>/",
        views.BlogPostDetailView.as_view(),
        name="blogpost-detail",
    ),

    # Events
    path(
        "events/",
        views.EventListView.as_view(),
        name="event-list",
    ),
    path(
        "events/<slug:slug>/",
        views.EventDetailView.as_view(),
        name="event-detail",
    ),

    # Temples
    path(
        "temples/",
        views.TempleListView.as_view(),
        name="temple-list",
    ),

    path(
        "temples/<slug:slug>/",
            views.TempleDetailView.as_view(),
            name="temple-detail",
        ),

    # Request to join
    path(
        "join-a-community/",
        views.MemberRequestFormCreateView.as_view(),
        name="join-community",
    ),
    path(
        "join-a-community/success/",
        views.MemberRequestSuccessView.as_view(),
        name="join-community-success",
    ),
]
