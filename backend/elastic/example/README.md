# ElasticSearch

## Pre-requirements

- OpenStack RC file and API password obtained and sourced in current shell (see [here](../installation/README.md#client-configuration))
- A Kubernetes cluster created on NeCTAR (see [here](../installation/README.md#elasticsearch))
- Connect to [Campus network](https://studentit.unimelb.edu.au/wifi-vpn#uniwireless) if on-campus or [UniMelb Student VPN](https://studentit.unimelb.edu.au/wifi-vpn#vpn) if off-campus
- Kubernetes cluster is accessible (see [here](../installation/README.md#accessing-the-kubernetes-cluster))
- ElasticSearch is installed (see [here](../installation/README.md#elasticsearch))
- Node.js 16.x to load test data

> Note: the code used here is for didactic purposes only. It has no error handling, no testing, and is not production-ready.

## Accessing the ElasticSearch API and the Kibana User Interface

Before accessing Kubernetes services, an SSH tunnel to the bastion node has to be opened in a different shell and kept open.
In addition, the `openrc` file has to be source and the kubeconfig file put under the `~/.kube` directory (see the READM in
the `installation` folder for more details).

To access services on the cluster, one has to use the `port-forward` command of `kubectl` in a new terminal window.

```shell
kubectl port-forward service/elasticsearch-master -n elastic 9200:9200
```

To access the Kibana user interface, one has to use the `port-forward` command of `kubectl` (another terminal window):

```shell
kubectl port-forward service/kibana-kibana -n elastic 5601:5601
```

> Note: Thess commands will start the port forwarding so please keep the terminals open and do not close it.
> Note: The port forwarding can be stopped by pressing `Ctrl + C` and closing the terminal window. The port forwarding is only active when the terminal window is open. Once it is stopped, you need to re-run the command to start the port forwarding again.


Test the ElasticSearch API:

```shell
curl -k 'https://127.0.0.1:9200/_cluster/health' --user 'elastic:elastic' | jq '.'
```

Test the Kibana user interface by pointing the browser to: `http://127.0.0.1:5601/` (the default credentials are `elastic:elastic`).

## Create an ElasticSearch Index

```shell
curl -XPUT -k 'https://127.0.0.1:9200/students'\
   --header 'Content-Type: application/json'\
   --data '{
    "settings": {
        "index": {
            "number_of_shards": 3,
            "number_of_replicas": 1
        }
    },
    "mappings": {
        "properties": {
            "id": {
                "type": "keyword"
            },
            "name": {
                "type": "text"
            },
            "course": {
                "type": "text"
            },
            "mark": {
                "type": "short"
            }
        }
    }
}'\
   --user 'elastic:elastic' | jq '.'
```

The index should now be shown in the Kibana dashboard ("Management / Index management"). To be able to see indexes in 
Kibana, they have to be added as a data view.

Let's add some documents to the newly created index:
```shell
curl -XPUT -k "https://127.0.0.1:9200/students/_doc/1234567"\
  --header 'Content-Type: application/json'\
  --data '{
        "name": "John Smith",
        "course": "Cloud Computing",
        "mark": 80
  }'\
  --user 'elastic:elastic' | jq '.'

curl -XPUT -k "https://127.0.0.1:9200/students/_doc/0123456"\
  --header 'Content-Type: application/json'\
  --data '{
        "name": "Jane Doe",
        "course": "Cloud Computing",
        "mark": 90
    }'\
  --user 'elastic:elastic' | jq '.'
```

You can now do a full text search by just typing "John" in the search box and pressing enter.

Let's do a search via the API:

```shell
curl -XGET -k "https://127.0.0.1:9200/students/_search"\
  --header 'Content-Type: application/json'\
  --data '{
      "query": {
        "match": {
          "course": "cloud"
        }
      }
    }'\
  --user 'elastic:elastic' | jq '.'
```

(Note that, since "course" is a "text" field, it is case-insensitive and regexp can be used.)

## Create a data view from Kibana

Go to Kibana (Management / Kibana / Data views) , create a data view named "students" with pattern "student*", and check that the documents have been
added to the index by going to "Analysis / Discover".

Now Kibana can be used to test search queries or to have a look at data.
In Kibana, go to "Discover" and select the "students" data view. Create the KQL expressione `course : "cloud"`,
two documents should be returned (the expression language used in the Discover tab of Kibana is neither SQL nor Query DSL, but KQL).


## ElasticSearch parent-child join

To avoid repeating data about the course, it is possible to create a parent-child relationship between the student and the course.
with some limitations.

Create a `coursesstudents` database with a mapping that defines the parent-child relationship:
```shell
curl -XPUT -k 'https://127.0.0.1:9200/coursesstudents' \
  --header 'Content-Type: application/json' \
  --data '{
    "settings": {
        "index": {
            "number_of_shards": 3,
            "number_of_replicas": 1
        }
    },
    "mappings": {
        "properties": {
            "name": {
                "type": "text"
            },
            "mark": {
                "type": "short"
            },
            "coursedescription": {
                "type": "text"
            },
            "relation_type": {
                "type": "join",
                "relations": {
                    "course": "student"
                }
            }
        }
    }
}' \
  --user 'elastic:elastic' | jq '.'
```
Let's insert some data about courses and students that use the parent-child relationship:

```shell
curl -XPUT -k "https://127.0.0.1:9200/coursesstudents/_doc/comp90024?routing=comp"\
  --header 'Content-Type: application/json'\
  --data '{
        "name": "COMP90024",
        "coursedescription": "Cloud Computing",
        "relation_type": {
          "name": "course"
        }
    }'\
  --user 'elastic:elastic' | jq '.'

curl -XPUT -k "https://127.0.0.1:9200/coursesstudents/_doc/1234567?routing=comp"\
  --header 'Content-Type: application/json'\
  --data '{
        "name": "John Smith",
        "mark": 80,
        "relation_type": {
          "name": "student",
          "parent": "comp90024"
        }
  }'\
  --user 'elastic:elastic' | jq '.'

curl -XPUT -k "https://127.0.0.1:9200/coursesstudents/_doc/0123456?routing=comp"\
  --header 'Content-Type: application/json'\
  --data '{
        "name": "Jane Doe",
        "mark": 90,
        "relation_type": {
          "name": "student",
          "parent": "comp90024"
        }
      }'\
  --user 'elastic:elastic' | jq '.'
```

NOTE: the "routing" parameter has to be added so that all children are in the same shard as their parent.

Example of a query that returns all students of course whose description contains "computing" hat have a mark greater than 80:

```shell
curl -XGET -k "https://127.0.0.1:9200/coursesstudents/_search"\
  --header 'Content-Type: application/json'\
  --data '{
    "query": {
        "bool": {
            "must": [
                {
                    "range": {
                        "mark": {
                            "gt": 80
                        }
                    }
                },
                {
                    "has_parent": {
                        "parent_type": "course",
                        "query": {
                            "match": {
                                "coursedescription": "computing"
                            }
                        }
                    }
                }
            ]
        }
    }
}'\
  --user 'elastic:elastic' | jq '.'
```

## Use of ElasticSearch as a vector DBMS

### Data setup

Let's create an ElasticSearch Index to hold temperatures (it uses dynamic mapping):
```shell
curl -XPUT -k 'https://127.0.0.1:9200/temperatures'\
   --header 'Content-Type: application/json'\
   --data '{
    "settings": {
        "index": {
            "number_of_shards": 3,
            "number_of_replicas": 1
        }
    },
    "mappings": {
        "properties": {
            "date": {
                "type": "date"
            },
            "temperature": {
                "type": "dense_vector",
                "dims": 24,
                "index": true,
                "similarity": "cosine",
                "index_options": {
                    "type": "hnsw",
                    "m": 16,
                    "ef_construction": 100
                }
            }
        }
    }
}'\
   --user 'elastic:elastic' | jq '.'
```

Load temperatures data as vectors in the index (temperatures are expressed in Kelvins):
```shell
(
  cd elastic
  node loadTemperature.js
)
```

### Vector search

Search for the most similar temperature vector to a vector of typical Vancouver temperatures in the month of January (expressed in Kelvin).

```shell
curl -XGET -k "https://127.0.0.1:9200/temperatures/_search"\
  --header 'Content-Type: application/json'\
  --data '{
  "knn": {
    "field": "temperature",
    "query_vector": [274.62,275.18,275.9,276.74,277.65,278.56,279.4,280.12,280.68,281.03,281.15,281.03,280.68,280.12,279.4,278.56,277.65,276.74,275.9,275.18,274.62,274.27,274.15,274.27],
    "k": 3,
    "num_candidates": 100
  },
  "fields": [ "date" ]
}'\
  --user 'elastic:elastic' | jq '.'
```

## Use of Kibana to test queries

Create  a data view out of the "temperatures" index on Kibana (select "date" as timestamp field). 
Go to "Dev Tools / Console" and try the following queries:

Match partial strings:
```shell
POST /_sql?format=txt
{
 "query": "SELECT * FROM students WHERE MATCH(course, 'computing')"
}
```

Histogram query with CASTing of a text field to a timestamp:
```shell
POST /_sql?format=txt
{
 "query": "SELECT HISTOGRAM(CAST(date AS TIMESTAMP), INTERVAL 1 MONTH) AS D, COUNT(*) AS N FROM temperatures GROUP BY D"
}
```

### Use Kibana to convert queries from SQL to Query DSL

Change the endpoint of thw query to `POST /_sql/translate` and execute it: the result will be the equivalent Query DSL query.


### Use of Kibana to browse data

When there is a timestamp in your data, as it is the case for the `temperatures` index, you can use Kibana to select data easily by time range
(the "temperatures" index contains data from 2012, hence you have to select an appropriate time range).


## Removal of indexes

To remove the data views in Kibana, go to "Management / Kibana / Data views" and delete the data views you want to remove.

To remove the indexes created in this workshop, use the following commands:

```shell
curl -XDELETE -k 'https://127.0.0.1:9200/students' --user 'elastic:elastic' | jq '.'
curl -XDELETE -k 'https://127.0.0.1:9200/coursesstudents' --user 'elastic:elastic' | jq '.'
curl -XDELETE -k 'https://127.0.0.1:9200/temperatures' --user 'elastic:elastic' | jq '.'
```


