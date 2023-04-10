--
-- PostgreSQL database dump
--

-- Dumped from database version 15.2 (Debian 15.2-1.pgdg110+1)
-- Dumped by pg_dump version 15.1

-- Started on 2023-04-10 15:41:25 UTC

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
-- TOC entry 228 (class 1259 OID 90598)
-- Name: help_centre; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.help_centre (
    staff_id bigint NOT NULL,
    person_id bigint,
    status integer
);


ALTER TABLE public.help_centre OWNER TO postgres;

--
-- TOC entry 227 (class 1259 OID 90597)
-- Name: help_centre_staff_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.help_centre_staff_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.help_centre_staff_id_seq OWNER TO postgres;

--
-- TOC entry 3417 (class 0 OID 0)
-- Dependencies: 227
-- Name: help_centre_staff_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.help_centre_staff_id_seq OWNED BY public.help_centre.staff_id;


--
-- TOC entry 218 (class 1259 OID 90538)
-- Name: owners; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.owners (
    owner_id bigint NOT NULL,
    person_id bigint
);


ALTER TABLE public.owners OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 90537)
-- Name: owners_owner_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.owners_owner_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.owners_owner_id_seq OWNER TO postgres;

--
-- TOC entry 3418 (class 0 OID 0)
-- Dependencies: 217
-- Name: owners_owner_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.owners_owner_id_seq OWNED BY public.owners.owner_id;


--
-- TOC entry 216 (class 1259 OID 90526)
-- Name: persons; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.persons (
    id bigint NOT NULL,
    name character varying(50) NOT NULL,
    lastname character varying(50) NOT NULL,
    phone integer NOT NULL,
    mail character varying(100),
    address character varying(100),
    created timestamp without time zone,
    status integer,
    password character varying(255)
);


ALTER TABLE public.persons OWNER TO postgres;

--
-- TOC entry 215 (class 1259 OID 90525)
-- Name: persons_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.persons_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.persons_id_seq OWNER TO postgres;

--
-- TOC entry 3419 (class 0 OID 0)
-- Dependencies: 215
-- Name: persons_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.persons_id_seq OWNED BY public.persons.id;


--
-- TOC entry 226 (class 1259 OID 90586)
-- Name: pets; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.pets (
    pet_id bigint NOT NULL,
    species character varying(50),
    breed character varying(100),
    gender character(2),
    medical_condition character varying(50),
    current_treatment character varying(50),
    resent_vaccination date,
    name character varying(50),
    birth_date date,
    owner_id bigint
);


ALTER TABLE public.pets OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 90585)
-- Name: pets_pet_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.pets_pet_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.pets_pet_id_seq OWNER TO postgres;

--
-- TOC entry 3420 (class 0 OID 0)
-- Dependencies: 225
-- Name: pets_pet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.pets_pet_id_seq OWNED BY public.pets.pet_id;


--
-- TOC entry 224 (class 1259 OID 90569)
-- Name: spec_combo; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.spec_combo (
    id bigint NOT NULL,
    vet_id bigint,
    spec_id bigint
);


ALTER TABLE public.spec_combo OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 90568)
-- Name: spec_combo_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.spec_combo_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.spec_combo_id_seq OWNER TO postgres;

--
-- TOC entry 3421 (class 0 OID 0)
-- Dependencies: 223
-- Name: spec_combo_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.spec_combo_id_seq OWNED BY public.spec_combo.id;


--
-- TOC entry 220 (class 1259 OID 90550)
-- Name: specialities; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.specialities (
    spec_id bigint NOT NULL,
    specialty character varying(50),
    description character varying(150)
);


ALTER TABLE public.specialities OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 90549)
-- Name: specialities_spec_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.specialities_spec_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.specialities_spec_id_seq OWNER TO postgres;

--
-- TOC entry 3422 (class 0 OID 0)
-- Dependencies: 219
-- Name: specialities_spec_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.specialities_spec_id_seq OWNED BY public.specialities.spec_id;


--
-- TOC entry 214 (class 1259 OID 90520)
-- Name: statuses; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.statuses (
    status integer NOT NULL,
    explenation character varying(50)
);


ALTER TABLE public.statuses OWNER TO postgres;

--
-- TOC entry 222 (class 1259 OID 90557)
-- Name: vets; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.vets (
    vet_id bigint NOT NULL,
    person_id bigint
);


ALTER TABLE public.vets OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 90556)
-- Name: vets_vet_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.vets_vet_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.vets_vet_id_seq OWNER TO postgres;

--
-- TOC entry 3423 (class 0 OID 0)
-- Dependencies: 221
-- Name: vets_vet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.vets_vet_id_seq OWNED BY public.vets.vet_id;


--
-- TOC entry 230 (class 1259 OID 90610)
-- Name: visits; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.visits (
    visit_id bigint NOT NULL,
    vet_id bigint,
    pet_id bigint,
    owner_id bigint,
    diagnosis character varying(100),
    treatment character varying(50),
    date date
);


ALTER TABLE public.visits OWNER TO postgres;

--
-- TOC entry 229 (class 1259 OID 90609)
-- Name: visits_visit_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.visits_visit_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.visits_visit_id_seq OWNER TO postgres;

--
-- TOC entry 3424 (class 0 OID 0)
-- Dependencies: 229
-- Name: visits_visit_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.visits_visit_id_seq OWNED BY public.visits.visit_id;


--
-- TOC entry 3221 (class 2604 OID 90601)
-- Name: help_centre staff_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.help_centre ALTER COLUMN staff_id SET DEFAULT nextval('public.help_centre_staff_id_seq'::regclass);


--
-- TOC entry 3216 (class 2604 OID 90541)
-- Name: owners owner_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.owners ALTER COLUMN owner_id SET DEFAULT nextval('public.owners_owner_id_seq'::regclass);


--
-- TOC entry 3215 (class 2604 OID 90529)
-- Name: persons id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.persons ALTER COLUMN id SET DEFAULT nextval('public.persons_id_seq'::regclass);


--
-- TOC entry 3220 (class 2604 OID 90589)
-- Name: pets pet_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pets ALTER COLUMN pet_id SET DEFAULT nextval('public.pets_pet_id_seq'::regclass);


--
-- TOC entry 3219 (class 2604 OID 90572)
-- Name: spec_combo id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.spec_combo ALTER COLUMN id SET DEFAULT nextval('public.spec_combo_id_seq'::regclass);


--
-- TOC entry 3217 (class 2604 OID 90553)
-- Name: specialities spec_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.specialities ALTER COLUMN spec_id SET DEFAULT nextval('public.specialities_spec_id_seq'::regclass);


--
-- TOC entry 3218 (class 2604 OID 90560)
-- Name: vets vet_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.vets ALTER COLUMN vet_id SET DEFAULT nextval('public.vets_vet_id_seq'::regclass);


--
-- TOC entry 3222 (class 2604 OID 90613)
-- Name: visits visit_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.visits ALTER COLUMN visit_id SET DEFAULT nextval('public.visits_visit_id_seq'::regclass);




--
-- TOC entry 3405 (class 0 OID 90569)
-- Dependencies: 224
-- Data for Name: spec_combo; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.spec_combo (id, vet_id, spec_id) FROM stdin;
\.


--
-- TOC entry 3401 (class 0 OID 90550)
-- Dependencies: 220
-- Data for Name: specialities; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.specialities (spec_id, specialty, description) FROM stdin;
1	Anesthesiology	Specializes in administering anesthesia and monitoring patients during surgery.
2	Behavioral Medicine	Specializes in diagnosing and treating behavioral issues in animals.
3	Dentistry	Specializes in diagnosing and treating dental problems in animals.
4	Endocrinology	Specializes in diagnosing and treating hormonal imbalances in animals.
5	Gastroenterology	Specializes in diagnosing and treating digestive system disorders in animals.
6	Neurology	Specializes in diagnosing and treating disorders of the nervous system in animals.
7	Opthalmology	Specializes in diagnosing and treating eye disorders in animals.
8	Rehabilitation	Specializes in providing physical therapy and rehabilitation to animals.
9	Radiology	Specializes in diagnosing and treating diseases using medical imaging techniques.
10	Surgery	Specializes in performing surgical procedures on animals.
\.


--
-- TOC entry 3395 (class 0 OID 90520)
-- Dependencies: 214
-- Data for Name: statuses; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.statuses (status, explenation) FROM stdin;
1	Owner
2	Staff
4	Vet
3	Owner/Staff
5	Owner/Vet
6	Staff/Vet
7	Owner/Staff/Vet

--

SELECT pg_catalog.setval('public.help_centre_staff_id_seq', 15, true);


--
-- TOC entry 3426 (class 0 OID 0)
-- Dependencies: 217
-- Name: owners_owner_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.owners_owner_id_seq', 48, true);


--
-- TOC entry 3427 (class 0 OID 0)
-- Dependencies: 215
-- Name: persons_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.persons_id_seq', 54, true);


--
-- TOC entry 3428 (class 0 OID 0)
-- Dependencies: 225
-- Name: pets_pet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.pets_pet_id_seq', 15, true);


--
-- TOC entry 3429 (class 0 OID 0)
-- Dependencies: 223
-- Name: spec_combo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.spec_combo_id_seq', 1, true);


--
-- TOC entry 3430 (class 0 OID 0)
-- Dependencies: 219
-- Name: specialities_spec_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.specialities_spec_id_seq', 10, true);


--
-- TOC entry 3431 (class 0 OID 0)
-- Dependencies: 221
-- Name: vets_vet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.vets_vet_id_seq', 13, true);


--
-- TOC entry 3432 (class 0 OID 0)
-- Dependencies: 229
-- Name: visits_visit_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.visits_visit_id_seq', 5, true);


--
-- TOC entry 3240 (class 2606 OID 90603)
-- Name: help_centre help_centre_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.help_centre
    ADD CONSTRAINT help_centre_pkey PRIMARY KEY (staff_id);


--
-- TOC entry 3228 (class 2606 OID 90543)
-- Name: owners owners_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.owners
    ADD CONSTRAINT owners_pkey PRIMARY KEY (owner_id);


--
-- TOC entry 3226 (class 2606 OID 90531)
-- Name: persons persons_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.persons
    ADD CONSTRAINT persons_pkey PRIMARY KEY (id);


--
-- TOC entry 3238 (class 2606 OID 90591)
-- Name: pets pets_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pets
    ADD CONSTRAINT pets_pkey PRIMARY KEY (pet_id);


--
-- TOC entry 3236 (class 2606 OID 90574)
-- Name: spec_combo spec_combo_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.spec_combo
    ADD CONSTRAINT spec_combo_pkey PRIMARY KEY (id);


--
-- TOC entry 3230 (class 2606 OID 90555)
-- Name: specialities specialities_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.specialities
    ADD CONSTRAINT specialities_pkey PRIMARY KEY (spec_id);


--
-- TOC entry 3224 (class 2606 OID 90524)
-- Name: statuses statuses_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.statuses
    ADD CONSTRAINT statuses_pkey PRIMARY KEY (status);


--
-- TOC entry 3232 (class 2606 OID 98713)
-- Name: specialities unique_specialty; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.specialities
    ADD CONSTRAINT unique_specialty UNIQUE (specialty);


--
-- TOC entry 3234 (class 2606 OID 90562)
-- Name: vets vets_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.vets
    ADD CONSTRAINT vets_pkey PRIMARY KEY (vet_id);


--
-- TOC entry 3242 (class 2606 OID 90615)
-- Name: visits visits_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.visits
    ADD CONSTRAINT visits_pkey PRIMARY KEY (visit_id);


--
-- TOC entry 3249 (class 2606 OID 90604)
-- Name: help_centre help_centre_person_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.help_centre
    ADD CONSTRAINT help_centre_person_id_fkey FOREIGN KEY (person_id) REFERENCES public.persons(id);


--
-- TOC entry 3244 (class 2606 OID 90544)
-- Name: owners owners_person_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.owners
    ADD CONSTRAINT owners_person_id_fkey FOREIGN KEY (person_id) REFERENCES public.persons(id);


--
-- TOC entry 3243 (class 2606 OID 90532)
-- Name: persons persons_status_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.persons
    ADD CONSTRAINT persons_status_fkey FOREIGN KEY (status) REFERENCES public.statuses(status);


--
-- TOC entry 3248 (class 2606 OID 90592)
-- Name: pets pets_owner_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pets
    ADD CONSTRAINT pets_owner_id_fkey FOREIGN KEY (owner_id) REFERENCES public.owners(owner_id);


--
-- TOC entry 3246 (class 2606 OID 90580)
-- Name: spec_combo spec_combo_spec_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.spec_combo
    ADD CONSTRAINT spec_combo_spec_id_fkey FOREIGN KEY (spec_id) REFERENCES public.specialities(spec_id);


--
-- TOC entry 3247 (class 2606 OID 90575)
-- Name: spec_combo spec_combo_vet_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.spec_combo
    ADD CONSTRAINT spec_combo_vet_id_fkey FOREIGN KEY (vet_id) REFERENCES public.vets(vet_id);


--
-- TOC entry 3245 (class 2606 OID 90563)
-- Name: vets vets_person_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.vets
    ADD CONSTRAINT vets_person_id_fkey FOREIGN KEY (person_id) REFERENCES public.persons(id);


--
-- TOC entry 3250 (class 2606 OID 90626)
-- Name: visits visits_owner_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.visits
    ADD CONSTRAINT visits_owner_id_fkey FOREIGN KEY (owner_id) REFERENCES public.owners(owner_id);


--
-- TOC entry 3251 (class 2606 OID 90621)
-- Name: visits visits_pet_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.visits
    ADD CONSTRAINT visits_pet_id_fkey FOREIGN KEY (pet_id) REFERENCES public.pets(pet_id);


--
-- TOC entry 3252 (class 2606 OID 90616)
-- Name: visits visits_vet_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.visits
    ADD CONSTRAINT visits_vet_id_fkey FOREIGN KEY (vet_id) REFERENCES public.vets(vet_id);


-- Completed on 2023-04-10 15:41:25 UTC

--
-- PostgreSQL database dump complete
--

