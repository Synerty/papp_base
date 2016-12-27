import os
from abc import ABCMeta, abstractproperty
from typing import Optional

from jsoncfg.value_mappers import require_string
from sqlalchemy import MetaData
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm.session import Session

from peek_plugin_base.storage.DbConnection import DbConnection


class PluginServerStorageEntryHookMixin:

    def _migrateStorageSchema(self, metadata: MetaData) -> None:
        """ Initialise the DB

        This method is called by the platform between the load() and start() calls.
        There should be no need for a plugin to call this method it's self.

        :param metadata: the SQLAlchemy metadata for this plugins schema

        """

        relDir = self._packageCfg.config.storage.alembicDir(require_string)
        alembicDir = os.path.join(self.rootDir, relDir)
        if not os.path.isdir(alembicDir): raise NotADirectoryError(alembicDir)

        self._dbConn = DbConnection(
            dbConnectString=self.platform.dbConnectString,
            metadata=metadata,
            alembicDir=alembicDir
        )

        self._dbConn.migrate()

    @property
    def dbSession(self) -> Session:
        """ Database Session

        This is a helper property that can be used by the papp to get easy access to
        the SQLAlchemy C{Session}

        :return: An instance of the sqlalchemy ORM session

        """
        return self._dbConn.ormSession()

    @property
    def dbEngine(self) -> Engine:
        """ DB Engine

        This is a helper property that can be used by the papp to get easy access to
        the SQLAlchemy C{Engine}

        :return: The instance of the database engine for this plugin

        """
        return self._dbConn._dbEngine

    @property
    def dbMetadata(self) -> MetaData:
        """ DB Metadata

        This property returns an instance to the metadata from the ORM Declarative
         on which, all the ORM classes have inherited.

        This means the metadata knows about all the tables.

        NOTE: The plugin must be constructed with a schema matching the plugin package

        :return: The instance of the metadata for this plugin.

        Example from peek_plugin_noop.storage.DeclarativeBase.py
        --------------------------------------------------------

        ::

            metadata = MetaData(schema="noop")
            DeclarativeBase = declarative_base(metadata=metadata)

        """
        pass

    @property
    def publishedStorageApi(self, requestingPluginName: str) -> Optional[object]:
        """ Published Storage API

        :param requestingPluginName: The name of the peek app requesting the API

        :return An object implementing an API that may be used by other apps in
        the platform.
        """
        return None

