drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  photoPath text not null, -- File name
  comm text not null -- Description
);