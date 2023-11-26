--
-- PostgreSQL database dump
--

-- Dumped from database version 14.9 (Ubuntu 14.9-0ubuntu0.22.04.1)
-- Dumped by pg_dump version 14.9 (Ubuntu 14.9-0ubuntu0.22.04.1)

-- Started on 2023-11-26 14:12:39 CET

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
-- TOC entry 3499 (class 1262 OID 17096)
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
-- TOC entry 238 (class 1255 OID 17097)
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
-- TOC entry 239 (class 1255 OID 17098)
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
-- TOC entry 240 (class 1255 OID 17099)
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
-- TOC entry 209 (class 1259 OID 17100)
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
-- TOC entry 210 (class 1259 OID 17105)
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
-- TOC entry 211 (class 1259 OID 17109)
-- Name: base; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.base (
    start_datetime timestamp with time zone,
    log_user character varying
);


ALTER TABLE public.base OWNER TO postgres;

--
-- TOC entry 212 (class 1259 OID 17114)
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
-- TOC entry 213 (class 1259 OID 17118)
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
-- TOC entry 214 (class 1259 OID 17123)
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
-- TOC entry 237 (class 1259 OID 17322)
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
-- TOC entry 236 (class 1259 OID 17321)
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
-- TOC entry 215 (class 1259 OID 17124)
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
-- TOC entry 216 (class 1259 OID 17129)
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
-- TOC entry 217 (class 1259 OID 17130)
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
-- TOC entry 218 (class 1259 OID 17135)
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
-- TOC entry 219 (class 1259 OID 17136)
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
-- TOC entry 220 (class 1259 OID 17141)
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
-- TOC entry 221 (class 1259 OID 17142)
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
-- TOC entry 222 (class 1259 OID 17147)
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
-- TOC entry 223 (class 1259 OID 17148)
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
-- TOC entry 224 (class 1259 OID 17149)
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
-- TOC entry 225 (class 1259 OID 17154)
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
-- TOC entry 226 (class 1259 OID 17159)
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
-- TOC entry 227 (class 1259 OID 17160)
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
-- TOC entry 228 (class 1259 OID 17161)
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
-- TOC entry 229 (class 1259 OID 17166)
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
-- TOC entry 230 (class 1259 OID 17167)
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
-- TOC entry 231 (class 1259 OID 17172)
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
-- TOC entry 232 (class 1259 OID 17173)
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
-- TOC entry 233 (class 1259 OID 17178)
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
-- TOC entry 234 (class 1259 OID 17179)
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
-- TOC entry 235 (class 1259 OID 17184)
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
-- TOC entry 3288 (class 2606 OID 17186)
-- Name: class_ class_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.class_
    ADD CONSTRAINT class_pkey PRIMARY KEY (id);


--
-- TOC entry 3325 (class 2606 OID 17328)
-- Name: hour hour_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.hour
    ADD CONSTRAINT hour_pkey PRIMARY KEY (id);


--
-- TOC entry 3294 (class 2606 OID 17188)
-- Name: person person_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.person
    ADD CONSTRAINT person_pkey PRIMARY KEY (id);


--
-- TOC entry 3298 (class 2606 OID 17190)
-- Name: person_to_subject_in_class person_to_subject_in_class_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.person_to_subject_in_class
    ADD CONSTRAINT person_to_subject_in_class_pkey PRIMARY KEY (id);


--
-- TOC entry 3301 (class 2606 OID 17192)
-- Name: room room_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.room
    ADD CONSTRAINT room_pkey PRIMARY KEY (id);


--
-- TOC entry 3303 (class 2606 OID 17194)
-- Name: school_history school_history_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.school_history
    ADD CONSTRAINT school_history_pkey PRIMARY KEY (id);


--
-- TOC entry 3286 (class 2606 OID 17196)
-- Name: school school_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.school
    ADD CONSTRAINT school_pkey PRIMARY KEY (id);


--
-- TOC entry 3308 (class 2606 OID 17198)
-- Name: school_year_history school_year_history_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.school_year_history
    ADD CONSTRAINT school_year_history_pkey PRIMARY KEY (id);


--
-- TOC entry 3306 (class 2606 OID 17200)
-- Name: school_year school_year_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.school_year
    ADD CONSTRAINT school_year_pkey PRIMARY KEY (id);


--
-- TOC entry 3311 (class 2606 OID 17202)
-- Name: section section_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.section
    ADD CONSTRAINT section_pkey PRIMARY KEY (id);


--
-- TOC entry 3319 (class 2606 OID 17204)
-- Name: subject_in_class subject_in_class_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subject_in_class
    ADD CONSTRAINT subject_in_class_pkey PRIMARY KEY (id);


--
-- TOC entry 3314 (class 2606 OID 17206)
-- Name: subject subject_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subject
    ADD CONSTRAINT subject_pkey PRIMARY KEY (id);


--
-- TOC entry 3322 (class 2606 OID 17208)
-- Name: year year_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.year
    ADD CONSTRAINT year_pkey PRIMARY KEY (id);


--
-- TOC entry 3289 (class 1259 OID 17209)
-- Name: fki_FK_class_schoolyear; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "fki_FK_class_schoolyear" ON public.class_ USING btree (school_year_id);


--
-- TOC entry 3290 (class 1259 OID 17210)
-- Name: fki_FK_class_section; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "fki_FK_class_section" ON public.class_ USING btree (section_id);


--
-- TOC entry 3291 (class 1259 OID 17211)
-- Name: fki_FK_class_year; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "fki_FK_class_year" ON public.class_ USING btree (year_id);


--
-- TOC entry 3323 (class 1259 OID 17334)
-- Name: fki_FK_hour_school; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "fki_FK_hour_school" ON public.hour USING btree (school_id);


--
-- TOC entry 3292 (class 1259 OID 17212)
-- Name: fki_FK_person_school; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "fki_FK_person_school" ON public.person USING btree (school_id);


--
-- TOC entry 3295 (class 1259 OID 17213)
-- Name: fki_FK_person_to_subject_in_class_person; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "fki_FK_person_to_subject_in_class_person" ON public.person_to_subject_in_class USING btree (person_id);


--
-- TOC entry 3296 (class 1259 OID 17214)
-- Name: fki_FK_person_to_subject_in_class_subject_in_class; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "fki_FK_person_to_subject_in_class_subject_in_class" ON public.person_to_subject_in_class USING btree (subject_in_class_id);


--
-- TOC entry 3299 (class 1259 OID 17215)
-- Name: fki_FK_room_school; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "fki_FK_room_school" ON public.room USING btree (school_id);


--
-- TOC entry 3304 (class 1259 OID 17216)
-- Name: fki_FK_schoolyear_school; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "fki_FK_schoolyear_school" ON public.school_year USING btree (school_id);


--
-- TOC entry 3309 (class 1259 OID 17217)
-- Name: fki_FK_section_school; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "fki_FK_section_school" ON public.section USING btree (school_id);


--
-- TOC entry 3315 (class 1259 OID 17218)
-- Name: fki_FK_subject_in_class_class; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "fki_FK_subject_in_class_class" ON public.subject_in_class USING btree (class_id);


--
-- TOC entry 3316 (class 1259 OID 17219)
-- Name: fki_FK_subject_in_class_room; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "fki_FK_subject_in_class_room" ON public.subject_in_class USING btree (room_id);


--
-- TOC entry 3317 (class 1259 OID 17220)
-- Name: fki_FK_subject_in_class_subject; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "fki_FK_subject_in_class_subject" ON public.subject_in_class USING btree (subject_id);


--
-- TOC entry 3312 (class 1259 OID 17221)
-- Name: fki_FK_subject_school; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "fki_FK_subject_school" ON public.subject USING btree (school_id);


--
-- TOC entry 3320 (class 1259 OID 17222)
-- Name: fki_FK_year_school; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "fki_FK_year_school" ON public.year USING btree (school_id);


--
-- TOC entry 3343 (class 2620 OID 17223)
-- Name: class_ tr_class_start_datetime; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER tr_class_start_datetime BEFORE INSERT OR UPDATE ON public.class_ FOR EACH ROW EXECUTE FUNCTION public.tr_fn_update_start_datetime();


--
-- TOC entry 3353 (class 2620 OID 17335)
-- Name: hour tr_hour_start_datetime; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER tr_hour_start_datetime BEFORE INSERT OR UPDATE ON public.hour FOR EACH ROW EXECUTE FUNCTION public.tr_fn_update_start_datetime();


--
-- TOC entry 3344 (class 2620 OID 17224)
-- Name: person tr_person_start_datetime; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER tr_person_start_datetime BEFORE INSERT OR UPDATE ON public.person FOR EACH ROW EXECUTE FUNCTION public.tr_fn_update_start_datetime();


--
-- TOC entry 3345 (class 2620 OID 17225)
-- Name: person_to_subject_in_class tr_person_to_subject_in_class_start_datetime; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER tr_person_to_subject_in_class_start_datetime BEFORE INSERT OR UPDATE ON public.person_to_subject_in_class FOR EACH ROW EXECUTE FUNCTION public.tr_fn_update_start_datetime();


--
-- TOC entry 3346 (class 2620 OID 17226)
-- Name: room tr_room_start_datetime; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER tr_room_start_datetime BEFORE INSERT OR UPDATE ON public.room FOR EACH ROW EXECUTE FUNCTION public.tr_fn_update_start_datetime();


--
-- TOC entry 3341 (class 2620 OID 17227)
-- Name: school tr_school_history; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER tr_school_history AFTER UPDATE ON public.school FOR EACH ROW EXECUTE FUNCTION public.tr_fn_school_history();


--
-- TOC entry 3342 (class 2620 OID 17228)
-- Name: school tr_school_start_datetime; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER tr_school_start_datetime BEFORE INSERT OR UPDATE ON public.school FOR EACH ROW EXECUTE FUNCTION public.tr_fn_update_start_datetime();


--
-- TOC entry 3348 (class 2620 OID 17229)
-- Name: school_year tr_school_start_datetime; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER tr_school_start_datetime BEFORE INSERT OR UPDATE ON public.school_year FOR EACH ROW EXECUTE FUNCTION public.tr_fn_update_start_datetime();


--
-- TOC entry 3347 (class 2620 OID 17230)
-- Name: school_year tr_school_year_history; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER tr_school_year_history AFTER UPDATE ON public.school_year FOR EACH ROW EXECUTE FUNCTION public.tr_fn_school_year_history();


--
-- TOC entry 3349 (class 2620 OID 17231)
-- Name: section tr_section_start_datetime; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER tr_section_start_datetime BEFORE INSERT OR UPDATE ON public.section FOR EACH ROW EXECUTE FUNCTION public.tr_fn_update_start_datetime();


--
-- TOC entry 3351 (class 2620 OID 17232)
-- Name: subject_in_class tr_subject_in_class_start_datetime; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER tr_subject_in_class_start_datetime BEFORE INSERT OR UPDATE ON public.subject_in_class FOR EACH ROW EXECUTE FUNCTION public.tr_fn_update_start_datetime();


--
-- TOC entry 3350 (class 2620 OID 17233)
-- Name: subject tr_subject_start_datetime; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER tr_subject_start_datetime BEFORE INSERT OR UPDATE ON public.subject FOR EACH ROW EXECUTE FUNCTION public.tr_fn_update_start_datetime();


--
-- TOC entry 3352 (class 2620 OID 17234)
-- Name: year tr_year_start_datetime; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER tr_year_start_datetime BEFORE INSERT OR UPDATE ON public.year FOR EACH ROW EXECUTE FUNCTION public.tr_fn_update_start_datetime();


--
-- TOC entry 3326 (class 2606 OID 17235)
-- Name: class_ FK_class_schoolyear; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.class_
    ADD CONSTRAINT "FK_class_schoolyear" FOREIGN KEY (school_year_id) REFERENCES public.school_year(id) NOT VALID;


--
-- TOC entry 3327 (class 2606 OID 17240)
-- Name: class_ FK_class_section; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.class_
    ADD CONSTRAINT "FK_class_section" FOREIGN KEY (section_id) REFERENCES public.section(id) NOT VALID;


--
-- TOC entry 3328 (class 2606 OID 17245)
-- Name: class_ FK_class_year; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.class_
    ADD CONSTRAINT "FK_class_year" FOREIGN KEY (year_id) REFERENCES public.year(id) NOT VALID;


--
-- TOC entry 3340 (class 2606 OID 17329)
-- Name: hour FK_hour_school; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.hour
    ADD CONSTRAINT "FK_hour_school" FOREIGN KEY (school_id) REFERENCES public.school(id);


--
-- TOC entry 3329 (class 2606 OID 17250)
-- Name: person FK_person_school; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.person
    ADD CONSTRAINT "FK_person_school" FOREIGN KEY (school_id) REFERENCES public.school(id) NOT VALID;


--
-- TOC entry 3331 (class 2606 OID 17255)
-- Name: person_to_subject_in_class FK_person_to_subject_in_class_person; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.person_to_subject_in_class
    ADD CONSTRAINT "FK_person_to_subject_in_class_person" FOREIGN KEY (person_id) REFERENCES public.person(id);


--
-- TOC entry 3330 (class 2606 OID 17260)
-- Name: person_to_subject_in_class FK_person_to_subject_in_class_subject_in_class; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.person_to_subject_in_class
    ADD CONSTRAINT "FK_person_to_subject_in_class_subject_in_class" FOREIGN KEY (subject_in_class_id) REFERENCES public.subject_in_class(id) NOT VALID;


--
-- TOC entry 3332 (class 2606 OID 17265)
-- Name: room FK_room_school; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.room
    ADD CONSTRAINT "FK_room_school" FOREIGN KEY (school_id) REFERENCES public.school(id) NOT VALID;


--
-- TOC entry 3333 (class 2606 OID 17270)
-- Name: school_year FK_schoolyear_school; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.school_year
    ADD CONSTRAINT "FK_schoolyear_school" FOREIGN KEY (school_id) REFERENCES public.school(id) NOT VALID;


--
-- TOC entry 3334 (class 2606 OID 17275)
-- Name: section FK_section_school; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.section
    ADD CONSTRAINT "FK_section_school" FOREIGN KEY (school_id) REFERENCES public.school(id) NOT VALID;


--
-- TOC entry 3336 (class 2606 OID 17280)
-- Name: subject_in_class FK_subject_in_class_class; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subject_in_class
    ADD CONSTRAINT "FK_subject_in_class_class" FOREIGN KEY (class_id) REFERENCES public.class_(id) NOT VALID;


--
-- TOC entry 3337 (class 2606 OID 17285)
-- Name: subject_in_class FK_subject_in_class_room; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subject_in_class
    ADD CONSTRAINT "FK_subject_in_class_room" FOREIGN KEY (room_id) REFERENCES public.room(id);


--
-- TOC entry 3338 (class 2606 OID 17290)
-- Name: subject_in_class FK_subject_in_class_subject; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subject_in_class
    ADD CONSTRAINT "FK_subject_in_class_subject" FOREIGN KEY (subject_id) REFERENCES public.subject(id) NOT VALID;


--
-- TOC entry 3335 (class 2606 OID 17295)
-- Name: subject FK_subject_school; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subject
    ADD CONSTRAINT "FK_subject_school" FOREIGN KEY (school_id) REFERENCES public.school(id) NOT VALID;


--
-- TOC entry 3339 (class 2606 OID 17300)
-- Name: year FK_year_school; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.year
    ADD CONSTRAINT "FK_year_school" FOREIGN KEY (school_id) REFERENCES public.school(id) NOT VALID;


-- Completed on 2023-11-26 14:12:39 CET

--
-- PostgreSQL database dump complete
--

