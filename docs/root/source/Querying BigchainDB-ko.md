
.. Copyright BigchainDB GmbH and BigchainDB contributors
   SPDX-License-Identifier: (Apache-2.0 AND CC-BY-4.0)
   Code is Apache-2.0 and docs are CC-BY-4.0

BigchainDB ����
===================

��� operator�� MongoDB�� ���� ������ �ִ� ������ ����Ͽ� ��� Ʈ�����, �ڻ� �� ��Ÿ�����͸� �����Ͽ� ����� ��� �����͸� �˻��ϰ� ������ �� �ֽ��ϴ�.
��� operator�� �ܺ� ����ڿ��� �󸶳� ���� ���� �Ŀ��� �������� ������ ������ �� �ֽ��ϴ�.


���� ������ ���Ե� ��α� �Խù�
------------------------------


BigchainDB ��α׿� MongoDB ������ ����Ͽ� BigchainDB ����� MongoDB �����ͺ��̽��� �����ϴ� ����� ���� �Խù��� �÷Ƚ��ϴ�.

�����Ϳ� ���� �Ϻ� Ư�� ���� ������ �ֿ� �����Դϴ�.
`���⼭ Ȯ���ϼ��� <https://blog.bigchaindb.com/using-mongodb-to-query-bigchaindb-data-3fc651e0861b>`_.

MongoDB�� �����ϱ�
-------------------------


MongoDB �����ͺ��̽��� �����Ϸ��� ���� �����ͺ��̽��� �����ؾ� �մϴ�. �׷��� ���ؼ� ȣ��Ʈ �̸��� ��Ʈ�� �˾ƾ� �մϴ�.

���� �� �׽�Ʈ�� ���� ���� ��ǻ�Ϳ��� BigchainDB ��带 ���� ���� ��� ȣ��Ʈ �̸��� "���� ȣ��Ʈ"���� �ϸ� �̷��� ���� �������� �ʴ� �� ��Ʈ�� "27017"�̾�� �մϴ�. ���� �ý��ۿ��� BigchainDB ��带 ���� ���̸� �ش� �ý��ۿ� SSH�� �� �ִ� ��쿡�� ���������Դϴ�.

���� �ý��ۿ��� BigchainDB ��带 �����ϰ� MongoDB�� auth�� ����ϰ� ���������� �׼����� �� �ֵ��� ������ ���(������ �ִ� ����ڿ���) ȣ��Ʈ �̸��� ��Ʈ�� Ȯ���� �� �ֽ��ϴ�.

�����ϱ�
------------

BigchainDB ��� ��ڴ� ���� MongoDB �ν��Ͻ��� ���� ��ü �׼��� ������ �����Ƿ� �����ϴµ� MongoDB�� ������ API�� ����� �� �ֽ��ϴ�:

- `the Mongo Shell <https://docs.mongodb.com/manual/mongo/>`_,
- `MongoDB Compass <https://www.mongodb.com/products/compass>`_,
- one of `the MongoDB drivers <https://docs.mongodb.com/ecosystem/drivers/>`_, such as `PyMongo <https://api.mongodb.com/python/current/>`_, or
- MongoDB ������ ���� ������Ƽ��,  RazorSQL, Studio 3T, Mongo Management Studio, NoSQLBooster for MongoDB, or Dr. Mongo.

.. note::

    SQL�� �̿��� mongoDB �����ͺ��̽��� ������ �� �ֽ��ϴ�. ���� ���:
   
   * Studio 3T: "`How to Query MongoDB with SQL <https://studio3t.com/whats-new/how-to-query-mongodb-with-sql/>`_"
   * NoSQLBooster for MongoDB: "`How to Query MongoDB with SQL SELECT <https://mongobooster.com/blog/query-mongodb-with-sql/>`_"

���� ��� �⺻ BigchainDB ��带 �����ϴ� �ý��ۿ� �ִ� ���  Mongo Shell (``mongo``)�� ����Ͽ� �����ϰ� ������ ���� �� �� �ֽ��ϴ�.

.. code::

    $ mongo
    MongoDB shell version v3.6.5
    connecting to: mongodb://127.0.0.1:27017
    MongoDB server version: 3.6.4
    ...
    > show dbs
    admin     0.000GB
    bigchain  0.000GB
    config    0.000GB
    local     0.000GB
    > use bigchain
    switched to db bigchain
    > show collections
    abci_chains
    assets
    blocks
    elections
    metadata
    pre_commit
    transactions
    utxos
    validators

�� ������ �� ���� ��Ȳ�� �����ݴϴ�:


* BigchainDB�� �����͸� ``bigchain``.�̶�� �����ͺ��̽��� �����մϴ�.
* ``bigchain` �����ͺ��̽����� ���� `collections<https://docs.mongodb.com/manual/core/databases-and-collections/>`_.�� ���ԵǾ� �ֽ��ϴ�.
* � �÷��ǿ��� ��ǥ�� ������� �ʽ��ϴ�. �̷� �����ʹ� ��� ��ü(LevelDB) �����ͺ��̽��� ���� ó���ǰ� ����˴ϴ�.

�÷��ǿ� ���� ���
---------------------------------------

``bigchain`` �����ͺ��̽��� ���� ��̷ο� �κ��� �Ʒ��� �����ϴ�:

- transactions
- assets
- metadata
- blocks

``db.assets.findOne()`` �� MongoDB ������ ����Ͽ� �̷��� �÷��ǵ��� Ž���� �� �ֽ��ϴ�. 


Ʈ����ǿ� ���� ���
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


transaction �÷��ǿ��� CREATE Ʈ����ǿ��� �߰�  ``"_id"`` �ʵ�(MongoDB�� �߰���)�� ���ԵǸ� ``"asset"``�� ``"metadata"`` �ʵ忡�� �����Ͱ� ����Ǿ� ���� �ʽ��ϴ�.

.. code::

    {  
        "_id":ObjectId("5b17b9fa6ce88300067b6804"),
        "inputs":[��],
        "outputs":[��],
        "operation":"CREATE",
        "version":"2.0",
        "id":"816c4dd7��851af1629"
    }

A TRANSFER transaction from the transactions collection is similar, but it keeps its ``"asset"`` field.

.. code::

    {  
        "_id":ObjectId("5b17b9fa6ce88300067b6807"),
        "inputs":[��],
        "outputs":[��],
        "operation":"TRANSFER",
        "asset":{  
            "id":"816c4dd7ae��51af1629"
        },
        "version":"2.0",
        "id":"985ee697d��a3296b9"
    }

assets�� ���� ���
~~~~~~~~~~~~~~~~~~~~~~~~~~~~


assets�� ���� ������� MongoDB�� �߰��� ``"_id"` �о߿� CREATE �ŷ����� ���� `asset.data`` �׸��� ``"id"``  �� ���� �ֻ��� �о߷� �����Ǿ� �ֽ��ϴ�.
.. code::

    {  
        "_id":ObjectId("5b17b9fe6ce88300067b6823"),
        "data":{  
            "type":"cow",
            "name":"Mildred"
        },
        "id":"96002ef8740��45869959d8"
    }

 metadata�� ���� ���
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

metadata �÷����� ������ MongoDB�� �߰��� ``"ID"`�ʵ�� �ŷ����� ���� `asset.data``�׸��� �ŷ����� ���� ``"ID"`` �� ���� �ֻ��� �о߷� �����Ǿ� �ֽ��ϴ�.

.. code::

    {  
        "_id":ObjectId("5b17ba006ce88300067b683d"),
        "metadata":{
            "transfer_time":1058568256
        },
        "id":"53cba620e��ae9fdee0"
    }

blocks�� ���� 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code::

    {
        "_id":ObjectId("5b212c1ceaaa420006f41c57"),
        "app_hash":"2b0b75c2c2��7fb2652ce26c6",
        "height":17,
        "transactions":[
            "5f1f2d6b��ed98c1e"
        ]
    }

��� operator�� �ܺ��������� ����� ��
-------------------------------------------------

�� ��� operator�� �ܺ� ����ڰ� �ڽ��� ���� MongoDB �����ͺ��̽����� ������ ��� ����� ������ �� �ֽ��ϴ�. :

- �ܺ������� ���� ó���ϴ� ���� MongoDB �����ͺ��̽� �ѵ� ���ѵ� ������ ���� ������ ���� MongoDB ����� ��) read-only
- ���ѵ� �̸� ���ǵ� ���� ������ ����ϴ� ���ѵ� HTTP API(BigchainDB �������� �����ϴ� HTTP API)<http://bigchaindb.com/http-api>`_, Ȥ��Django, Express, Ruby on Rails, or ASP.NET.�� �̿��� ������ Ŀ���� HTTP API 
- �ٸ� API(��: GraphQL API) ��3���� ����� ���� �ڵ� �Ǵ� �ڵ带 ����Ͽ� ������ �� �ֽ��ϴ�..


�� ��� operator�� ���� MongoDB �����ͺ��̽��� ���� �ٸ� ���� �Ǵ� ������ �׼����� ������ �� �ֽ��ϴ�.
���� ���, �� ��� operator�� ����ȭ�� ���� ������ �������� �����ϱ�� ���� �� �ֽ��ϴ�.<https://docs.mongodb.com/manual/reference/operator/query-geospatial/>`_.

���� �������
-----------------------

BigchainDB ���� 1.3.0 ���� ���������� �ϳ���  MongoDB �� �����ͺ��̽��� �־��� ������ �ܺ� ����ڿ��� �����ͺ��̽��� �����ϴ� ���� �ſ� ���������� ������� �ʽ��ϴ�.
"drop database"�� ������ MongoDB �����ͺ��̽��� �����մϴ�.


BigchainDB ���� 2.0.0 �̻󿡼� �� ��忡 ������ ���� ���� MongoDB �����ͺ��̽��� �����մϴ�.
��� �� ����� �Ʒ� �׸� 1������ ���� MongoDB ���������� �ƴ� Tendermint ���������� ����Ͽ� ����˴ϴ�.
����� ���� MongoDB �����ͺ��̽��� �ջ�Ǿ �ٸ� ���� ������ ���� �ʽ��ϴ�.

.. figure:: _static/schemaDB.png
   :alt: Diagram of a four-node BigchainDB 2.0 network
   :align: center
   
   Figure 1: A Four-Node BigchainDB 2.0 Network

.. raw:: html

   <br>
   <br>
   <br>

�����ս� �� ��� �������
-----------------------------------

���� ���μ����� ����� ���� ���ҽ��� �Ҹ��� �� �����Ƿ�, BigchainDB ���� �� Tendermint Core�� ������ ��ǻ�Ϳ��� MongoDB�� �����ϴ� ���� �����ϴ�.

��� operator �� ��ȸ�� ���Ǵ� ���ҽ��� �����Ͽ� ��ȸ�� ��û�� ����� �������� ����� û���� �� �ֽ��ϴ�.

�Ϻ� ������ �ʹ� ���� �ɸ��ų� ���ҽ��� �ʹ� ���� ����� �� �ֽ��ϴ�. ��� operator�� ����� �� �ִ� ���ҽ��� ������ �ΰ�, �ʰ��ȴٸ� ����(�Ǵ� ����)�ؾ� �մϴ�.

MongoDB ������ ���� ȿ�������� ����� ����  _`�ε��� <https://docs.mongodb.com/manual/indexes/>`_�� ���� �� �ֽ��ϴ�.  �̷��� �ε����� ��� operator �Ǵ� �Ϻ� �ܺ� ����ڰ� ������ �� �ֽ��ϴ�(��� ��ڰ� ����ϴ� ���). �ε����� ��� ���� �ʽ��ϴ�. �� �����͸� �÷��ǿ� �߰��� ������ �ش� �ε����� ������Ʈ�ؾ� �մϴ�. ��� ��ڴ� �̷��� ����� �ε����� ������ ������� �����ϰ��� �� �� �ֽ��ϴ�. mongoDB������ ���� �÷����� 64�� ������ �ε����� ���� �� �ֽ��ϴ�.
<https://docs.mongodb.com/manual/reference/limits/#Number-of-Indexes-per-Collection>`_.

One can create a follower node: a node with Tendermint voting power 0. It would still have a copy of all the data, so it could be used as read-only node. A follower node could offer specialized queries as a service without affecting the workload on the voting validators (which can also write). There could even be followers of followers.
Tendermint voting�Ŀ��� 0�� ����� ������ ��带 ������ �� �ִ�. ������ ��� �������� ���纻�� �����Ƿ� �б� ���� ���� ����� �� �ֽ��ϴ�. Follower ���� ��ǥ �������� �۾� ���Ͽ� ������ ��ġ�� �ʰ� ���񽺷� ����ȭ�� ������ ������ �� �ֽ��ϴ�(���⵵ ����). �ȷο��� �ȷο��鵵 ���� �� �ֽ��ϴ�.

�ڹٽ�ũ��Ʈ ���� �ڵ� ����s
------------------------------

���� �� �ϳ��� ����Ͽ� ����� MongoDB �����ͺ��̽��� ������ �� �ֽ��ϴ�.
MongoDB node.js ����̹��� ���� MongoDB ����̹���
<https://mongodb.github.io/node-mongodb-native/?jmp=docs>`_.

���� �ڹٽ�ũ��Ʈ ���� �ڵ忡 ���� ��ũ�� �ֽ��ϴ�

- `The BigchainDB JavaScript/Node.js driver source code <https://github.com/bigchaindb/js-bigchaindb-driver>`_
- `Example code by @manolodewiner <https://github.com/manolodewiner/query-mongodb-bigchaindb/blob/master/queryMongo.js>`_
- `More example code by @manolodewiner <https://github.com/bigchaindb/bigchaindb/issues/2315#issuecomment-392724279>`_
