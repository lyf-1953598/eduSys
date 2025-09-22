--
-- PostgreSQL database dump
--

-- Dumped from database version 14.7
-- Dumped by pg_dump version 14.7

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
-- Name: case_case; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.case_case (
    id bigint NOT NULL,
    name character varying(200) NOT NULL,
    longitude double precision NOT NULL,
    latitude double precision NOT NULL,
    url character varying(200) NOT NULL,
    type character varying(200) NOT NULL,
    size integer NOT NULL
);


ALTER TABLE public.case_case OWNER TO postgres;

--
-- Name: case_case_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.case_case_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.case_case_id_seq OWNER TO postgres;

--
-- Name: case_case_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.case_case_id_seq OWNED BY public.case_case.id;


--
-- Name: case_case id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.case_case ALTER COLUMN id SET DEFAULT nextval('public.case_case_id_seq'::regclass);


--
-- Data for Name: case_case; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.case_case (id, name, longitude, latitude, url, type, size) FROM stdin;
1	故宫博物院	116.4	39.92	https://www.dpm.org.cn	excellent	150
2	东方明珠	121.5	31.24	https://www.orientalpearltower.com	excellent	100
\.


--
-- Name: case_case_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.case_case_id_seq', 2, true);


--
-- Name: case_case case_case_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.case_case
    ADD CONSTRAINT case_case_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

