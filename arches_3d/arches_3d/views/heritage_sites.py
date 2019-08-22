from collections import defaultdict
from django.views.generic import View
from django.shortcuts import render
from arches.app.views.base import BaseManagerView
from arches.app.models import models
from arches.app.models.resource import Resource
from arches.app.models.card import Card
from arches.app.models.graph import Graph
from arches.app.models.tile import Tile
from arches.app.utils.betterJSONSerializer import JSONSerializer

from arches_3d.models.viewmodels.portfolio_item import PortfolioItemViewModel

class HeritageSitesView(BaseManagerView):

    def get(self, request):
        sites = Resource.objects.filter(graph_id='fad0563b-b8f8-11e6-84a5-026d961c88e6')
        site_viewmodels = []

        for site in sites:
            site_viewmodel = PortfolioItemViewModel()
            tiles = Tile.objects.filter(resourceinstance=site)
            for tile in tiles:
                if str(tile.nodegroup_id) == 'a13a9486-d134-11e8-a039-0242ac1a0004':
                    if len(tile.data['a13a9cc4-d134-11e8-a039-0242ac1a0004']) > 0:
                        site_viewmodel.thumbnail_url = tile.data['a13a9cc4-d134-11e8-a039-0242ac1a0004'][0]['url'] or ''

                elif str(tile.nodegroup_id) == '709e4cf8-b12e-11e8-81d7-0242ac140004':
                    site_viewmodel.category_display_name = models.Value.objects \
                                        .get(pk=tile.data['709e5d74-b12e-11e8-81d7-0242ac140004']).value

            if site_viewmodel.category_display_name:
                site_viewmodel.category = site_viewmodel.category_display_name.replace(' ','-')
            else: 
                site_viewmodel.category = 'other'
                site_viewmodel.category_display_name = 'Other'

            site_viewmodel.display_name = site.displayname
            site_viewmodel.resource_instance_id = site.resourceinstanceid

            site_viewmodels.append(site_viewmodel)
 
        site_viewmodels.sort(key=lambda site: site.category)

        return render(request, 'views/heritage-sites.htm', { 'sites': site_viewmodels })
