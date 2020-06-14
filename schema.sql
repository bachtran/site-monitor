-- Table: public.site_check_events

-- DROP TABLE public.site_check_events;

CREATE TABLE public.site_check_events
(
    code integer,
    content_ok boolean,
    id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    response_time double precision,
    url character varying(512) COLLATE pg_catalog."default",
    "timestamp" double precision,
    CONSTRAINT site_check_events_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE public.site_check_events
    OWNER to avnadmin;