==========================================
Documentation of the toolsapi_test project
==========================================

Bloks
=====

anyblok-core
------------


    This blok is required by all anyblok application. This blok define the main
    fonctionnality to install, update and uninstall blok. And also list the
    known models, fields, columns and relationships
    

Parameter:

* **author** = Suzanne Jean-Sébastien
* **version** = 0.9.10
* **installed_version** = 0.9.10

.. This file is a part of the AnyBlok project
..
..    Copyright (C) 2014 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
..
.. This Source Code Form is subject to the terms of the Mozilla Public License,
.. v. 2.0. If a copy of the MPL was not distributed with this file,You can
.. obtain one at http://mozilla.org/MPL/2.0/.

This blok is required by all anyblok application. This blok define the main
fonctionnality to install, update and uninstall blok. And also list the
known models, fields, columns and relationships:

* Core ``Model``
    - Base: inherited by all the Model
    - SqlBase: Inherited only by the model with table
    - SqlViewBase: Inherited only by the sql view model

* System Models
    - Blok: List the bloks
    - Model: List the models
    - Field: List of the fields
    - Column: List of the columns
    - Relationship: List of the relation ship
    - Sequence: Define database sequence
    - Parameter: Define application parameter

Sequence
~~~~~~~~

Some behaviours need to have sequence::

    sequence = registry.System.Sequence.insert(
        code="string code",
        formater="One prefix {seq} One suffix")

.. note::

    It is a python formater, you can use the variable:

    * seq: numero of the current data base sequence
    * code: code field
    * id: id field

Get the next value of the sequence::

    sequence.nextval()

exemple::

    seq = Sequence.insert(code='SO', formater="{code}-{seq:06d}")
    seq.nextval()
    >>> SO-000001
    seq.nextval()
    >>> SO-000002

Parameter
~~~~~~~~~

Parameter is a simple model key / value:

* key: must be a String
* value: any type

Add new value in the paramter model::

    registry.System.Parameter.set(key, value)

.. note::

    If the key already exist, then the value of the key is updated

Get an existing value::

    registry.System.Parameter.get(key)

.. warning::

    If the key does not existing then an ExceptionParameter will raise

Check the key exist::

    registry.System.Parameter.is_exist(key)  # return a Boolean

Return and remove the parameter::

    registry.System.Parameter.pop(key)


toolsapiblok
------------

Toolsapiblok's Blok class definition
    

Parameter:

* **author** = Franck Bret
* **version** = 0.1.0
* **installed_version** = 0.1.0



Models
======

This the differents models defined on the project

Model.System
------------

Properties:

* **table name** : No table

Attributes, methods and class methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* add_in_table_args

list() -> new empty list
list(iterable) -> new list initialized from iterable's items

* hybrid_property_columns

list() -> new empty list
list(iterable) -> new list initialized from iterable's items

* is_sql

bool(x) -> bool

Returns True when the argument x is true, False otherwise.
The builtins True and False are the only two instances of the class bool.
The class bool is a subclass of the class int, and cannot be subclassed.

* is_sql_view

bool(x) -> bool

Returns True when the argument x is true, False otherwise.
The builtins True and False are the only two instances of the class bool.
The class bool is a subclass of the class int, and cannot be subclassed.

Model.System.Model
------------------

Models assembled

Properties:

* **table name** : system_model

Fields
~~~~~~

* name

 **code** (system_model.name),  **model** (Model.System.Model),  **label** (Name),  **ftype** (String),  **entity_type** (Model.System.Column),  **autoincrement** (False),  **foreign_key** (None),  **primary_key** (True),  **unique** (None),  **nullable** (False),  **remote_model** (None)

* table

 **code** (system_model.table),  **model** (Model.System.Model),  **label** (Table),  **ftype** (String),  **entity_type** (Model.System.Column),  **autoincrement** (False),  **foreign_key** (None),  **primary_key** (False),  **unique** (None),  **nullable** (True),  **remote_model** (None)

* is_sql_model

 **code** (system_model.is_sql_model),  **model** (Model.System.Model),  **label** (Is a SQL model),  **ftype** (Boolean),  **entity_type** (Model.System.Column),  **autoincrement** (False),  **foreign_key** (None),  **primary_key** (False),  **unique** (None),  **nullable** (True),  **remote_model** (None)

* description

 **code** (system_model.description),  **model** (Model.System.Model),  **label** (Description),  **ftype** (Function),  **entity_type** (Model.System.Field)

Model.System.Field
------------------

Properties:

* **table name** : system_field

Fields
~~~~~~

* name

 **code** (system_field.name),  **model** (Model.System.Field),  **label** (Name),  **ftype** (String),  **entity_type** (Model.System.Column),  **autoincrement** (False),  **foreign_key** (None),  **primary_key** (True),  **unique** (None),  **nullable** (False),  **remote_model** (None)

* code

 **code** (system_field.code),  **model** (Model.System.Field),  **label** (Code),  **ftype** (String),  **entity_type** (Model.System.Column),  **autoincrement** (False),  **foreign_key** (None),  **primary_key** (False),  **unique** (None),  **nullable** (True),  **remote_model** (None)

* model

 **code** (system_field.model),  **model** (Model.System.Field),  **label** (Model),  **ftype** (String),  **entity_type** (Model.System.Column),  **autoincrement** (False),  **foreign_key** (None),  **primary_key** (True),  **unique** (None),  **nullable** (False),  **remote_model** (None)

* label

 **code** (system_field.label),  **model** (Model.System.Field),  **label** (Label),  **ftype** (String),  **entity_type** (Model.System.Column),  **autoincrement** (False),  **foreign_key** (None),  **primary_key** (False),  **unique** (None),  **nullable** (True),  **remote_model** (None)

* ftype

 **code** (system_field.ftype),  **model** (Model.System.Field),  **label** (Type),  **ftype** (String),  **entity_type** (Model.System.Column),  **autoincrement** (False),  **foreign_key** (None),  **primary_key** (False),  **unique** (None),  **nullable** (True),  **remote_model** (None)

* entity_type

 **code** (system_field.entity_type),  **model** (Model.System.Field),  **label** (Entity type),  **ftype** (String),  **entity_type** (Model.System.Column),  **autoincrement** (False),  **foreign_key** (None),  **primary_key** (False),  **unique** (None),  **nullable** (True),  **remote_model** (None)

Attributes, methods and class methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* _description

* _format_field

* add_field

 Insert a field definition

        :param rname: name of the field
        :param label: label of the field
        :param model: namespace of the model
        :param table: name of the table of the model
        :param ftype: type of the AnyBlok Field
        

* add_in_table_args

list() -> new empty list
list(iterable) -> new list initialized from iterable's items

* alter_field

 Update an existing field

        :param field: instance of the Field model to update
        :param label: label of the field
        :param ftype: type of the AnyBlok Field
        

* code

* define_mapper_args

* define_table_args

* entity_type

* expire

 Expire the attribute of the instance, theses attributes will be
        load at the next  call of the instance

        see: http://docs.sqlalchemy.org/en/latest/orm/session_api.html
        #sqlalchemy.orm.session.Session.expire
        

* expire_relationship_mapped

 Expire the objects linked with this object, in function of
        the mappers definition
        

* expunge

Expunge the instance in the session

* find_relationship

* find_remote_attribute_to_expire

* ftype

* getFieldType

Return the type of the column

        ::

            TheModel.getFieldType(nameOfTheColumn)

        this method take care if it is a polymorphic model or not

        :param name: name of the column
        :rtype: String, the name of the Type of column used
        

* get_cname

* get_hybrid_property_columns

* hybrid_property_columns

list() -> new empty list
list(iterable) -> new list initialized from iterable's items

* is_sql

bool(x) -> bool

Returns True when the argument x is true, False otherwise.
The builtins True and False are the only two instances of the class bool.
The class bool is a subclass of the class int, and cannot be subclassed.

* is_sql_view

bool(x) -> bool

Returns True when the argument x is true, False otherwise.
The builtins True and False are the only two instances of the class bool.
The class bool is a subclass of the class int, and cannot be subclassed.

* label

* metadata

A collection of :class:`.Table` objects and their associated schema
    constructs.

    Holds a collection of :class:`.Table` objects as well as
    an optional binding to an :class:`.Engine` or
    :class:`.Connection`.  If bound, the :class:`.Table` objects
    in the collection and their columns may participate in implicit SQL
    execution.

    The :class:`.Table` objects themselves are stored in the
    :attr:`.MetaData.tables` dictionary.

    :class:`.MetaData` is a thread-safe object for read operations.
    Construction of new tables within a single :class:`.MetaData` object,
    either explicitly or via reflection, may not be completely thread-safe.

    .. seealso::

        :ref:`metadata_describing` - Introduction to database metadata

    

* model

* name

* refresh

 Expire and reload all the attribute of the instance

        See: http://docs.sqlalchemy.org/en/latest/orm/session_api.html
        #sqlalchemy.orm.session.Session.refresh
        

Model.System.Column
-------------------

Properties:

* **table name** : system_column

Fields
~~~~~~

* name

 **code** (system_column.name),  **model** (Model.System.Column),  **label** (Name),  **ftype** (String),  **entity_type** (Model.System.Column),  **autoincrement** (False),  **foreign_key** (None),  **primary_key** (True),  **unique** (None),  **nullable** (False),  **remote_model** (None)

* model

 **code** (system_column.model),  **model** (Model.System.Column),  **label** (Model),  **ftype** (String),  **entity_type** (Model.System.Column),  **autoincrement** (False),  **foreign_key** (None),  **primary_key** (True),  **unique** (None),  **nullable** (False),  **remote_model** (None)

* autoincrement

 **code** (system_column.autoincrement),  **model** (Model.System.Column),  **label** (Auto increment),  **ftype** (Boolean),  **entity_type** (Model.System.Column),  **autoincrement** (False),  **foreign_key** (None),  **primary_key** (False),  **unique** (None),  **nullable** (True),  **remote_model** (None)

* foreign_key

 **code** (system_column.foreign_key),  **model** (Model.System.Column),  **label** (Foreign key),  **ftype** (String),  **entity_type** (Model.System.Column),  **autoincrement** (False),  **foreign_key** (None),  **primary_key** (False),  **unique** (None),  **nullable** (True),  **remote_model** (None)

* primary_key

 **code** (system_column.primary_key),  **model** (Model.System.Column),  **label** (Primary key),  **ftype** (Boolean),  **entity_type** (Model.System.Column),  **autoincrement** (False),  **foreign_key** (None),  **primary_key** (False),  **unique** (None),  **nullable** (True),  **remote_model** (None)

* unique

 **code** (system_column.unique),  **model** (Model.System.Column),  **label** (Unique),  **ftype** (Boolean),  **entity_type** (Model.System.Column),  **autoincrement** (False),  **foreign_key** (None),  **primary_key** (False),  **unique** (None),  **nullable** (True),  **remote_model** (None)

* nullable

 **code** (system_column.nullable),  **model** (Model.System.Column),  **label** (Nullable),  **ftype** (Boolean),  **entity_type** (Model.System.Column),  **autoincrement** (False),  **foreign_key** (None),  **primary_key** (False),  **unique** (None),  **nullable** (True),  **remote_model** (None)

* remote_model

 **code** (system_column.remote_model),  **model** (Model.System.Column),  **label** (Remote model),  **ftype** (String),  **entity_type** (Model.System.Column),  **autoincrement** (False),  **foreign_key** (None),  **primary_key** (False),  **unique** (None),  **nullable** (True),  **remote_model** (None)

Attributes, methods and class methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* _description

* _format_field

* add_field

 Insert a column definition

        :param cname: name of the column
        :param column: instance of the column
        :param model: namespace of the model
        :param table: name of the table of the model
        :param ftype: type of the AnyBlok Field
        

* add_in_table_args

list() -> new empty list
list(iterable) -> new list initialized from iterable's items

* alter_field

 Update an existing column

        :param column: instance of the Column model to update
        :param meta_column: instance of the SqlAlchemy column
        :param ftype: type of the AnyBlok Field
        

* autoincrement

* code

* define_mapper_args

* define_table_args

* entity_type

* expire

 Expire the attribute of the instance, theses attributes will be
        load at the next  call of the instance

        see: http://docs.sqlalchemy.org/en/latest/orm/session_api.html
        #sqlalchemy.orm.session.Session.expire
        

* expire_relationship_mapped

 Expire the objects linked with this object, in function of
        the mappers definition
        

* expunge

Expunge the instance in the session

* find_relationship

* find_remote_attribute_to_expire

* foreign_key

* ftype

* getFieldType

Return the type of the column

        ::

            TheModel.getFieldType(nameOfTheColumn)

        this method take care if it is a polymorphic model or not

        :param name: name of the column
        :rtype: String, the name of the Type of column used
        

* get_cname

 Return the real name of the column

        :param field: the instance of the column
        :param cname: Not use here
        :rtype: string of the real column name
        

* get_hybrid_property_columns

* hybrid_property_columns

list() -> new empty list
list(iterable) -> new list initialized from iterable's items

* is_sql

bool(x) -> bool

Returns True when the argument x is true, False otherwise.
The builtins True and False are the only two instances of the class bool.
The class bool is a subclass of the class int, and cannot be subclassed.

* is_sql_view

bool(x) -> bool

Returns True when the argument x is true, False otherwise.
The builtins True and False are the only two instances of the class bool.
The class bool is a subclass of the class int, and cannot be subclassed.

* label

* metadata

A collection of :class:`.Table` objects and their associated schema
    constructs.

    Holds a collection of :class:`.Table` objects as well as
    an optional binding to an :class:`.Engine` or
    :class:`.Connection`.  If bound, the :class:`.Table` objects
    in the collection and their columns may participate in implicit SQL
    execution.

    The :class:`.Table` objects themselves are stored in the
    :attr:`.MetaData.tables` dictionary.

    :class:`.MetaData` is a thread-safe object for read operations.
    Construction of new tables within a single :class:`.MetaData` object,
    either explicitly or via reflection, may not be completely thread-safe.

    .. seealso::

        :ref:`metadata_describing` - Introduction to database metadata

    

* model

* name

* nullable

* primary_key

* refresh

 Expire and reload all the attribute of the instance

        See: http://docs.sqlalchemy.org/en/latest/orm/session_api.html
        #sqlalchemy.orm.session.Session.refresh
        

* remote_model

* unique

* use

Model.System.RelationShip
-------------------------

Properties:

* **table name** : system_relationship

Fields
~~~~~~

* name

 **code** (system_relationship.name),  **model** (Model.System.RelationShip),  **label** (Name),  **ftype** (String),  **entity_type** (Model.System.Column),  **autoincrement** (False),  **foreign_key** (None),  **primary_key** (True),  **unique** (None),  **nullable** (False),  **remote_model** (None)

* model

 **code** (system_relationship.model),  **model** (Model.System.RelationShip),  **label** (Model),  **ftype** (String),  **entity_type** (Model.System.Column),  **autoincrement** (False),  **foreign_key** (None),  **primary_key** (True),  **unique** (None),  **nullable** (False),  **remote_model** (None)

* local_column

 **code** (system_relationship.local_column),  **model** (Model.System.RelationShip),  **label** (Local column),  **ftype** (String),  **entity_type** (Model.System.Column),  **autoincrement** (False),  **foreign_key** (None),  **primary_key** (False),  **unique** (None),  **nullable** (True),  **remote_model** (None)

* remote_column

 **code** (system_relationship.remote_column),  **model** (Model.System.RelationShip),  **label** (Remote column),  **ftype** (String),  **entity_type** (Model.System.Column),  **autoincrement** (False),  **foreign_key** (None),  **primary_key** (False),  **unique** (None),  **nullable** (True),  **remote_model** (None)

* remote_name

 **code** (system_relationship.remote_name),  **model** (Model.System.RelationShip),  **label** (Remote name),  **ftype** (String),  **entity_type** (Model.System.Column),  **autoincrement** (False),  **foreign_key** (None),  **primary_key** (False),  **unique** (None),  **nullable** (True),  **remote_model** (None)

* remote_model

 **code** (system_relationship.remote_model),  **model** (Model.System.RelationShip),  **label** (Remote model),  **ftype** (String),  **entity_type** (Model.System.Column),  **autoincrement** (False),  **foreign_key** (None),  **primary_key** (False),  **unique** (None),  **nullable** (False),  **remote_model** (None)

* remote

 **code** (system_relationship.remote),  **model** (Model.System.RelationShip),  **label** (Remote),  **ftype** (Boolean),  **entity_type** (Model.System.Column),  **autoincrement** (False),  **foreign_key** (None),  **primary_key** (False),  **unique** (None),  **nullable** (True),  **remote_model** (None)

* nullable

 **code** (system_relationship.nullable),  **model** (Model.System.RelationShip),  **label** (Nullable),  **ftype** (Boolean),  **entity_type** (Model.System.Column),  **autoincrement** (False),  **foreign_key** (None),  **primary_key** (False),  **unique** (None),  **nullable** (True),  **remote_model** (None)

Attributes, methods and class methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* _description

* _format_field

* add_field

 Insert a relationship definition

        :param rname: name of the relationship
        :param relation: instance of the relationship
        :param model: namespace of the model
        :param table: name of the table of the model
        :param ftype: type of the AnyBlok Field
        

* add_in_table_args

list() -> new empty list
list(iterable) -> new list initialized from iterable's items

* alter_field

* code

* define_mapper_args

* define_table_args

* entity_type

* expire

 Expire the attribute of the instance, theses attributes will be
        load at the next  call of the instance

        see: http://docs.sqlalchemy.org/en/latest/orm/session_api.html
        #sqlalchemy.orm.session.Session.expire
        

* expire_relationship_mapped

 Expire the objects linked with this object, in function of
        the mappers definition
        

* expunge

Expunge the instance in the session

* find_relationship

* find_remote_attribute_to_expire

* ftype

* getFieldType

Return the type of the column

        ::

            TheModel.getFieldType(nameOfTheColumn)

        this method take care if it is a polymorphic model or not

        :param name: name of the column
        :rtype: String, the name of the Type of column used
        

* get_cname

* get_hybrid_property_columns

* hybrid_property_columns

list() -> new empty list
list(iterable) -> new list initialized from iterable's items

* is_sql

bool(x) -> bool

Returns True when the argument x is true, False otherwise.
The builtins True and False are the only two instances of the class bool.
The class bool is a subclass of the class int, and cannot be subclassed.

* is_sql_view

bool(x) -> bool

Returns True when the argument x is true, False otherwise.
The builtins True and False are the only two instances of the class bool.
The class bool is a subclass of the class int, and cannot be subclassed.

* label

* local_column

* metadata

A collection of :class:`.Table` objects and their associated schema
    constructs.

    Holds a collection of :class:`.Table` objects as well as
    an optional binding to an :class:`.Engine` or
    :class:`.Connection`.  If bound, the :class:`.Table` objects
    in the collection and their columns may participate in implicit SQL
    execution.

    The :class:`.Table` objects themselves are stored in the
    :attr:`.MetaData.tables` dictionary.

    :class:`.MetaData` is a thread-safe object for read operations.
    Construction of new tables within a single :class:`.MetaData` object,
    either explicitly or via reflection, may not be completely thread-safe.

    .. seealso::

        :ref:`metadata_describing` - Introduction to database metadata

    

* model

* name

* nullable

* refresh

 Expire and reload all the attribute of the instance

        See: http://docs.sqlalchemy.org/en/latest/orm/session_api.html
        #sqlalchemy.orm.session.Session.refresh
        

* remote

* remote_column

* remote_model

* remote_name

* use

Model.System.Blok
-----------------

Properties:

* **table name** : system_blok

Fields
~~~~~~

* name

 **code** (system_blok.name),  **model** (Model.System.Blok),  **label** (Name),  **ftype** (String),  **entity_type** (Model.System.Column),  **autoincrement** (False),  **foreign_key** (None),  **primary_key** (True),  **unique** (None),  **nullable** (False),  **remote_model** (None)

* state

 **code** (system_blok.state),  **model** (Model.System.Blok),  **label** (State),  **ftype** (Selection),  **entity_type** (Model.System.Column),  **autoincrement** (False),  **foreign_key** (None),  **primary_key** (False),  **unique** (None),  **nullable** (False),  **remote_model** (None)

* author

 **code** (system_blok.author),  **model** (Model.System.Blok),  **label** (Author),  **ftype** (String),  **entity_type** (Model.System.Column),  **autoincrement** (False),  **foreign_key** (None),  **primary_key** (False),  **unique** (None),  **nullable** (True),  **remote_model** (None)

* order

 **code** (system_blok.order),  **model** (Model.System.Blok),  **label** (Order),  **ftype** (Integer),  **entity_type** (Model.System.Column),  **autoincrement** (False),  **foreign_key** (None),  **primary_key** (False),  **unique** (None),  **nullable** (False),  **remote_model** (None)

* short_description

 **code** (system_blok.short_description),  **model** (Model.System.Blok),  **label** (Short description),  **ftype** (Function),  **entity_type** (Model.System.Field)

* long_description

 **code** (system_blok.long_description),  **model** (Model.System.Blok),  **label** (Long description),  **ftype** (Function),  **entity_type** (Model.System.Field)

* logo

 **code** (system_blok.logo),  **model** (Model.System.Blok),  **label** (Logo),  **ftype** (Function),  **entity_type** (Model.System.Field)

* version

 **code** (system_blok.version),  **model** (Model.System.Blok),  **label** (Version),  **ftype** (String),  **entity_type** (Model.System.Column),  **autoincrement** (False),  **foreign_key** (None),  **primary_key** (False),  **unique** (None),  **nullable** (False),  **remote_model** (None)

* installed_version

 **code** (system_blok.installed_version),  **model** (Model.System.Blok),  **label** (Installed version),  **ftype** (String),  **entity_type** (Model.System.Column),  **autoincrement** (False),  **foreign_key** (None),  **primary_key** (False),  **unique** (None),  **nullable** (True),  **remote_model** (None)

Model.System.Cache
------------------

Properties:

* **table name** : system_cache

Fields
~~~~~~

* id

 **code** (system_cache.id),  **model** (Model.System.Cache),  **label** (Id),  **ftype** (Integer),  **entity_type** (Model.System.Column),  **autoincrement** (True),  **foreign_key** (None),  **primary_key** (True),  **unique** (None),  **nullable** (False),  **remote_model** (None)

* registry_name

 **code** (system_cache.registry_name),  **model** (Model.System.Cache),  **label** (Registry name),  **ftype** (String),  **entity_type** (Model.System.Column),  **autoincrement** (False),  **foreign_key** (None),  **primary_key** (False),  **unique** (None),  **nullable** (False),  **remote_model** (None)

* method

 **code** (system_cache.method),  **model** (Model.System.Cache),  **label** (Method),  **ftype** (String),  **entity_type** (Model.System.Column),  **autoincrement** (False),  **foreign_key** (None),  **primary_key** (False),  **unique** (None),  **nullable** (False),  **remote_model** (None)

Attributes, methods and class methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* _format_field

* add_in_table_args

list() -> new empty list
list(iterable) -> new list initialized from iterable's items

* clear_invalidate_cache

 Invalidate the cache that needs to be invalidated
        

* define_mapper_args

* define_table_args

* detect_invalidation

 Return True if a new invalidation is found in the table

        :rtype: Boolean
        

* expire

 Expire the attribute of the instance, theses attributes will be
        load at the next  call of the instance

        see: http://docs.sqlalchemy.org/en/latest/orm/session_api.html
        #sqlalchemy.orm.session.Session.expire
        

* expire_relationship_mapped

 Expire the objects linked with this object, in function of
        the mappers definition
        

* expunge

Expunge the instance in the session

* find_relationship

* find_remote_attribute_to_expire

* getFieldType

Return the type of the column

        ::

            TheModel.getFieldType(nameOfTheColumn)

        this method take care if it is a polymorphic model or not

        :param name: name of the column
        :rtype: String, the name of the Type of column used
        

* get_hybrid_property_columns

* get_invalidation

 Return the pointer of the method to invalidate
        

* get_last_id

 Return the last primary key ``id`` value
        

* hybrid_property_columns

list() -> new empty list
list(iterable) -> new list initialized from iterable's items

* id

* invalidate

 Call the invalidation for a specific method cached on a model

        :param registry_name: namespace of the model
        :param method: name of the method on the model
        :exception: CacheException
        

* invalidate_all

* is_sql

bool(x) -> bool

Returns True when the argument x is true, False otherwise.
The builtins True and False are the only two instances of the class bool.
The class bool is a subclass of the class int, and cannot be subclassed.

* is_sql_view

bool(x) -> bool

Returns True when the argument x is true, False otherwise.
The builtins True and False are the only two instances of the class bool.
The class bool is a subclass of the class int, and cannot be subclassed.

* last_cache_id

int(x=0) -> integer
int(x, base=10) -> integer

Convert a number or string to an integer, or return 0 if no arguments
are given.  If x is a number, return x.__int__().  For floating point
numbers, this truncates towards zero.

If x is not a number or if base is given, then x must be a string,
bytes, or bytearray instance representing an integer literal in the
given base.  The literal can be preceded by '+' or '-' and be surrounded
by whitespace.  The base defaults to 10.  Valid bases are 0 and 2-36.
Base 0 means to interpret the base from the string as an integer literal.
>>> int('0b100', base=0)
4

* lrus

dict() -> new empty dictionary
dict(mapping) -> new dictionary initialized from a mapping object's
    (key, value) pairs
dict(iterable) -> new dictionary initialized as if via:
    d = {}
    for k, v in iterable:
        d[k] = v
dict(**kwargs) -> new dictionary initialized with the name=value pairs
    in the keyword argument list.  For example:  dict(one=1, two=2)

* metadata

A collection of :class:`.Table` objects and their associated schema
    constructs.

    Holds a collection of :class:`.Table` objects as well as
    an optional binding to an :class:`.Engine` or
    :class:`.Connection`.  If bound, the :class:`.Table` objects
    in the collection and their columns may participate in implicit SQL
    execution.

    The :class:`.Table` objects themselves are stored in the
    :attr:`.MetaData.tables` dictionary.

    :class:`.MetaData` is a thread-safe object for read operations.
    Construction of new tables within a single :class:`.MetaData` object,
    either explicitly or via reflection, may not be completely thread-safe.

    .. seealso::

        :ref:`metadata_describing` - Introduction to database metadata

    

* method

* refresh

 Expire and reload all the attribute of the instance

        See: http://docs.sqlalchemy.org/en/latest/orm/session_api.html
        #sqlalchemy.orm.session.Session.refresh
        

* registry_name

Model.System.Parameter
----------------------

System Parameter

Properties:

* **table name** : system_parameter

Fields
~~~~~~

* key

 **code** (system_parameter.key),  **model** (Model.System.Parameter),  **label** (Key),  **ftype** (String),  **entity_type** (Model.System.Column),  **autoincrement** (False),  **foreign_key** (None),  **primary_key** (True),  **unique** (None),  **nullable** (False),  **remote_model** (None)

* value

 **code** (system_parameter.value),  **model** (Model.System.Parameter),  **label** (Value),  **ftype** (Json),  **entity_type** (Model.System.Column),  **autoincrement** (False),  **foreign_key** (None),  **primary_key** (False),  **unique** (None),  **nullable** (False),  **remote_model** (None)

* multi

 **code** (system_parameter.multi),  **model** (Model.System.Parameter),  **label** (Multi),  **ftype** (Boolean),  **entity_type** (Model.System.Column),  **autoincrement** (False),  **foreign_key** (None),  **primary_key** (False),  **unique** (None),  **nullable** (True),  **remote_model** (None)

Attributes, methods and class methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* _format_field

* add_in_table_args

list() -> new empty list
list(iterable) -> new list initialized from iterable's items

* define_mapper_args

* define_table_args

* expire

 Expire the attribute of the instance, theses attributes will be
        load at the next  call of the instance

        see: http://docs.sqlalchemy.org/en/latest/orm/session_api.html
        #sqlalchemy.orm.session.Session.expire
        

* expire_relationship_mapped

 Expire the objects linked with this object, in function of
        the mappers definition
        

* expunge

Expunge the instance in the session

* find_relationship

* find_remote_attribute_to_expire

* get

 Return the value of the key

        :param key: key to check
        :rtype: return value
        :exception: ExceptionParameter
        

* getFieldType

Return the type of the column

        ::

            TheModel.getFieldType(nameOfTheColumn)

        this method take care if it is a polymorphic model or not

        :param name: name of the column
        :rtype: String, the name of the Type of column used
        

* get_hybrid_property_columns

* hybrid_property_columns

list() -> new empty list
list(iterable) -> new list initialized from iterable's items

* is_exist

 Check if one parameter exist for the key

        :param key: key to check
        :rtype: Boolean, True if exist
        

* is_sql

bool(x) -> bool

Returns True when the argument x is true, False otherwise.
The builtins True and False are the only two instances of the class bool.
The class bool is a subclass of the class int, and cannot be subclassed.

* is_sql_view

bool(x) -> bool

Returns True when the argument x is true, False otherwise.
The builtins True and False are the only two instances of the class bool.
The class bool is a subclass of the class int, and cannot be subclassed.

* key

* metadata

A collection of :class:`.Table` objects and their associated schema
    constructs.

    Holds a collection of :class:`.Table` objects as well as
    an optional binding to an :class:`.Engine` or
    :class:`.Connection`.  If bound, the :class:`.Table` objects
    in the collection and their columns may participate in implicit SQL
    execution.

    The :class:`.Table` objects themselves are stored in the
    :attr:`.MetaData.tables` dictionary.

    :class:`.MetaData` is a thread-safe object for read operations.
    Construction of new tables within a single :class:`.MetaData` object,
    either explicitly or via reflection, may not be completely thread-safe.

    .. seealso::

        :ref:`metadata_describing` - Introduction to database metadata

    

* multi

* pop

Remove return the value of the key

        :param key: key to check
        :rtype: return value
        :exception: ExceptionParameter
        

* refresh

 Expire and reload all the attribute of the instance

        See: http://docs.sqlalchemy.org/en/latest/orm/session_api.html
        #sqlalchemy.orm.session.Session.refresh
        

* set

 Insert or Update parameter for the key

        :param key: key to save
        :param value: value to save
        

* value

Model.System.Sequence
---------------------

 System sequence 

Properties:

* **table name** : system_sequence

Fields
~~~~~~

* id

 **code** (system_sequence.id),  **model** (Model.System.Sequence),  **label** (Id),  **ftype** (Integer),  **entity_type** (Model.System.Column),  **autoincrement** (True),  **foreign_key** (None),  **primary_key** (True),  **unique** (None),  **nullable** (False),  **remote_model** (None)

* code

 **code** (system_sequence.code),  **model** (Model.System.Sequence),  **label** (Code),  **ftype** (String),  **entity_type** (Model.System.Column),  **autoincrement** (False),  **foreign_key** (None),  **primary_key** (False),  **unique** (None),  **nullable** (False),  **remote_model** (None)

* number

 **code** (system_sequence.number),  **model** (Model.System.Sequence),  **label** (Number),  **ftype** (Integer),  **entity_type** (Model.System.Column),  **autoincrement** (False),  **foreign_key** (None),  **primary_key** (False),  **unique** (None),  **nullable** (False),  **remote_model** (None)

* seq_name

 **code** (system_sequence.seq_name),  **model** (Model.System.Sequence),  **label** (Seq name),  **ftype** (String),  **entity_type** (Model.System.Column),  **autoincrement** (False),  **foreign_key** (None),  **primary_key** (False),  **unique** (None),  **nullable** (False),  **remote_model** (None)

* formater

 **code** (system_sequence.formater),  **model** (Model.System.Sequence),  **label** (Formater),  **ftype** (String),  **entity_type** (Model.System.Column),  **autoincrement** (False),  **foreign_key** (None),  **primary_key** (False),  **unique** (None),  **nullable** (False),  **remote_model** (None)

Attributes, methods and class methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* _cls_seq_name

str(object='') -> str
str(bytes_or_buffer[, encoding[, errors]]) -> str

Create a new string object from the given object. If encoding or
errors is specified, then the object must expose a data buffer
that will be decoded using the given encoding and error handler.
Otherwise, returns the result of object.__str__() (if defined)
or repr(object).
encoding defaults to sys.getdefaultencoding().
errors defaults to 'strict'.

* _format_field

* add_in_table_args

list() -> new empty list
list(iterable) -> new list initialized from iterable's items

* code

* create_sequence

 create the sequence for one instance 

* define_mapper_args

* define_table_args

* expire

 Expire the attribute of the instance, theses attributes will be
        load at the next  call of the instance

        see: http://docs.sqlalchemy.org/en/latest/orm/session_api.html
        #sqlalchemy.orm.session.Session.expire
        

* expire_relationship_mapped

 Expire the objects linked with this object, in function of
        the mappers definition
        

* expunge

Expunge the instance in the session

* find_relationship

* find_remote_attribute_to_expire

* formater

* getFieldType

Return the type of the column

        ::

            TheModel.getFieldType(nameOfTheColumn)

        this method take care if it is a polymorphic model or not

        :param name: name of the column
        :rtype: String, the name of the Type of column used
        

* get_hybrid_property_columns

* hybrid_property_columns

list() -> new empty list
list(iterable) -> new list initialized from iterable's items

* id

* is_sql

bool(x) -> bool

Returns True when the argument x is true, False otherwise.
The builtins True and False are the only two instances of the class bool.
The class bool is a subclass of the class int, and cannot be subclassed.

* is_sql_view

bool(x) -> bool

Returns True when the argument x is true, False otherwise.
The builtins True and False are the only two instances of the class bool.
The class bool is a subclass of the class int, and cannot be subclassed.

* metadata

A collection of :class:`.Table` objects and their associated schema
    constructs.

    Holds a collection of :class:`.Table` objects as well as
    an optional binding to an :class:`.Engine` or
    :class:`.Connection`.  If bound, the :class:`.Table` objects
    in the collection and their columns may participate in implicit SQL
    execution.

    The :class:`.Table` objects themselves are stored in the
    :attr:`.MetaData.tables` dictionary.

    :class:`.MetaData` is a thread-safe object for read operations.
    Construction of new tables within a single :class:`.MetaData` object,
    either explicitly or via reflection, may not be completely thread-safe.

    .. seealso::

        :ref:`metadata_describing` - Introduction to database metadata

    

* nextval

 return the next value of the sequence 

* nextvalBy

 Get the first sequence filtering by entries and return the next
        value 

* number

* refresh

 Expire and reload all the attribute of the instance

        See: http://docs.sqlalchemy.org/en/latest/orm/session_api.html
        #sqlalchemy.orm.session.Session.refresh
        

* seq_name

Model.System.Cron
-----------------

Properties:

* **table name** : No table

Attributes, methods and class methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* add_in_table_args

list() -> new empty list
list(iterable) -> new list initialized from iterable's items

* add_worker_for

* close_worker_on_error

* close_worker_with_success

* hybrid_property_columns

list() -> new empty list
list(iterable) -> new list initialized from iterable's items

* is_sql

bool(x) -> bool

Returns True when the argument x is true, False otherwise.
The builtins True and False are the only two instances of the class bool.
The class bool is a subclass of the class int, and cannot be subclassed.

* is_sql_view

bool(x) -> bool

Returns True when the argument x is true, False otherwise.
The builtins True and False are the only two instances of the class bool.
The class bool is a subclass of the class int, and cannot be subclassed.

* lock_one_job

* run

* started

bool(x) -> bool

Returns True when the argument x is true, False otherwise.
The builtins True and False are the only two instances of the class bool.
The class bool is a subclass of the class int, and cannot be subclassed.

Model.System.Cron.Job
---------------------

Properties:

* **table name** : system_cron_job

Fields
~~~~~~

* id

 **code** (system_cron_job.id),  **model** (Model.System.Cron.Job),  **label** (Id),  **ftype** (Integer),  **entity_type** (Model.System.Column),  **autoincrement** (True),  **foreign_key** (None),  **primary_key** (True),  **unique** (None),  **nullable** (False),  **remote_model** (None)

* available_at

 **code** (system_cron_job.available_at),  **model** (Model.System.Cron.Job),  **label** (Available at),  **ftype** (DateTime),  **entity_type** (Model.System.Column),  **autoincrement** (False),  **foreign_key** (None),  **primary_key** (False),  **unique** (None),  **nullable** (True),  **remote_model** (None)

* done_at

 **code** (system_cron_job.done_at),  **model** (Model.System.Cron.Job),  **label** (Done at),  **ftype** (DateTime),  **entity_type** (Model.System.Column),  **autoincrement** (False),  **foreign_key** (None),  **primary_key** (False),  **unique** (None),  **nullable** (True),  **remote_model** (None)

* model

 **code** (system_cron_job.model),  **model** (Model.System.Cron.Job),  **label** (Model),  **ftype** (String),  **entity_type** (Model.System.Column),  **autoincrement** (False),  **foreign_key** (system_model.name),  **primary_key** (False),  **unique** (None),  **nullable** (False),  **remote_model** (Model.System.Model)

* method

 **code** (system_cron_job.method),  **model** (Model.System.Cron.Job),  **label** (Method),  **ftype** (String),  **entity_type** (Model.System.Column),  **autoincrement** (False),  **foreign_key** (None),  **primary_key** (False),  **unique** (None),  **nullable** (False),  **remote_model** (None)

* is_a_class_method

 **code** (system_cron_job.is_a_class_method),  **model** (Model.System.Cron.Job),  **label** (Is a class method),  **ftype** (Boolean),  **entity_type** (Model.System.Column),  **autoincrement** (False),  **foreign_key** (None),  **primary_key** (False),  **unique** (None),  **nullable** (True),  **remote_model** (None)

* params

 **code** (system_cron_job.params),  **model** (Model.System.Cron.Job),  **label** (Params),  **ftype** (Json),  **entity_type** (Model.System.Column),  **autoincrement** (False),  **foreign_key** (None),  **primary_key** (False),  **unique** (None),  **nullable** (True),  **remote_model** (None)

* error

 **code** (system_cron_job.error),  **model** (Model.System.Cron.Job),  **label** (Error),  **ftype** (Text),  **entity_type** (Model.System.Column),  **autoincrement** (False),  **foreign_key** (None),  **primary_key** (False),  **unique** (None),  **nullable** (True),  **remote_model** (None)

Attributes, methods and class methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* _format_field

* add_in_table_args

list() -> new empty list
list(iterable) -> new list initialized from iterable's items

* available_at

* define_mapper_args

* define_table_args

* done_at

* error

* expire

 Expire the attribute of the instance, theses attributes will be
        load at the next  call of the instance

        see: http://docs.sqlalchemy.org/en/latest/orm/session_api.html
        #sqlalchemy.orm.session.Session.expire
        

* expire_relationship_mapped

 Expire the objects linked with this object, in function of
        the mappers definition
        

* expunge

Expunge the instance in the session

* find_relationship

* find_remote_attribute_to_expire

* getFieldType

Return the type of the column

        ::

            TheModel.getFieldType(nameOfTheColumn)

        this method take care if it is a polymorphic model or not

        :param name: name of the column
        :rtype: String, the name of the Type of column used
        

* get_hybrid_property_columns

* hybrid_property_columns

list() -> new empty list
list(iterable) -> new list initialized from iterable's items

* id

* is_a_class_method

* is_sql

bool(x) -> bool

Returns True when the argument x is true, False otherwise.
The builtins True and False are the only two instances of the class bool.
The class bool is a subclass of the class int, and cannot be subclassed.

* is_sql_view

bool(x) -> bool

Returns True when the argument x is true, False otherwise.
The builtins True and False are the only two instances of the class bool.
The class bool is a subclass of the class int, and cannot be subclassed.

* metadata

A collection of :class:`.Table` objects and their associated schema
    constructs.

    Holds a collection of :class:`.Table` objects as well as
    an optional binding to an :class:`.Engine` or
    :class:`.Connection`.  If bound, the :class:`.Table` objects
    in the collection and their columns may participate in implicit SQL
    execution.

    The :class:`.Table` objects themselves are stored in the
    :attr:`.MetaData.tables` dictionary.

    :class:`.MetaData` is a thread-safe object for read operations.
    Construction of new tables within a single :class:`.MetaData` object,
    either explicitly or via reflection, may not be completely thread-safe.

    .. seealso::

        :ref:`metadata_describing` - Introduction to database metadata

    

* method

* model

* params

* refresh

 Expire and reload all the attribute of the instance

        See: http://docs.sqlalchemy.org/en/latest/orm/session_api.html
        #sqlalchemy.orm.session.Session.refresh
        

Model.System.Cron.Worker
------------------------

Properties:

* **table name** : No table

Attributes, methods and class methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* _bootstrap

* _bootstrap_inner

* _delete

Remove current thread from the dict of currently running threads.

* _exc_info

exc_info() -> (type, value, traceback)

Return information about the most recent exception caught by an except
clause in the current stack frame or in an older stack frame.

* _initialized

bool(x) -> bool

Returns True when the argument x is true, False otherwise.
The builtins True and False are the only two instances of the class bool.
The class bool is a subclass of the class int, and cannot be subclassed.

* _reset_internal_locks

* _set_ident

* _set_tstate_lock


        Set a lock object which will be released by the interpreter when
        the underlying thread state (see pystate.h) gets deleted.
        

* _stop

* _wait_for_tstate_lock

* add_in_table_args

list() -> new empty list
list(iterable) -> new list initialized from iterable's items

* call_method

* daemon

A boolean value indicating whether this thread is a daemon thread.

        This must be set before start() is called, otherwise RuntimeError is
        raised. Its initial value is inherited from the creating thread; the
        main thread is not a daemon thread and therefore all threads created in
        the main thread default to daemon = False.

        The entire Python program exits when no alive non-daemon threads are
        left.

        

* getName

* get_args_and_kwargs

* get_error

* get_model_record

* hybrid_property_columns

list() -> new empty list
list(iterable) -> new list initialized from iterable's items

* ident

Thread identifier of this thread or None if it has not been started.

        This is a nonzero integer. See the thread.get_ident() function. Thread
        identifiers may be recycled when a thread exits and another thread is
        created. The identifier is available even after the thread has exited.

        

* isAlive

Return whether the thread is alive.

        This method returns True just before the run() method starts until just
        after the run() method terminates. The module function enumerate()
        returns a list of all alive threads.

        

* isDaemon

* is_alive

Return whether the thread is alive.

        This method returns True just before the run() method starts until just
        after the run() method terminates. The module function enumerate()
        returns a list of all alive threads.

        

* is_sql

bool(x) -> bool

Returns True when the argument x is true, False otherwise.
The builtins True and False are the only two instances of the class bool.
The class bool is a subclass of the class int, and cannot be subclassed.

* is_sql_view

bool(x) -> bool

Returns True when the argument x is true, False otherwise.
The builtins True and False are the only two instances of the class bool.
The class bool is a subclass of the class int, and cannot be subclassed.

* join

Wait until the thread terminates.

        This blocks the calling thread until the thread whose join() method is
        called terminates -- either normally or through an unhandled exception
        or until the optional timeout occurs.

        When the timeout argument is present and not None, it should be a
        floating point number specifying a timeout for the operation in seconds
        (or fractions thereof). As join() always returns None, you must call
        isAlive() after join() to decide whether a timeout happened -- if the
        thread is still alive, the join() call timed out.

        When the timeout argument is not present or None, the operation will
        block until the thread terminates.

        A thread can be join()ed many times.

        join() raises a RuntimeError if an attempt is made to join the current
        thread as that would cause a deadlock. It is also an error to join() a
        thread before it has been started and attempts to do so raises the same
        exception.

        

* name

A string used for identification purposes only.

        It has no semantics. Multiple threads may be given the same name. The
        initial name is set by the constructor.

        

* run

* setDaemon

* setName

* start

Start the thread's activity.

        It must be called at most once per thread object. It arranges for the
        object's run() method to be invoked in a separate thread of control.

        This method will raise a RuntimeError if called more than once on the
        same thread object.

        

Model.Authorization
-------------------

Namespace for models supporting authorization policies.

Properties:

* **table name** : No table

Attributes, methods and class methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* add_in_table_args

list() -> new empty list
list(iterable) -> new list initialized from iterable's items

* hybrid_property_columns

list() -> new empty list
list(iterable) -> new list initialized from iterable's items

* is_sql

bool(x) -> bool

Returns True when the argument x is true, False otherwise.
The builtins True and False are the only two instances of the class bool.
The class bool is a subclass of the class int, and cannot be subclassed.

* is_sql_view

bool(x) -> bool

Returns True when the argument x is true, False otherwise.
The builtins True and False are the only two instances of the class bool.
The class bool is a subclass of the class int, and cannot be subclassed.

Model.Documentation
-------------------

Properties:

* **table name** : No table

Attributes, methods and class methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* _auto_doc

* _toRST

* add_in_table_args

list() -> new empty list
list(iterable) -> new list initialized from iterable's items

* auto_doc

* auto_doc_blok

* auto_doc_model

* chapter2RST

* footer2RST

* header2RST

* hybrid_property_columns

list() -> new empty list
list(iterable) -> new list initialized from iterable's items

* is_sql

bool(x) -> bool

Returns True when the argument x is true, False otherwise.
The builtins True and False are the only two instances of the class bool.
The class bool is a subclass of the class int, and cannot be subclassed.

* is_sql_view

bool(x) -> bool

Returns True when the argument x is true, False otherwise.
The builtins True and False are the only two instances of the class bool.
The class bool is a subclass of the class int, and cannot be subclassed.

* toRST

* toRST_blok

* toRST_model

* toSQL

* toUML

Model.Documentation.Blok
------------------------

Properties:

* **table name** : No table

Attributes, methods and class methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* add_in_table_args

list() -> new empty list
list(iterable) -> new list initialized from iterable's items

* exist

* filterBloks

* footer2RST

* getelements

* header2RST

* hybrid_property_columns

list() -> new empty list
list(iterable) -> new list initialized from iterable's items

* is_sql

bool(x) -> bool

Returns True when the argument x is true, False otherwise.
The builtins True and False are the only two instances of the class bool.
The class bool is a subclass of the class int, and cannot be subclassed.

* is_sql_view

bool(x) -> bool

Returns True when the argument x is true, False otherwise.
The builtins True and False are the only two instances of the class bool.
The class bool is a subclass of the class int, and cannot be subclassed.

* toRST

* toRST_get_field

* toRST_write_params

Model.Documentation.Model
-------------------------

Properties:

* **table name** : No table

Attributes, methods and class methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* _auto_doc

* _toRST

* add_in_table_args

list() -> new empty list
list(iterable) -> new list initialized from iterable's items

* exist

* filterModel

* footer2RST

* get_all_models

* getelements

* header2RST

* hybrid_property_columns

list() -> new empty list
list(iterable) -> new list initialized from iterable's items

* is_sql

bool(x) -> bool

Returns True when the argument x is true, False otherwise.
The builtins True and False are the only two instances of the class bool.
The class bool is a subclass of the class int, and cannot be subclassed.

* is_sql_view

bool(x) -> bool

Returns True when the argument x is true, False otherwise.
The builtins True and False are the only two instances of the class bool.
The class bool is a subclass of the class int, and cannot be subclassed.

* toRST

* toRST_docstring

* toRST_field

* toRST_method

* toRST_properties

* toRST_properties_get

* toSQL_add_fields

* toSQL_add_table

* toUML_add_attributes

* toUML_add_model

Model.Documentation.Model.Field
-------------------------------

Properties:

* **table name** : No table

Attributes, methods and class methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* add_in_table_args

list() -> new empty list
list(iterable) -> new list initialized from iterable's items

* exist

* filterField

* footer2RST

* getelements

* header2RST

* hybrid_property_columns

list() -> new empty list
list(iterable) -> new list initialized from iterable's items

* is_sql

bool(x) -> bool

Returns True when the argument x is true, False otherwise.
The builtins True and False are the only two instances of the class bool.
The class bool is a subclass of the class int, and cannot be subclassed.

* is_sql_view

bool(x) -> bool

Returns True when the argument x is true, False otherwise.
The builtins True and False are the only two instances of the class bool.
The class bool is a subclass of the class int, and cannot be subclassed.

* mappers

dict() -> new empty dictionary
dict(mapping) -> new dictionary initialized from a mapping object's
    (key, value) pairs
dict(iterable) -> new dictionary initialized as if via:
    d = {}
    for k, v in iterable:
        d[k] = v
dict(**kwargs) -> new dictionary initialized with the name=value pairs
    in the keyword argument list.  For example:  dict(one=1, two=2)

* toRST

* toRST_docstring

* toRST_properties

* toRST_properties_get

* toSQL

* toSQL_column

* toSQL_field

* toSQL_relationship

* toUML

* toUML_column

* toUML_field

* toUML_relationship

Model.Documentation.Model.Attribute
-----------------------------------

Properties:

* **table name** : No table

Attributes, methods and class methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* add_in_table_args

list() -> new empty list
list(iterable) -> new list initialized from iterable's items

* exist

* filterAttribute

* footer2RST

* getelements

* header2RST

* hybrid_property_columns

list() -> new empty list
list(iterable) -> new list initialized from iterable's items

* is_sql

bool(x) -> bool

Returns True when the argument x is true, False otherwise.
The builtins True and False are the only two instances of the class bool.
The class bool is a subclass of the class int, and cannot be subclassed.

* is_sql_view

bool(x) -> bool

Returns True when the argument x is true, False otherwise.
The builtins True and False are the only two instances of the class bool.
The class bool is a subclass of the class int, and cannot be subclassed.

* toRST

* toRST_docstring

* toUML

Model.Example
-------------

 Example Model, see more column field
    http://anyblok.readthedocs.io/en/latest/MEMENTO.html#column
    

Properties:

* **table name** : example

Fields
~~~~~~

* id

 **code** (example.id),  **model** (Model.Example),  **label** (Id),  **ftype** (Integer),  **entity_type** (Model.System.Column),  **autoincrement** (True),  **foreign_key** (None),  **primary_key** (True),  **unique** (None),  **nullable** (False),  **remote_model** (None)

* name

 **code** (example.name),  **model** (Model.Example),  **label** (Name),  **ftype** (String),  **entity_type** (Model.System.Column),  **autoincrement** (False),  **foreign_key** (None),  **primary_key** (False),  **unique** (True),  **nullable** (False),  **remote_model** (None)

Attributes, methods and class methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* _format_field

* add_in_table_args

list() -> new empty list
list(iterable) -> new list initialized from iterable's items

* define_mapper_args

* define_table_args

* expire

 Expire the attribute of the instance, theses attributes will be
        load at the next  call of the instance

        see: http://docs.sqlalchemy.org/en/latest/orm/session_api.html
        #sqlalchemy.orm.session.Session.expire
        

* expire_relationship_mapped

 Expire the objects linked with this object, in function of
        the mappers definition
        

* expunge

Expunge the instance in the session

* find_relationship

* find_remote_attribute_to_expire

* getFieldType

Return the type of the column

        ::

            TheModel.getFieldType(nameOfTheColumn)

        this method take care if it is a polymorphic model or not

        :param name: name of the column
        :rtype: String, the name of the Type of column used
        

* get_hybrid_property_columns

* hybrid_property_columns

list() -> new empty list
list(iterable) -> new list initialized from iterable's items

* id

* is_sql

bool(x) -> bool

Returns True when the argument x is true, False otherwise.
The builtins True and False are the only two instances of the class bool.
The class bool is a subclass of the class int, and cannot be subclassed.

* is_sql_view

bool(x) -> bool

Returns True when the argument x is true, False otherwise.
The builtins True and False are the only two instances of the class bool.
The class bool is a subclass of the class int, and cannot be subclassed.

* metadata

A collection of :class:`.Table` objects and their associated schema
    constructs.

    Holds a collection of :class:`.Table` objects as well as
    an optional binding to an :class:`.Engine` or
    :class:`.Connection`.  If bound, the :class:`.Table` objects
    in the collection and their columns may participate in implicit SQL
    execution.

    The :class:`.Table` objects themselves are stored in the
    :attr:`.MetaData.tables` dictionary.

    :class:`.MetaData` is a thread-safe object for read operations.
    Construction of new tables within a single :class:`.MetaData` object,
    either explicitly or via reflection, may not be completely thread-safe.

    .. seealso::

        :ref:`metadata_describing` - Introduction to database metadata

    

* name

* refresh

 Expire and reload all the attribute of the instance

        See: http://docs.sqlalchemy.org/en/latest/orm/session_api.html
        #sqlalchemy.orm.session.Session.refresh
        

