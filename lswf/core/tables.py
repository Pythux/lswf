
tables = ['''
    CREATE TABLE directory
        (directory_id INTEGER PRIMARY KEY NOT NULL,
        last_update timestamp NOT NULL, path TEXT UNIQUE NOT NULL,
        listdir TEXT NOT NULL)
    ''', '''
    CREATE TABLE file
        (file_id INTEGER PRIMARY KEY NOT NULL,
        last_update timestamp NOT NULL, path TEXT UNIQUE NOT NULL)
    ''', '''
    create table directory_update_frequence
        (directory_id INTEGER NOT NULL,
        update_time timestamp NOT NULL,
        CONSTRAINT UC_key UNIQUE (directory_id, update_time)
        CONSTRAINT fk_directory
            FOREIGN KEY (directory_id)
            REFERENCES directory(directory_id)
            ON DELETE CASCADE
        )
    ''', '''
    create table file_update_frequence
        (file_id INTEGER NOT NULL,
        update_time timestamp NOT NULL,
        CONSTRAINT UC_key UNIQUE (file_id, update_time)
        CONSTRAINT fk_file
            FOREIGN KEY (file_id)
            REFERENCES file(file_id)
            ON DELETE CASCADE
        )
    ''', '''
    create table too_big_directory
        (id INTEGER PRIMARY KEY NOT NULL,
        path TEXT UNIQUE NOT NULL)
    ''', '''
    create table symlink
        (symlink_id INTEGER PRIMARY KEY NOT NULL,
        is_dir boolean NOT NULL,
        path TEXT UNIQUE NOT NULL,
        symlink_to TEXT,
        save_mode TEXT)
    ''']
