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

import logging

logger = logging.getLogger(__name__)


class ThreeDModelsView(BaseManagerView):

    def __init__(self):

        self.graph_types = {
            '36bcaff4-b82f-11e8-8598-0242ac120004': {
                'graph_type_name': 'three-d-hop',
                'display_name': '3D HOP'
            },
            '6ba5a68c-f58b-11e8-a354-0242ac120004': {
                'graph_type_name': 'sketchfab',
                'display_name': 'Sketchfab'
            }
        }

        self.images_nodegroup_ids = {
            'three-d-hop': '4b9b3314-d12f-11e8-85df-0242ac1a0004',
            'sketchfab': '6ba5aa06-f58b-11e8-a354-0242ac120004'
        }

        self.thumbnail_node_ids = {
            'three-d-hop': '4b9b3c7e-d12f-11e8-85df-0242ac1a0004',
            'sketchfab': '6ba5cea0-f58b-11e8-a354-0242ac120004'
        }

    def get(self, request):
        three_d_models = Resource.objects.filter(
            graph_id='36bcaff4-b82f-11e8-8598-0242ac120004') | Resource.objects.filter(graph_id='6ba5a68c-f58b-11e8-a354-0242ac120004')

        for three_d_model in three_d_models:

            try:
                graph_type = self.graph_types[str(three_d_model.graph_id)]
            except IndexError:
                logger.exception("View '{view_name}' not configured properly. Could not find graph type with id '{graph_id}'"
                                 .format(
                                     view_name=self.__class__.__name__,
                                     graph_id=str(three_d_model.graph_id)))
                continue

            graph_type_name = graph_type['graph_type_name']
            nodegroup_id = self.images_nodegroup_ids[graph_type_name] or None
            thumbnail_node_id = self.thumbnail_node_ids[graph_type_name] or None

            if not nodegroup_id or not thumbnail_node_id:
                continue

            images_tile = self.get_images_tile(three_d_model, nodegroup_id)
            if not images_tile:
                continue

            thumbnail_url = self.get_thumbnail_url(images_tile, thumbnail_node_id)
            if not thumbnail_url:
                continue

            three_d_model.thumbnail_url = thumbnail_url
            three_d_model.css_safe_type = graph_type['graph_type_name']
            three_d_model.type = graph_type['display_name']

        return render(request, 'views/three-d-models.htm', {'three_d_models': three_d_models})

    def get_images_tile(self, three_d_model, nodegroup_id):
        tiles = Tile.objects.filter(resourceinstance=three_d_model)
        try:
            return tiles.get(nodegroup_id=nodegroup_id)
        except Tile.DoesNotExist:
            None

    def get_thumbnail_url(self, images_tile, thumbnail_node_id):
        thumbnail_nodes = images_tile.data.get(thumbnail_node_id)
        if thumbnail_nodes:
            thumbnail_node = thumbnail_nodes[0] or None
            return thumbnail_node['url'] or None
        else:
            return None
