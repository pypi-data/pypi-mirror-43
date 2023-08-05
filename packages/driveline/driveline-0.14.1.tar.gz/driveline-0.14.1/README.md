# Driveline Python SDK


At the core of the Python SDK is the class `DrivelineClient`.

```python
import asyncio

from driveline import DrivelineClient, run_async

async def main():
    async with DrivelineClient('ws://127.0.0.1:8080') as client:
    
        # list all streams
        async for stream_name in await client.list_streams('*'):
            print('found stream:', stream_name)
            
        # list all keys is the document store
        async for key_name in await client.list_keys('*'):
            print('found document with key', key_name)
            
            
        # store a document in the document store
        await client.store('key/1', dict(title='Welcome', body='Hello, world!'))
        
        # load a key from the document store
        future_record = await client.load('key/1')
        record = await future_record
        print('document associated with key/1 is:', record.record, 'id:', record.record_id)
            
        # remove all records in the document store with keys matching 'key/...'
        await client.removeMatches('key/*')
        
        # run a live query against a stream. 
        # We want all records that have an odd index
        def query_handler(res):
            print('query returned record:', res.record, 'id:', res.record_id)
        query = await client.continuous_query('SELECT * FROM STREAM my_stream where index % 1 == 1', query_handler)
        
        
        # stop the query
        await asyncio.sleep(10)
        await client.cancel(query)
        
        # quit
        await client.close()
        
if __name__ == '__main__':
    run_async(main())
```


# DQL Driveline Query Language

## Query syntax

### Basic syntax

```sql
SELECT <selector> FROM STREAM <stream> [WHERE <expression>]
SELECT * FROM STREAM stream_1
SELECT * FROM STREAM stream_1 WHERE key=value
SELECT time AS t,(2+3) AS five FROM STREAM stream_1 WHERE age BETWEEN 21 AND 25 OR name LIKE 'Joe%'
```

`DQL` supports standard `SQL` query syntax, excluding Joins and
Aggregates. This means `DQL` can be used for all forms of data filtering
and partitioning of data over live streams.

### KV query

```sql
SELECT <selector> FROM <string-key-name-expression> [WHERE <expression>]
SELECT * FROM 'users/*' WHERE color='red'
```

Multi key query is a `DQL` extension that lets you subscribe to multiple
event streams, automatically subscribing to new streams as they form,
based on the stream name expression. Stream name expression use file-system/Pythong `Glob`,
with `?`, `*` and `**` serving as the wildcard match characters.

### ECMAScript Object Notation (JavaScript extensions)

```sql
SELECT {time,name:user.name,phone_number:user.phone.mobile.number,original:{...*}} FROM stream
```

With inputs of the form:

```javascript
{time:123, user: {name:'joe', phone: {mobile: {number:'1-800-123-4567'}}}}
```

Results in:

```javascript
{time:123,name:'joe',phone_number:'1-800-123-4567',original:{time:123,user:phone:{...}}}
```

## Operators

The following table summarizes all language operators in order of
precedence

| Name                                      | Description         | Example                                               | Additional details                                                                                                |
|:------------------------------------------|:--------------------|:------------------------------------------------------|:------------------------------------------------------------------------------------------------------------------|
| `OR`                                      | extended logical OR | `SELECT * FROM STREAM stream WHERE a OR b`            | `if (a) return a; else return b;`                                                                                 |
| `AND`                                     | logical AND         | `SELECT * FROM STREAM stream WHERE a AND b`           | `if (a && b) return true; else return false;`                                                                     |
| `NOT`                                     | logical NOT         | `SELECT * FROM STREAM stream WHERE NOT a`             | `if (a) return false; else return true;`                                                                          |
| `IS [NOT] NULL`                           | Null check          | `SELECT * FROM STREAM stream WHERE a IS NOT NULL`     | `if (null===a) return true; return false;`                                                                        |
| `IN`                                      | Set lookup          | `SELECT * FROM STREAM stream WHERE a IN (1,2,3)`      | All values in paranthesis must be constants                                                                       |
| `BETWEEN`                                 | Compare range       | `SELECT * FROM STREAM stream WHERE a BETWEEN b AND c` | `if (b<c) return (a>=b && a<=c); else return (a>=c && a<=b);`                                                     |
| `=` `>=` `<=` `!=` `>` `<` `!<` `!>` `<>` | Compare             | `SELECT * FROM STREAM STREAM WHERE a <> b`            |                                                                                                                   |
| `LIKE`                                    | Pattern match       | `SELECT * FROM STREAM stream WHERE a like '%b%'`      | `_` stands for single, `%` stands for multi-char match                                                            |
| `+` `-`                                   | Unary plus/minus    | `SELECT * FROM STREAM stream WHERE -5 < +5`           |                                                                                                                   |
| `+` `-`                                   | Addition            | `SELECT * FROM STREAM stream WHERE 1+2=3`             |                                                                                                                   |
| `*` `/` `%`                               | Multiplicative      | `SELECT * FROM STREAM stream WHERE 3%2=1`             |                                                                                                                   |
| `( exp )`                                 | Paranthesis         | `SELECT * FROM STREAM stream WHERE (1+2)*3=9`         |                                                                                                                   |
| `true` `false` `null`                     | Constant            | `SELECT * FROM STREAM stream WHERE true != false`     |                                                                                                                   |
| `-123.45e-1`                              | Numeric constant    |                                                       |                                                                                                                   |
| `'hello'`                                 | String constant     |                                                       | `SELECT * FROM stream WHERE name='joe'`                                                                           |
| `name`                                    | Identifier          | `SELECT name FROM STREAM stream`                      |                                                                                                                   |
| `` `user name` ``                         | Identifier          | ``SELECT `user name` FROM STREAM stream``             | (backticks) Allows using identifier names that are otherwise invalid, e.g., contain invalid characters or symbols |


## Built-in functions

| Name        | Description                                         | Example                                                             |
|:------------|:----------------------------------------------------|:--------------------------------------------------------------------|
| ABS         | Absolute value `float=>float`                       | `SELECT ABS(-5) AS num FROM stream` `{num:5}`                       |
| CEIL        | Rounded up value `float=>float`                     | `SELECT CEIL(4.5) AS num FROM stream` `{num:5}`                     |
| FLOOR       | Rounded down value `float=>float`                   | `SELECT FLOOR(4.5) AS num FROM stream` `{num:4}`                    |
| EXP         | Natural exponent `float=>float`                     | `SELECT EXP(1) AS num FROM stream` `{num:2.718281828459045}`        |
| LN          | Natural logarithm `float=>float`                    | `SELECT LN(2) AS num FROM stream` `{num:0.6931471805599453}`        |
| SQRT        | Square root `float=>float`                          | `SELECT SQRT(9) AS num FROM stream` `{num:3}`                       |
| HASH        | Hash function `any=>uint64`                         | `SELECT HASH('abc') AS num FROM stream` `{num:4952883123889572249}` |
| CHAR_LENGTH | Length of string `string->int32`                    | `SELECT CHAR_LENGTH('abc') AS num FROM stream` `{num:3}`            |
| POSITION    | Index of substring in string `string,string->int32` | `SELECT POSITION('bc' IN 'abc') AS num FROM stream` `{num:2}`       |
| LOCATE      | Index of substring in string `string,string->int32` | `SELECT LOCATE('bc', 'abc') AS num FROM stream` `{num:2}`           |

