# the database module is much more testable as its actions are largely atomic
# that said, the database module could certain be refactored to achieve decoupling
# in fact, either the implementation of the Unit of Work or just changing to sqlalchemy would be good.

import os
from datetime import datetime
import sqlite3

import pytest


from database import DatabaseManager

@pytest.fixture
def database_manager() -> DatabaseManager:
    """
    What is a fixture? https://docs.pytest.org/en/stable/fixture.html#what-fixtures-are
    """
    filename = "test_bookmarks.db"
    dbm = DatabaseManager(filename)
    yield dbm
    dbm.__del__()           # explicitly release the database manager
    os.remove(filename)


def test_database_manager_create_table(database_manager):
    # arrange and act
    database_manager.create_table(
        "bookmarks",
        {
            "id": "integer primary key autoincrement",
            "title": "text not null",
            "url": "text not null",
            "notes": "text",
            "date_added": "text not null",
        },
    )

    #assert
    conn = database_manager.connection
    cursor = conn.cursor()

    cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='bookmarks' ''')

    assert cursor.fetchone()[0] == 1

    #cleanup
    #database_manager.drop_table("bookmarks")


def test_database_manager_add_bookmark(database_manager):

    # arrange
    database_manager.create_table(
        "bookmarks",
        {
            "id": "integer primary key autoincrement",
            "title": "text not null",
            "url": "text not null",
            "notes": "text",
            "date_added": "text not null",
        },
    )

    data = {
        "title": "test_title",
        "url": "http://example.com",
        "notes": "test notes",
        "date_added": datetime.utcnow().isoformat()        
    }

    # act
    database_manager.add("bookmarks", data)

    # assert
    conn = database_manager.connection
    cursor = conn.cursor()
    cursor.execute(''' SELECT * FROM bookmarks WHERE title='test_title' ''')    
    assert cursor.fetchone()[0] == 1  

    # Delete -------------------------

def test_database_manager_delete_bookmark(database_manager):

    # arrange
    database_manager.create_table(
        "bookmarks",
        {
            "id": "integer primary key autoincrement",
            "title": "text not null",
            "url": "text not null",
            "notes": "text",
            "date_added": "text not null",
        },
    )

    criteria = {
        "title": "test_title",
        "url": "http://Test.com",
        "notes": "this is the test notes",
        "date_added": datetime.utcnow().isoformat()        
    }

    # act
    database_manager.delete("bookmarks",criteria)    

    # assert
    conn = database_manager.connection
    cursor = conn.cursor()
    #print("Contents of the table: ")
    #cursor.execute(''' SELECT * FROM bookmarks''')
    #print(cursor.fetchall())
    cursor.execute(''' Delete FROM bookmarks WHERE title='test_title' ''')    
    assert cursor.rowcount== 0

    #Order ----------------------------------
     #select
def test_database_manager_select_bookmark(database_manager):

    # arrange
    database_manager.create_table(
        "bookmarks",
        {
            "id": "integer primary key autoincrement",
            "title": "text not null",
            "url": "text not null",
            "notes": "text",
            "date_added": "text not null",
        },
    )

    criteria = {
        "title": "test_title",
        "url": "http://Test.com",
        "notes": "this is the test notes",
        "date_added": datetime.utcnow().isoformat()        
    }

    # act
    database_manager.select("bookmarks", criteria)
    database_manager.select("bookmarks", criteria, order_by="title")
    conn = database_manager.connection
    cursor = conn.cursor()
    cursor.execute(''' Select * FROM bookmarks order by title ''')  
    result=cursor.fetchall()
    for x in result:
        assert cursor.fetchall==x


    
    
  