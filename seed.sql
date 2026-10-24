--
-- PostgreSQL database dump
--

\restrict NM5CXaDhbp1gNpCb2i6KbHiuvtu7hw1iL4HJ0ggerIhEjOjaNxNK9Qt5eNbbNyO

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

--
-- Data for Name: machines; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.machines VALUES (1, 'Paper Rewinder', 'Rewinding', '2022-03-15', true);
INSERT INTO public.machines VALUES (2, 'Slitting Machine', 'Cutting', '2021-06-10', true);
INSERT INTO public.machines VALUES (3, 'Packaging Line', 'Packaging', '2023-01-20', true);


--
-- Data for Name: sensor_readings; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.sensor_readings VALUES (1, 1, '2026-10-22 08:00:00', 45.2, 1.8, 12.5, 1450);
INSERT INTO public.sensor_readings VALUES (2, 1, '2026-10-22 08:05:00', 47.1, 2.1, 13, 1455);
INSERT INTO public.sensor_readings VALUES (3, 1, '2026-10-22 08:10:00', 52.6, 3.4, 14.2, 1440);
INSERT INTO public.sensor_readings VALUES (4, 2, '2026-10-22 08:00:00', 41.3, 1.5, 10.8, 1200);
INSERT INTO public.sensor_readings VALUES (5, 2, '2026-10-22 08:05:00', 43.7, 1.7, 11.2, 1210);
INSERT INTO public.sensor_readings VALUES (6, 1, '2026-10-22 08:15:00', 68.5, 5.2, 17.8, 1320);
INSERT INTO public.sensor_readings VALUES (7, 1, '2026-10-22 08:20:00', 72, 5.8, 18.5, 1300);
INSERT INTO public.sensor_readings VALUES (8, 1, '2026-10-22 08:25:00', 48, 2, 13.2, 1450);
INSERT INTO public.sensor_readings VALUES (9, 1, '2026-10-22 08:30:00', 75, 6.2, 19, 1280);


--
-- Data for Name: anomaly_predictions; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.anomaly_predictions VALUES (1, 3, -0.677281842263322, -0.612429207808737, 'ANOMALY', '2026-10-24 09:06:26.116236');
INSERT INTO public.anomaly_predictions VALUES (4, 1, -0.39764020120238985, -0.612429207808737, 'NORMAL', '2026-10-24 09:19:42.009663');
INSERT INTO public.anomaly_predictions VALUES (5, 4, -0.5842551743324019, -0.612429207808737, 'NORMAL', '2026-10-24 09:19:42.009663');
INSERT INTO public.anomaly_predictions VALUES (6, 2, -0.40169074301067087, -0.612429207808737, 'NORMAL', '2026-10-24 09:19:42.009663');
INSERT INTO public.anomaly_predictions VALUES (7, 5, -0.522907886397116, -0.612429207808737, 'NORMAL', '2026-10-24 09:19:42.009663');
INSERT INTO public.anomaly_predictions VALUES (14, 6, -0.7363978913805016, -0.612429207808737, 'ANOMALY', '2026-10-24 09:21:40.462405');
INSERT INTO public.anomaly_predictions VALUES (15, 7, -0.7363978913805016, -0.612429207808737, 'ANOMALY', '2026-10-24 14:17:42.378867');
INSERT INTO public.anomaly_predictions VALUES (16, 8, -0.43183960901326846, -0.612429207808737, 'NORMAL', '2026-10-24 14:22:06.704571');
INSERT INTO public.anomaly_predictions VALUES (18, 9, -0.7363978913805016, -0.612429207808737, 'ANOMALY', '2026-10-24 14:35:21.601607');


--
-- Data for Name: downtime_events; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.downtime_events VALUES (1, 1, '2026-10-22 09:00:00', '2026-10-22 09:15:00', 'Motor Overheating', 'Failure');
INSERT INTO public.downtime_events VALUES (2, 1, '2026-10-22 11:00:00', '2026-10-22 11:25:00', 'High Vibration', 'Investigation');
INSERT INTO public.downtime_events VALUES (3, 1, '2026-10-22 14:00:00', '2026-10-22 14:10:00', 'Material Jam', 'Process Stop');
INSERT INTO public.downtime_events VALUES (4, 2, '2026-10-22 10:00:00', '2026-10-22 10:20:00', 'Blade Adjustment', 'Adjustment');
INSERT INTO public.downtime_events VALUES (5, 2, '2026-10-22 13:00:00', '2026-10-22 13:30:00', 'Mechanical Failure', 'Failure');
INSERT INTO public.downtime_events VALUES (6, 3, '2026-10-22 12:00:00', '2026-10-22 12:12:00', 'Packaging Jam', 'Process Stop');


--
-- Data for Name: machine_operations; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.machine_operations VALUES (1, 1, '2026-10-22', 480, 430);
INSERT INTO public.machine_operations VALUES (2, 2, '2026-10-22', 480, 430);
INSERT INTO public.machine_operations VALUES (3, 3, '2026-10-22', 480, 468);


--
-- Name: anomaly_predictions_prediction_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.anomaly_predictions_prediction_id_seq', 18, true);


--
-- Name: downtime_events_event_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.downtime_events_event_id_seq', 6, true);


--
-- Name: machine_operations_operation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.machine_operations_operation_id_seq', 3, true);


--
-- Name: machines_machine_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.machines_machine_id_seq', 3, true);


--
-- Name: sensor_readings_reading_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.sensor_readings_reading_id_seq', 9, true);


--
-- PostgreSQL database dump complete
--

\unrestrict NM5CXaDhbp1gNpCb2i6KbHiuvtu7hw1iL4HJ0ggerIhEjOjaNxNK9Qt5eNbbNyO

