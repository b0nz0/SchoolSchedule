--
-- PostgreSQL database dump
--

-- Dumped from database version 16.0 (Ubuntu 16.0-1.pgdg22.04+1)
-- Dumped by pg_dump version 16.0 (Ubuntu 16.0-1.pgdg22.04+1)

-- Started on 2023-11-06 16:05:22 CET

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
-- TOC entry 3410 (class 1262 OID 16388)
-- Name: school_schedule; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE school_schedule WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_US.UTF-8';


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
-- TOC entry 225 (class 1255 OID 16505)
-- Name: tr_fn_school_history(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.tr_fn_school_history() RETURNS trigger
    LANGUAGE plpgsql
    AS $$BEGIN
 INSERT INTO school_history (object_id, start_datetime, end_datetime, active, name, log_user)
	  VALUES (OLD.id, OLD.start_datetime, now(), false, OLD.name, OLD.log_user);
 RETURN NULL;
END;$$;


ALTER FUNCTION public.tr_fn_school_history() OWNER TO postgres;

--
-- TOC entry 224 (class 1255 OID 16522)
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
-- TOC entry 215 (class 1259 OID 16389)
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
-- TOC entry 217 (class 1259 OID 16464)
-- Name: school_history; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.school_history (
    id integer NOT NULL,
    name character varying(256) NOT NULL
)
INHERITS (public.base_history);


ALTER TABLE public.school_history OWNER TO postgres;

--
-- TOC entry 222 (class 1259 OID 16516)
-- Name: active_school; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.active_school AS
 SELECT object_id,
    start_datetime,
    name,
    log_user
   FROM public.school_history
  ORDER BY object_id;


ALTER VIEW public.active_school OWNER TO postgres;

--
-- TOC entry 220 (class 1259 OID 16490)
-- Name: base; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.base (
    start_datetime timestamp with time zone,
    log_user character varying
);


ALTER TABLE public.base OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 16500)
-- Name: school; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.school (
    name character varying(256) NOT NULL,
    id integer NOT NULL
)
INHERITS (public.base);


ALTER TABLE public.school OWNER TO postgres;

--
-- TOC entry 216 (class 1259 OID 16463)
-- Name: school_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.school_history ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.school_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 223 (class 1259 OID 16524)
-- Name: school_id_seq1; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.school ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.school_id_seq1
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 219 (class 1259 OID 16477)
-- Name: school_year; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.school_year (
    id integer NOT NULL,
    identifier character varying(256),
    school integer NOT NULL
)
INHERITS (public.base_history);


ALTER TABLE public.school_year OWNER TO postgres;

--
-- TOC entry 218 (class 1259 OID 16476)
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
-- TOC entry 3245 (class 2604 OID 16467)
-- Name: school_history active; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.school_history ALTER COLUMN active SET DEFAULT true;


--
-- TOC entry 3246 (class 2604 OID 16480)
-- Name: school_year active; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.school_year ALTER COLUMN active SET DEFAULT true;


--
-- TOC entry 3402 (class 0 OID 16490)
-- Dependencies: 220
-- Data for Name: base; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3397 (class 0 OID 16389)
-- Dependencies: 215
-- Data for Name: base_history; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3403 (class 0 OID 16500)
-- Dependencies: 221
-- Data for Name: school; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.school OVERRIDING SYSTEM VALUE VALUES ('nome6', '2023-11-06 12:56:18.021058+01', 'admin', 1);


--
-- TOC entry 3399 (class 0 OID 16464)
-- Dependencies: 217
-- Data for Name: school_history; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.school_history OVERRIDING SYSTEM VALUE VALUES (1, '2023-11-06 12:45:26.330548+01', '2023-11-06 12:50:12.54036+01', false, 11, 'nome2', 'admin');
INSERT INTO public.school_history OVERRIDING SYSTEM VALUE VALUES (1, '2023-11-06 12:45:26.330548+01', '2023-11-06 12:51:52.16434+01', false, 12, 'nome3', 'admin');
INSERT INTO public.school_history OVERRIDING SYSTEM VALUE VALUES (1, '2023-11-06 12:45:26.330548+01', '2023-11-06 12:54:18.190876+01', false, 13, 'nome4', 'admin');
INSERT INTO public.school_history OVERRIDING SYSTEM VALUE VALUES (1, '2023-11-06 12:54:18.190876+01', '2023-11-06 12:54:22.727758+01', false, 14, 'nome5', 'admin');
INSERT INTO public.school_history OVERRIDING SYSTEM VALUE VALUES (1, '2023-11-06 12:54:22.727758+01', '2023-11-06 12:56:18.021058+01', false, 15, 'nome5', 'admin');


--
-- TOC entry 3401 (class 0 OID 16477)
-- Dependencies: 219
-- Data for Name: school_year; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3411 (class 0 OID 0)
-- Dependencies: 216
-- Name: school_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.school_id_seq', 15, true);


--
-- TOC entry 3412 (class 0 OID 0)
-- Dependencies: 223
-- Name: school_id_seq1; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.school_id_seq1', 1, true);


--
-- TOC entry 3413 (class 0 OID 0)
-- Dependencies: 218
-- Name: school_year_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.school_year_id_seq', 1, false);


--
-- TOC entry 3248 (class 2606 OID 16514)
-- Name: school_history school_history_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.school_history
    ADD CONSTRAINT school_history_pkey PRIMARY KEY (id);


--
-- TOC entry 3250 (class 2606 OID 16484)
-- Name: school_year school_year_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.school_year
    ADD CONSTRAINT school_year_pkey PRIMARY KEY (id);


--
-- TOC entry 3251 (class 2620 OID 16515)
-- Name: school tr_school_history; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER tr_school_history AFTER UPDATE ON public.school FOR EACH ROW EXECUTE FUNCTION public.tr_fn_school_history();


--
-- TOC entry 3252 (class 2620 OID 16523)
-- Name: school tr_start_datetime; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER tr_start_datetime BEFORE INSERT OR UPDATE ON public.school FOR EACH ROW EXECUTE FUNCTION public.tr_fn_update_start_datetime();


-- Completed on 2023-11-06 16:05:24 CET

--
-- PostgreSQL database dump complete
--

