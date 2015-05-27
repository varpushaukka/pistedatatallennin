--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET client_encoding = 'SQL_ASCII';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;

SET search_path = public, pg_catalog;

--
-- Name: rooli; Type: TYPE; Schema: public; Owner: varpushaukka
--

CREATE TYPE rooli AS ENUM (
    'tavis',
    'admin'
);


ALTER TYPE public.rooli OWNER TO varpushaukka;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: kayttaja; Type: TABLE; Schema: public; Owner: varpushaukka; Tablespace: 
--

CREATE TABLE kayttaja (
    id integer NOT NULL,
    nimi text,
    tunnus text NOT NULL,
    salasana text,
    luotu timestamp with time zone DEFAULT now(),
    muokattu timestamp with time zone DEFAULT now(),
    rooli rooli
);


ALTER TABLE public.kayttaja OWNER TO varpushaukka;

--
-- Name: kayttaja_id_seq; Type: SEQUENCE; Schema: public; Owner: varpushaukka
--

CREATE SEQUENCE kayttaja_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.kayttaja_id_seq OWNER TO varpushaukka;

--
-- Name: kayttaja_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: varpushaukka
--

ALTER SEQUENCE kayttaja_id_seq OWNED BY kayttaja.id;


--
-- Name: kayttaja_id_seq; Type: SEQUENCE SET; Schema: public; Owner: varpushaukka
--

SELECT pg_catalog.setval('kayttaja_id_seq', 1, true);


--
-- Name: kuvaus; Type: TABLE; Schema: public; Owner: varpushaukka; Tablespace: 
--

CREATE TABLE kuvaus (
    id integer NOT NULL,
    paikka integer NOT NULL,
    kuvaus text NOT NULL,
    luotu timestamp with time zone DEFAULT now()
);


ALTER TABLE public.kuvaus OWNER TO varpushaukka;

--
-- Name: kuvaus_id_seq; Type: SEQUENCE; Schema: public; Owner: varpushaukka
--

CREATE SEQUENCE kuvaus_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.kuvaus_id_seq OWNER TO varpushaukka;

--
-- Name: kuvaus_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: varpushaukka
--

ALTER SEQUENCE kuvaus_id_seq OWNED BY kuvaus.id;


--
-- Name: kuvaus_id_seq; Type: SEQUENCE SET; Schema: public; Owner: varpushaukka
--

SELECT pg_catalog.setval('kuvaus_id_seq', 1, false);


--
-- Name: paikka; Type: TABLE; Schema: public; Owner: varpushaukka; Tablespace: 
--

CREATE TABLE paikka (
    id integer NOT NULL,
    koordinaatti point NOT NULL,
    omistaja integer,
    luotu date DEFAULT now(),
    yhdpaikkaan integer
);


ALTER TABLE public.paikka OWNER TO varpushaukka;

--
-- Name: paikka_id_seq; Type: SEQUENCE; Schema: public; Owner: varpushaukka
--

CREATE SEQUENCE paikka_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.paikka_id_seq OWNER TO varpushaukka;

--
-- Name: paikka_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: varpushaukka
--

ALTER SEQUENCE paikka_id_seq OWNED BY paikka.id;


--
-- Name: paikka_id_seq; Type: SEQUENCE SET; Schema: public; Owner: varpushaukka
--

SELECT pg_catalog.setval('paikka_id_seq', 1, false);


--
-- Name: paikkatagi; Type: TABLE; Schema: public; Owner: varpushaukka; Tablespace: 
--

CREATE TABLE paikkatagi (
    paikka integer,
    tagi integer
);


ALTER TABLE public.paikkatagi OWNER TO varpushaukka;

--
-- Name: tagi; Type: TABLE; Schema: public; Owner: varpushaukka; Tablespace: 
--

CREATE TABLE tagi (
    id integer NOT NULL,
    tagi text NOT NULL,
    lang text
);


ALTER TABLE public.tagi OWNER TO varpushaukka;

--
-- Name: tagi_id_seq; Type: SEQUENCE; Schema: public; Owner: varpushaukka
--

CREATE SEQUENCE tagi_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.tagi_id_seq OWNER TO varpushaukka;

--
-- Name: tagi_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: varpushaukka
--

ALTER SEQUENCE tagi_id_seq OWNED BY tagi.id;


--
-- Name: tagi_id_seq; Type: SEQUENCE SET; Schema: public; Owner: varpushaukka
--

SELECT pg_catalog.setval('tagi_id_seq', 1, false);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: varpushaukka
--

ALTER TABLE ONLY kayttaja ALTER COLUMN id SET DEFAULT nextval('kayttaja_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: varpushaukka
--

ALTER TABLE ONLY kuvaus ALTER COLUMN id SET DEFAULT nextval('kuvaus_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: varpushaukka
--

ALTER TABLE ONLY paikka ALTER COLUMN id SET DEFAULT nextval('paikka_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: varpushaukka
--

ALTER TABLE ONLY tagi ALTER COLUMN id SET DEFAULT nextval('tagi_id_seq'::regclass);


--
-- Name: kayttaja_pkey; Type: CONSTRAINT; Schema: public; Owner: varpushaukka; Tablespace: 
--

ALTER TABLE ONLY kayttaja
    ADD CONSTRAINT kayttaja_pkey PRIMARY KEY (id);


--
-- Name: kuvaus_pkey; Type: CONSTRAINT; Schema: public; Owner: varpushaukka; Tablespace: 
--

ALTER TABLE ONLY kuvaus
    ADD CONSTRAINT kuvaus_pkey PRIMARY KEY (id);


--
-- Name: paikka_pkey; Type: CONSTRAINT; Schema: public; Owner: varpushaukka; Tablespace: 
--

ALTER TABLE ONLY paikka
    ADD CONSTRAINT paikka_pkey PRIMARY KEY (id);


--
-- Name: tagi_pkey; Type: CONSTRAINT; Schema: public; Owner: varpushaukka; Tablespace: 
--

ALTER TABLE ONLY tagi
    ADD CONSTRAINT tagi_pkey PRIMARY KEY (id);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

