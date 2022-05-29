# mini api

the api access a postgres database, connection parameters are stored in a database.ini file with a content similar to the following:
```
[postgresql]
host=localhost
database=mydb
user=myuser
password=mypassword
```

a initial test db can be created using the ```fill_test.sql``` file

the api is contained in the file ```api.py``` and uses flask as the web framework.
