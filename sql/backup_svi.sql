--
-- PostgreSQL database dump
--

-- Dumped from database version 14.9 (Ubuntu 14.9-0ubuntu0.22.04.1)
-- Dumped by pg_dump version 14.9 (Ubuntu 14.9-0ubuntu0.22.04.1)

-- Started on 2023-11-08 17:21:50 CET

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
-- TOC entry 3398 (class 1262 OID 16510)
-- Name: school_schedule; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE school_schedule WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'it_IT.UTF-8';


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
-- TOC entry 220 (class 1255 OID 16511)
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
-- TOC entry 221 (class 1255 OID 16512)
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
-- TOC entry 212 (class 1259 OID 16531)
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
-- TOC entry 215 (class 1259 OID 16558)
-- Name: active_schools; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.active_schools AS
 SELECT school.id,
    school.start_datetime,
    school.log_user,
    school.name
   FROM public.school
  ORDER BY school.id;


ALTER TABLE public.active_schools OWNER TO postgres;

--
-- TOC entry 211 (class 1259 OID 16526)
-- Name: base; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.base (
    start_datetime timestamp with time zone,
    log_user character varying
);


ALTER TABLE public.base OWNER TO postgres;

--
-- TOC entry 209 (class 1259 OID 16513)
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
-- TOC entry 210 (class 1259 OID 16517)
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
-- TOC entry 213 (class 1259 OID 16536)
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
-- TOC entry 214 (class 1259 OID 16537)
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
-- TOC entry 216 (class 1259 OID 16562)
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
-- TOC entry 217 (class 1259 OID 16567)
-- Name: school_year_history; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.school_year_history (
    id integer NOT NULL,
    object_id integer NOT NULL,
    start_datetime timestamp with time zone NOT NULL,
    end_datetime timestamp with time zone,
    log_user character varying(256),
    identifier character varying(256),
    school_id integer NOT NULL
);


ALTER TABLE public.school_year_history OWNER TO postgres;

--
-- TOC entry 218 (class 1259 OID 16572)
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
-- TOC entry 219 (class 1259 OID 16573)
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
-- TOC entry 3385 (class 0 OID 16526)
-- Dependencies: 211
-- Data for Name: base; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3383 (class 0 OID 16513)
-- Dependencies: 209
-- Data for Name: base_history; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3386 (class 0 OID 16531)
-- Dependencies: 212
-- Data for Name: school; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.school OVERRIDING SYSTEM VALUE VALUES (1, '2023-11-08 16:37:54.461834+01', 'Fede', 'Morgagni');
INSERT INTO public.school OVERRIDING SYSTEM VALUE VALUES (2, '2023-11-08 16:39:44.08809+01', 'Fede', 'Morgagni');
INSERT INTO public.school OVERRIDING SYSTEM VALUE VALUES (3, '2023-11-08 16:39:44.099655+01', 'Fede', 'New Morgagni');
INSERT INTO public.school OVERRIDING SYSTEM VALUE VALUES (4, '2023-11-08 16:41:47.56457+01', 'Fede', 'Morgagni');
INSERT INTO public.school OVERRIDING SYSTEM VALUE VALUES (5, '2023-11-08 16:41:47.575906+01', 'Fede', 'New Morgagni');
INSERT INTO public.school OVERRIDING SYSTEM VALUE VALUES (6, '2023-11-08 16:47:08.462737+01', 'Fede', 'Morgagni');
INSERT INTO public.school OVERRIDING SYSTEM VALUE VALUES (7, '2023-11-08 16:56:33.733158+01', 'Fede', 'Morgagni');
INSERT INTO public.school OVERRIDING SYSTEM VALUE VALUES (8, '2023-11-08 17:00:34.003919+01', 'Fede', 'Morgagni');
INSERT INTO public.school OVERRIDING SYSTEM VALUE VALUES (9, '2023-11-08 17:02:13.082652+01', 'Fede', 'Morgagni');
INSERT INTO public.school OVERRIDING SYSTEM VALUE VALUES (10, '2023-11-08 17:05:59.591494+01', 'Fede', 'Morgagni');
INSERT INTO public.school OVERRIDING SYSTEM VALUE VALUES (11, '2023-11-08 17:09:11.799032+01', 'Fede', 'Morgagni');
INSERT INTO public.school OVERRIDING SYSTEM VALUE VALUES (12, '2023-11-08 17:10:10.679371+01', 'Fede', 'New Morgagni');
INSERT INTO public.school OVERRIDING SYSTEM VALUE VALUES (13, '2023-11-08 17:10:56.435342+01', 'Fede', 'New Morgagni');
INSERT INTO public.school OVERRIDING SYSTEM VALUE VALUES (14, '2023-11-08 17:17:44.514653+01', 'Fede', 'New Morgagni');
INSERT INTO public.school OVERRIDING SYSTEM VALUE VALUES (15, '2023-11-08 17:19:01.697595+01', 'Fede', 'New Morgagni');
INSERT INTO public.school OVERRIDING SYSTEM VALUE VALUES (16, '2023-11-08 17:19:33.693634+01', 'Fede', 'New Morgagni');


--
-- TOC entry 3384 (class 0 OID 16517)
-- Dependencies: 210
-- Data for Name: school_history; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.school_history OVERRIDING SYSTEM VALUE VALUES (1, 12, '2023-11-08 17:10:10.659919+01', '2023-11-08 17:10:10.679371+01', 'Fede', 'Morgagni');
INSERT INTO public.school_history OVERRIDING SYSTEM VALUE VALUES (2, 13, '2023-11-08 17:10:56.414211+01', '2023-11-08 17:10:56.435342+01', 'Fede', 'Morgagni');
INSERT INTO public.school_history OVERRIDING SYSTEM VALUE VALUES (3, 14, '2023-11-08 17:17:44.464797+01', '2023-11-08 17:17:44.514653+01', 'Fede', 'Morgagni');
INSERT INTO public.school_history OVERRIDING SYSTEM VALUE VALUES (4, 15, '2023-11-08 17:19:01.674651+01', '2023-11-08 17:19:01.697595+01', 'Fede', 'Morgagni');
INSERT INTO public.school_history OVERRIDING SYSTEM VALUE VALUES (5, 16, '2023-11-08 17:19:33.665426+01', '2023-11-08 17:19:33.693634+01', 'Fede', 'Morgagni');


--
-- TOC entry 3389 (class 0 OID 16562)
-- Dependencies: 216
-- Data for Name: school_year; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3390 (class 0 OID 16567)
-- Dependencies: 217
-- Data for Name: school_year_history; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3399 (class 0 OID 0)
-- Dependencies: 213
-- Name: school_history_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.school_history_id_seq', 5, true);


--
-- TOC entry 3400 (class 0 OID 0)
-- Dependencies: 214
-- Name: school_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.school_id_seq', 16, true);


--
-- TOC entry 3401 (class 0 OID 0)
-- Dependencies: 218
-- Name: school_year_history_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.school_year_history_id_seq', 1, false);


--
-- TOC entry 3402 (class 0 OID 0)
-- Dependencies: 219
-- Name: school_year_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.school_year_id_seq', 1, false);


--
-- TOC entry 3240 (class 2606 OID 16545)
-- Name: school_history school_history_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.school_history
    ADD CONSTRAINT school_history_pkey PRIMARY KEY (id);


--
-- TOC entry 3242 (class 2620 OID 16548)
-- Name: school tr_school_history; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER tr_school_history AFTER UPDATE ON public.school FOR EACH ROW EXECUTE FUNCTION public.tr_fn_school_history();


--
-- TOC entry 3241 (class 2620 OID 16549)
-- Name: school tr_start_datetime; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER tr_start_datetime BEFORE INSERT OR UPDATE ON public.school FOR EACH ROW EXECUTE FUNCTION public.tr_fn_update_start_datetime();


-- Completed on 2023-11-08 17:21:50 CET

--
-- PostgreSQL database dump complete
--

