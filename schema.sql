drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  photo_name text not null,
  comm text not null,
  author text not null
);