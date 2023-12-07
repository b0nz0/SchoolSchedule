--
-- PostgreSQL database dump
--

-- Dumped from database version 14.9 (Ubuntu 14.9-0ubuntu0.22.04.1)
-- Dumped by pg_dump version 14.9 (Ubuntu 14.9-0ubuntu0.22.04.1)

-- Started on 2023-12-07 14:58:41 CET

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
-- TOC entry 3541 (class 1262 OID 17957)
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
-- TOC entry 246 (class 1255 OID 17958)
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
-- TOC entry 247 (class 1255 OID 17959)
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
-- TOC entry 248 (class 1255 OID 17960)
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
-- TOC entry 209 (class 1259 OID 17961)
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
-- TOC entry 210 (class 1259 OID 17966)
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
-- TOC entry 211 (class 1259 OID 17970)
-- Name: base; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.base (
    start_datetime timestamp with time zone,
    log_user character varying
);


ALTER TABLE public.base OWNER TO postgres;

--
-- TOC entry 212 (class 1259 OID 17975)
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
-- TOC entry 213 (class 1259 OID 17979)
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
-- TOC entry 214 (class 1259 OID 17984)
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
-- TOC entry 215 (class 1259 OID 17985)
-- Name: class_plan; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.class_plan (
    id integer NOT NULL,
    start_datetime timestamp with time zone,
    log_user character varying,
    class_id integer NOT NULL,
    plan_id integer NOT NULL
);


ALTER TABLE public.class_plan OWNER TO postgres;

--
-- TOC entry 216 (class 1259 OID 17990)
-- Name: class_plan_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.class_plan ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.class_plan_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 245 (class 1259 OID 18255)
-- Name: constraint; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."constraint" (
    id integer NOT NULL,
    start_datetime timestamp with time zone,
    log_user character varying,
    identifier character varying,
    kind character varying,
    configuration character varying,
    engine_id integer
);


ALTER TABLE public."constraint" OWNER TO postgres;

--
-- TOC entry 244 (class 1259 OID 18254)
-- Name: constraint_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public."constraint" ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.constraint_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 217 (class 1259 OID 17991)
-- Name: daily_hour; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.daily_hour (
    id integer NOT NULL,
    start_datetime timestamp with time zone,
    log_user character varying,
    week_day character varying(24),
    ordinal smallint,
    plan_id integer NOT NULL,
    hour_id integer NOT NULL
);


ALTER TABLE public.daily_hour OWNER TO postgres;

--
-- TOC entry 218 (class 1259 OID 17996)
-- Name: daily_hour_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.daily_hour ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.daily_hour_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 219 (class 1259 OID 17997)
-- Name: hour; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.hour (
    id integer NOT NULL,
    start_datetime timestamp with time zone,
    log_user character varying,
    start time without time zone,
    minutes smallint,
    school_id integer NOT NULL
);


ALTER TABLE public.hour OWNER TO postgres;

--
-- TOC entry 220 (class 1259 OID 18002)
-- Name: hour_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.hour ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.hour_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 221 (class 1259 OID 18003)
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
-- TOC entry 222 (class 1259 OID 18008)
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
-- TOC entry 223 (class 1259 OID 18009)
-- Name: person_to_subject_in_class; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.person_to_subject_in_class (
    id integer NOT NULL,
    start_datetime timestamp with time zone,
    log_user character varying,
    subject_in_class_id integer NOT NULL,
    person_id integer NOT NULL
);


ALTER TABLE public.person_to_subject_in_class OWNER TO postgres;

--
-- TOC entry 224 (class 1259 OID 18014)
-- Name: person_to_subject_in_class_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.person_to_subject_in_class ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.person_to_subject_in_class_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 225 (class 1259 OID 18015)
-- Name: plan; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.plan (
    id integer NOT NULL,
    start_datetime timestamp with time zone,
    log_user character varying,
    identifier character varying,
    school_id integer NOT NULL
);


ALTER TABLE public.plan OWNER TO postgres;

--
-- TOC entry 226 (class 1259 OID 18020)
-- Name: plan_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.plan ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.plan_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 227 (class 1259 OID 18021)
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
-- TOC entry 228 (class 1259 OID 18026)
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
-- TOC entry 229 (class 1259 OID 18027)
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
-- TOC entry 230 (class 1259 OID 18032)
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
-- TOC entry 231 (class 1259 OID 18033)
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
-- TOC entry 232 (class 1259 OID 18034)
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
-- TOC entry 233 (class 1259 OID 18039)
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
-- TOC entry 234 (class 1259 OID 18044)
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
-- TOC entry 235 (class 1259 OID 18045)
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
-- TOC entry 236 (class 1259 OID 18046)
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
-- TOC entry 237 (class 1259 OID 18051)
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
-- TOC entry 238 (class 1259 OID 18052)
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
-- TOC entry 239 (class 1259 OID 18057)
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
-- TOC entry 240 (class 1259 OID 18058)
-- Name: subject_in_class; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.subject_in_class (
    id integer NOT NULL,
    start_datetime timestamp with time zone,
    log_user character varying,
    hours_total numeric,
    max_hours_per_day numeric,
    class_id integer NOT NULL,
    subject_id integer NOT NULL,
    room_id integer
);


ALTER TABLE public.subject_in_class OWNER TO postgres;

--
-- TOC entry 241 (class 1259 OID 18063)
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
-- TOC entry 242 (class 1259 OID 18064)
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
-- TOC entry 243 (class 1259 OID 18069)
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
-- TOC entry 3308 (class 2606 OID 18071)
-- Name: class_ class_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.class_
    ADD CONSTRAINT class_pkey PRIMARY KEY (id);


--
-- TOC entry 3313 (class 2606 OID 18073)
-- Name: class_plan class_plan_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.class_plan
    ADD CONSTRAINT class_plan_pkey PRIMARY KEY (id);


--
-- TOC entry 3358 (class 2606 OID 18261)
-- Name: constraint constraint_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."constraint"
    ADD CONSTRAINT constraint_pkey PRIMARY KEY (id);


--
-- TOC entry 3317 (class 2606 OID 18075)
-- Name: daily_hour daily_hour_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.daily_hour
    ADD CONSTRAINT daily_hour_pkey PRIMARY KEY (id);


--
-- TOC entry 3322 (class 2606 OID 18077)
-- Name: hour hour_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.hour
    ADD CONSTRAINT hour_pkey PRIMARY KEY (id);


--
-- TOC entry 3325 (class 2606 OID 18079)
-- Name: person person_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.person
    ADD CONSTRAINT person_pkey PRIMARY KEY (id);


--
-- TOC entry 3329 (class 2606 OID 18081)
-- Name: person_to_subject_in_class person_to_subject_in_class_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.person_to_subject_in_class
    ADD CONSTRAINT person_to_subject_in_class_pkey PRIMARY KEY (id);


--
-- TOC entry 3332 (class 2606 OID 18083)
-- Name: plan plan_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.plan
    ADD CONSTRAINT plan_pkey PRIMARY KEY (id);


--
-- TOC entry 3335 (class 2606 OID 18085)
-- Name: room room_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.room
    ADD CONSTRAINT room_pkey PRIMARY KEY (id);


--
-- TOC entry 3337 (class 2606 OID 18087)
-- Name: school_history school_history_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.school_history
    ADD CONSTRAINT school_history_pkey PRIMARY KEY (id);


--
-- TOC entry 3306 (class 2606 OID 18089)
-- Name: school school_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.school
    ADD CONSTRAINT school_pkey PRIMARY KEY (id);


--
-- TOC entry 3342 (class 2606 OID 18091)
-- Name: school_year_history school_year_history_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.school_year_history
    ADD CONSTRAINT school_year_history_pkey PRIMARY KEY (id);


--
-- TOC entry 3340 (class 2606 OID 18093)
-- Name: school_year school_year_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.school_year
    ADD CONSTRAINT school_year_pkey PRIMARY KEY (id);


--
-- TOC entry 3345 (class 2606 OID 18095)
-- Name: section section_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.section
    ADD CONSTRAINT section_pkey PRIMARY KEY (id);


--
-- TOC entry 3353 (class 2606 OID 18097)
-- Name: subject_in_class subject_in_class_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subject_in_class
    ADD CONSTRAINT subject_in_class_pkey PRIMARY KEY (id);


--
-- TOC entry 3348 (class 2606 OID 18099)
-- Name: subject subject_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subject
    ADD CONSTRAINT subject_pkey PRIMARY KEY (id);


--
-- TOC entry 3356 (class 2606 OID 18101)
-- Name: year year_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.year
    ADD CONSTRAINT year_pkey PRIMARY KEY (id);


--
-- TOC entry 3314 (class 1259 OID 18102)
-- Name: fki_FK_class_plan_class; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "fki_FK_class_plan_class" ON public.class_plan USING btree (class_id);


--
-- TOC entry 3315 (class 1259 OID 18103)
-- Name: fki_FK_class_plan_plan; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "fki_FK_class_plan_plan" ON public.class_plan USING btree (plan_id);


--
-- TOC entry 3309 (class 1259 OID 18104)
-- Name: fki_FK_class_schoolyear; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "fki_FK_class_schoolyear" ON public.class_ USING btree (school_year_id);


--
-- TOC entry 3310 (class 1259 OID 18105)
-- Name: fki_FK_class_section; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "fki_FK_class_section" ON public.class_ USING btree (section_id);


--
-- TOC entry 3311 (class 1259 OID 18106)
-- Name: fki_FK_class_year; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "fki_FK_class_year" ON public.class_ USING btree (year_id);


--
-- TOC entry 3318 (class 1259 OID 18107)
-- Name: fki_FK_daily_hour_hour; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "fki_FK_daily_hour_hour" ON public.daily_hour USING btree (hour_id);


--
-- TOC entry 3319 (class 1259 OID 18108)
-- Name: fki_FK_daily_hour_plan; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "fki_FK_daily_hour_plan" ON public.daily_hour USING btree (plan_id);


--
-- TOC entry 3320 (class 1259 OID 18109)
-- Name: fki_FK_hour_school; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "fki_FK_hour_school" ON public.hour USING btree (school_id);


--
-- TOC entry 3323 (class 1259 OID 18110)
-- Name: fki_FK_person_school; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "fki_FK_person_school" ON public.person USING btree (school_id);


--
-- TOC entry 3326 (class 1259 OID 18111)
-- Name: fki_FK_person_to_subject_in_class_person; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "fki_FK_person_to_subject_in_class_person" ON public.person_to_subject_in_class USING btree (person_id);


--
-- TOC entry 3327 (class 1259 OID 18112)
-- Name: fki_FK_person_to_subject_in_class_subject_in_class; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "fki_FK_person_to_subject_in_class_subject_in_class" ON public.person_to_subject_in_class USING btree (subject_in_class_id);


--
-- TOC entry 3330 (class 1259 OID 18113)
-- Name: fki_FK_plan_school; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "fki_FK_plan_school" ON public.plan USING btree (school_id);


--
-- TOC entry 3333 (class 1259 OID 18114)
-- Name: fki_FK_room_school; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "fki_FK_room_school" ON public.room USING btree (school_id);


--
-- TOC entry 3338 (class 1259 OID 18115)
-- Name: fki_FK_schoolyear_school; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "fki_FK_schoolyear_school" ON public.school_year USING btree (school_id);


--
-- TOC entry 3343 (class 1259 OID 18116)
-- Name: fki_FK_section_school; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "fki_FK_section_school" ON public.section USING btree (school_id);


--
-- TOC entry 3349 (class 1259 OID 18117)
-- Name: fki_FK_subject_in_class_class; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "fki_FK_subject_in_class_class" ON public.subject_in_class USING btree (class_id);


--
-- TOC entry 3350 (class 1259 OID 18118)
-- Name: fki_FK_subject_in_class_room; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "fki_FK_subject_in_class_room" ON public.subject_in_class USING btree (room_id);


--
-- TOC entry 3351 (class 1259 OID 18119)
-- Name: fki_FK_subject_in_class_subject; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "fki_FK_subject_in_class_subject" ON public.subject_in_class USING btree (subject_id);


--
-- TOC entry 3346 (class 1259 OID 18120)
-- Name: fki_FK_subject_school; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "fki_FK_subject_school" ON public.subject USING btree (school_id);


--
-- TOC entry 3354 (class 1259 OID 18121)
-- Name: fki_FK_year_school; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "fki_FK_year_school" ON public.year USING btree (school_id);


--
-- TOC entry 3382 (class 2620 OID 18122)
-- Name: class_plan tr_class_plan_start_datetime; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER tr_class_plan_start_datetime BEFORE INSERT OR UPDATE ON public.class_plan FOR EACH ROW EXECUTE FUNCTION public.tr_fn_update_start_datetime();


--
-- TOC entry 3381 (class 2620 OID 18123)
-- Name: class_ tr_class_start_datetime; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER tr_class_start_datetime BEFORE INSERT OR UPDATE ON public.class_ FOR EACH ROW EXECUTE FUNCTION public.tr_fn_update_start_datetime();


--
-- TOC entry 3395 (class 2620 OID 18262)
-- Name: constraint tr_constraint_start_datetime; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER tr_constraint_start_datetime BEFORE INSERT OR UPDATE ON public."constraint" FOR EACH ROW EXECUTE FUNCTION public.tr_fn_update_start_datetime();


--
-- TOC entry 3383 (class 2620 OID 18124)
-- Name: daily_hour tr_daily_hour_start_datetime; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER tr_daily_hour_start_datetime BEFORE INSERT OR UPDATE ON public.daily_hour FOR EACH ROW EXECUTE FUNCTION public.tr_fn_update_start_datetime();


--
-- TOC entry 3384 (class 2620 OID 18125)
-- Name: hour tr_hour_start_datetime; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER tr_hour_start_datetime BEFORE INSERT OR UPDATE ON public.hour FOR EACH ROW EXECUTE FUNCTION public.tr_fn_update_start_datetime();


--
-- TOC entry 3385 (class 2620 OID 18126)
-- Name: person tr_person_start_datetime; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER tr_person_start_datetime BEFORE INSERT OR UPDATE ON public.person FOR EACH ROW EXECUTE FUNCTION public.tr_fn_update_start_datetime();


--
-- TOC entry 3386 (class 2620 OID 18127)
-- Name: person_to_subject_in_class tr_person_to_subject_in_class_start_datetime; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER tr_person_to_subject_in_class_start_datetime BEFORE INSERT OR UPDATE ON public.person_to_subject_in_class FOR EACH ROW EXECUTE FUNCTION public.tr_fn_update_start_datetime();


--
-- TOC entry 3387 (class 2620 OID 18128)
-- Name: plan tr_plan_start_datetime; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER tr_plan_start_datetime BEFORE INSERT OR UPDATE ON public.plan FOR EACH ROW EXECUTE FUNCTION public.tr_fn_update_start_datetime();


--
-- TOC entry 3388 (class 2620 OID 18129)
-- Name: room tr_room_start_datetime; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER tr_room_start_datetime BEFORE INSERT OR UPDATE ON public.room FOR EACH ROW EXECUTE FUNCTION public.tr_fn_update_start_datetime();


--
-- TOC entry 3379 (class 2620 OID 18130)
-- Name: school tr_school_history; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER tr_school_history AFTER UPDATE ON public.school FOR EACH ROW EXECUTE FUNCTION public.tr_fn_school_history();


--
-- TOC entry 3380 (class 2620 OID 18131)
-- Name: school tr_school_start_datetime; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER tr_school_start_datetime BEFORE INSERT OR UPDATE ON public.school FOR EACH ROW EXECUTE FUNCTION public.tr_fn_update_start_datetime();


--
-- TOC entry 3389 (class 2620 OID 18132)
-- Name: school_year tr_school_start_datetime; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER tr_school_start_datetime BEFORE INSERT OR UPDATE ON public.school_year FOR EACH ROW EXECUTE FUNCTION public.tr_fn_update_start_datetime();


--
-- TOC entry 3390 (class 2620 OID 18133)
-- Name: school_year tr_school_year_history; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER tr_school_year_history AFTER UPDATE ON public.school_year FOR EACH ROW EXECUTE FUNCTION public.tr_fn_school_year_history();


--
-- TOC entry 3391 (class 2620 OID 18134)
-- Name: section tr_section_start_datetime; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER tr_section_start_datetime BEFORE INSERT OR UPDATE ON public.section FOR EACH ROW EXECUTE FUNCTION public.tr_fn_update_start_datetime();


--
-- TOC entry 3393 (class 2620 OID 18135)
-- Name: subject_in_class tr_subject_in_class_start_datetime; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER tr_subject_in_class_start_datetime BEFORE INSERT OR UPDATE ON public.subject_in_class FOR EACH ROW EXECUTE FUNCTION public.tr_fn_update_start_datetime();


--
-- TOC entry 3392 (class 2620 OID 18136)
-- Name: subject tr_subject_start_datetime; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER tr_subject_start_datetime BEFORE INSERT OR UPDATE ON public.subject FOR EACH ROW EXECUTE FUNCTION public.tr_fn_update_start_datetime();


--
-- TOC entry 3394 (class 2620 OID 18137)
-- Name: year tr_year_start_datetime; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER tr_year_start_datetime BEFORE INSERT OR UPDATE ON public.year FOR EACH ROW EXECUTE FUNCTION public.tr_fn_update_start_datetime();


--
-- TOC entry 3362 (class 2606 OID 18138)
-- Name: class_plan FK_class_plan_class; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.class_plan
    ADD CONSTRAINT "FK_class_plan_class" FOREIGN KEY (class_id) REFERENCES public.class_(id);


--
-- TOC entry 3363 (class 2606 OID 18143)
-- Name: class_plan FK_class_plan_plan; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.class_plan
    ADD CONSTRAINT "FK_class_plan_plan" FOREIGN KEY (plan_id) REFERENCES public.plan(id);


--
-- TOC entry 3359 (class 2606 OID 18148)
-- Name: class_ FK_class_schoolyear; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.class_
    ADD CONSTRAINT "FK_class_schoolyear" FOREIGN KEY (school_year_id) REFERENCES public.school_year(id) NOT VALID;


--
-- TOC entry 3360 (class 2606 OID 18153)
-- Name: class_ FK_class_section; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.class_
    ADD CONSTRAINT "FK_class_section" FOREIGN KEY (section_id) REFERENCES public.section(id) NOT VALID;


--
-- TOC entry 3361 (class 2606 OID 18158)
-- Name: class_ FK_class_year; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.class_
    ADD CONSTRAINT "FK_class_year" FOREIGN KEY (year_id) REFERENCES public.year(id) NOT VALID;


--
-- TOC entry 3364 (class 2606 OID 18163)
-- Name: daily_hour FK_daily_hour_hour; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.daily_hour
    ADD CONSTRAINT "FK_daily_hour_hour" FOREIGN KEY (hour_id) REFERENCES public.hour(id);


--
-- TOC entry 3365 (class 2606 OID 18168)
-- Name: daily_hour FK_daily_hour_plan; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.daily_hour
    ADD CONSTRAINT "FK_daily_hour_plan" FOREIGN KEY (plan_id) REFERENCES public.plan(id);


--
-- TOC entry 3366 (class 2606 OID 18173)
-- Name: hour FK_hour_school; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.hour
    ADD CONSTRAINT "FK_hour_school" FOREIGN KEY (school_id) REFERENCES public.school(id);


--
-- TOC entry 3367 (class 2606 OID 18178)
-- Name: person FK_person_school; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.person
    ADD CONSTRAINT "FK_person_school" FOREIGN KEY (school_id) REFERENCES public.school(id) NOT VALID;


--
-- TOC entry 3368 (class 2606 OID 18183)
-- Name: person_to_subject_in_class FK_person_to_subject_in_class_person; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.person_to_subject_in_class
    ADD CONSTRAINT "FK_person_to_subject_in_class_person" FOREIGN KEY (person_id) REFERENCES public.person(id);


--
-- TOC entry 3369 (class 2606 OID 18188)
-- Name: person_to_subject_in_class FK_person_to_subject_in_class_subject_in_class; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.person_to_subject_in_class
    ADD CONSTRAINT "FK_person_to_subject_in_class_subject_in_class" FOREIGN KEY (subject_in_class_id) REFERENCES public.subject_in_class(id) NOT VALID;


--
-- TOC entry 3370 (class 2606 OID 18193)
-- Name: plan FK_plan_school; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.plan
    ADD CONSTRAINT "FK_plan_school" FOREIGN KEY (school_id) REFERENCES public.school(id);


--
-- TOC entry 3371 (class 2606 OID 18198)
-- Name: room FK_room_school; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.room
    ADD CONSTRAINT "FK_room_school" FOREIGN KEY (school_id) REFERENCES public.school(id) NOT VALID;


--
-- TOC entry 3372 (class 2606 OID 18203)
-- Name: school_year FK_schoolyear_school; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.school_year
    ADD CONSTRAINT "FK_schoolyear_school" FOREIGN KEY (school_id) REFERENCES public.school(id) NOT VALID;


--
-- TOC entry 3373 (class 2606 OID 18208)
-- Name: section FK_section_school; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.section
    ADD CONSTRAINT "FK_section_school" FOREIGN KEY (school_id) REFERENCES public.school(id) NOT VALID;


--
-- TOC entry 3375 (class 2606 OID 18213)
-- Name: subject_in_class FK_subject_in_class_class; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subject_in_class
    ADD CONSTRAINT "FK_subject_in_class_class" FOREIGN KEY (class_id) REFERENCES public.class_(id) NOT VALID;


--
-- TOC entry 3376 (class 2606 OID 18218)
-- Name: subject_in_class FK_subject_in_class_room; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subject_in_class
    ADD CONSTRAINT "FK_subject_in_class_room" FOREIGN KEY (room_id) REFERENCES public.room(id);


--
-- TOC entry 3377 (class 2606 OID 18223)
-- Name: subject_in_class FK_subject_in_class_subject; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subject_in_class
    ADD CONSTRAINT "FK_subject_in_class_subject" FOREIGN KEY (subject_id) REFERENCES public.subject(id) NOT VALID;


--
-- TOC entry 3374 (class 2606 OID 18228)
-- Name: subject FK_subject_school; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subject
    ADD CONSTRAINT "FK_subject_school" FOREIGN KEY (school_id) REFERENCES public.school(id) NOT VALID;


--
-- TOC entry 3378 (class 2606 OID 18233)
-- Name: year FK_year_school; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.year
    ADD CONSTRAINT "FK_year_school" FOREIGN KEY (school_id) REFERENCES public.school(id) NOT VALID;


-- Completed on 2023-12-07 14:58:42 CET

--
-- PostgreSQL database dump complete
--

