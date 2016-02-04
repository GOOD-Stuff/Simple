drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  photoPath text not null,
  comm text not null,
  author text not null
);