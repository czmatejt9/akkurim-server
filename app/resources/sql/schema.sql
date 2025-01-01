-- This script was generated by the ERD tool in pgAdmin 4.
-- Please log an issue at https://github.com/pgadmin-org/pgadmin4/issues/new/choose if you find any bugs, including reproduction steps.
BEGIN;


CREATE TABLE IF NOT EXISTS athlete_status
(
    id uuid NOT NULL,
    name text NOT NULL,
    description text,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS guardian
(
    id uuid NOT NULL,
    first_name text NOT NULL,
    last_name text NOT NULL,
    email text NOT NULL,
    phone text NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS item_type
(
    id uuid NOT NULL,
    name text NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS item
(
    id uuid NOT NULL,
    name text NOT NULL,
    description text,
    image text,
    count smallint NOT NULL,
    item_type_id uuid NOT NULL,
    athlete_id uuid,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS athlete
(
    id uuid NOT NULL,
    birth_number text NOT NULL,
    first_name text NOT NULL,
    last_name text NOT NULL,
    street text NOT NULL,
    city text NOT NULL,
    zip text NOT NULL,
    email text,
    phone text,
    ean text,
    note text,
    /* club_id text
       profile_picture text */
    athlete_status_id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    PRIMARY KEY (id)
);


CREATE TABLE IF NOT EXISTS athlete_guardian
(
    athlete_id uuid NOT NULL,
    guardian_id uuid NOT NULL
);

CREATE TABLE IF NOT EXISTS trainer_status
(
    id uuid NOT NULL,
    name text NOT NULL,
    description text,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS trainer
(
    id uuid NOT NULL,
    athlete_id uuid NOT NULL,
    trainer_status_id uuid NOT NULL,
    qualification text NOT NULL,
    salary_per_hour smallint NOT NULL,
    device_token text,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (athlete_id)
);

CREATE TABLE IF NOT EXISTS athlete_item
(
    athlete_id uuid NOT NULL,
    item_id uuid NOT NULL
);

CREATE TABLE IF NOT EXISTS school_year
(
    id uuid NOT NULL,
    name text NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS web_post
(
    id uuid NOT NULL,
    title text NOT NULL,
    content text NOT NULL,
    trainer_id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS "group"
(
    id uuid NOT NULL,
    name text NOT NULL,
    description text,
    training_time_id uuid NOT NULL,
    school_year_id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS group_athlete
(
    group_id uuid NOT NULL,
    athlete_id uuid NOT NULL
);

CREATE TABLE IF NOT EXISTS group_trainer
(
    group_id uuid NOT NULL,
    trainer_id uuid NOT NULL
);

CREATE TABLE IF NOT EXISTS training
(
    id uuid NOT NULL,
    datetime_ timestamp with time zone NOT NULL,
    group_id uuid NOT NULL,
    description text,
    duration_minutes smallint NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS training_time
(
    id uuid NOT NULL,
    day text NOT NULL,
    summer_time time with time zone NOT NULL,
    winter_time time with time zone NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS training_athlete
(
    training_id uuid NOT NULL,
    athlete_id uuid NOT NULL,
    presence text NOT NULL
);

CREATE TABLE IF NOT EXISTS training_trainer
(
    training_id uuid NOT NULL,
    trainer_id uuid NOT NULL,
    presence text
);

CREATE TABLE IF NOT EXISTS sign_up_form
(
    id uuid NOT NULL,
    birth_number text NOT NULL,
    first_name text NOT NULL,
    last_name text NOT NULL,
    street text NOT NULL,
    city text NOT NULL,
    zip text NOT NULL,
    email text,
    phone text,
    guardian_first_name1 text NOT NULL,
    guardian_last_name1 text NOT NULL,
    guardian_first_name2 text,
    guardian_last_name2 text,
    guardian_phone1 text NOT NULL,
    guardian_email1 text NOT NULL,
    guardian_phone2 text,
    guardian_email2 text,
    note text,
    sign_up_form_status_id uuid NOT NULL,
    school_year_id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS sign_up_form_status
(
    id uuid NOT NULL,
    name text NOT NULL,
    description text,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS discipline
(
    id smallint NOT NULL,
    discipline_type_id smallint NOT NULL,
    description text NOT NULL,
    short_description text NOT NULL,
    description_en text NOT NULL,
    short_description_en text NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS discipline_type
(
    id smallint NOT NULL,
    name text NOT NULL,
    description text,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS meet
(
    id text NOT NULL,
    name text NOT NULL,
    start_at timestamp with time zone NOT NULL,
    end_at timestamp with time zone NOT NULL,
    location text,
    organizer text,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS meet_event
(
    id uuid NOT NULL,
    meet_id text NOT NULL,
    meet_type text NOT NULL,
    discipline_id smallint NOT NULL,
    category_id smallint NOT NULL,
    start_at timestamp with time zone NOT NULL,
    phase text,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS category
(
    id smallint NOT NULL,
    sex smallint NOT NULL,
    description text NOT NULL,
    short_description text NOT NULL,
    description_en text NOT NULL,
    short_description_en text NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS athlete_meet_event
(
    athlete_id uuid NOT NULL,
    meet_event_id uuid NOT NULL,
    result text,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL
);

CREATE TABLE IF NOT EXISTS athlete_sign_up_form
(
    athlete_id uuid NOT NULL,
    sign_up_form_id uuid NOT NULL
);

ALTER TABLE IF EXISTS item
    ADD FOREIGN KEY (item_type_id)
    REFERENCES item_type (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS athlete
    ADD FOREIGN KEY (athlete_status_id)
    REFERENCES athlete_status (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS athlete_guardian
    ADD FOREIGN KEY (athlete_id)
    REFERENCES athlete (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS athlete_guardian
    ADD FOREIGN KEY (guardian_id)
    REFERENCES guardian (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS trainer
    ADD FOREIGN KEY (athlete_id)
    REFERENCES athlete (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS trainer
    ADD FOREIGN KEY (trainer_status_id)
    REFERENCES trainer_status (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS athlete_item
    ADD FOREIGN KEY (athlete_id)
    REFERENCES athlete (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS athlete_item
    ADD FOREIGN KEY (item_id)
    REFERENCES item (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS web_post
    ADD FOREIGN KEY (trainer_id)
    REFERENCES trainer (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS "group"
    ADD FOREIGN KEY (school_year_id)
    REFERENCES school_year (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS "group"
    ADD FOREIGN KEY (training_time_id)
    REFERENCES training_time (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS group_athlete
    ADD FOREIGN KEY (group_id)
    REFERENCES "group" (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS group_athlete
    ADD FOREIGN KEY (athlete_id)
    REFERENCES athlete (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS group_trainer
    ADD FOREIGN KEY (group_id)
    REFERENCES "group" (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS group_trainer
    ADD FOREIGN KEY (trainer_id)
    REFERENCES trainer (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS training
    ADD FOREIGN KEY (group_id)
    REFERENCES "group" (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS training_athlete
    ADD FOREIGN KEY (training_id)
    REFERENCES training (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS training_athlete
    ADD FOREIGN KEY (athlete_id)
    REFERENCES athlete (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS training_trainer
    ADD FOREIGN KEY (training_id)
    REFERENCES training (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS training_trainer
    ADD FOREIGN KEY (trainer_id)
    REFERENCES trainer (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS sign_up_form
    ADD FOREIGN KEY (sign_up_form_status_id)
    REFERENCES sign_up_form_status (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS sign_up_form
    ADD FOREIGN KEY (school_year_id)
    REFERENCES school_year (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS discipline
    ADD FOREIGN KEY (discipline_type_id)
    REFERENCES discipline_type (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS meet_event
    ADD FOREIGN KEY (category_id)
    REFERENCES category (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS meet_event
    ADD FOREIGN KEY (discipline_id)
    REFERENCES discipline (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS meet_event
    ADD FOREIGN KEY (meet_id)
    REFERENCES meet (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS meet_event
    ADD FOREIGN KEY (meet_type)
    REFERENCES meet (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS athlete_meet_event
    ADD FOREIGN KEY (athlete_id)
    REFERENCES athlete (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS athlete_meet_event
    ADD FOREIGN KEY (meet_event_id)
    REFERENCES meet_event (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS athlete_sign_up_form
    ADD FOREIGN KEY (athlete_id)
    REFERENCES athlete (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS athlete_sign_up_form
    ADD FOREIGN KEY (sign_up_form_id)
    REFERENCES sign_up_form (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;

END;