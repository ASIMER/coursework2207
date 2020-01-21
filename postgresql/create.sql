/*==============================================================*/
/* DBMS name:      PostgreSQL 9.x                               */
/* Created on:     15/01/2020 04:40:08                          */
/*==============================================================*/


drop index block_has_theme_FK;

drop index page_contains_blocks_FK;

drop index block_PK;

drop table block;

drop index site_has_pages_FK;

drop index page_PK;

drop table page;

drop index user_has_sites_FK;

drop index site_PK;

drop table site;

drop index theme_PK;

drop table theme;

drop index user_PK;

drop table "user";

/*==============================================================*/
/* Table: block                                                 */
/*==============================================================*/
create table block (
   site_address         TEXT                 not null,
   path                 TEXT                 not null,
   "position"           TEXT                 not null,
   theme_name           TEXT                 null,
   block_type           TEXT                 not null,
   content              TEXT                 null,
   focus_time           TIME                 not null,
   constraint PK_BLOCK primary key (site_address, path, "position")
);

/*==============================================================*/
/* Index: block_PK                                              */
/*==============================================================*/
create unique index block_PK on block (
site_address,
path,
"position"
);

/*==============================================================*/
/* Index: page_contains_blocks_FK                               */
/*==============================================================*/
create  index page_contains_blocks_FK on block (
site_address,
path
);

/*==============================================================*/
/* Index: block_has_theme_FK                                    */
/*==============================================================*/
create  index block_has_theme_FK on block (
theme_name
);

/*==============================================================*/
/* Table: page                                                  */
/*==============================================================*/
create table page (
   site_address         TEXT                 not null,
   path                 TEXT                 not null,
   title                TEXT                 null,
   constraint PK_PAGE primary key (site_address, path)
);

/*==============================================================*/
/* Index: page_PK                                               */
/*==============================================================*/
create unique index page_PK on page (
site_address,
path
);

/*==============================================================*/
/* Index: site_has_pages_FK                                     */
/*==============================================================*/
create  index site_has_pages_FK on page (
site_address
);

/*==============================================================*/
/* Table: site                                                  */
/*==============================================================*/
create table site (
   site_address         TEXT                 not null,
   login                TEXT                 null,
   site_name            TEXT                 null,
   create_date          DATE                 not null,
   constraint PK_SITE primary key (site_address)
);

/*==============================================================*/
/* Index: site_PK                                               */
/*==============================================================*/
create unique index site_PK on site (
site_address
);

/*==============================================================*/
/* Index: user_has_sites_FK                                     */
/*==============================================================*/
create  index user_has_sites_FK on site (
login
);

/*==============================================================*/
/* Table: theme                                                 */
/*==============================================================*/
create table theme (
   theme_name           TEXT                 not null,
   theme_popularity     INT4                 not null,
   code                 TEXT                 null,
   constraint PK_THEME primary key (theme_name)
);

/*==============================================================*/
/* Index: theme_PK                                              */
/*==============================================================*/
create unique index theme_PK on theme (
theme_name
);

/*==============================================================*/
/* Table: "user"                                                */
/*==============================================================*/
create table "user" (
   login                TEXT                 not null,
   password             TEXT                 not null,
   role                 TEXT                 not null,
   constraint PK_USER primary key (login)
);

/*==============================================================*/
/* Index: user_PK                                               */
/*==============================================================*/
create unique index user_PK on "user" (
login
);

alter table block
   add constraint FK_BLOCK_BLOCK_HAS_THEME foreign key (theme_name)
      references theme (theme_name)
      on delete restrict on update restrict;

alter table block
   add constraint FK_BLOCK_PAGE_CONT_PAGE foreign key (site_address, path)
      references page (site_address, path)
      on delete restrict on update restrict;

alter table page
   add constraint FK_PAGE_SITE_HAS__SITE foreign key (site_address)
      references site (site_address)
      on delete restrict on update restrict;

alter table site
   add constraint FK_SITE_USER_HAS__USER foreign key (login)
      references "user" (login)
      on delete restrict on update restrict;

