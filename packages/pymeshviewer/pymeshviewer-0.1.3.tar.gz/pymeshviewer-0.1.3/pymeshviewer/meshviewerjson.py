from datetime import datetime

from pymeshviewer.nodecollection import NodeCollection


class MeshviewerJSON(NodeCollection):
    def __init__(self, timestamp: datetime, nodes: list, links: list):
        """
        Constructor for a MeshviewerJSON object
        :param timestamp: timestamp of MeshviewerJSON
        :param nodes: list of nodes
        :param links: list of links
        """
        super().__init__(nodes)
        self.timestamp = timestamp
        self.nodes = nodes
        self.links = links
