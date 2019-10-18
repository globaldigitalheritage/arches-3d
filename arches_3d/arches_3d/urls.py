from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from arches_3d.views import brochure
from arches_3d.views.auth import SignupView, ConfirmSignupView
from arches_3d.views import projects, heritage_sites, three_d_models, meta_data


urlpatterns = [
    url(r'^projects$', projects.ProjectsView.as_view(), name="projects"),
    url(r'^sites$', heritage_sites.HeritageSitesView.as_view(), name="sites"),
    url(r'^3d-models$', three_d_models.ThreeDModelsView.as_view(), name="three_d_models"),
    url(r'^node_values$', meta_data.get_node_values, name="node_values"),
    url(r'^team/', brochure.team, name='team'),
    url(r'^equipment/', brochure.equipment, name='equipment'),
    url(r'^news/', brochure.news, name='news'),
    url(r'^publications/', brochure.publications, name='publications'),
    url(r'^labs/', brochure.labs, name='labs'),
    url(r'^auth/signup$', SignupView.as_view(), name='signup'),
    url(r'^auth/confirm_signup$', ConfirmSignupView.as_view(), name='confirm_signup'),
    url(r'^', include('arches.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [ 
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
