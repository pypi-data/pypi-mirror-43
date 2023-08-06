# ApiKit

A collection of tools which will be used in all new API project.
These tools including the following parts:

## Bottle

### 1. Plugins
#### 1.1 FlexibleJsonPlugin

Usage:

```python
from datetime import datetime
from decimal import Decimal

from bottle import Bottle, run

from cocktail_apikit import FlexibleJsonPlugin

app = Bottle()
app.install(FlexibleJsonPlugin())

@app.get('/')
def index():
    return {
        'now': datetime.now(),
        'float_number': Decimal(123.4567),
        'int_number': Decimal(4567)
    }

if __name__ == '__main__':
    run(app)
```


#### 1.2 APISpecPlugin

Usage:
```python
from bottle import Bottle, run
from marshmallow import Schema
from marshmallow.fields import String

from cocktail_apikit import APISpecPlugin

app = Bottle()


class MySchema(Schema):
    id = String()
    value = String()


@app.get('/')
def index():
    """API endpoint that return MySchema
    ---
    get:
        description: API endpoint that return MySchema
        responses:
            200:
                description: It works!!!!
                schema: MySchema
    """
    data, error = MySchema.load('id', 'value')
    return data


app.install(APISpecPlugin(
    title='Example API',
    version='1.0.0',
    openapi_version='2.0',
    scan_package='.')
)

run(app)
```

#### 1.3 Cors

Usage:
```python
from bottle import Bottle, request, run
from cocktail_apikit import CorsPlugin, enable_cors

app = Bottle()

@app.get('/')
def index():
    """
    CORS is disabled for this route
    """
    return "cors is disabled here"

@enable_cors
@app.get('/endpoint_1')
def endpoint_1():
    """
    CORS is enabled for this route. 
    OPTIONS requests will be handled by the plugin itself
    """
    return "cors is enabled, OPTIONS handled by plugin"

@enable_cors
@app.route('/endpoint_2', method=['GET', 'POST', 'OPTIONS'])
def endpoint_2():
    """
    CORS is enabled for this route. 
    OPTIONS requests will be handled by *you*
    """
    if request.method == 'OPTIONS':
        # do something here?
        pass
    return "cors is enabled, OPTIONS handled by you!"

app.install(CorsPlugin(origins=['http://list.of.allowed.domains.com', 'https://another.domain.org']))

run(app)
```

#### 1.4 ResourcePlugin

A plugin which implemented class-base view to manage a collection api endpoint

Usage
```python
from bottle import default_app
from cocktail_apikit import  ResourcePlugin, route_mark, FlexibleJsonPlugin, CorsPlugin, APISpecPlugin

app = default_app()

class DriverResource(ResourcePlugin):
    
    @route_mark('/drivers')
    def list_driver(self):
        return {
            'drivers':list(range(10))
        }
        
    @route_mark('/drivers', 'POST')
    def create_driver(self):
        return 'OK'

app.install(DriverResource())

app.install(FlexibleJsonPlugin())
app.install(CorsPlugin())
app.install(APISpecPlugin(title="APIkit", version='1.0', openapi_version='2.0'))

app.run()

``` 

### 2. Utils

#### 2.1 error handlers

Usage:
```python
from bottle import Bottle, run

from cocktail_apikit import  ValidationError, APP_ERROR_HANDLER

app = Bottle()

app.error_handler = APP_ERROR_HANDLER

@app.get('/')
def index():
    raise ValidationError('Test error handler')

run(app)

```


## Marshmallow
### 1. Customized Common Base Schema 

BaseSchema contains 4 common fields which are useful for create new schema, also including a classmethod call 'valid_mongo_query_fields' to fetch all valid mongo-style query fields
 
### 2. Customized Fields

## MongoDB
### 1. Customized Mongo Client 

## AWS
### 1. Customized AWS S3 Client

## Settings
A project scope global setting object where contains all system configurations, 
In this apikit we have a DefaultSettings, however we can customize any other configurations by extend this class.

Usage:
```python
from cocktail_apikit import DefaultSettings
from cocktail_apikit import MongoDBManager

class MySettings(DefaultSettings):
    API_DEFAULT_LIMIT = 50 # change the default api return from default 20 to 50
    
    MONGODB_URI = 'localhost:27017'
    MONGO_DATABASE = {
        "DOCUMENTATION": {
            "development":{
                "DB_ANME":"development_document_db" ,
                "COLLECTION_NAME":"document"
            },
            "test":{
                "DB_ANME":"test_document_db" ,
                "COLLECTION_NAME":"document"
            },
            "homolog":{
                "DB_ANME":"homolog_document_db" ,
                "COLLECTION_NAME":"document"
            },
            "staging":{
                "DB_ANME":"staging_document_db" ,
                "COLLECTION_NAME":"document"
            },
            "production":{
                "DB_ANME":"development_document_db" ,
                "COLLECTION_NAME":"document"
            }
        }
    }
   
 
 document_bd = MongoDBManager(MySettings.mongo_db_config("DOCUMENTATION"))

```


## Constants
Contains some common constants which are used by current apikit project 
```python


############################################################
# Categories of marshmallow default fields, used to build valid mongo query field names
############################################################
MARSHMALLOW_LIST_FIELDS = (List,)
MARSHMALLOW_NESTED_FIELDS = (Nested,)
MARSHMALLOW_DICT_FIELDS = (Dict,)
MARSHMALLOW_SCALAR_FIELDS = (
    Raw, Constant,
    UUID, String, Str, FormattedString, str,
    Number, Integer, Int, int, Decimal,
    Boolean, Bool, bool,
    Float, float,
    Date, DateTime, LocalDateTime, Time, TimeDelta,
    Email, URL, Url,
    # Function, Method
)


############################################################
# Mongo operator customie mapping
############################################################
MONGO_LOOKUPS_MAPPINGS = {
    'lt': '$lt',
    'lte': '$lte',
    'gt': '$gt',
    'gte': '$gte',
    'in': '$in',
    'regex': '$regex',
    'exists': '$exists',
    'all': '$all',
    'size': '$size',
    'type': '$type',
    'text': '$text',
    'where': '$where',

    # 'elemmatch': '$elemmatch',

    # TODO: there are more other operaters need to introduce here
    # ...
}

############################################################
# Separator which used to separate request's field & operator
############################################################
REQUEST_LOOKUP_MARK = '__'

############################################################
# Mark to indicate sort a field by desc order
############################################################
REQUEST_DESC_SORT_MARK = '-'


############################################################
# Request's query string's constants
############################################################
SORT_KEY = 'sort'
PAGE_KEY = 'page'
LIMIT_KEY = 'limit'

############################################################
# Database constances
############################################################
RECORD_ACTIVE_FLAG_FIELD = '_enabled' # Database record active status
```

## MISCs


