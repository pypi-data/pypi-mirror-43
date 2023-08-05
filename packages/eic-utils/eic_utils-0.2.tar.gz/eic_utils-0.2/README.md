# eic_utils
utils for python3

## requirement
1.  python3.x enviroment
2.  python3.x packages:
        pip3 install os, pickle, json, sqlite3
## usage
```bash
pip3 install eic_utils
```
or see <a href="https://github.com/indestinee/eic_utils">here</a>

## components

### class Cache

### class DataBase
require <strong>sqlite</strong>
#### Functions
```python
from eic_utils import *
def __init__(self, path, name, tables)
    ''' 
    @params:
        path(str): path to store
        name(str): database name
        tables(list/dict): consists of one or several dicts
        
        table(dict): keys: 'name', 'attr', 'extra'
            name(str): name of table
            attr(list): each item is a dict
                item(dict): describe a column in table, keys: 'key'(column name), 'db_type'(type)
            extra(list): extra informs
    '''

def dump(self)
    # @save to disk

def execute(self, cmd, *args, dump)
    '''
    @params:
        cmd(str): command
        args(list): params for command
        dump(bool): dump to disk if true else memory only
            *we have two database, one in memory, the other in disk*
            *if you only read from the database, use dump=False, otherwise, dump=True*
    '''

def list_table(self)
    # return a list, table names

def destroy(self)
    # destroy database

def drop_table(self, name)
    '''
    @params:
        name(str): table name
    '''

def add_tabls(self, tables):
    '''
    @params:
        tables(list/dict): same as tables@init
    '''

def add_row(self, table_name, data)
    '''
    @params:
        table_name(str): table name
        data(dict): keys, values for the row
    '''

def del_row(self, table_name, limitation)
    '''
    @params:
        table_name(str): table name
        limitation(dict, None, str): WHERE key_1=value_1, key_2=value_2, ...
    '''

def upd_row(self, table_name, data, limitation)
    '''
    @params:
        table_name(str): table name
        data(dict): keys, values for the row, SET key_1=value_1, key_2=value_2, ...
        limitation(dict, None, str): WHERE key_1=value_1, key_2=value_2, ...
    '''

def select(self, table_name, data, limitation, keys)
    '''
    @params:
        table_name(str): table name
        data(dict): keys, values for the row
        limitation(dict, None, str): WHERE key_1=value_1, key_2=value_2, ...
        keys(str, list): interest of columns
    '''

def count(self, table_name, limitation=None)
    '''
    SELECT COUNT(*) WHERE ...
    '''
```

#### Example
```python
# init 
from eic_utils import *
tables = [{
        'name': 'user',
        'attr': [{
                'key': 'id',
                'db_type': 'INTEGER PRIMARY KEY AUTOINCREMENT',
             }, {
                'key': 'username',
                'db_type': 'TEXT UNIQUE NOT NULL',
            }, {
                'key': 'interest',
                'db_type': 'INTEGER',
            }
        ], 'extra': [
            'FOREIGN KEY (interest) REFERENCES interest(id)',
        ],   
    }, {
        'name': 'interest',
        'attr': [{
                'key': 'id',
                'db_type': 'INTEGER PRIMARY KEY AUTOINCREMENT',
            }, {
                'key': 'description',
                'db_type': 'TEXT UNIQUE NOT NULL'
            }
        ]
    },
]
db = DataBase(path='data', name='mydata.db', tables=tables) # store in ./data/mydata.db
db.add_row('interest', data={'description': 'play soccer'})
db.add_row('interest', data={'description': 'play baseball'})
db.add_row('interest', data={'description': 'swimming'})
data = db.execute('SELECT * FROM interest').fetchall()
print('raw use:', data)
data = db.select('interest', return_dict=True)
print('dict:', data)
data = db.select('interest', return_dict=True, limitation='id<3')
print('id<3, dict:', data)
data = db.select('interest', return_dict=True, limitation={'id': '3'}, keys={'description'})
print('id=3, return name only, dict:', data)
```
![image](https://github.com/indestinee/utils/raw/master/images/database.jpg)

### class ColorfulPrint
#### Color List
black, red (r), green (g), yellow (y), blue (b), magenta, cyan, white (w)

#### Example
from eic_utils import cp
```python
cp('(#[COLOR in Color List])[Your Sentence(#)]')
cp('hi') 			# same as print('hi')
cp('(#g)hi(#)')		# print a green 'hi'
cp('(#g)hi, ops, forgot to reset color to default') # (#) means reset
print('-'*32)

s = cp.trans('(#y)hi(#) ') # cp.trans return str
print(s, end='')
print('is equals to ', end='')
cp('(#y)hi(#)')

print('-'*32)
cp.wrn('this is a warning msg') # print warning with yellow
cp.suc('this is a successful msg') # print warning with green
cp.log('this is a log msg') # print warning with blue
cp.err('this is an (#r)error(#) msg') # print warning with red

print('-'*32)
hint = cp.trans('(#b)input: (#g)', auto_end=False)
x = input(hint)
cp('', end='')

```
![image](https://github.com/indestinee/utils/raw/master/images/colorful_print.jpg)
### class procedure
#### Example
```python
from eic_utils import procedure
with procedure('waiting for 5 sec and overwrite the line', same_line=True) as p:
	time.sleep(5)

with procedure('waiting for 5 sec', same_line=False) as p:
	time.sleep(5)
	p.msg += ' (#g):)(#)'
```
![image](https://github.com/indestinee/utils/raw/master/images/procedure_1.jpg)
![image](https://github.com/indestinee/utils/raw/master/images/procedure_2.jpg)


### base.py
