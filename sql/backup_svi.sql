--
-- PostgreSQL database dump
--

-- Dumped from database version 16.0 (Ubuntu 16.0-1.pgdg22.04+1)
-- Dumped by pg_dump version 16.0 (Ubuntu 16.0-1.pgdg22.04+1)

-- Started on 2023-11-05 16:19:58 CET

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 215 (class 1259 OID 16389)
-- Name: base; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.base (
    object_id integer NOT NULL,
    start_datetime timestamp with time zone NOT NULL,
    end_datetime timestamp with time zone,
    active boolean DEFAULT true NOT NULL,
    log_user character varying(256)
);


ALTER TABLE public.base OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 16464)
-- Name: school; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.school (
    id integer NOT NULL,
    name character varying(256) NOT NULL
)
INHERITS (public.base);


ALTER TABLE public.school OWNER TO postgres;

--
-- TOC entry 218 (class 1259 OID 16470)
-- Name: active_school; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.active_school AS
 SELECT object_id,
    start_datetime,
    end_datetime,
    active,
    id,
    name,
    log_user
   FROM public.school
  WHERE ((active = true) AND (end_datetime IS NULL))
  ORDER BY object_id;


ALTER VIEW public.active_school OWNER TO postgres;

--
-- TOC entry 216 (class 1259 OID 16463)
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
-- TOC entry 3229 (class 2604 OID 16467)
-- Name: school active; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.school ALTER COLUMN active SET DEFAULT true;


--
-- TOC entry 3374 (class 0 OID 16389)
-- Dependencies: 215
-- Data for Name: base; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.base (object_id, start_datetime, end_datetime, active, log_user) FROM stdin;
\.


--
-- TOC entry 3376 (class 0 OID 16464)
-- Dependencies: 217
-- Data for Name: school; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.school (object_id, start_datetime, end_datetime, active, id, name, log_user) FROM stdin;
1	2023-11-03 18:52:09.010172+01	2023-11-03 18:59:39.681425+01	f	1	test	admin
1	2023-11-03 19:00:45.93331+01	\N	t	2	test	admin
\.


--
-- TOC entry 3382 (class 0 OID 0)
-- Dependencies: 216
-- Name: school_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.school_id_seq', 2, true);


-- Completed on 2023-11-05 16:19:59 CET

--
-- PostgreSQL database dump complete
--

