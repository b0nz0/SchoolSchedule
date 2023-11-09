--
-- PostgreSQL database dump
--

-- Dumped from database version 16.0 (Ubuntu 16.0-1.pgdg22.04+1)
-- Dumped by pg_dump version 16.0 (Ubuntu 16.0-1.pgdg22.04+1)

-- Started on 2023-11-09 17:12:11 CET

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

DROP DATABASE IF EXISTS school_schedule;
--
-- TOC entry 3452 (class 1262 OID 16533)
-- Name: school_schedule; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE school_schedule WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'it_IT.UTF-8';


ALTER DATABASE school_schedule OWNER TO postgres;

\connect school_schedule

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

--
-- TOC entry 232 (class 1255 OID 16534)
-- Name: tr_fn_school_history(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.tr_fn_school_history() RETURNS trigger
    LANGUAGE plpgsql
    AS $$BEGIN
 INSERT INTO school_history (object_id, start_datetime, end_datetime, name, log_user)
	  VALUES (OLD.id, OLD.start_datetime, now(), OLD.name, OLD.log_user);
 RETURN NULL;
END;$$;


ALTER FUNCTION public.tr_fn_school_history() OWNER TO postgres;

--
-- TOC entry 234 (class 1255 OID 16577)
-- Name: tr_fn_school_year_history(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.tr_fn_school_year_history() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
 INSERT INTO school_year_history (object_id, start_datetime, end_datetime, identifier, school_id, log_user)
	  VALUES (OLD.id, OLD.start_datetime, now(), OLD.identifier, OLD.school_id, OLD.log_user);
 RETURN NULL;
END;
$$;


ALTER FUNCTION public.tr_fn_school_year_history() OWNER TO postgres;

--
-- TOC entry 233 (class 1255 OID 16535)
-- Name: tr_fn_update_start_datetime(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.tr_fn_update_start_datetime() RETURNS trigger
    LANGUAGE plpgsql
    AS $$BEGIN
  NEW.start_datetime = now();
  return NEW;
END;$$;


ALTER FUNCTION public.tr_fn_update_start_datetime() OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 215 (class 1259 OID 16536)
-- Name: school; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.school (
    id integer NOT NULL,
    start_datetime timestamp with time zone,
    log_user character varying,
    name character varying(256) NOT NULL
);


ALTER TABLE public.school OWNER TO postgres;

--
-- TOC entry 216 (class 1259 OID 16541)
-- Name: active_schools; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.active_schools AS
 SELECT id,
    start_datetime,
    log_user,
    name
   FROM public.school
  ORDER BY id;


ALTER VIEW public.active_schools OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 16545)
-- Name: base; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.base (
    start_datetime timestamp with time zone,
    log_user character varying
);


ALTER TABLE public.base OWNER TO postgres;

--
-- TOC entry 218 (class 1259 OID 16550)
-- Name: base_history; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.base_history (
    object_id integer NOT NULL,
    start_datetime timestamp with time zone NOT NULL,
    end_datetime timestamp with time zone,
    active boolean DEFAULT true NOT NULL,
    log_user character varying(256)
);


ALTER TABLE public.base_history OWNER TO postgres;

--
-- TOC entry 231 (class 1259 OID 16603)
-- Name: class; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.class (
    id integer NOT NULL,
    start_datetime timestamp with time zone,
    log_user character varying,
    school_year_id integer NOT NULL,
    year_id integer NOT NULL,
    section_id integer NOT NULL
);


ALTER TABLE public.class OWNER TO postgres;

--
-- TOC entry 230 (class 1259 OID 16602)
-- Name: class_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.class ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.class_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 219 (class 1259 OID 16554)
-- Name: school_history; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.school_history (
    id integer NOT NULL,
    object_id integer NOT NULL,
    start_datetime timestamp with time zone NOT NULL,
    end_datetime timestamp with time zone,
    log_user character varying(256),
    name character varying(256) NOT NULL
);


ALTER TABLE public.school_history OWNER TO postgres;

--
-- TOC entry 220 (class 1259 OID 16559)
-- Name: school_history_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.school_history ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.school_history_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 221 (class 1259 OID 16560)
-- Name: school_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.school ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.school_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 222 (class 1259 OID 16561)
-- Name: school_year; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.school_year (
    id integer NOT NULL,
    start_datetime timestamp with time zone,
    log_user character varying,
    identifier character varying(256),
    school_id integer NOT NULL
);


ALTER TABLE public.school_year OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 16566)
-- Name: school_year_history; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.school_year_history (
    id integer NOT NULL,
    object_id integer NOT NULL,
    start_datetime timestamp with time zone NOT NULL,
    end_datetime timestamp with time zone,
    log_user character varying(256),
    identifier character varying(256),
    school_id integer
);


ALTER TABLE public.school_year_history OWNER TO postgres;

--
-- TOC entry 224 (class 1259 OID 16571)
-- Name: school_year_history_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.school_year_history ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.school_year_history_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 225 (class 1259 OID 16572)
-- Name: school_year_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.school_year ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.school_year_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 229 (class 1259 OID 16596)
-- Name: section; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.section (
    id integer NOT NULL,
    start_datetime timestamp with time zone,
    log_user character varying,
    identifier character varying(256),
    school_id integer NOT NULL
);


ALTER TABLE public.section OWNER TO postgres;

--
-- TOC entry 228 (class 1259 OID 16595)
-- Name: section_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.section ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.section_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 227 (class 1259 OID 16582)
-- Name: year; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.year (
    id integer NOT NULL,
    start_datetime timestamp with time zone,
    log_user character varying,
    identifier character varying(256),
    school_id integer NOT NULL
);


ALTER TABLE public.year OWNER TO postgres;

--
-- TOC entry 226 (class 1259 OID 16581)
-- Name: year_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.year ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.year_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 3432 (class 0 OID 16545)
-- Dependencies: 217
-- Data for Name: base; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3433 (class 0 OID 16550)
-- Dependencies: 218
-- Data for Name: base_history; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3446 (class 0 OID 16603)
-- Dependencies: 231
-- Data for Name: class; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.class OVERRIDING SYSTEM VALUE VALUES (7, '2023-11-09 17:09:58.209703+01', 'Fede', 9, 7, 7);
INSERT INTO public.class OVERRIDING SYSTEM VALUE VALUES (8, '2023-11-09 17:09:58.214302+01', 'Fede', 9, 7, 8);
INSERT INTO public.class OVERRIDING SYSTEM VALUE VALUES (9, '2023-11-09 17:09:58.218508+01', 'Fede', 9, 8, 7);


--
-- TOC entry 3431 (class 0 OID 16536)
-- Dependencies: 215
-- Data for Name: school; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.school OVERRIDING SYSTEM VALUE VALUES (37, '2023-11-09 17:09:58.156269+01', 'Fede', 'Morgagni');


--
-- TOC entry 3434 (class 0 OID 16554)
-- Dependencies: 219
-- Data for Name: school_history; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.school_history OVERRIDING SYSTEM VALUE VALUES (1, 12, '2023-11-08 17:10:10.659919+01', '2023-11-08 17:10:10.679371+01', 'Fede', 'Morgagni');
INSERT INTO public.school_history OVERRIDING SYSTEM VALUE VALUES (2, 13, '2023-11-08 17:10:56.414211+01', '2023-11-08 17:10:56.435342+01', 'Fede', 'Morgagni');
INSERT INTO public.school_history OVERRIDING SYSTEM VALUE VALUES (3, 14, '2023-11-08 17:17:44.464797+01', '2023-11-08 17:17:44.514653+01', 'Fede', 'Morgagni');
INSERT INTO public.school_history OVERRIDING SYSTEM VALUE VALUES (4, 15, '2023-11-08 17:19:01.674651+01', '2023-11-08 17:19:01.697595+01', 'Fede', 'Morgagni');
INSERT INTO public.school_history OVERRIDING SYSTEM VALUE VALUES (5, 16, '2023-11-08 17:19:33.665426+01', '2023-11-08 17:19:33.693634+01', 'Fede', 'Morgagni');
INSERT INTO public.school_history OVERRIDING SYSTEM VALUE VALUES (6, 17, '2023-11-09 09:08:43.433973+01', '2023-11-09 09:08:43.452406+01', 'Fede', 'Morgagni');
INSERT INTO public.school_history OVERRIDING SYSTEM VALUE VALUES (7, 18, '2023-11-09 09:17:50.193759+01', '2023-11-09 09:17:50.210703+01', 'Fede', 'Morgagni');
INSERT INTO public.school_history OVERRIDING SYSTEM VALUE VALUES (8, 19, '2023-11-09 09:45:40.13624+01', '2023-11-09 09:45:40.147493+01', 'Fede', 'Morgagni');
INSERT INTO public.school_history OVERRIDING SYSTEM VALUE VALUES (9, 20, '2023-11-09 09:48:13.061723+01', '2023-11-09 09:48:13.076769+01', 'Fede', 'Morgagni');
INSERT INTO public.school_history OVERRIDING SYSTEM VALUE VALUES (10, 21, '2023-11-09 09:50:04.556696+01', '2023-11-09 09:50:04.570063+01', 'Fede', 'Morgagni');
INSERT INTO public.school_history OVERRIDING SYSTEM VALUE VALUES (11, 22, '2023-11-09 09:50:38.950669+01', '2023-11-09 09:50:38.978078+01', 'Fede', 'Morgagni');
INSERT INTO public.school_history OVERRIDING SYSTEM VALUE VALUES (12, 23, '2023-11-09 11:15:45.25343+01', '2023-11-09 11:15:45.270998+01', 'Fede', 'Morgagni');
INSERT INTO public.school_history OVERRIDING SYSTEM VALUE VALUES (13, 24, '2023-11-09 11:18:37.858564+01', '2023-11-09 11:18:37.871648+01', 'Fede', 'Morgagni');
INSERT INTO public.school_history OVERRIDING SYSTEM VALUE VALUES (14, 25, '2023-11-09 11:43:55.509153+01', '2023-11-09 11:43:55.530915+01', 'Fede', 'Morgagni');
INSERT INTO public.school_history OVERRIDING SYSTEM VALUE VALUES (15, 26, '2023-11-09 11:45:45.623123+01', '2023-11-09 11:45:45.65779+01', 'Fede', 'Morgagni');
INSERT INTO public.school_history OVERRIDING SYSTEM VALUE VALUES (16, 27, '2023-11-09 11:46:07.368061+01', '2023-11-09 11:46:07.376358+01', 'Fede', 'Morgagni');
INSERT INTO public.school_history OVERRIDING SYSTEM VALUE VALUES (17, 28, '2023-11-09 11:46:26.174365+01', '2023-11-09 11:46:26.189891+01', 'Fede', 'Morgagni');
INSERT INTO public.school_history OVERRIDING SYSTEM VALUE VALUES (18, 29, '2023-11-09 11:46:39.932899+01', '2023-11-09 11:46:39.950876+01', 'Fede', 'Morgagni');
INSERT INTO public.school_history OVERRIDING SYSTEM VALUE VALUES (19, 30, '2023-11-09 11:47:43.877857+01', '2023-11-09 11:47:43.88529+01', 'Fede', 'Morgagni');
INSERT INTO public.school_history OVERRIDING SYSTEM VALUE VALUES (20, 31, '2023-11-09 11:51:55.251276+01', '2023-11-09 11:51:55.259649+01', 'Fede', 'Morgagni');
INSERT INTO public.school_history OVERRIDING SYSTEM VALUE VALUES (21, 32, '2023-11-09 11:56:10.84718+01', '2023-11-09 11:56:10.861796+01', 'Fede', 'Morgagni');
INSERT INTO public.school_history OVERRIDING SYSTEM VALUE VALUES (22, 33, '2023-11-09 11:58:06.628129+01', '2023-11-09 11:58:06.647957+01', 'Fede', 'Morgagni');
INSERT INTO public.school_history OVERRIDING SYSTEM VALUE VALUES (23, 34, '2023-11-09 12:19:48.326436+01', '2023-11-09 12:19:48.341197+01', 'Fede', 'Morgagni');
INSERT INTO public.school_history OVERRIDING SYSTEM VALUE VALUES (24, 35, '2023-11-09 12:20:12.841249+01', '2023-11-09 12:20:12.858754+01', 'Fede', 'Morgagni');
INSERT INTO public.school_history OVERRIDING SYSTEM VALUE VALUES (25, 36, '2023-11-09 12:29:18.860409+01', '2023-11-09 12:29:18.873682+01', 'Fede', 'Morgagni');
INSERT INTO public.school_history OVERRIDING SYSTEM VALUE VALUES (26, 36, '2023-11-09 12:29:18.873682+01', '2023-11-09 13:00:23.400897+01', 'Fede', 'New Morgagni');


--
-- TOC entry 3437 (class 0 OID 16561)
-- Dependencies: 222
-- Data for Name: school_year; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.school_year OVERRIDING SYSTEM VALUE VALUES (9, '2023-11-09 17:09:58.170981+01', 'Fede', '2023/24', 37);


--
-- TOC entry 3438 (class 0 OID 16566)
-- Dependencies: 223
-- Data for Name: school_year_history; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.school_year_history OVERRIDING SYSTEM VALUE VALUES (2, 2, '2023-11-09 11:18:37.880338+01', '2023-11-09 11:18:37.889264+01', 'Fede', '2023/24', 24);
INSERT INTO public.school_year_history OVERRIDING SYSTEM VALUE VALUES (3, 3, '2023-11-09 11:43:55.539736+01', '2023-11-09 11:43:55.54663+01', 'Fede', '2023/24', 25);
INSERT INTO public.school_year_history OVERRIDING SYSTEM VALUE VALUES (4, 4, '2023-11-09 11:45:45.670623+01', '2023-11-09 11:45:45.680751+01', 'Fede', '2023/24', 26);
INSERT INTO public.school_year_history OVERRIDING SYSTEM VALUE VALUES (5, 5, '2023-11-09 11:46:07.387068+01', '2023-11-09 11:46:07.393274+01', 'Fede', '2023/24', 27);
INSERT INTO public.school_year_history OVERRIDING SYSTEM VALUE VALUES (6, 6, '2023-11-09 11:46:26.198575+01', '2023-11-09 11:46:26.208118+01', 'Fede', '2023/24', 28);
INSERT INTO public.school_year_history OVERRIDING SYSTEM VALUE VALUES (7, 7, '2023-11-09 11:46:39.95864+01', '2023-11-09 11:46:39.96721+01', 'Fede', '2023/24', 29);


--
-- TOC entry 3444 (class 0 OID 16596)
-- Dependencies: 229
-- Data for Name: section; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.section OVERRIDING SYSTEM VALUE VALUES (7, '2023-11-09 17:09:58.198114+01', 'Fede', 'A', 37);
INSERT INTO public.section OVERRIDING SYSTEM VALUE VALUES (8, '2023-11-09 17:09:58.202617+01', 'Fede', 'B', 37);
INSERT INTO public.section OVERRIDING SYSTEM VALUE VALUES (9, '2023-11-09 17:09:58.205633+01', 'Fede', 'C', 37);


--
-- TOC entry 3442 (class 0 OID 16582)
-- Dependencies: 227
-- Data for Name: year; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.year OVERRIDING SYSTEM VALUE VALUES (7, '2023-11-09 17:09:58.176439+01', 'Fede', 'I', 37);
INSERT INTO public.year OVERRIDING SYSTEM VALUE VALUES (8, '2023-11-09 17:09:58.181222+01', 'Fede', 'II', 37);
INSERT INTO public.year OVERRIDING SYSTEM VALUE VALUES (9, '2023-11-09 17:09:58.185954+01', 'Fede', 'III', 37);
INSERT INTO public.year OVERRIDING SYSTEM VALUE VALUES (10, '2023-11-09 17:09:58.190394+01', 'Fede', 'IV', 37);
INSERT INTO public.year OVERRIDING SYSTEM VALUE VALUES (11, '2023-11-09 17:09:58.193467+01', 'Fede', 'V', 37);


--
-- TOC entry 3453 (class 0 OID 0)
-- Dependencies: 230
-- Name: class_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.class_id_seq', 9, true);


--
-- TOC entry 3454 (class 0 OID 0)
-- Dependencies: 220
-- Name: school_history_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.school_history_id_seq', 26, true);


--
-- TOC entry 3455 (class 0 OID 0)
-- Dependencies: 221
-- Name: school_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.school_id_seq', 37, true);


--
-- TOC entry 3456 (class 0 OID 0)
-- Dependencies: 224
-- Name: school_year_history_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.school_year_history_id_seq', 7, true);


--
-- TOC entry 3457 (class 0 OID 0)
-- Dependencies: 225
-- Name: school_year_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.school_year_id_seq', 9, true);


--
-- TOC entry 3458 (class 0 OID 0)
-- Dependencies: 228
-- Name: section_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.section_id_seq', 9, true);


--
-- TOC entry 3459 (class 0 OID 0)
-- Dependencies: 226
-- Name: year_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.year_id_seq', 11, true);


--
-- TOC entry 3279 (class 2606 OID 16612)
-- Name: class class_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.class
    ADD CONSTRAINT class_pkey PRIMARY KEY (id);


--
-- TOC entry 3269 (class 2606 OID 16574)
-- Name: school_history school_history_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.school_history
    ADD CONSTRAINT school_history_pkey PRIMARY KEY (id);


--
-- TOC entry 3267 (class 2606 OID 16610)
-- Name: school school_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.school
    ADD CONSTRAINT school_pkey PRIMARY KEY (id);


--
-- TOC entry 3273 (class 2606 OID 16616)
-- Name: school_year_history school_year_history_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.school_year_history
    ADD CONSTRAINT school_year_history_pkey PRIMARY KEY (id);


--
-- TOC entry 3271 (class 2606 OID 16614)
-- Name: school_year school_year_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.school_year
    ADD CONSTRAINT school_year_pkey PRIMARY KEY (id);


--
-- TOC entry 3277 (class 2606 OID 16618)
-- Name: section section_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.section
    ADD CONSTRAINT section_pkey PRIMARY KEY (id);


--
-- TOC entry 3275 (class 2606 OID 16620)
-- Name: year year_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.year
    ADD CONSTRAINT year_pkey PRIMARY KEY (id);


--
-- TOC entry 3286 (class 2620 OID 16608)
-- Name: class tr_class_start_datetime; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER tr_class_start_datetime BEFORE INSERT OR UPDATE ON public.class FOR EACH ROW EXECUTE FUNCTION public.tr_fn_update_start_datetime();


--
-- TOC entry 3280 (class 2620 OID 16575)
-- Name: school tr_school_history; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER tr_school_history AFTER UPDATE ON public.school FOR EACH ROW EXECUTE FUNCTION public.tr_fn_school_history();


--
-- TOC entry 3281 (class 2620 OID 16576)
-- Name: school tr_school_start_datetime; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER tr_school_start_datetime BEFORE INSERT OR UPDATE ON public.school FOR EACH ROW EXECUTE FUNCTION public.tr_fn_update_start_datetime();


--
-- TOC entry 3282 (class 2620 OID 16580)
-- Name: school_year tr_school_start_datetime; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER tr_school_start_datetime BEFORE INSERT OR UPDATE ON public.school_year FOR EACH ROW EXECUTE FUNCTION public.tr_fn_update_start_datetime();


--
-- TOC entry 3283 (class 2620 OID 16578)
-- Name: school_year tr_school_year_history; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER tr_school_year_history AFTER UPDATE ON public.school_year FOR EACH ROW EXECUTE FUNCTION public.tr_fn_school_year_history();


--
-- TOC entry 3285 (class 2620 OID 16601)
-- Name: section tr_section_start_datetime; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER tr_section_start_datetime BEFORE INSERT OR UPDATE ON public.section FOR EACH ROW EXECUTE FUNCTION public.tr_fn_update_start_datetime();


--
-- TOC entry 3284 (class 2620 OID 16594)
-- Name: year tr_year_start_datetime; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER tr_year_start_datetime BEFORE INSERT OR UPDATE ON public.year FOR EACH ROW EXECUTE FUNCTION public.tr_fn_update_start_datetime();


-- Completed on 2023-11-09 17:12:11 CET

--
-- PostgreSQL database dump complete
--

