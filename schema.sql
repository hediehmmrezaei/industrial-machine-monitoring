--
-- PostgreSQL database dump
--

\restrict uV4aSr4Nq0evsiWmxQ5bsfFgNc3apP5OuhIATwqak5ROgpzod8N6RKAWPzEBaZL

-- Dumped from database version 18.6 (Postgres.app)
-- Dumped by pg_dump version 18.6 (Postgres.app)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
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
-- Name: anomaly_predictions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.anomaly_predictions (
    prediction_id integer NOT NULL,
    reading_id integer NOT NULL,
    anomaly_score double precision NOT NULL,
    threshold double precision NOT NULL,
    predicted_status character varying(20) NOT NULL,
    predicted_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT anomaly_predictions_predicted_status_check CHECK (((predicted_status)::text = ANY ((ARRAY['NORMAL'::character varying, 'ANOMALY'::character varying])::text[])))
);


--
-- Name: anomaly_predictions_prediction_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.anomaly_predictions_prediction_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: anomaly_predictions_prediction_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.anomaly_predictions_prediction_id_seq OWNED BY public.anomaly_predictions.prediction_id;


--
-- Name: downtime_events; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.downtime_events (
    event_id integer NOT NULL,
    machine_id integer NOT NULL,
    start_time timestamp without time zone NOT NULL,
    end_time timestamp without time zone NOT NULL,
    reason character varying(100),
    event_type character varying(30),
    CONSTRAINT downtime_events_check CHECK ((end_time > start_time))
);


--
-- Name: downtime_events_event_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.downtime_events_event_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: downtime_events_event_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.downtime_events_event_id_seq OWNED BY public.downtime_events.event_id;


--
-- Name: machine_operations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.machine_operations (
    operation_id integer NOT NULL,
    machine_id integer NOT NULL,
    operation_date date NOT NULL,
    planned_minutes integer NOT NULL,
    operating_minutes integer NOT NULL,
    CONSTRAINT machine_operations_check CHECK ((operating_minutes <= planned_minutes)),
    CONSTRAINT machine_operations_operating_minutes_check CHECK ((operating_minutes >= 0)),
    CONSTRAINT machine_operations_planned_minutes_check CHECK ((planned_minutes > 0))
);


--
-- Name: machine_operations_operation_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.machine_operations_operation_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: machine_operations_operation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.machine_operations_operation_id_seq OWNED BY public.machine_operations.operation_id;


--
-- Name: machines; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.machines (
    machine_id integer NOT NULL,
    machine_name character varying(100) NOT NULL,
    machine_type character varying(50),
    installation_date date,
    is_active boolean DEFAULT true
);


--
-- Name: machines_machine_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.machines_machine_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: machines_machine_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.machines_machine_id_seq OWNED BY public.machines.machine_id;


--
-- Name: sensor_readings; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.sensor_readings (
    reading_id integer NOT NULL,
    machine_id integer NOT NULL,
    recorded_at timestamp without time zone NOT NULL,
    temperature_c double precision,
    vibration_mm_s double precision,
    motor_current_a double precision,
    speed_rpm double precision
);


--
-- Name: sensor_readings_reading_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.sensor_readings_reading_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: sensor_readings_reading_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.sensor_readings_reading_id_seq OWNED BY public.sensor_readings.reading_id;


--
-- Name: anomaly_predictions prediction_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.anomaly_predictions ALTER COLUMN prediction_id SET DEFAULT nextval('public.anomaly_predictions_prediction_id_seq'::regclass);


--
-- Name: downtime_events event_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.downtime_events ALTER COLUMN event_id SET DEFAULT nextval('public.downtime_events_event_id_seq'::regclass);


--
-- Name: machine_operations operation_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.machine_operations ALTER COLUMN operation_id SET DEFAULT nextval('public.machine_operations_operation_id_seq'::regclass);


--
-- Name: machines machine_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.machines ALTER COLUMN machine_id SET DEFAULT nextval('public.machines_machine_id_seq'::regclass);


--
-- Name: sensor_readings reading_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sensor_readings ALTER COLUMN reading_id SET DEFAULT nextval('public.sensor_readings_reading_id_seq'::regclass);


--
-- Name: anomaly_predictions anomaly_predictions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.anomaly_predictions
    ADD CONSTRAINT anomaly_predictions_pkey PRIMARY KEY (prediction_id);


--
-- Name: downtime_events downtime_events_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.downtime_events
    ADD CONSTRAINT downtime_events_pkey PRIMARY KEY (event_id);


--
-- Name: machine_operations machine_operations_machine_id_operation_date_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.machine_operations
    ADD CONSTRAINT machine_operations_machine_id_operation_date_key UNIQUE (machine_id, operation_date);


--
-- Name: machine_operations machine_operations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.machine_operations
    ADD CONSTRAINT machine_operations_pkey PRIMARY KEY (operation_id);


--
-- Name: machines machines_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.machines
    ADD CONSTRAINT machines_pkey PRIMARY KEY (machine_id);


--
-- Name: sensor_readings sensor_readings_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sensor_readings
    ADD CONSTRAINT sensor_readings_pkey PRIMARY KEY (reading_id);


--
-- Name: anomaly_predictions unique_sensor_prediction; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.anomaly_predictions
    ADD CONSTRAINT unique_sensor_prediction UNIQUE (reading_id);


--
-- Name: anomaly_predictions anomaly_predictions_reading_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.anomaly_predictions
    ADD CONSTRAINT anomaly_predictions_reading_id_fkey FOREIGN KEY (reading_id) REFERENCES public.sensor_readings(reading_id);


--
-- Name: downtime_events downtime_events_machine_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.downtime_events
    ADD CONSTRAINT downtime_events_machine_id_fkey FOREIGN KEY (machine_id) REFERENCES public.machines(machine_id);


--
-- Name: machine_operations machine_operations_machine_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.machine_operations
    ADD CONSTRAINT machine_operations_machine_id_fkey FOREIGN KEY (machine_id) REFERENCES public.machines(machine_id);


--
-- Name: sensor_readings sensor_readings_machine_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sensor_readings
    ADD CONSTRAINT sensor_readings_machine_id_fkey FOREIGN KEY (machine_id) REFERENCES public.machines(machine_id);


--
-- PostgreSQL database dump complete
--

\unrestrict uV4aSr4Nq0evsiWmxQ5bsfFgNc3apP5OuhIATwqak5ROgpzod8N6RKAWPzEBaZL

