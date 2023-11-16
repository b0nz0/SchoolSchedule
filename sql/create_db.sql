--
-- PostgreSQL database dump
--

-- Dumped from database version 14.9 (Ubuntu 14.9-0ubuntu0.22.04.1)
-- Dumped by pg_dump version 14.9 (Ubuntu 14.9-0ubuntu0.22.04.1)

-- Started on 2023-11-16 19:53:00 CET

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
-- TOC entry 3453 (class 1262 OID 16752)
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
-- TOC entry 234 (class 1255 OID 16753)
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
-- TOC entry 235 (class 1255 OID 16754)
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
-- TOC entry 236 (class 1255 OID 16755)
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
-- TOC entry 209 (class 1259 OID 16756)
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
-- TOC entry 210 (class 1259 OID 16761)
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
-- TOC entry 211 (class 1259 OID 16765)
-- Name: base; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.base (
    start_datetime timestamp with time zone,
    log_user character varying
);


ALTER TABLE public.base OWNER TO postgres;

--
-- TOC entry 212 (class 1259 OID 16770)
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
-- TOC entry 213 (class 1259 OID 16774)
-- Name: class_; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.class_ (
    id integer NOT NULL,
    start_datetime timestamp with time zone,
    log_user character varying,
    school_year_id integer NOT NULL,
    year_id integer NOT NULL,
    section_id integer NOT NULL
);


ALTER TABLE public.class_ OWNER TO postgres;

--
-- TOC entry 214 (class 1259 OID 16779)
-- Name: class_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.class_ ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.class_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 215 (class 1259 OID 16780)
-- Name: person; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.person (
    id integer NOT NULL,
    start_datetime timestamp with time zone,
    log_user character varying,
    fullname character varying(256),
    title character varying(24),
    is_impersonal boolean,
    person_type character varying(24),
    school_id integer NOT NULL
);


ALTER TABLE public.person OWNER TO postgres;

--
-- TOC entry 216 (class 1259 OID 16785)
-- Name: person_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.person ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.person_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 217 (class 1259 OID 16786)
-- Name: room; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.room (
    id integer NOT NULL,
    start_datetime timestamp with time zone,
    log_user character varying,
    identifier character varying(256),
    room_type character varying(256),
    school_id integer NOT NULL
);


ALTER TABLE public.room OWNER TO postgres;

--
-- TOC entry 218 (class 1259 OID 16791)
-- Name: room_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.room ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.room_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 219 (class 1259 OID 16792)
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
-- TOC entry 220 (class 1259 OID 16797)
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
-- TOC entry 221 (class 1259 OID 16798)
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
-- TOC entry 222 (class 1259 OID 16799)
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
-- TOC entry 223 (class 1259 OID 16804)
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
-- TOC entry 224 (class 1259 OID 16809)
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
-- TOC entry 225 (class 1259 OID 16810)
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
-- TOC entry 226 (class 1259 OID 16811)
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
-- TOC entry 227 (class 1259 OID 16816)
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
-- TOC entry 228 (class 1259 OID 16817)
-- Name: subject; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.subject (
    id integer NOT NULL,
    start_datetime timestamp with time zone,
    log_user character varying,
    identifier character varying(256),
    school_id integer NOT NULL
);


ALTER TABLE public.subject OWNER TO postgres;

--
-- TOC entry 229 (class 1259 OID 16822)
-- Name: subject_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.subject ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.subject_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 233 (class 1259 OID 16869)
-- Name: subject_in_class; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.subject_in_class (
    id integer NOT NULL,
    start_datetime timestamp with time zone,
    log_user character varying,
    hours_total numeric,
    max_hours_per_day numeric,
    class_id integer NOT NULL,
    subject_id integer NOT NULL
);


ALTER TABLE public.subject_in_class OWNER TO postgres;

--
-- TOC entry 232 (class 1259 OID 16868)
-- Name: subject_in_class_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.subject_in_class ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.subject_in_class_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 230 (class 1259 OID 16823)
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
-- TOC entry 231 (class 1259 OID 16828)
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
-- TOC entry 3278 (class 2606 OID 16830)
-- Name: class_ class_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.class_
    ADD CONSTRAINT class_pkey PRIMARY KEY (id);


--
-- TOC entry 3280 (class 2606 OID 16832)
-- Name: person person_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.person
    ADD CONSTRAINT person_pkey PRIMARY KEY (id);


--
-- TOC entry 3282 (class 2606 OID 16834)
-- Name: room room_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.room
    ADD CONSTRAINT room_pkey PRIMARY KEY (id);


--
-- TOC entry 3284 (class 2606 OID 16836)
-- Name: school_history school_history_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.school_history
    ADD CONSTRAINT school_history_pkey PRIMARY KEY (id);


--
-- TOC entry 3276 (class 2606 OID 16838)
-- Name: school school_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.school
    ADD CONSTRAINT school_pkey PRIMARY KEY (id);


--
-- TOC entry 3288 (class 2606 OID 16840)
-- Name: school_year_history school_year_history_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.school_year_history
    ADD CONSTRAINT school_year_history_pkey PRIMARY KEY (id);


--
-- TOC entry 3286 (class 2606 OID 16842)
-- Name: school_year school_year_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.school_year
    ADD CONSTRAINT school_year_pkey PRIMARY KEY (id);


--
-- TOC entry 3290 (class 2606 OID 16844)
-- Name: section section_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.section
    ADD CONSTRAINT section_pkey PRIMARY KEY (id);


--
-- TOC entry 3296 (class 2606 OID 16875)
-- Name: subject_in_class subject_in_class_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subject_in_class
    ADD CONSTRAINT subject_in_class_pkey PRIMARY KEY (id);


--
-- TOC entry 3292 (class 2606 OID 16846)
-- Name: subject subject_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subject
    ADD CONSTRAINT subject_pkey PRIMARY KEY (id);


--
-- TOC entry 3294 (class 2606 OID 16848)
-- Name: year year_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.year
    ADD CONSTRAINT year_pkey PRIMARY KEY (id);


--
-- TOC entry 3299 (class 2620 OID 16849)
-- Name: class_ tr_class_start_datetime; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER tr_class_start_datetime BEFORE INSERT OR UPDATE ON public.class_ FOR EACH ROW EXECUTE FUNCTION public.tr_fn_update_start_datetime();


--
-- TOC entry 3300 (class 2620 OID 16850)
-- Name: person tr_person_start_datetime; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER tr_person_start_datetime BEFORE INSERT OR UPDATE ON public.person FOR EACH ROW EXECUTE FUNCTION public.tr_fn_update_start_datetime();


--
-- TOC entry 3301 (class 2620 OID 16851)
-- Name: room tr_room_start_datetime; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER tr_room_start_datetime BEFORE INSERT OR UPDATE ON public.room FOR EACH ROW EXECUTE FUNCTION public.tr_fn_update_start_datetime();


--
-- TOC entry 3298 (class 2620 OID 16852)
-- Name: school tr_school_history; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER tr_school_history AFTER UPDATE ON public.school FOR EACH ROW EXECUTE FUNCTION public.tr_fn_school_history();


--
-- TOC entry 3297 (class 2620 OID 16853)
-- Name: school tr_school_start_datetime; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER tr_school_start_datetime BEFORE INSERT OR UPDATE ON public.school FOR EACH ROW EXECUTE FUNCTION public.tr_fn_update_start_datetime();


--
-- TOC entry 3303 (class 2620 OID 16854)
-- Name: school_year tr_school_start_datetime; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER tr_school_start_datetime BEFORE INSERT OR UPDATE ON public.school_year FOR EACH ROW EXECUTE FUNCTION public.tr_fn_update_start_datetime();


--
-- TOC entry 3302 (class 2620 OID 16855)
-- Name: school_year tr_school_year_history; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER tr_school_year_history AFTER UPDATE ON public.school_year FOR EACH ROW EXECUTE FUNCTION public.tr_fn_school_year_history();


--
-- TOC entry 3304 (class 2620 OID 16856)
-- Name: section tr_section_start_datetime; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER tr_section_start_datetime BEFORE INSERT OR UPDATE ON public.section FOR EACH ROW EXECUTE FUNCTION public.tr_fn_update_start_datetime();


--
-- TOC entry 3307 (class 2620 OID 16876)
-- Name: subject_in_class tr_subject_in_class_start_datetime; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER tr_subject_in_class_start_datetime BEFORE INSERT OR UPDATE ON public.subject_in_class FOR EACH ROW EXECUTE FUNCTION public.tr_fn_update_start_datetime();


--
-- TOC entry 3305 (class 2620 OID 16857)
-- Name: subject tr_subject_start_datetime; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER tr_subject_start_datetime BEFORE INSERT OR UPDATE ON public.subject FOR EACH ROW EXECUTE FUNCTION public.tr_fn_update_start_datetime();


--
-- TOC entry 3306 (class 2620 OID 16858)
-- Name: year tr_year_start_datetime; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER tr_year_start_datetime BEFORE INSERT OR UPDATE ON public.year FOR EACH ROW EXECUTE FUNCTION public.tr_fn_update_start_datetime();


-- Completed on 2023-11-16 19:53:01 CET

--
-- PostgreSQL database dump complete
--

