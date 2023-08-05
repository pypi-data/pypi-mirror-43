from rdflib import URIRef
from banal import ensure_list, ensure_dict, as_bool

from followthemoney.property import Property
from followthemoney.types import registry
from followthemoney.exc import InvalidData, InvalidModel
from followthemoney.util import gettext, NS


class Schema(object):
    """Defines the abstract data model.

    Schema items define the entities and links available in the model.
    """

    def __init__(self, model, name, data):
        self.model = model
        self.name = name
        self.data = data
        self._label = data.get('label', name)
        self._plural = data.get('plural', self.label)
        self._description = data.get('description')
        self.uri = URIRef(data.get('rdf', NS[name]))

        # Do not show in listings:
        self.abstract = as_bool(data.get('abstract'), False)

        # Try to perform fuzzy matching. Fuzzy similarity search does not
        # make sense for entities which have a lot of similar names, such
        # as land plots, assets etc.
        self.matchable = as_bool(data.get('matchable'), True)

        # Mark a set of properties as important, i.e. they should be shown
        # first, or in an abridged view of the entity.
        self.featured = ensure_list(data.get('featured'))

        # A transform of the entity into an edge for its representation in
        # the context of a property graph representation like Neo4J/Gephi.
        edge = data.get('edge', {})
        self.edge_source = edge.get('source')
        self.edge_target = edge.get('target')
        self.edge = self.edge_source and self.edge_target

        self.extends = set()
        self.schemata = set([self])
        self.names = set([self.name])
        self.descendants = set()
        self.properties = {}
        for name, prop in data.get('properties', {}).items():
            self.properties[name] = Property(self, name, prop)

    def generate(self):
        for parent in ensure_list(self.data.get('extends')):
            parent = self.model.get(parent)
            parent.generate()

            for name, prop in parent.properties.items():
                if name not in self.properties:
                    self.properties[name] = prop

            self.extends.add(parent)
            for ancestor in parent.schemata:
                self.schemata.add(ancestor)
                self.names.add(ancestor.name)
                ancestor.descendants.add(self)

        for prop in self.properties.values():
            prop.generate()

        for featured in self.featured:
            if self.get(featured) is None:
                raise InvalidModel("Missing featured property: %s" % featured)

        if self.edge:
            if self.get(self.edge_source) is None:
                msg = "Missing edge source: %s" % self.edge_source
                raise InvalidModel(msg)

            if self.get(self.edge_target) is None:
                msg = "Missing edge target: %s" % self.edge_target
                raise InvalidModel(msg)

    def _add_reverse(self, data, other):
        name = data.get('name', None)
        if name is None:
            raise InvalidModel("Unnamed reverse: %s" % other)

        prop = self.get(name)
        if prop is None:
            data.update({
                'type': registry.entity.name,
                'reverse': {'name': other.name},
                'range': other.schema.name,
                'stub': True
            })
            prop = Property(self, name, data)
            prop.generate()
            self.properties[name] = prop
        return prop

    @property
    def label(self):
        return gettext(self._label)

    @property
    def plural(self):
        return gettext(self._plural)

    @property
    def description(self):
        return gettext(self._description)

    @property
    def sorted_properties(self):
        return sorted(self.properties.values(),
                      key=lambda p: (not p.caption,
                                     p.name not in self.featured,
                                     p.label))

    @property
    def matchable_schemata(self):
        """The set of comparable types."""
        if not self.matchable:
            return
        # This is used by the cross-referencer to determine what
        # other schemata should be considered for matches. For
        # example, a Company may be compared to a Legal Entity,
        # but it makes no sense to compare it to an Aircraft.
        matchable = set(self.schemata)
        matchable.update(self.descendants)
        for schema in matchable:
            if schema.matchable:
                yield schema

    def is_a(self, parent):
        return parent in self.schemata

    def get(self, name):
        return self.properties.get(name)

    def validate(self, data):
        """Validate a dataset against the given schema.
        This will also drop keys which are not present as properties.
        """
        errors = {}
        properties = ensure_dict(data.get('properties'))
        for name, prop in self.properties.items():
            values = properties.get(name)
            error = prop.validate(values)
            if error is not None:
                errors[name] = error
        if len(errors):
            msg = gettext("Entity failed validation")
            raise InvalidData(msg, errors={'properties': errors})

    def to_dict(self):
        data = {
            'label': self.label,
            'plural': self.plural,
            'uri': str(self.uri),
            'schemata': self.names,
            'extends': [e.name for e in self.extends],
            'abstract': self.abstract,
            'matchable': self.matchable,
            'edge': {
                'source': self.edge_source,
                'target': self.edge_target,
            },
            'description': self.description,
            'featured': self.featured,
            'properties': {}
        }
        for name, prop in self.properties.items():
            data['properties'][name] = prop.to_dict()
        return data

    def __eq__(self, other):
        return hash(other) == hash(self)

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return '<Schema(%r)>' % self.name
