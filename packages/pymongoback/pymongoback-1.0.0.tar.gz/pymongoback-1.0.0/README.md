# PyMongoBack

**PyMongo** Back is a simple Python library designed to help you create MongoDB Backups from both local and remote servers.


## Install

You can easily install it using the following command:

    sudo pip3 install pymongoback

> In the server that is going to execute the script, it will be necessary to have installed **MongoDB** or  **Mongodb Tools**. Since you need to have installed mongodump.

## Usage

Starting to use PyMongoBack is very simple. You only need to import the library and create an object PyMongoBackup() with the parameters that you prefer.

|Param|Type|Description|
|--|--|--|
|username|str|Username for login MongoDB. Default None.|
|password|str|Password for login MongoDB. Default None.|
|host|str|IP address of the MongoDB server. Default 'localhost'.|
|days_backup|int|Maximum days that are saved backup. Default None (always save).|
|path_backup|str|Path where the backup is saved. Default './BackupMongo'.|
|log|bool|Indicates if the output is written to a log file. Default False.|
|path_log|str|Path where the log is saved. Default './BackupMongo/log'.|
|prefix|str|Indicates the prefix with which the backup will be saved. Default 'back_'.|
|datetime_format|str|Indicates the date format to name the backup. Default '%Y-%m-%d_%H-%M'.|

> Example of name backup file: back_2019-03-09_12-21.zip

|Methods|Description|Arguments|
|--|--|--|
|create_full_backup()|Create a backup of all databases||
|create_backup('db1')|Create a backup of a database|Name of database|
|create_multidb_backup(['db1','db2'])|Create a backup of several databases|List with the databases to make the backup|


### Examples

Backup of all databases on the local server.
 
    import pymongoback
    
    back = pymongoback.PyMongoBackup()  
    back.create_full_backup()

Backup of a database on the remote server and changing the prefix.

    import pymongoback  
    
    backone = pymongoback.PyMongoBackup(username='Rafa', password='pass1234',host='192.168.1.221', days_backup=5, prefix='backremote_')  
    backone.create_backup('db1')

Backup of two databases by changing the path where they are saved and log file activated.

    import pymongoback  
    
    backmulti = pymongoback.PyMongoBackup(username='Rafa', password='pass1234', path_backup="/var/BackupMongo", log=True, path_log='/var/log/BackupMongo/log', prefix='multiback_')
    
    databases = ['db1','db2']
    backmulti.create_multidb_backup(databases)
