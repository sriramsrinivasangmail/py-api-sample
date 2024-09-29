# py-api-sample

## Introduction

The goal here is to use an example to describe how best to use an OpenAPI yaml as the _source_ for your interfaces and incrementally enhance by introducing new endpoints or expanding the data models without overwriting existing code. Essentially "API first" design with the OpenAPI spec as the master reference to the interfaces exposed.

It is typical for developers to generate OpenAPI specs after development as a form of documentation or even use the OpenAPI spec just once, generate boilerplate code, but abandon it later on and simply introduce changes by manually coding everything. 

In this example, you will see, via a sample "micro-service" container  what it means to generate code from  an ever-changing API spec while retaining existing code. To that end, even the source code generated from the OpenAPI spec is not persisted [see .gitignore](.gitignore)- but is generated whenever there is a build, using the spec YAML as the source of truth. 

We would only want for a developer to focus on the "handler" implementation functions of the endpoints in a [library module](./app/src/aroma_lib/) and not need have them code the mechanisms to expose the interface or stand up a micro-service. As a bonus, you get very well defined interfaces from the start.


## Description 

a) [The OpenAPI spec](./app/src/api/aroma-api.yaml) used in this example includes the endpoints, schema and other artifacts that identify the interface this service will expose.
-  Note the assignment of one `tag` representing each entity,for every path, such as the [customer tag](./app/src/api/aroma-api.yaml#L95). This unique tag will define the endpoint FastAPI routes as well as follow our own set of conventions to invoke the actual implementation functions that handle those routes.

b) [./app/bin/generate.sh](./app/bin/generate.sh) leverages [fastapi-code-generator](https://github.com/koxudaxi/fastapi-code-generator) to generate python fastAPI code from the OpenAPI spec. This example also leverages a set of [router based templates](./app/src/api/templates) to customize the generated python code and fastAPI routing modules including the invocation of the handler functions in a [library](./app/src/aroma_lib).

c) **Code layout**: All source is under [./app/src/](./app/src) and the container's [PYTHONPATH is set appropriately](./Dockerfile#L14)

- the OpenAPI spec is under [/app/src/api/](./app/src/api/)

- all generated code will land in a module called [generated](./app/src/generated/) under the [the root src directory](./app/src). 

- all handcrafted implementation should be in a [library module](./app/src/aroma_lib/)

d) [./build.sh](./build.sh) is used to generate the code from the OpenAPI spec and build a Docker image.

e) [./test-run.sh](./test-run.sh) is used to stand up the container and expose port 20080 to invoke the endpoints. The [run-service.sh entrypoint](./app/bin/run_service.sh) is a script that brings up the _generated_ `main.py` which sets up the routes etc. and serves the app using  `uvicorn` at port 20080.

f) [./dev-in-container.sh](./dev-in-container.sh) is used to stand up a container and land you in a bash prompt with this entire repository mounted withe source code available at `/app/src`. `vim` is also included for you develop or fine tune inside the container. You can also test out the ./generate.sh script and use `./app/bin/run_service.sh &` to stand up the service in an isolated fashion inside the container. `curl` is available to try out the `http://localhost:20080` routes.  

- For example:  

    `curl http://localhost:20080` 

    `curl http://localhost:20080/healthz` 

    `curl http://localhost:20080/coffees` 

    `curl http://localhost:20080/coffees/dummy` 

    `curl http://localhost:20080/orders/0000-6789-2345`

**warning**: As this repo is just a way to outline an _approach_ to developing a FastAPI based microservice, there isn't really much in terms of an implementation here - and most of the functions in the [library](./app/src/aroma_lib) do not even exist.

### Implementing library functions to handle endpoints

> i.e, how does the generated FastAPI routes know which of your hand crafted functions to call ?

- This example uses fastapi-code-generator [templates](./app/src/api/templates) to hook up the implementation library to the fastAPI routes.

- Our approach is to place the handlers inside the [library](./app/src/aroma_lib), using this naming convention: `<tag>_impl.py`. For example, the functions to handle the `order` endpoints would be in [./app/src/aroma_lib/order_impl.py](./app/src/aroma_lib/order_impl.py).

- The [`{{tag}}_impl.{{operation.function_name}}`](./app/src/api/templates/routers.jinja2#L46) jinja2 template causes that particular endpoint to invoke a specifically named library function.

For example, for the `coffee` tag, this results in:

a) `from aroma_lib import coffee_impl`  - [from the template here](./app/src/api/templates/routers.jinja2#L11)

b) For a generated route function such as:

```
@router.get('/coffees/{name}', response_model=Coffee, tags=['coffee'])
def get_coffee_by_name(name: str) -> Coffee:
```

in [the generated coffee route](./app/src/generated/routers/coffee.py), 

the function `coffee_impl.get_coffee_by_name(**locals())` from the library module is invoked. `locals()` is to indicate that all arguments passed into the generated route is passed as-is to the real implementation.  The expectation is that the function in the library returns `Coffee` as well [as seen in app/src/aroma_lib/coffee_impl.py](./app/src/aroma_lib/coffee_impl.py#L39). 

- The use of this template ensures that a subsequent generation of the FastAPI boilerplate code continues the convention of importing and invoking the library function.

Similarly,  [order_impl.py in the library](https://github.com/sriramsrinivasangmail/py-api-sample/blob/main/app/src/aroma_lib/order_impl.py#L6) is invoked from a ['order'](./app/src/generated/routers/order.py) generate route function.

### OpenAPI schema components are pydantic models 

The schema elements are also generated from the spec and are implemented as Classes in [./app/src/generated/models.py](./app/src/generated/models.py). 

For example there is a `class Coffee`  and even a `class Status(Enum)` for enumerations.

Since, these land under the [generated](./app/src/generated/) module, you can see them being imported in the library implementation, such as [coffee_impl](./app/src/aroma_lib/coffee_impl.py#L4)

### Adding new routes

Lets assume that we want to add another entity called 'inventory' to the OpenAPI spec.  There would also be additional schema components in the spec to describe the 'inventory' entity.

- **important**: make sure to tag each path in the spec with 'inventory'

We will see how to implement our functions in the library to handle the inventory endpoints.

a) Generate the code (easiest inside the 'dev' container) using the 'bin/generate.sh' script

b) You will see additional Classes in the models.py generated file.

c) There will be a new FastAPI route under `src/generated/routers/`  called 'inventory.py'.  This will include an import such as this: `from aroma_lib import inventory_impl`

d) Introduce  `src/aroma_lib/inventory_impl.py` for the endpoint functions.  You need at least a blank .py, otherwise the Service won't even come up. 
- For example [./app/src/aroma_lib/customer_impl.py](./app/src/aroma_lib/customer_impl.py) is empty .. with handlers yet to be implemented.  Of course, invoking the customer related paths will cause a runtime internal server error.

e) Implement each function that the generated route expects to invoke from `inventory_impl`. You can look at the generated `inventory.py` route file to figure out the function's input and output args. inventory_impl will also need to include a few imports , similar to [](./app/src/aroma_lib/order_impl.py##L1)

f) Use `run_service.sh` to start up the micro-service and validate.

---