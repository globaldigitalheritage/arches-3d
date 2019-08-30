from arches.app.views.base import BaseManagerView
from arches.app.models.tile import Tile

class BaseView(BaseManagerView):

    def get_nodegroup_from_resource_instance(self, resource_instance, nodegroup_id):
        tiles = Tile.objects.filter(resourceinstance=resource_instance)
        try:
            return tiles.get(nodegroup_id=nodegroup_id)
        except Tile.DoesNotExist:
            return None

    def get_thumbnail_url(self, images_tile, thumbnail_node_id):
        try:
            thumbnail_nodes = images_tile.data.get(thumbnail_node_id)
            if thumbnail_nodes:
                thumbnail_node = thumbnail_nodes[0] or None
                return thumbnail_node['url'] or None
        except AttributeError:
            pass

        return None