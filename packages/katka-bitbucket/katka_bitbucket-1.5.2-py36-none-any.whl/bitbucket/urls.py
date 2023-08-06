from django.urls import path

from . import views

app_name = 'katka_bitbucket'

urlpatterns = [
    path(
        'projects/',
        views.BitbucketProjectsView.as_view(),
        name='projects'
    ),
    path(
        'projects/<str:project_key>/repos/<str:repo_name>/',
        views.BitbucketRepoView.as_view(),
        name='repo'
    ),  # this one is here to define how the interface should look like -> it's not implemented yet
    path(
        'projects/<str:project_key>/repos/',
        views.BitbucketReposView.as_view(),
        name='repos'
    ),
    path(
        'projects/<str:project_key>/repos/<str:repository_name>/commits/',
        views.BitbucketCommitsView.as_view(),
        name='commits'
    )
]
