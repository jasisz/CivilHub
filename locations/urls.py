# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from ideas.views import IdeasListView, IdeasDetailView
from blog.views import NewsDetailView, NewsListView, NewsCreateView, NewsUpdateView
from topics.views import DiscussionDetailView
from polls.views import PollDetails, PollResults
from gallery.views import LocationGalleryView, PlacePictureView, \
                           LocationGalleryCreateView, location_gallery_delete, \
                           LocationGalleryUpdateView
from projects import views as project_views
import api
from locations.views import *
from staticpages.views import PageView

from rest.routers import HybridRouter
router = HybridRouter()
router.register('locations', api.LocationAPIViewSet, 'locations')
router.register('markers', api.LocationMapViewSet, 'markers')
router.register('actions', api.LocationActionsRestViewSet, 'actions')
router.register('sublocations', api.SublocationAPIViewSet, 'sublocations')
router.register('countries', api.CountryAPIViewSet, 'countries')
router.add_api_view('follow', url(r'^follow/', api.LocationFollowAPIView.as_view(), name='follow'))
router.add_api_view('contents', url(r'^contents/', api.LocationSummaryAPI.as_view(), name='contents'))
router.add_api_view('capital', url(r'^capital/', api.CapitalAPI.as_view(), name='capital'))

urlpatterns = patterns('',
    url(r'^create/', CreateLocationView.as_view(), name='create'),
    url(r'^places/', LocationListView.as_view(), name='index'),
    url(r'^(?P<slug>[\w-]+)/$', LocationDetailView.as_view(), name='details'),
    # lista sub-lokalizacji
    url(r'^(?P<slug>[\w-]+)/sublocations/$', SublocationList.as_view(), name='sublocations'),
    # wyszukiwanie treści w/g tagów
    url(r'^(?P<slug>[\w-]+)/search/(?P<tag>[\w-]+)$', LocationContentSearch.as_view(), name='tag_search'),
    url(r'^(?P<slug>[\w-]+)/search/$', LocationContentSearch.as_view(), name='tag_search_index'),
    # wyszukiwanie treści w/g kategorii
    url(r'^(?P<slug>[\w-]+)/filter/(?P<app>[\w-]+)/(?P<model>[\w-]+)/(?P<category>\d+)/$', LocationContentFilter.as_view(), name='category_search'),

    # POMYSŁY
    url(r'^(?P<slug>[\w-]+)/ideas/create/', LocationIdeaCreate.as_view(), name='new_idea'),
    url(r'^(?P<place_slug>[\w-]+)/ideas/(?P<slug>[\w-]+)/', IdeasDetailView.as_view(), name='idea_detail'),
    url(r'^(?P<location_slug>[\w-]+)/ideas/', IdeasListView.as_view(), name='ideas'),

    # BLOG
    url(r'^(?P<location_slug>[\w-]+)/news/create', NewsCreateView.as_view(), name='news_create'),
    url(r'^(?P<location_slug>[\w-]+)/news/(?P<slug>[\w-]+)/update/', NewsUpdateView.as_view(), name='news_update'),
    url(r'^(?P<location_slug>[\w-]+)/news/(?P<slug>[\w-]+)', NewsDetailView.as_view(), name='news_detail'),
    url(r'^(?P<location_slug>[\w-]+)/news/', NewsListView.as_view(), name='news'),

    # FORUM (dyskusje)
    url(r'^(?P<slug>[\w-]+)/discussion/create/', LocationDiscussionCreate.as_view(), name='new_topic'),
    url(r'^(?P<place_slug>[\w-]+)/discussion/(?P<slug>[\w-]+)/', DiscussionDetailView.as_view(), name='topic'),
    url(r'^(?P<slug>[\w-]+)/discussion/', LocationDiscussionsList.as_view(), name='discussions'),
    url(r'^(?P<slug>[\w-]+)/discussions/', ajax_discussion_list, name='ajaxlist'),
    #url(r'^(?P<slug>[\w-]+)/discussions/(?P<limit>[\w-]+)/', location_discussion_list, name='dsublist'),
    # Location polls (create, edit, delete etc. just for this location)
    url(r'^(?P<slug>[\w-]+)/polls/create/', LocationPollCreate.as_view(), name='new_poll'),
    url(r'^(?P<place_slug>[\w-]+)/polls/(?P<slug>[\w-]+)/results/', PollResults.as_view(), name='results'),
    url(r'^(?P<place_slug>[\w-]+)/polls/(?P<slug>[\w-]+)', PollDetails.as_view(), name='poll'),
    url(r'^(?P<slug>[\w-]+)/polls/', LocationPollsList.as_view(), name='polls'),
    # Location followers list
    url(r'^(?P<slug>[\w-]+)/followers/', LocationFollowersList.as_view(), name='followers'),
    # Delete content from location collections
    url(r'^remove_content/(?P<content_type>\d+)/(?P<object_pk>\d+)/', LocationContentDelete.as_view(), name='remove_content'),
    # Location media gallery
    url(r'^(?P<slug>[\w-]+)/gallery/upload/', LocationGalleryCreateView.as_view(), name='upload'),
    url(r'^(?P<slug>[\w-]+)/gallery/update/(?P<pk>\d+)/', LocationGalleryUpdateView.as_view(), name='gallery_update'),
    url(r'^(?P<slug>[\w-]+)/gallery/delete/(?P<pk>\d+)/', location_gallery_delete, name='remove_picture'),
    url(r'^(?P<slug>[\w-]+)/gallery/(?P<pk>\d+)/', PlacePictureView.as_view(), name='picture'),
    url(r'^(?P<slug>[\w-]+)/gallery/', LocationGalleryView.as_view(), name='gallery'),
    
    # PROJEKTY w ramach lokalizacji
    url(r'^(?P<location_slug>[\w-]+)/projects/create/', project_views.CreateProjectView.as_view(), name='project_create'),
    url(r'^(?P<location_slug>[\w-]+)/projects/(?P<slug>[\w-]+)/details/', project_views.ProjectSummaryView.as_view(), name='project_summary'),
    url(r'^(?P<location_slug>[\w-]+)/projects/(?P<slug>[\w-]+)/participants/', project_views.ProjectParticipantsView.as_view(), name='project_participants'),
    url(r'^(?P<location_slug>[\w-]+)/projects/(?P<slug>[\w-]+)/join/', project_views.JoinProjectView.as_view(), name='project_join'),
    url(r'^(?P<location_slug>[\w-]+)/projects/(?P<slug>[\w-]+)/group_create/', project_views.CreateTaskGroupView.as_view(), name='project_create_task_group'),
    url(r'^(?P<location_slug>[\w-]+)/projects/(?P<slug>[\w-]+)/group/(?P<group_id>\d+)/delete/', project_views.DeleteTaskGroupView.as_view(), name='project_delete_group'),
    url(r'^(?P<location_slug>[\w-]+)/projects/(?P<slug>[\w-]+)/group/(?P<group_id>\d+)/update/', project_views.UpdateTaskGroupView.as_view(), name='project_update_group'),
    url(r'^(?P<location_slug>[\w-]+)/projects/(?P<slug>[\w-]+)/group/(?P<group_id>\d+)/', project_views.CreateTaskView.as_view(), name='project_create_task'),
    url(r'^(?P<location_slug>[\w-]+)/projects/(?P<slug>[\w-]+)/update/', project_views.ProjectUpdateView.as_view(), name='project_update'),
    url(r'^(?P<location_slug>[\w-]+)/projects/(?P<slug>[\w-]+)/(?P<task_id>\d+)/delete/', project_views.DeleteTaskView.as_view(), name='task_delete'),
    url(r'^(?P<location_slug>[\w-]+)/projects/(?P<slug>[\w-]+)/(?P<task_id>\d+)/update/', project_views.UpdateTaskView.as_view(), name='task_update'),
    url(r'^(?P<location_slug>[\w-]+)/projects/(?P<slug>[\w-]+)/(?P<task_id>\d+)/join/', project_views.JoinTaskView.as_view(), name='task_join'),
    url(r'^(?P<location_slug>[\w-]+)/projects/(?P<slug>[\w-]+)/(?P<task_id>\d+)/', project_views.ProjectDetailView.as_view(), name='task_details'),
    url(r'^(?P<location_slug>[\w-]+)/projects/(?P<slug>[\w-]+)/', project_views.ProjectDetailView.as_view(), name='project_details'),
    url(r'^(?P<location_slug>[\w-]+)/projects/', project_views.ProjectListView.as_view(), name='project_list'),
    # Generic location views
    url(r'delete/(?P<slug>[\w-]+)/', DeleteLocationView.as_view(), name='delete'),
    url(r'update/(?P<slug>[\w-]+)/', UpdateLocationView.as_view(), name='update'),
    # Ajaxy functions - follow/unfollow location actions
    url(r'add_follower/(?P<pk>\d+)', add_follower, name='add_follower'),
    url(r'remove_follower/(?P<pk>\d+)', remove_follower, name='remove_follower'),
    #url(r'background/(?P<pk>\d+)', change_background, name='background'),
    url(r'background/(?P<pk>\d+)', LocationBackgroundView.as_view(), name='background'),
    # Ajaxy functions - invite other users to follow location.
    url(r'invite_users/(?P<pk>\d+)', InviteUsersView.as_view(), name='invite')
)
