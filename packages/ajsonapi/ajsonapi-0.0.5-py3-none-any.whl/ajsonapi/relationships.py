# Copyright © 2018-2019 Roel van der Goot
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
"""Module relationships provides relationship classes."""

from abc import ABC, abstractmethod

from ajsonapi.conversions import id_number_to_name


class Relationship(ABC):
    """Abstract base class for all relationships between resources.
    """

    # pylint: disable=too-few-public-methods

    def __init__(self, rtable):
        self.rtable = rtable
        self.table = None  # Overridden in Table.__init_subclass__
        self.name = None  # Overridden in Table.__init_subclass__
        self.reverse = None  # Overridden in Table.__init_subclass__
        self.collection = None  # Overriden in Table.__init_subclass__

    @abstractmethod
    def is_reverse(self, other):
        """Detects whether relationships are each other's reverse.

        Args:
            other: A Relationship instance.

        Returns:
           True if self and other are each other's reverse relationship, False
           otherwise.
        """


class LocalRelationship(Relationship):
    """A relationship with a local foreign key."""

    def __init__(self, rtable, lfkey):
        super().__init__(rtable)
        self.lfkey = lfkey

    @abstractmethod
    def is_reverse(self, other):
        pass

    def sql(self):
        """Produces the SQL column definition for the local foreign key of
        this object.

        Returns:
            A string containing the SQL column definition for the local
            foreign key of this object.
        """

        return f'{self.lfkey} UUID'

    def __str__(self):
        return self.lfkey


class OneToOneLocalRelationship(LocalRelationship):
    """A one-to-one relationship between resources with a local foreign key.
    """

    def is_reverse(self, other):
        return (isinstance(other, OneToOneRemoteRelationship) and
                other.table and self.rtable and
                other.table.name == self.rtable.name and other.rtable and
                self.table and other.rtable.name == self.table.name and
                other.rfkey == self.lfkey)

    def sql_constraints(self):
        """Returns the SQL unique and foreign key constraints for this
        OneToOneLocalRelationship.
        """

        return (f'UNIQUE ({self.lfkey}),\n'
                f'FOREIGN KEY ({self.lfkey}) REFERENCES {self.rtable.name}(id)')


class OneToOneRemoteRelationship(Relationship):
    """A one-to-one relationship between resources with a remote foreign key.
    """

    def __init__(self, rtable, rfkey):
        super().__init__(rtable)
        self.rfkey = rfkey

    def is_reverse(self, other):
        return (isinstance(other, OneToOneLocalRelationship) and other.table and
                self.rtable and other.table.name == self.rtable.name and
                other.rtable and self.table and
                other.rtable.name == self.table.name and
                other.lfkey == self.rfkey)

    async def get_collection_data(self, env):
        """Creates the response data member for OneToOneRemoteRelationships.

        Specifically, after this call the environment's data_by_lid member is
        updated with something like the following:

        env.data_by_lid = {
            1: {
                'relationships': {
                    'one_one_remote': {
                        'data': {
                            'type': 'one_one_remotes',
                            'id': UUID_21,
                        },
                        'links': {
                            'self': '/centers/1/relationships/one_one_remote',
                            'related': '/centers/1/one_one_remote',
                        },
                    },
                },
            },
            2: {
                ...,
            },
            ...
        }
        """
        stmt = (f'SELECT {self.rfkey}, id '
                f'FROM {self.rtable.name} '
                f'WHERE {self.rfkey} IS NOT NULL;')
        async with env.lock:
            records = await env.connection.fetch(stmt)
        await env.event.wait()
        rid_by_lid = {record[self.rfkey]: record['id'] for record in records}
        for lid, data in env.data_by_lid.items():
            if lid in rid_by_lid:
                relationship_data = {
                    'type': self.reverse.collection.name,
                    'id': id_number_to_name(rid_by_lid[lid]),
                }
            else:
                relationship_data = None
            data.setdefault('relationships', {})[self.name] = {
                'data': relationship_data,
                'links': {
                    'self': (f'/{self.collection.name}/{lid}/relationships/'
                             f'{self.name}'),
                    'related': (f'/{self.collection.name}/{lid}/'
                                f'{self.name}'),
                },
            }

    async def get_object_data(self, env):
        """Creates the response data member for OneToOneRemoteRelationships.

        Specifically, after this call the environment's data member is updated
        with something like the following:

        env.data = {
            'relationships': {
                'one_one_remote': {
                    'data': {
                        'type': 'one_one_remotes',
                        'id': UUID_21,
                    },
                    'links': {
                        'self': '/centers/1/relationships/one_one_remote',
                        'related': '/centers/1/one_one_remote',
                    },
                },
            },
        }
        """
        stmt = (f"SELECT id "
                f"FROM {self.rtable.name} "
                f"WHERE {self.rfkey} = $1;")
        async with env.lock:
            record = await env.connection.fetchrow(stmt, env.obj.id.number)
        await env.event.wait()
        if record:
            rel_data = {
                'type': self.reverse.collection.name,
                'id': record['id'],
            }
        else:
            rel_data = None
        env.data['relationships'][self.name] = {
            'data': rel_data,
            'links': {
                'self': (f'/{self.collection.name}/{env.obj.id.name}/'
                         f'relationships/{self.name}'),
                'related': (f'/{self.collection.name}/{env.obj.id.name}/'
                            f'{self.name}'),
            },
        }

    async def get_to_one_related_data(self, env):
        """Creates the response data member for OneToOneRemoteRelationships.

        Specifically, after this call the environment's data member is updated
        with something like the following:

        env.data = {
            'relationships': {
                'one_one_remote': {
                    'data': {
                        'type': 'one_one_remotes',
                        'id': UUID_21,
                        'attributes': {
                            ...
                        },
                        'relationships': {
                            ...
                        },
                    },
                    'links': {
                        'self': '/one_one_remotes/UUID_21',
                    },
                },
            },
        }
        """
        if isinstance(env.related.relationship, LocalRelationship):
            # OneToOneLocalRelationship or ManyToOneLocalRelationship
            stmt = (f'SELECT id '
                    f'FROM {self.rtable.name} '
                    f'WHERE {self.rfkey} IN ('
                    f' SELECT {env.related.relationship.lfkey}'
                    f' FROM {env.related.table.name}'
                    f' WHERE id = $1)')
        else:  # OneToOneRemoteRelationship
            stmt = (f'SELECT id '
                    f'FROM {self.rtable.name} '
                    f'WHERE {self.rfkey} IN ('
                    f' SELECT id'
                    f' FROM {env.related.relationship.rtable.name}'
                    f' WHERE {env.related.relationship.rfkey} = $1)')
        async with env.lock:
            record = await env.connection.fetchrow(stmt, env.related.id.number)
        await env.event.wait()
        if env.data is None:
            return
        if record:
            rel_data = {
                'type': self.reverse.collection.name,
                'id': id_number_to_name(record[0]),
            }
        else:
            rel_data = None
        env.data.setdefault('relationships', {})[self.name] = {
            'data': rel_data,
            'links': {
                'self': (f'/{env.related.relationship.collection.name}/'
                         f'{env.related.id.name}')
            },
        }

    async def get_to_many_related_data(self, env):
        """Creates the response data member for OneToOneRemoteRelationships.

        Specifically, after this call the environment's data member is updated
        with something like the following:

        env.data = {
            'relationships': {
                'one_one_remote': {
                    'data': {
                        'type': 'one_one_remotes',
                        'id': UUID_21,
                        'attributes': {
                            ...
                        },
                        'relationships': {
                            ...
                        },
                    },
                    'links': {
                        'self': '/one_one_remotes/UUID_21',
                    },
                },
            },
        }
        """
        if isinstance(env.related.relationship, ManyToManyRelationship):
            stmt = (f'SELECT {self.rfkey}, id '
                    f'FROM {self.rtable.name} '
                    f'WHERE {self.rfkey} IN ('
                    f' SELECT {env.related.relationship.rafkey}'
                    f' FROM {env.related.relationship.atable.name}'
                    f' WHERE {env.related.relationship.lafkey} = $1)')
        else:  # OneToManyRelationship
            stmt = (f'SELECT {self.rfkey}, id '
                    f'FROM {self.rtable.name} '
                    f'WHERE {self.rfkey} IN ('
                    f' SELECT id'
                    f' FROM {env.related.relationship.rtable.name}'
                    f' WHERE {env.related.relationship.rfkey} = $1)')
        async with env.lock:
            records = await env.connection.fetch(stmt, env.related.id.number)
        await env.event.wait()
        rids_by_lid = {}
        for record in records:
            rids_by_lid.setdefault(record[0], []).append(record[1])
        for lid, data in env.data_by_lid.items():
            if lid in rids_by_lid:
                rids = rids_by_lid[lid]
                assert len(rids) == 1
                relationship_data = {
                    'type': self.reverse.collection.name,
                    'id': id_number_to_name(rids[0]),
                }
            else:
                relationship_data = None
            data.setdefault('relationships', {})[self.name] = {
                'data': relationship_data,
                'links': {
                    'self': (f'/{env.related.relationship.collection.name}/'
                             f'{env.related.id.name}')
                },
            }


class OneToManyRelationship(Relationship):
    """A one-to-many relationship between resources."""

    def __init__(self, rtable, rfkey):
        super().__init__(rtable)
        self.rfkey = rfkey

    def is_reverse(self, other):
        return (isinstance(other, ManyToOneRelationship) and other.table and
                self.rtable and other.table.name == self.rtable.name and
                other.rtable and self.table and
                other.rtable.name == self.table.name and
                other.lfkey == self.rfkey)

    async def get_collection_data(self, env):
        """Creates the response data member for OneToManyRelationships.

        Specifically, after this call the environment's data_by_lid member is
        updated with something like the following:

        env.data_by_lid = {
            1: {
                'relationships': {
                    'one_manys': {
                        'data': [
                            {
                                'type': 'one_manys',
                                'id': UUID_41,
                            },
                            ...
                        ],
                        'links': {
                            'self': '/centers/1/relationships/one_manys',
                            'related': '/centers/1/one_manys',
                        },
                    },
                },
            },
            2: {
                ...,
            },
            ...
        }
        """
        stmt = (f'SELECT {self.rfkey}, id '
                f'FROM {self.rtable.name} '
                f'WHERE {self.rfkey} IS NOT NULL')
        async with env.lock:
            records = await env.connection.fetch(stmt)
        await env.event.wait()
        rids_by_lid = {}
        for record in records:
            rids_by_lid.setdefault(record[self.rfkey], []).append(record['id'])
        for lid, data in env.data_by_lid.items():
            if lid in rids_by_lid:
                relationship_data = [{
                    'type': self.reverse.collection.name,
                    'id': id_number_to_name(rid),
                } for rid in rids_by_lid[lid]]
            else:
                relationship_data = []
            data.setdefault('relationships', {})[self.name] = {
                'data': relationship_data,
                'links': {
                    'self': (f'/{self.collection.name}/{lid}/relationsihps/'
                             f'{self.name}'),
                    'related': (f'/{self.collection.name}/{lid}/'
                                f'{self.name}'),
                }
            }

    async def get_object_data(self, env):
        """Creates the response data member for OneToManyRelationships.

        Specifically, after this call the environment's data member is updated
        with something like the following:

        env.data = {
            'relationships': {
                'one_manys': {
                    'data': [
                        {
                            'type': 'one_manys',
                            'id': UUID_41,
                        },
                        ...
                    ],
                    'links': {
                        'self': '/centers/1/relationships/one_manys',
                        'related': '/centers/1/one_manys',
                    },
                },
            },
        }
        """
        lfkey_name = self.rfkey
        stmt = (f"SELECT id "
                f"FROM {self.rtable.name} "
                f"WHERE {lfkey_name} = $1;")
        async with env.lock:
            records = await env.connection.fetch(stmt, env.obj.id.number)
        await env.event.wait()
        rids = [record['id'] for record in records]
        env.data['relationships'][self.name] = {
            'data': [{
                'type': self.reverse.collection.name,
                'id': id_number_to_name(rid),
            } for rid in rids],
            'links': {
                'self': (f'/{self.collection.name}/{env.obj.id.name}/'
                         f'relationships/{self.name}'),
                'related': (f'/{self.collection.name}/{env.obj.id.name}/'
                            f'{self.name}'),
            },
        }

    async def get_to_one_related_data(self, env):
        """Creates the response data member for OneToManyRelationships.

        Specifically, after this call the environment's data member is updated
        with something like the following:

        env.data = {
            'relationships': {
                'one_manys': {
                    'data': [{
                        'type': 'one_manys',
                        'id': UUID_41,
                        'attributes': {
                            ...
                        },
                        'relationships': {
                            ...
                        },
                    },
                    ...
                    ],
                    'links': {
                        'self': '/one_manys/UUID_41',
                    },
                },
            },
        }
        """
        if isinstance(env.related.relationship, LocalRelationship):
            # OneToOneLocalRelationship or ManyToOneRelationship
            stmt = (f'SELECT id '
                    f'FROM {self.rtable.name} '
                    f'WHERE {self.rfkey} IN ('
                    f' SELECT {env.related.relationship.lfkey}'
                    f' FROM {env.related.table.name}'
                    f' WHERE id = $1)')
        else:  # OneToOneRemoteRelationship
            stmt = (f'SELECT id '
                    f'FROM {self.rtable.name} '
                    f'WHERE {self.rfkey} IN ('
                    f' SELECT id'
                    f' FROM {env.related.relationship.rtable.name}'
                    f' WHERE {env.related.relationship.rfkey} = $1)')
        async with env.lock:
            record = await env.connection.fetchrow(stmt, env.related.id.number)
        await env.event.wait()
        if env.data is None:
            return
        if record is not None:
            rel_data = [{'type': self.rtable.collection.name, 'id': record[0]}]
        else:
            rel_data = []
        env.data.setdefault('relationships', {})[self.name] = {
            'data': rel_data,
            'links': {
                'self': f'/{self.rtable.collection.name}/{env.related.id.name}'
            },
        }

    async def get_to_many_related_data(self, env):
        """Creates the response data member for OneToManyRelationships.

        Specifically, after this call the environment's data member is updated
        with something like the following:

        env.data = {
            'relationships': {
                'one_manys': {
                    'data': [{
                        'type': 'one_manys',
                        'id': UUID_41,
                        'attributes': {
                            ...
                        },
                        'relationships': {
                            ...
                        },
                    },
                    ...
                    ],
                    'links': {
                        'self': '/one_manys/UUID_41',
                    },
                },
            },
        }
        """
        if isinstance(env.related.relationship, ManyToManyRelationship):
            stmt = (f'SELECT {self.rfkey}, id '
                    f'FROM {self.rtable.name} '
                    f'WHERE {self.rfkey} IN ('
                    f' SELECT {env.related.relationship.rafkey}'
                    f' FROM {env.related.relationship.atable.name}'
                    f' WHERE {env.related.relationship.lafkey} = $1)')
        else:  # OneToManyRelationship
            stmt = (f'SELECT {self.rfkey}, id '
                    f'FROM {self.rtable.name} '
                    f'WHERE {self.rfkey} IN ('
                    f' SELECT id'
                    f' FROM {env.related.relationship.rtable.name}'
                    f' WHERE {env.related.relationship.rfkey} = $1)')
        async with env.lock:
            records = await env.connection.fetch(stmt, env.related.id.number)
        await env.event.wait()
        rids_by_lid = {}
        for record in records:
            rids_by_lid.setdefault(record[0], []).append(record[1])
        for lid, data in env.data_by_lid.items():
            if lid in rids_by_lid:
                relationship_data = [{
                    'type': self.reverse.collection.name,
                    'id': id_number_to_name(rid),
                } for rid in rids_by_lid[lid]]
            else:
                relationship_data = []
            data.setdefault('relationships', {})[self.name] = {
                'data': relationship_data,
                'links': {
                    'self': (f'/{self.collection.name}/{lid}/'
                             f'relationships/{self.name}'),
                    'related': (f'/{self.collection.name}/{lid}/'
                                f'{self.name}'),
                },
            }


class ManyToOneRelationship(LocalRelationship):
    """A many-to-one relationship between resources."""

    def is_reverse(self, other):
        return (isinstance(other, OneToManyRelationship) and other.table and
                self.rtable and other.table.name == self.rtable.name and
                not isinstance(other.rtable, str) and self.table and
                other.rtable.name == self.table.name and
                other.rfkey == self.lfkey)

    def sql_constraints(self):
        """Returns the SQL foreign key constraint for this
        ManyToOneRelationship.
        """

        return f'FOREIGN KEY ({self.lfkey}) REFERENCES {self.rtable.name}(id)'


class ManyToManyRelationship(Relationship):
    """A many-to-many relationship between resources."""

    def __init__(self, rtable, atable, lafkey, rafkey):
        # pylint: disable=too-many-arguments
        super().__init__(rtable)
        self.atable = atable
        self.lafkey = lafkey
        self.rafkey = rafkey

    def is_reverse(self, other):
        return (isinstance(other, ManyToManyRelationship) and other.table and
                self.rtable and other.table.name == self.rtable.name and
                other.rtable and self.table and
                other.rtable.name == self.table.name and
                other.atable == self.atable and other.lafkey == self.rafkey and
                other.rafkey == self.lafkey)

    async def get_collection_data(self, env):
        """Creates the response data member for ManyToManyRelationships.

        Specifically, after this call the environment's data_by_lid member is
        updated with something like the following:

        env.data_by_lid = {
            1: {
                'relationships': {
                    'many_manys': {
                        'data': [
                            {
                                'type': 'many_manys',
                                'id': UUID_51,
                            },
                            ...
                        ],
                        'links': {
                            'self': '/centers/1/relationships/many_manys',
                            'related': '/centers/1/many_manys',
                        },
                    },
                },
            },
            2: {
                ...,
            },
            ...
        }
        """
        stmt = (f'SELECT {self.lafkey}, {self.rafkey} '
                f'FROM {self.atable.name};')
        async with env.lock:
            records = await env.connection.fetch(stmt)
        await env.event.wait()
        rids_by_lid = {}
        for record in records:
            rids_by_lid.setdefault(record[self.lafkey],
                                   []).append(record[self.rafkey])
        for lid, data in env.data_by_lid.items():
            if lid in rids_by_lid:
                relationship_data = [{
                    'type': self.reverse.collection.name,
                    'id': id_number_to_name(rid),
                } for rid in rids_by_lid[lid]]
            else:
                relationship_data = []
            data.setdefault('relationships', {})[self.name] = {
                'data': relationship_data,
                'links': {
                    'self': (f'/{self.collection.name}/{lid}/'
                             f'relationships/{self.name}'),
                    'related': (f'/{self.collection.name}/{lid}/'
                                f'{self.name}'),
                },
            }

    async def get_object_data(self, env):
        """Creates the response data member for ManyToManyRelationships.

        Specifically, after this call the environment's data is updated with
        something like the following:

        env.data = {
            'relationships': {
                'many_manys': {
                    'data': [
                        {
                            'type': 'many_manys',
                            'id': UUID_51,
                        },
                        ...
                    ],
                    'links': {
                        'self': '/centers/1/relationships/many_manys',
                        'related': '/centers/1/many_manys',
                    },
                },
            }
        }
        """
        stmt = (f"SELECT {self.rafkey} "
                f"FROM {self.atable.name} "
                f"WHERE {self.lafkey} = $1;")
        async with env.lock:
            records = await env.connection.fetch(stmt, env.obj.id.number)
        await env.event.wait()
        rids = [record[self.rafkey] for record in records]
        rafkeys_by_lafkey = {}
        for record in records:
            rafkeys_by_lafkey.setdefault(env.obj.id.number,
                                         []).append(record[self.rafkey])
        env.data['relationships'][self.name] = {
            'data': [{
                'type': self.reverse.collection.name,
                'id': id_number_to_name(rid),
            } for rid in rids],
            'links': {
                'self': (f'/{self.collection.name}/{env.obj.id.name}/'
                         f'relationships/{self.name}'),
                'related': (f'/{self.collection.name}/{env.obj.id.name}/'
                            f'{self.name}'),
            },
        }

    async def get_to_one_related_data(self, env):
        """Creates the response data member for OneToManyRelationships.

        Specifically, after this call the environment's data member is updated
        with something like the following:

        env.data = {
            'relationships': {
                'one_manys': {
                    'data': [{
                        'type': 'one_manys',
                        'id': UUID_41,
                        'attributes': {
                            ...
                        },
                        'relationships': {
                            ...
                        },
                    },
                    ...
                    ],
                    'links': {
                        'self': '/one_manys/UUID_41',
                    },
                },
            },
        }
        """
        if isinstance(env.related.relationship, LocalRelationship):
            # OneToOneLocalRelationship or ManyToOneRelationship
            stmt = (f'SELECT {self.rafkey} '
                    f'FROM {self.atable.name} '
                    f'WHERE {self.lafkey} IN ('
                    f' SELECT {env.related.relationship.lfkey}'
                    f' FROM {env.related.table.name}'
                    f' WHERE id = $1)')
        else:  # OneToOneRemoteRelationship
            stmt = (f'SELECT {self.rafkey} '
                    f'FROM {self.atable.name} '
                    f'WHERE {self.lafkey} IN ('
                    f' SELECT id'
                    f' FROM {env.related.relationship.rtable.name}'
                    f' WHERE {env.related.relationship.rfkey} = $1)')
        async with env.lock:
            records = await env.connection.fetch(stmt, env.related.id.number)
        await env.event.wait()
        if env.data is None:
            return
        rids = [record[0] for record in records]
        relationship_data = [{
            'type': self.reverse.collection.name,
            'id': id_number_to_name(rid),
        } for rid in rids]
        env.data.setdefault('relationships', {})[self.name] = {
            'data': relationship_data,
            'links': {
                'self': f'/{env.related.collection_name}/{env.related.id.name}'
            },
        }

    async def get_to_many_related_data(self, env):
        """Creates the response data member for OneToManyRelationships.

        Specifically, after this call the environment's data member is updated
        with something like the following:

        env.data = {
            'relationships': {
                'one_manys': {
                    'data': [{
                        'type': 'one_manys',
                        'id': UUID_41,
                        'attributes': {
                            ...
                        },
                        'relationships': {
                            ...
                        },
                    },
                    ...
                    ],
                    'links': {
                        'self': '/one_manys/UUID_41',
                    },
                },
            },
        }
        """
        if isinstance(env.related.relationship, ManyToManyRelationship):
            stmt = (f'SELECT {self.lafkey}, {self.rafkey} '
                    f'FROM {self.atable.name} '
                    f'WHERE {self.lafkey} IN ('
                    f' SELECT {env.related.relationship.rafkey}'
                    f' FROM {env.related.relationship.atable.name}'
                    f' WHERE {env.related.relationship.lafkey} = $1)')
        else:  # OneToManyRelationship
            stmt = (f'SELECT {self.lafkey}, {self.rafkey} '
                    f'FROM {self.atable.name} '
                    f'WHERE {self.lafkey} IN ('
                    f' SELECT id'
                    f' FROM {env.related.relationship.rtable.name}'
                    f' WHERE {env.related.relationship.rfkey} = $1)')
        async with env.lock:
            records = await env.connection.fetch(stmt, env.related.id.number)
        await env.event.wait()
        rids_by_lid = {}
        for record in records:
            rids_by_lid.setdefault(record[0], []).append(record[1])
        for lid, data in env.data_by_lid.items():
            if lid in rids_by_lid:
                relationship_data = [{
                    'type': self.reverse.collection.name,
                    'id': id_number_to_name(rid),
                } for rid in rids_by_lid[lid]]
            else:
                relationship_data = []
            data.setdefault('relationships', {})[self.name] = {
                'data': relationship_data,
                'links': {
                    'self':
                    f'/{env.related.collection_name}/{env.related.id.name}'
                },
            }
