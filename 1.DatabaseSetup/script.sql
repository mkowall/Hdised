SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

CREATE SCHEMA mal;

ALTER SCHEMA mal OWNER TO postgres;

CREATE SCHEMA "myAnimeList";


ALTER SCHEMA "myAnimeList" OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

CREATE TABLE "myAnimeList"."Anime" (
    "Id" integer NOT NULL,
    "Name" text NOT NULL,
    "Episodes" integer
);

CREATE TABLE "myAnimeList"."AnimeRating" (
    "Id" integer NOT NULL,
    "Rating" integer NOT NULL,
    "Id_Anime" integer NOT NULL,
    "Id_User" integer NOT NULL
);

CREATE TABLE "myAnimeList"."Anime_Genre" (
    id integer NOT NULL,
    "Id_Anime" integer,
    "Id_Genre" integer
);

CREATE SEQUENCE "myAnimeList"."Anime_Genre_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE "myAnimeList"."Anime_Genre_id_seq" OWNED BY "myAnimeList"."Anime_Genre".id;

CREATE SEQUENCE "myAnimeList"."Anime_Id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE "myAnimeList"."Anime_Id_seq" OWNED BY "myAnimeList"."AnimeRating"."Id";

CREATE TABLE "myAnimeList"."Anime_Licensor" (
    id integer NOT NULL,
    "id_Anime" integer NOT NULL,
    "id_Licensor" integer NOT NULL
);

CREATE SEQUENCE "myAnimeList"."Anime_Licensor_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE "myAnimeList"."Anime_Licensor_id_seq" OWNED BY "myAnimeList"."Anime_Licensor".id;

CREATE TABLE "myAnimeList"."Genre" (
    id integer NOT NULL,
    name text NOT NULL
);

CREATE SEQUENCE "myAnimeList"."Genre_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE "myAnimeList"."Genre_id_seq" OWNED BY "myAnimeList"."Genre".id;

CREATE TABLE "myAnimeList"."Licensor" (
    "Id" integer NOT NULL,
    "Name" text NOT NULL
);

CREATE SEQUENCE "myAnimeList"."Licensor_Id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE "myAnimeList"."Licensor_Id_seq" OWNED BY "myAnimeList"."Licensor"."Id";

CREATE TABLE "myAnimeList"."Status" (
    id integer NOT NULL,
    name text NOT NULL
);

CREATE TABLE "myAnimeList"."UserAnimeInfo" (
    "Id" integer NOT NULL,
    "Id_User" integer NOT NULL,
    "id_Status" integer,
    "WatchedEpisodes" integer
);

CREATE SEQUENCE "myAnimeList"."UserAnimeInfo_Id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE "myAnimeList"."UserAnimeInfo_Id_seq" OWNED BY "myAnimeList"."UserAnimeInfo"."Id";

ALTER TABLE ONLY "myAnimeList"."AnimeRating" ALTER COLUMN "Id" SET DEFAULT nextval('"myAnimeList"."Anime_Id_seq"'::regclass);
ALTER TABLE ONLY "myAnimeList"."Anime_Genre" ALTER COLUMN id SET DEFAULT nextval('"myAnimeList"."Anime_Genre_id_seq"'::regclass);
ALTER TABLE ONLY "myAnimeList"."Anime_Licensor" ALTER COLUMN id SET DEFAULT nextval('"myAnimeList"."Anime_Licensor_id_seq"'::regclass);
ALTER TABLE ONLY "myAnimeList"."Genre" ALTER COLUMN id SET DEFAULT nextval('"myAnimeList"."Genre_id_seq"'::regclass);
ALTER TABLE ONLY "myAnimeList"."Licensor" ALTER COLUMN "Id" SET DEFAULT nextval('"myAnimeList"."Licensor_Id_seq"'::regclass);
ALTER TABLE ONLY "myAnimeList"."UserAnimeInfo" ALTER COLUMN "Id" SET DEFAULT nextval('"myAnimeList"."UserAnimeInfo_Id_seq"'::regclass);


SELECT pg_catalog.setval('"myAnimeList"."Anime_Genre_id_seq"', 1, false);

SELECT pg_catalog.setval('"myAnimeList"."Anime_Id_seq"', 1, false);

SELECT pg_catalog.setval('"myAnimeList"."Anime_Licensor_id_seq"', 1, false);

SELECT pg_catalog.setval('"myAnimeList"."Genre_id_seq"', 1, false);

SELECT pg_catalog.setval('"myAnimeList"."Licensor_Id_seq"', 1, false);

SELECT pg_catalog.setval('"myAnimeList"."UserAnimeInfo_Id_seq"', 1, false);

ALTER TABLE ONLY "myAnimeList"."Anime_Licensor"
    ADD CONSTRAINT "Anime_Licensor_pkey" PRIMARY KEY (id);

ALTER TABLE ONLY "myAnimeList"."Anime"
    ADD CONSTRAINT "Anime_pkey" PRIMARY KEY ("Id");

ALTER TABLE ONLY "myAnimeList"."Genre"
    ADD CONSTRAINT "Genre_pkey" PRIMARY KEY (id);

ALTER TABLE ONLY "myAnimeList"."Licensor"
    ADD CONSTRAINT "Licensor_pkey" PRIMARY KEY ("Id");

ALTER TABLE ONLY "myAnimeList"."AnimeRating"
    ADD CONSTRAINT "PrimaryAnime" PRIMARY KEY ("Id");

ALTER TABLE ONLY "myAnimeList"."Status"
    ADD CONSTRAINT "Status_pkey" PRIMARY KEY (id);

ALTER TABLE ONLY "myAnimeList"."UserAnimeInfo"
    ADD CONSTRAINT "UserAnimeInfo_pkey" PRIMARY KEY ("Id");

ALTER TABLE ONLY "myAnimeList"."AnimeRating"
    ADD CONSTRAINT "AnimeRating_Id_Anime_fkey" FOREIGN KEY ("Id_Anime") REFERENCES "myAnimeList"."Anime"("Id") NOT VALID;

ALTER TABLE ONLY "myAnimeList"."AnimeRating"
    ADD CONSTRAINT "AnimeRating_Id_User_fkey" FOREIGN KEY ("Id_User") REFERENCES "myAnimeList"."UserAnimeInfo"("Id") NOT VALID;

ALTER TABLE ONLY "myAnimeList"."Anime_Genre"
    ADD CONSTRAINT "Anime_Genre_Id_Anime_fkey" FOREIGN KEY ("Id_Anime") REFERENCES "myAnimeList"."Anime"("Id") NOT VALID;

ALTER TABLE ONLY "myAnimeList"."Anime_Genre"
    ADD CONSTRAINT "Anime_Genre_Id_Genre_fkey" FOREIGN KEY ("Id_Genre") REFERENCES "myAnimeList"."Genre"(id) NOT VALID;

ALTER TABLE ONLY "myAnimeList"."Anime_Licensor"
    ADD CONSTRAINT "Anime_Licensor_id_Anime_fkey" FOREIGN KEY ("id_Anime") REFERENCES "myAnimeList"."Anime"("Id") NOT VALID;

ALTER TABLE ONLY "myAnimeList"."Anime_Licensor"
    ADD CONSTRAINT "Anime_Licensor_id_Licensor_fkey" FOREIGN KEY ("id_Licensor") REFERENCES "myAnimeList"."Licensor"("Id") NOT VALID;

ALTER TABLE ONLY "myAnimeList"."Genre"
    ADD CONSTRAINT "Genre_name_key" UNIQUE (name);

ALTER TABLE ONLY "myAnimeList"."Licensor"
    ADD CONSTRAINT "Licensor_Name_key" UNIQUE ("Name");