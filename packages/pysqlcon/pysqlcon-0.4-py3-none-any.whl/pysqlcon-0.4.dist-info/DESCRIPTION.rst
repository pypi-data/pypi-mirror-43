## Sort of Documentation for the PySQLCon Library

**Dependencies to be installed are**:

1. pyodbc
2. ODBC Driver 13 for SQL Server https://www.microsoft.com/en-us/download/details.aspx?id=53339



First step is to create a connection to the database: 

```python
from pysqlcon import PySQLCon

# The server here can be the IP address of the server which hosts the database, or the domain name
# for example, if the database is on your machine it would be localhost
server = 'someserver'

# The name of the database
database_name = 'dbname'

# The user id/user name for connecting to the database, most people use sa but it can be any user with priviledges to access and modify the database specified above
userid = 'sa'
userpassword = 'somepasswordhere'

# So the database connection is defined as a PySQLCon object which takes in server, database, userid and the user password 
sqlconnection = PySQLCon(server, database_name, userid, userpassword)
```



Second step is to create a session from the connection defined above

```python
from pysqlcon import Session

# session takes in the connection defined
session = Session(sqlconnection)
```



For querying the database, you have to define a Query. This query takes in the following parameters:

- `query`  string:   this is the query you wish to execute. If it is a stored procedure, you specify the name of the stored procedure, but if it is a raw sql query, you specify as it is.
- `query_type` string(optional):  this is the type of query you wish to execute. There are three types basically but the third one might not work, since it hasn't been tested. The three types are raw, sp and file. Raw => a raw sql string like `Select * from users where username='me'` . Sp => a stored procedure defined on the server. File => a file containing a very long sql query. By default, this is set to raw.
- `params` tuple (optional):  the parameters you wish to pass to the query as a tuple.



```python
from pysqlcon import Query

"""
The following scenarios are for selecting information from the database.
"""

# for a raw sql query with default parameters
raw_sql_query = Query("Select * from users")
rows = session.query_select(raw_sql_query)

# for a raw sql query with parameters
raw_query_parameters = Query("Select * from users where email=?", params=('someone@someco.com',))
rows = session.query_select(raw_query_parameters)


# for a stored procedure without parameters
stored_proc_noparams = Query("UsersSelect", query_type="sp")
rows = session.query_select(stored_proc_noparams)

# for a stored procedure with parameters
# example stored procedure which selects a single user from @id parameter
stored_proc_params = Query("UserSelect", query_type="sp", params=(1,))
rows = session.query_select(stored_proc_params)

"""
The following scenarios are for inserting information into the database.
"""
# for a raw sql query with parameters
raw_sql_query = Query("insert into users (email, username, password) values(?, ?, ?)", params=("someone@someco.com", "someusername", "somepassword"))
session.query(raw_sql_query)

# for a stored procedure with parameters
# example stored procedure which inserts a user with parameters @email, @username and @password
stored_proc_params = Query("UserInsert", query_type="sp", params=("someone@someco.com", "someusername", "somepassword"))
rows = session.query_select(stored_proc_params)



```



