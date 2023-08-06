# Cocktail ApiKit

A collection of tools which will be used in all new API project, which including: Bottle, marshmallow, mongo and aws

## Usage Example

### 1. Install cocktail apikit
```
pip install cocktail-apikit
```

### 2. Create a demo project

```python

### 1. create a global scope configuration file "settings.py"

from cocktail_apikit import DefaultSettings
class Settings(DefaultSettings):

    # specify configuration file names to load configuration from file
    # Be aware, any configuration fields in configuration file should be 
    # declare in the settings class  or any its super class, just 
    # to make us have better IDE auto-complete help
    _config_files = ['config/database.ini']
    


### 2. create an application file 'application.py' included api endpoints

import uuid 
from settings import Settings
from bottle import request, default_app
from marshmallow import fields 

from cocktail_apikit import (
    ResourcePlugin, FlexibleJsonPlugin, route_mark, BaseSchema, ValidationError, APP_ERROR_HANDLER, MongoDBManager, CorsPlugin, enable_cors,
    BottleMongoQueryBuilder, Pagination
)



class DemoSchema(BaseSchema):
    name = fields.Str()


demo_db = MongoDBManager(Settings.mongo_db_config('demo')) # specify a Config option name or be the given name
demo_schema = DemoSchema()

class DemoResource(ResourcePlugin):

    # a simple demo endpoint
    @route_mark('/index')
    def index(self):
        return 'hello cocktail apikit'

    @route_mark('/demos')
    @enable_cors # allow cors for endpoint
    def list_demo(self):

        mongo_query_builder = BottleMongoQueryBuilder(request, demo_schema)
        mongo_query = mongo_query_builder.to_mongo_query()
        results, count = demo_db.filter(mongo_query)
        pagination = Pagination(mongo_query, results, count)
        return pagination.serialize(demo_schema)


    @route_mark('/demos', 'POST')
    def create_demo(self):
        payload = request.json
        cleaned_obj, errors = demo_schema.load(payload)
        if errors:
            raise ValidationError(errors)

        created_ids, errors = demo_db.create(cleaned_obj)

        if errors:
            raise ValidationError(errors)

        return {
            "ids": created_ids 
        }


app  = default_app()

app.install(FlexibleJsonPlugin())


app.install(DemoResource())
app.install(CorsPlugin())

#config application object's error handlers
app.error_handler = APP_ERROR_HANDLER

if __name__ == "__main__":
    app.run(port=8000, debug=True, reloader=True)

### 3 Then we can run 'python application.py', and access 
# GET  http://localhost:8000/demos: fetch all demos
# POST http://localhost:8000/demos: crate demo

```


