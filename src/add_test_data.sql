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
-- Name: kayttaja_id_seq; Type: SEQUENCE SET; Schema: public; Owner: varpushaukka
--

SELECT pg_catalog.setval('kayttaja_id_seq', 2, true);


--
-- Name: kuvaus_id_seq; Type: SEQUENCE SET; Schema: public; Owner: varpushaukka
--

SELECT pg_catalog.setval('kuvaus_id_seq', 3, true);


--
-- Name: paikka_id_seq; Type: SEQUENCE SET; Schema: public; Owner: varpushaukka
--

SELECT pg_catalog.setval('paikka_id_seq', 2, true);


--
-- Name: tagi_id_seq; Type: SEQUENCE SET; Schema: public; Owner: varpushaukka
--

SELECT pg_catalog.setval('tagi_id_seq', 2, true);


--
-- Data for Name: kayttaja; Type: TABLE DATA; Schema: public; Owner: varpushaukka
--

COPY kayttaja (id, nimi, tunnus, salasana, luotu, muokattu, rooli) FROM stdin;
1	Hessu Hopo	hhopo	\N	2015-05-21 12:21:43.581539+03	2015-05-21 12:21:43.581539+03	\N
2	Henna Kalliokoski	hennaruo	\N	2015-05-21 12:42:20.784138+03	2015-05-21 12:42:20.784138+03	\N
\.


--
-- Data for Name: kuvaus; Type: TABLE DATA; Schema: public; Owner: varpushaukka
--

COPY kuvaus (id, paikka, kuvaus, luotu) FROM stdin;
1	1	viikin kampus	2015-05-21 14:06:17.151197+03
2	2	kumpulan kampus	2015-05-21 14:06:49.232082+03
3	2	kiva hengailupaikka	2015-05-21 14:07:29.028065+03
\.


--
-- Data for Name: paikka; Type: TABLE DATA; Schema: public; Owner: varpushaukka
--

COPY paikka (id, koordinaatti, omistaja, luotu, yhdpaikkaan) FROM stdin;
1	(60.232080000000003,25.040400000000002)	1	2015-05-21	\N
2	(60.20458,24.962569999999999)	2	2015-05-21	\N
\.


--
-- Data for Name: paikkatagi; Type: TABLE DATA; Schema: public; Owner: varpushaukka
--

COPY paikkatagi (paikka, tagi) FROM stdin;
1	2
2	1
\.


--
-- Data for Name: tagi; Type: TABLE DATA; Schema: public; Owner: varpushaukka
--

COPY tagi (id, tagi, lang) FROM stdin;
1	yliopisto	\N
2	ulkoilu	\N
\.


--
-- PostgreSQL database dump complete
--

