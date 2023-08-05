#!/usr/bin/env python3

import sqlite3 as sql
import __init__ as dbq

if __name__ == '__main__':
    db = sql.connect(':memory:')
    dbq.create_table(db, 'main', 'id INT, username TEXT, name TEXT')
    main = dbq.Table(db, 'main')
    main.insert(0, 'root', 'root')
    main.insert(1, 'aka_dude', 'The Dude')
    main.insert(2, 'aka_doppel', 'The Dude')
    main(username='root').update(name='Groot')
    print(main.where_raw('username LIKE "aka_%"'))
    print({'username': 'aka_dude'} in main)
    print({'username': 'aka_anon'} in main)
    print(list(main().as_dict()))
    print(main())
