from __future__ import annotations

from typing import Any, Callable, Hashable
import collections
import itertools

from pypath_common import misc as _common

"""
Handling nodes of interest for network lookup queries.
"""

class Noi(collections.abc.Mapping):

    _DEFAULTS = {
        'id_type': 'uniprot',
        'entity_type': 'protein',
        'organism': 9606,
    }

    def __init__(
            self,
            noi: Noi | list[str] | list[list[str]] | dict[str, list[str]],
            groups: list[str] | dict[str, str] | None = None,
            id_type: str | None = 'uniprot',
            entity_type: str | None = 'protein',
            organism: int | str | None = 9606,
        ):
        """
        Nodes of interest.

        Args:
            noi:
                Nodes of interest, accepted notations are as follows:
                    - One string: one single node
                    - Iterable of strings: multiple nodes, grouping can be
                      specified by ``groups``
                    - Iterable of interables of strings: multiple groups of
                      nodes, group names can be specified by ``groups``
        """

        self._defaults = {
            'id_type': id_type,
            'entity_type': entity_type,
            'organism': organism,
        }
        self._setup(noi, groups)


    def _setup(
            self,
            noi: Noi | list[str] | list[list[str]] | dict[str, list[str]],
            groups: list[str] | dict[str, str] | None = None,
        ):

        self.nodes = self._parse(noi, groups)


    @staticmethod
    def _parse(
            noi: Noi | list[str] | list[list[str]] | dict[str, list[str]],
            groups: list[str] | dict[str, str] | None = None,
            id_type: str | None = 'uniprot',
            entity_type: str | None = 'protein',
            organism: int | str | None = 9606,
        ) -> dict[str, list[str]]:

        if isinstance(noi, Noi):

            return noi.nodes

        if isinstance(noi, dict):

            groups, noi = zip(*(
                (grp, n)
                for grp, nodes in noi.items()
                for n in nodes
            ))
            groups = list(groups)

        noi = [self._parse_node(n, locals()) for n in _common.to_list(noi)]

        if isinstance(groups, dict):

            groups = [groups[n] for n in noi]

        if isinstance(groups, list):

            if len(noi) != len(groups):

                raise ValueError('Nodes and groups are not the same length')

            _noi = collections.defaultdict(list)
            [_noi[g].append(n) for n, g in zip(noi, groups))]

            groups = dict(_noi)

        return groups or {'noi': noi}


    def _parse_node(
            self,
            node: str | Node | tuple | dict,
            attrs: dict,
        ) -> Node:

        return self.parse_node(node, self._defaults, attrs)


    @classmethod
    def parse_node(
            cls,
            node: str | Node | tuple | dict,
            *attrs: dict,
        ) -> Node:
        """
        Parse various node notations into Node object.

        Args:
            attrs:
                A series of dicts with node properties, from lowest to highest
                priority; elements with None values will be ignored.
        """

        if not isinstance(node, Node):

            if isinstance(node, str):

                node = (node,)

            if isinstance(node, tuple):

                node = dict(zip(Node._attrs, node))

            if isinstance(node, dict):

                attrs += (node,)

            _attrs = cls._DEFAULTS.copy()

            for a in attrs:

                _attrs.update({
                    k: v
                    for k, v in (a or {}).items()
                    if k in cls._DEFAULTS and v
                })

            if 'identifier' not in _attrs:

                raise ValueError(
                    'Nodes must have identifiers. '
                    f'Could not find identifier for `{node}`.',
                )

            node = Node(**_attrs)

        return node


    def __getitem__(self, key: Hashable) -> Any:

        return self.nodes[key]


    def __iter__(self):

        return self.nodes.__iter__()


    def __len__(self) -> int:

        return len(self.nodes)


    def __delitem__(self, key: Hashable):

        del self.nodes[key]


    def __setitem__(self, key: Hashable, value: Any):

        self.nodes[key] = value


    def as_idtype(self, id_type: str, entity_type: str = 'protein') -> Noi:
        """
        Translate nodes to a certain ID type.

        The translation applies to one entity type in one call, the rest of
        the nodes will be included unchanged.
        """

        return self.apply(
            lambda n: n.as_idtype(id_type),
            entity_type = entity_type,
        )


    def as_organism(
            self,
            organism: str | int = 10090,
            source_organism: str | int = 9606,
        ) -> Noi:
        """
        Translate nodes to a certain ID type.

        The translation applies to one entity type in one call, the rest of
        the nodes will be included unchanged.
        """

        return self.apply(
            lambda n: n.as_idtype(id_type),
            entity_type = entity_type,
        )


    def apply(self, proc: Callable, *args, **kwargs) -> Noi:
        """
        Apply a certain processing step to all matching nodes.

        Non matching nodes will be included unchanged.
        """

        return Noi(
            {
                grp: list(itertools.chain(*(
                    proc(n) if n.match(*args, **kwargs) else (n,)
                    for n in nodes
                )))
                for grp, nodes in self.nodes.items()
            }
        )


    def keep(self, *args, **kwargs) -> Noi:
        """
        Keep only matching nodes.
        """

        return self._filter(_common.identity, *args, **kwargs)


    def drop(self, *args, **kwargs) -> Noi:
        """
        Drop matching nodes.
        """

        return self._filter(_common.negate, *args, **kwargs)


    def _filter(self, op: Callable, *args, **kwargs) -> Noi:

        return Noi({
            grp: [n for n in nodes if op(n.match(*args, **kwargs))]
            for grp, nodes in self.nodes.items()
        })
