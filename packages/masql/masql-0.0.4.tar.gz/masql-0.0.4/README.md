# masql: mysql for humans
![image](https://warehouse-camo.cmh1.psfhosted.org/1912c9df2012392febbfa09e84588bc474d9d010/68747470733a2f2f696d672e736869656c64732e696f2f707970692f6c2f72657175657374732e737667)

Masql is a Non-GMO mysql library for Python, safe for human consumption.

## Install masql
```shell
pip install masql
```

## How to use
Behold, the power of masql

### Get connection
```python
from mysql import Mysql

mysql = Mysql(host='localhost', user='your db user', password='your db password', db='default')
```

### Creat test table and execute the raw sql

table name : test

column name : id, name
```python
mysql.execute_sql("CREATE SCHEMA IF NOT EXISTS `default`;")
table_sql = "CREATE TABLE IF NOT EXISTS test(id   int PRIMARY KEY AUTO_INCREMENT,name varchar(64))charset utf8mb4;"
mysql.execute_sql(table_sql)
```

### Send Dict Data (Strongly Suggested)
Use mysql just like mongo

```python
data = [{key0:value0,key1:value1},{key0:value0,key1:value1}]
```

The keys means column names, the values means the column value you want set.

```python
data = [{'id': 6, 'name': 'test'},
        {'id': 7, 'name': 'test'}]
mysql.insert('test', *data)
mysql.replace('test', *data)
mysql.insert_ignore('test', *data)
```

Another way equal to ```mysql.insert_ignore('test', *data)```

```python

mysql.insert_ignore('test', {'id': 6, 'name': 'test'}, {'id': 7,
                             'name': 'test'})

```

### Send List Data
```python
data = [[value0,value1],[value0,value1]]
```
Since no key values are defined, the first n length columns of the database are taken by default to match the input list.
Where n is the length of the input list.
```python
data = [[4, 'test'], [5, 'test']]
mysql.insert('test', *data)
mysql.replace('test', *data)
mysql.insert_ignore('test', *data)

mysql.close()
```

## More Example
[More Example](https://github.com/mahaoyang/masql/tree/master/mysql/tests)

## Thanks
[pymysql](https://github.com/PyMySQL/PyMySQL)


---






# masql: 给人用的mysql库
![image](https://warehouse-camo.cmh1.psfhosted.org/1912c9df2012392febbfa09e84588bc474d9d010/68747470733a2f2f696d672e736869656c64732e696f2f707970692f6c2f72657175657374732e737667)

适合人类食用的mysql库。优雅、有机、不用再为繁琐的入库操碎心

## 安装

```shell
pip install masql
```

## 如何使用

### 连接
```python
from mysql import Mysql

mysql = Mysql(host='localhost', user='your db user', password='your db password', db='default')
```

### 执行原生sql并创建test表

表名 : test

字段名 : id, name
```python
mysql.execute_sql("CREATE SCHEMA IF NOT EXISTS `default`;")
table_sql = "CREATE TABLE IF NOT EXISTS test(id   int PRIMARY KEY AUTO_INCREMENT,name varchar(64))charset utf8mb4;"
mysql.execute_sql(table_sql)
```

### 入库字典型数据（建议尽量使用该方式）

像mongo一样的使用方法

```python
data = [{key0:value0,key1:value1},{key0:value0,key1:value1}]
```

key表示列名，value表示要设置的列值。

```python
data = [{'id': 6, 'name': 'test'},
        {'id': 7, 'name': 'test'}]
mysql.insert('test', *data)
mysql.replace('test', *data)
mysql.insert_ignore('test', *data)
```

等价于 ```mysql.insert_ignore('test', *data)``` 的写法

```python
mysql.insert_ignore('test', {'id': 6, 'name': 'test'}, {'id': 7,
                             'name': 'test'})

```

### 入库列表型数据
```python
data = [[value0,value1],[value0,value1]]
```
由于没有定义键值，因此默认采用数据库的前n列来匹配输入列表。
其中n为输入列表的长度。
```python
data = [[4, 'test'], [5, 'test']]
mysql.insert('test', *data)
mysql.replace('test', *data)
mysql.insert_ignore('test', *data)

mysql.close()
```

## 更多例子
[More Example](https://github.com/mahaoyang/masql/tree/master/mysql/tests)

## 感谢
[pymysql](https://github.com/PyMySQL/PyMySQL)