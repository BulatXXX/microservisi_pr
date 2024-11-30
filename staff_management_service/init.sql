CREATE TABLE IF NOT EXISTS public.tasks
(
    title character varying COLLATE pg_catalog."default" NOT NULL,
    description text COLLATE pg_catalog."default",
    datetime timestamp without time zone,
    assigned_to integer,
    status character varying COLLATE pg_catalog."default" NOT NULL DEFAULT 'Created'::character varying,
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    CONSTRAINT tasks_pkey PRIMARY KEY (id)
);

ALTER TABLE IF EXISTS public.tasks
    OWNER TO postgres;

-- Создаем последовательность для staff
CREATE SEQUENCE IF NOT EXISTS staff_id_seq
    START 1
    INCREMENT 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

CREATE TABLE IF NOT EXISTS public.staff
(
    id integer NOT NULL DEFAULT nextval('staff_id_seq'::regclass),
    name character varying(255) COLLATE pg_catalog."default" NOT NULL,
    role character varying(255) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT staff_pkey PRIMARY KEY (id)
);

ALTER TABLE IF EXISTS public.staff
    OWNER TO postgres;

INSERT INTO public.staff (id, name, role) VALUES
    (1, 'Alice Johnson', 'Manager'),
    (2, 'Bob Smith', 'Engineer'),
    (3, 'Charlie Brown', 'Technician'),
    (4, 'Diana Prince', 'Coordinator'),
    (5, 'Edward Wilson', 'Analyst');