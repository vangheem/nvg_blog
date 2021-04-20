---
layout: post
title: 'Proposal: Federated OpenAPI Gateway'
date: 2021-04-19 10:30:00
categories: open-source REST OpenAPI gateway
description: Let's build a Federated OpenAPI Gateway
published: true
---

# Proposal: Federated OpenAPI Gateway

Apollo has this great project to build [federated GraphQL services](https://www.apollographql.com/docs/federation/).
It allows you to build many GraphQL services that get consolidated together into one service.
It also allows you to do something really neat--you can build you services
together so that some act as a sort of "foreign key" join on data.
It is a great tool to build de-coupled micro-services without
needing to build composition services.

Now, why isn't there anything like this for OpenAPI/REST?

Imagine having many services defining different endpoints all behind a gateway
to combine and consolidate them into one cohesive service.

![High Level](/assets/posts/openapi-gw/openapi-gw-high-level.png)

Where, as long as each service provides their own OpenAPI definitions, the gateway will
present one cohesive API.

User Service:

```json
{
  "paths": {
    "/users/{user_id}": {
      "get": {
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "schema": { "$ref": "#/components/schemas/User" }
              }
            }
          }
        }
      }
    }
  },
  "components": {
    "schemas": {
      "User": {
        "type": "object",
        "properties": {
          "name": { "type": "string" }
        }
      }
    }
  }
}
```

Review Service:

```json
{
  "paths": {
    "/users/{user_id}": {
      "get": {
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "schema": { "$ref": "#/components/schemas/User" }
              }
            }
          }
        }
      }
    }
  },
  "components": {
    "schemas": {
      "User": {
        "type": "object",
        "properties": {
          "reviews": {
            "type": "array",
            "items": { "$ref": "#/components/schemas/Review" }
          }
        }
      },
      "Review": {
        "type": "object",
        "properties": {
          "body": { "type": "string" },
          "product": { "$ref": "#/components/schemas/Product" }
        }
      }
    }
  }
}
```

Product Service:

```json
{
  "paths": {
    "/products/{product_id}": {
      "get": {
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "schema": { "$ref": "#/components/schemas/Product" }
              }
            }
          }
        }
      }
    }
  },
  "components": {
    "schemas": {
      "Product": {
        "type": "object",
        "properties": {
          "id": { "type": "string" },
          "name": { "type": "string" }
        }
      }
    }
  }
}
```

Which would output one OpenAPI and service that provides:

```json
{
  "paths": {
    "/users/{user_id}": {
      "get": {
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "schema": { "$ref": "#/components/schemas/User" }
              }
            }
          }
        }
      }
    },
    "/products/{product_id}": {
      "get": {
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "schema": { "$ref": "#/components/schemas/Product" }
              }
            }
          }
        }
      }
    }
  },
  "components": {
    "schemas": {
      "User": {
        "type": "object",
        "properties": {
          "name": { "type": "string" },
          "reviews": {
            "type": "array",
            "items": { "$ref": "#/components/schemas/Review" }
          }
        }
      },
      "Review": {
        "type": "object",
        "properties": {
          "body": { "type": "string" },
          "product": { "$ref": "#/components/schemas/Product" }
        }
      },
      "Product": {
        "type": "object",
        "properties": {
          "id": { "type": "string" },
          "name": { "type": "string" }
        }
      }
    }
  }
}
```

And a `GET` request to `/users/1` would then respond with:

```
{
  "name": "Foo bar",
  "reviews": [{
    "body": "Mario rocks",
    "product": {
      "id": "1",
      "name": "Nintendo"
    }
  }, {
    "body": "Sonic is better",
    "product": {
      "id": "2",
      "name": "Sego"
    }
  }]
}
```

Behind the scenes the following requests would then be made:

- User service: `GET /users/1`
- Reviews service: `GET /users/1`
- Products service: `GET /products/1` and `GET /products/2`

There are many different ways to build it; however, the above
examples are a simple way it could work.

# Harder problems

1. One of the advantages of GraphQL is you only get back what you ask for.
   An approach for OpenAPI would probably need to implement some sort of
   `?include=reviews,reviews.product` implementation in order to return the data you want. Otherwise, the fan-out could be quite bad.
2. GraphQL is built for running multiple operations at a time. This allows
   developers to leverage data loader patterns to alleviate fan-out problems.
   It's possible similar multi-operation endpoints would need to be
   available to downstream services in order to solve this.
3. Error handling. Federated GraphQL already has issues
   with this(no http status codes); however, I can see issues where one
   service responds correctly but another does not. What happens if
   a "foreign" key does not return a value?
