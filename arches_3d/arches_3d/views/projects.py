from django.views.generic import View
from django.shortcuts import render
from arches.app.views.base import BaseManagerView
from arches.app.models import models
from arches.app.models.resource import Resource
from arches.app.models.card import Card
from arches.app.models.graph import Graph
from arches.app.models.tile import Tile
from arches.app.utils.betterJSONSerializer import JSONSerializer

class ProjectsView(BaseManagerView):

    def get(self, request):
        projects = Resource.objects.filter(graph_id='243f8689-b8f6-11e6-84a5-026d961c88e6')

        for project in projects:

            tiles = Tile.objects.filter(resourceinstance=project).order_by('sortorder')

            for tile in tiles:
                if str(tile.nodegroup_id) == 'fb0c163e-d138-11e8-814d-0242ac1a0004':
                    if len(tile.data['fb0c1e72-d138-11e8-814d-0242ac1a0004']) > 0:
                        project.thumbnail_url = tile.data['fb0c1e72-d138-11e8-814d-0242ac1a0004'][0]['url']
                elif str(tile.nodegroup_id) == 'aee32ff0-af95-11e8-b710-0242ac120005': 
                    project.description = tile.data['aee33842-af95-11e8-b710-0242ac120005'] or ''

                if hasattr(project, 'country'):
                    project.css_safe_country = project.country.replace(' ','-')
                else: 
                    project.css_safe_country = 'other'
                    project.country = 'Other'

        return render(request, 'views/projects.htm', { 'projects': projects })