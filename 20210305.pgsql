--
-- PostgreSQL database dump
--

-- Dumped from database version 12.2 (Debian 12.2-2.pgdg100+1)
-- Dumped by pg_dump version 12.2 (Debian 12.2-2.pgdg100+1)

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
-- Name: accounts_account; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.accounts_account (
    id integer NOT NULL,
    name character varying(64) NOT NULL,
    email character varying(254),
    phone character varying(128),
    industry character varying(255),
    website character varying(200),
    description text,
    created_on timestamp with time zone NOT NULL,
    is_active boolean NOT NULL,
    created_by_id integer,
    status character varying(64) NOT NULL,
    lead_id integer,
    billing_address_line character varying(255),
    billing_city character varying(255),
    billing_country character varying(3),
    billing_postcode character varying(64),
    billing_state character varying(255),
    billing_street character varying(55),
    contact_name character varying(120) NOT NULL
);


ALTER TABLE public.accounts_account OWNER TO postgres;

--
-- Name: accounts_account_assigned_to; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.accounts_account_assigned_to (
    id integer NOT NULL,
    account_id integer NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.accounts_account_assigned_to OWNER TO postgres;

--
-- Name: accounts_account_assigned_to_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.accounts_account_assigned_to_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.accounts_account_assigned_to_id_seq OWNER TO postgres;

--
-- Name: accounts_account_assigned_to_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.accounts_account_assigned_to_id_seq OWNED BY public.accounts_account_assigned_to.id;


--
-- Name: accounts_account_contacts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.accounts_account_contacts (
    id integer NOT NULL,
    account_id integer NOT NULL,
    contact_id integer NOT NULL
);


ALTER TABLE public.accounts_account_contacts OWNER TO postgres;

--
-- Name: accounts_account_contacts_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.accounts_account_contacts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.accounts_account_contacts_id_seq OWNER TO postgres;

--
-- Name: accounts_account_contacts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.accounts_account_contacts_id_seq OWNED BY public.accounts_account_contacts.id;


--
-- Name: accounts_account_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.accounts_account_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.accounts_account_id_seq OWNER TO postgres;

--
-- Name: accounts_account_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.accounts_account_id_seq OWNED BY public.accounts_account.id;


--
-- Name: accounts_account_tags; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.accounts_account_tags (
    id integer NOT NULL,
    account_id integer NOT NULL,
    tags_id integer NOT NULL
);


ALTER TABLE public.accounts_account_tags OWNER TO postgres;

--
-- Name: accounts_account_tags_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.accounts_account_tags_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.accounts_account_tags_id_seq OWNER TO postgres;

--
-- Name: accounts_account_tags_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.accounts_account_tags_id_seq OWNED BY public.accounts_account_tags.id;


--
-- Name: accounts_account_teams; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.accounts_account_teams (
    id integer NOT NULL,
    account_id integer NOT NULL,
    teams_id integer NOT NULL
);


ALTER TABLE public.accounts_account_teams OWNER TO postgres;

--
-- Name: accounts_account_teams_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.accounts_account_teams_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.accounts_account_teams_id_seq OWNER TO postgres;

--
-- Name: accounts_account_teams_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.accounts_account_teams_id_seq OWNED BY public.accounts_account_teams.id;


--
-- Name: accounts_email; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.accounts_email (
    id integer NOT NULL,
    created_on timestamp with time zone NOT NULL,
    message_subject text,
    message_body text,
    from_account_id integer,
    from_email character varying(254) NOT NULL,
    rendered_message_body text,
    scheduled_date_time timestamp with time zone,
    scheduled_later boolean NOT NULL,
    timezone character varying(100) NOT NULL
);


ALTER TABLE public.accounts_email OWNER TO postgres;

--
-- Name: accounts_email_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.accounts_email_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.accounts_email_id_seq OWNER TO postgres;

--
-- Name: accounts_email_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.accounts_email_id_seq OWNED BY public.accounts_email.id;


--
-- Name: accounts_email_recipients; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.accounts_email_recipients (
    id integer NOT NULL,
    email_id integer NOT NULL,
    contact_id integer NOT NULL
);


ALTER TABLE public.accounts_email_recipients OWNER TO postgres;

--
-- Name: accounts_email_recipients_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.accounts_email_recipients_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.accounts_email_recipients_id_seq OWNER TO postgres;

--
-- Name: accounts_email_recipients_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.accounts_email_recipients_id_seq OWNED BY public.accounts_email_recipients.id;


--
-- Name: accounts_emaillog; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.accounts_emaillog (
    id integer NOT NULL,
    is_sent boolean NOT NULL,
    contact_id integer,
    email_id integer
);


ALTER TABLE public.accounts_emaillog OWNER TO postgres;

--
-- Name: accounts_emaillog_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.accounts_emaillog_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.accounts_emaillog_id_seq OWNER TO postgres;

--
-- Name: accounts_emaillog_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.accounts_emaillog_id_seq OWNED BY public.accounts_emaillog.id;


--
-- Name: accounts_tags; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.accounts_tags (
    id integer NOT NULL,
    name character varying(20) NOT NULL,
    slug character varying(20) NOT NULL
);


ALTER TABLE public.accounts_tags OWNER TO postgres;

--
-- Name: accounts_tags_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.accounts_tags_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.accounts_tags_id_seq OWNER TO postgres;

--
-- Name: accounts_tags_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.accounts_tags_id_seq OWNED BY public.accounts_tags.id;


--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO postgres;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_group_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_id_seq OWNER TO postgres;

--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_group_id_seq OWNED BY public.auth_group.id;


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO postgres;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_group_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_permissions_id_seq OWNER TO postgres;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_group_permissions_id_seq OWNED BY public.auth_group_permissions.id;


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO postgres;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_permission_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_permission_id_seq OWNER TO postgres;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_permission_id_seq OWNED BY public.auth_permission.id;


--
-- Name: cases_case; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cases_case (
    id integer NOT NULL,
    name character varying(64) NOT NULL,
    status character varying(64) NOT NULL,
    priority character varying(64) NOT NULL,
    case_type character varying(255),
    closed_on date NOT NULL,
    description text,
    created_on timestamp with time zone NOT NULL,
    is_active boolean NOT NULL,
    created_by_id integer,
    company_id integer
);


ALTER TABLE public.cases_case OWNER TO postgres;

--
-- Name: cases_case_assigned_to; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cases_case_assigned_to (
    id integer NOT NULL,
    case_id integer NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.cases_case_assigned_to OWNER TO postgres;

--
-- Name: cases_case_assigned_to_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.cases_case_assigned_to_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.cases_case_assigned_to_id_seq OWNER TO postgres;

--
-- Name: cases_case_assigned_to_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.cases_case_assigned_to_id_seq OWNED BY public.cases_case_assigned_to.id;


--
-- Name: cases_case_contacts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cases_case_contacts (
    id integer NOT NULL,
    case_id integer NOT NULL,
    contact_id integer NOT NULL
);


ALTER TABLE public.cases_case_contacts OWNER TO postgres;

--
-- Name: cases_case_contacts_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.cases_case_contacts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.cases_case_contacts_id_seq OWNER TO postgres;

--
-- Name: cases_case_contacts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.cases_case_contacts_id_seq OWNED BY public.cases_case_contacts.id;


--
-- Name: cases_case_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.cases_case_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.cases_case_id_seq OWNER TO postgres;

--
-- Name: cases_case_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.cases_case_id_seq OWNED BY public.cases_case.id;


--
-- Name: cases_case_teams; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cases_case_teams (
    id integer NOT NULL,
    case_id integer NOT NULL,
    teams_id integer NOT NULL
);


ALTER TABLE public.cases_case_teams OWNER TO postgres;

--
-- Name: cases_case_teams_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.cases_case_teams_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.cases_case_teams_id_seq OWNER TO postgres;

--
-- Name: cases_case_teams_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.cases_case_teams_id_seq OWNED BY public.cases_case_teams.id;


--
-- Name: common_address; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.common_address (
    id integer NOT NULL,
    address_line character varying(255),
    street character varying(55),
    city character varying(255),
    state character varying(255),
    postcode character varying(64),
    country character varying(3),
    lat double precision,
    lng double precision
);


ALTER TABLE public.common_address OWNER TO postgres;

--
-- Name: common_address_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.common_address_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.common_address_id_seq OWNER TO postgres;

--
-- Name: common_address_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.common_address_id_seq OWNED BY public.common_address.id;


--
-- Name: common_apisettings; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.common_apisettings (
    id integer NOT NULL,
    title character varying(1000) NOT NULL,
    apikey character varying(16) NOT NULL,
    created_on timestamp with time zone NOT NULL,
    created_by_id integer,
    website character varying(255) NOT NULL
);


ALTER TABLE public.common_apisettings OWNER TO postgres;

--
-- Name: common_apisettings_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.common_apisettings_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.common_apisettings_id_seq OWNER TO postgres;

--
-- Name: common_apisettings_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.common_apisettings_id_seq OWNED BY public.common_apisettings.id;


--
-- Name: common_apisettings_lead_assigned_to; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.common_apisettings_lead_assigned_to (
    id integer NOT NULL,
    apisettings_id integer NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.common_apisettings_lead_assigned_to OWNER TO postgres;

--
-- Name: common_apisettings_lead_assigned_to_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.common_apisettings_lead_assigned_to_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.common_apisettings_lead_assigned_to_id_seq OWNER TO postgres;

--
-- Name: common_apisettings_lead_assigned_to_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.common_apisettings_lead_assigned_to_id_seq OWNED BY public.common_apisettings_lead_assigned_to.id;


--
-- Name: common_apisettings_tags; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.common_apisettings_tags (
    id integer NOT NULL,
    apisettings_id integer NOT NULL,
    tags_id integer NOT NULL
);


ALTER TABLE public.common_apisettings_tags OWNER TO postgres;

--
-- Name: common_apisettings_tags_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.common_apisettings_tags_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.common_apisettings_tags_id_seq OWNER TO postgres;

--
-- Name: common_apisettings_tags_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.common_apisettings_tags_id_seq OWNED BY public.common_apisettings_tags.id;


--
-- Name: common_attachments; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.common_attachments (
    id integer NOT NULL,
    file_name character varying(60) NOT NULL,
    created_on timestamp with time zone NOT NULL,
    attachment character varying(1001) NOT NULL,
    account_id integer,
    contact_id integer,
    created_by_id integer,
    lead_id integer,
    opportunity_id integer,
    case_id integer,
    task_id integer,
    event_id integer,
    quotation_id integer,
    company_id integer
);


ALTER TABLE public.common_attachments OWNER TO postgres;

--
-- Name: common_attachments_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.common_attachments_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.common_attachments_id_seq OWNER TO postgres;

--
-- Name: common_attachments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.common_attachments_id_seq OWNED BY public.common_attachments.id;


--
-- Name: common_comment; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.common_comment (
    id integer NOT NULL,
    comment character varying(255) NOT NULL,
    commented_on timestamp with time zone NOT NULL,
    account_id integer,
    case_id integer,
    commented_by_id integer,
    contact_id integer,
    lead_id integer,
    opportunity_id integer,
    user_id integer,
    task_id integer,
    event_id integer,
    quotation_id integer,
    company_id integer
);


ALTER TABLE public.common_comment OWNER TO postgres;

--
-- Name: common_comment_files; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.common_comment_files (
    id integer NOT NULL,
    updated_on timestamp with time zone NOT NULL,
    comment_file character varying(100) NOT NULL,
    comment_id integer NOT NULL
);


ALTER TABLE public.common_comment_files OWNER TO postgres;

--
-- Name: common_comment_files_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.common_comment_files_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.common_comment_files_id_seq OWNER TO postgres;

--
-- Name: common_comment_files_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.common_comment_files_id_seq OWNED BY public.common_comment_files.id;


--
-- Name: common_comment_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.common_comment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.common_comment_id_seq OWNER TO postgres;

--
-- Name: common_comment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.common_comment_id_seq OWNED BY public.common_comment.id;


--
-- Name: common_document; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.common_document (
    id integer NOT NULL,
    title character varying(1000),
    document_file character varying(5000) NOT NULL,
    created_on timestamp with time zone NOT NULL,
    created_by_id integer,
    status character varying(64) NOT NULL
);


ALTER TABLE public.common_document OWNER TO postgres;

--
-- Name: common_document_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.common_document_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.common_document_id_seq OWNER TO postgres;

--
-- Name: common_document_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.common_document_id_seq OWNED BY public.common_document.id;


--
-- Name: common_document_shared_to; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.common_document_shared_to (
    id integer NOT NULL,
    document_id integer NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.common_document_shared_to OWNER TO postgres;

--
-- Name: common_document_shared_to_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.common_document_shared_to_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.common_document_shared_to_id_seq OWNER TO postgres;

--
-- Name: common_document_shared_to_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.common_document_shared_to_id_seq OWNED BY public.common_document_shared_to.id;


--
-- Name: common_document_teams; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.common_document_teams (
    id integer NOT NULL,
    document_id integer NOT NULL,
    teams_id integer NOT NULL
);


ALTER TABLE public.common_document_teams OWNER TO postgres;

--
-- Name: common_document_teams_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.common_document_teams_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.common_document_teams_id_seq OWNER TO postgres;

--
-- Name: common_document_teams_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.common_document_teams_id_seq OWNED BY public.common_document_teams.id;


--
-- Name: common_google; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.common_google (
    id integer NOT NULL,
    google_id character varying(200) NOT NULL,
    google_url character varying(1000) NOT NULL,
    verified_email character varying(200) NOT NULL,
    family_name character varying(200) NOT NULL,
    name character varying(200) NOT NULL,
    gender character varying(10) NOT NULL,
    dob character varying(50) NOT NULL,
    given_name character varying(200) NOT NULL,
    email character varying(200) NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.common_google OWNER TO postgres;

--
-- Name: common_google_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.common_google_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.common_google_id_seq OWNER TO postgres;

--
-- Name: common_google_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.common_google_id_seq OWNED BY public.common_google.id;


--
-- Name: common_profile; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.common_profile (
    id integer NOT NULL,
    activation_key character varying(50) NOT NULL,
    key_expires timestamp with time zone NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.common_profile OWNER TO postgres;

--
-- Name: common_profile_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.common_profile_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.common_profile_id_seq OWNER TO postgres;

--
-- Name: common_profile_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.common_profile_id_seq OWNED BY public.common_profile.id;


--
-- Name: common_user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.common_user (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(100) NOT NULL,
    first_name character varying(150) NOT NULL,
    last_name character varying(150) NOT NULL,
    email character varying(255),
    is_active boolean NOT NULL,
    is_admin boolean NOT NULL,
    is_staff boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL,
    role character varying(50) NOT NULL,
    profile_pic character varying(1000),
    has_marketing_access boolean NOT NULL,
    has_sales_access boolean NOT NULL,
    phone character varying(128),
    phone_verify boolean NOT NULL,
    verify_code character varying(6) NOT NULL,
    display_name character varying(150) NOT NULL,
    login_token character varying(12) NOT NULL,
    need_login_verify boolean NOT NULL,
    new_phone character varying(128),
    new_phone_verify_code character varying(6)
);


ALTER TABLE public.common_user OWNER TO postgres;

--
-- Name: common_user_groups; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.common_user_groups (
    id integer NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.common_user_groups OWNER TO postgres;

--
-- Name: common_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.common_user_groups_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.common_user_groups_id_seq OWNER TO postgres;

--
-- Name: common_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.common_user_groups_id_seq OWNED BY public.common_user_groups.id;


--
-- Name: common_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.common_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.common_user_id_seq OWNER TO postgres;

--
-- Name: common_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.common_user_id_seq OWNED BY public.common_user.id;


--
-- Name: common_user_user_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.common_user_user_permissions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.common_user_user_permissions OWNER TO postgres;

--
-- Name: common_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.common_user_user_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.common_user_user_permissions_id_seq OWNER TO postgres;

--
-- Name: common_user_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.common_user_user_permissions_id_seq OWNED BY public.common_user_user_permissions.id;


--
-- Name: companies_chargingstages; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.companies_chargingstages (
    id integer NOT NULL,
    quantity integer NOT NULL,
    "values" integer[] NOT NULL,
    descriptions text[] NOT NULL,
    company_id integer NOT NULL,
    CONSTRAINT companies_chargingstages_quantity_check CHECK ((quantity >= 0))
);


ALTER TABLE public.companies_chargingstages OWNER TO postgres;

--
-- Name: companies_chargingstages_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.companies_chargingstages_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.companies_chargingstages_id_seq OWNER TO postgres;

--
-- Name: companies_chargingstages_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.companies_chargingstages_id_seq OWNED BY public.companies_chargingstages.id;


--
-- Name: companies_company; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.companies_company (
    id integer NOT NULL,
    name character varying(64) NOT NULL,
    email character varying(254),
    phone character varying(128),
    industry character varying(255),
    billing_address_line character varying(255),
    billing_street character varying(55),
    billing_city character varying(255),
    billing_state character varying(255),
    billing_postcode character varying(64),
    billing_country character varying(3),
    website character varying(200),
    description text,
    created_on timestamp with time zone NOT NULL,
    is_active boolean NOT NULL,
    status character varying(64) NOT NULL,
    logo_pic character varying(100),
    br_pic character varying(100),
    created_by_id integer,
    owner_id integer NOT NULL,
    br_approved boolean NOT NULL,
    job_no integer NOT NULL,
    sign character varying(100),
    br_pic_height integer NOT NULL,
    br_pic_width integer NOT NULL,
    logo_pic_height integer NOT NULL,
    logo_pic_width integer NOT NULL,
    sign_height integer NOT NULL,
    sign_width integer NOT NULL,
    gen_invoice_count integer NOT NULL,
    gen_invoice_date date NOT NULL,
    gen_quot_count integer NOT NULL,
    gen_quot_date date NOT NULL,
    gen_receipt_count integer NOT NULL,
    gen_receipt_date date NOT NULL,
    CONSTRAINT companies_company_br_pic_height_check CHECK ((br_pic_height >= 0)),
    CONSTRAINT companies_company_br_pic_width_check CHECK ((br_pic_width >= 0)),
    CONSTRAINT companies_company_job_no_check CHECK ((job_no >= 0)),
    CONSTRAINT companies_company_logo_pic_height_check CHECK ((logo_pic_height >= 0)),
    CONSTRAINT companies_company_logo_pic_width_check CHECK ((logo_pic_width >= 0)),
    CONSTRAINT companies_company_sign_height_check CHECK ((sign_height >= 0)),
    CONSTRAINT companies_company_sign_width_check CHECK ((sign_width >= 0))
);


ALTER TABLE public.companies_company OWNER TO postgres;

--
-- Name: companies_company_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.companies_company_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.companies_company_id_seq OWNER TO postgres;

--
-- Name: companies_company_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.companies_company_id_seq OWNED BY public.companies_company.id;


--
-- Name: companies_company_tags; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.companies_company_tags (
    id integer NOT NULL,
    company_id integer NOT NULL,
    tags_id integer NOT NULL
);


ALTER TABLE public.companies_company_tags OWNER TO postgres;

--
-- Name: companies_company_tags_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.companies_company_tags_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.companies_company_tags_id_seq OWNER TO postgres;

--
-- Name: companies_company_tags_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.companies_company_tags_id_seq OWNED BY public.companies_company_tags.id;


--
-- Name: companies_documentformat; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.companies_documentformat (
    id integer NOT NULL,
    quot_upper_format character varying(20) NOT NULL,
    quot_middle_format character varying(20) NOT NULL,
    quot_lower_format character varying(20) NOT NULL,
    invoice_upper_format character varying(20) NOT NULL,
    invoice_middle_format character varying(20) NOT NULL,
    invoice_lower_format character varying(20) NOT NULL,
    receipt_upper_format character varying(20) NOT NULL,
    receipt_middle_format character varying(20) NOT NULL,
    receipt_lower_format character varying(20) NOT NULL,
    company_id integer NOT NULL,
    project_upper_format character varying(6) NOT NULL,
    project_lower_format character varying(20) NOT NULL,
    project_based_number integer NOT NULL,
    CONSTRAINT companies_documentformat_project_based_number_check CHECK ((project_based_number >= 0))
);


ALTER TABLE public.companies_documentformat OWNER TO postgres;

--
-- Name: companies_documentformat_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.companies_documentformat_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.companies_documentformat_id_seq OWNER TO postgres;

--
-- Name: companies_documentformat_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.companies_documentformat_id_seq OWNED BY public.companies_documentformat.id;


--
-- Name: companies_documentheaderinformation; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.companies_documentheaderinformation (
    id integer NOT NULL,
    tel character varying(20),
    email character varying(254),
    fax character varying(20),
    address character varying(512),
    company_id integer NOT NULL
);


ALTER TABLE public.companies_documentheaderinformation OWNER TO postgres;

--
-- Name: companies_documentheaderinformation_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.companies_documentheaderinformation_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.companies_documentheaderinformation_id_seq OWNER TO postgres;

--
-- Name: companies_documentheaderinformation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.companies_documentheaderinformation_id_seq OWNED BY public.companies_documentheaderinformation.id;


--
-- Name: companies_email; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.companies_email (
    id integer NOT NULL,
    message_subject text,
    message_body text,
    timezone character varying(100) NOT NULL,
    scheduled_date_time timestamp with time zone,
    scheduled_later boolean NOT NULL,
    created_on timestamp with time zone NOT NULL,
    from_email character varying(254) NOT NULL,
    rendered_message_body text,
    from_company_id integer
);


ALTER TABLE public.companies_email OWNER TO postgres;

--
-- Name: companies_email_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.companies_email_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.companies_email_id_seq OWNER TO postgres;

--
-- Name: companies_email_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.companies_email_id_seq OWNED BY public.companies_email.id;


--
-- Name: companies_email_recipients; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.companies_email_recipients (
    id integer NOT NULL,
    email_id integer NOT NULL,
    contact_id integer NOT NULL
);


ALTER TABLE public.companies_email_recipients OWNER TO postgres;

--
-- Name: companies_email_recipients_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.companies_email_recipients_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.companies_email_recipients_id_seq OWNER TO postgres;

--
-- Name: companies_email_recipients_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.companies_email_recipients_id_seq OWNED BY public.companies_email_recipients.id;


--
-- Name: companies_emaillog; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.companies_emaillog (
    id integer NOT NULL,
    is_sent boolean NOT NULL,
    contact_id integer,
    email_id integer
);


ALTER TABLE public.companies_emaillog OWNER TO postgres;

--
-- Name: companies_emaillog_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.companies_emaillog_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.companies_emaillog_id_seq OWNER TO postgres;

--
-- Name: companies_emaillog_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.companies_emaillog_id_seq OWNED BY public.companies_emaillog.id;


--
-- Name: companies_invoicegeneralremark; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.companies_invoicegeneralremark (
    id integer NOT NULL,
    index integer NOT NULL,
    content text NOT NULL,
    company_id integer NOT NULL,
    CONSTRAINT companies_invoicegeneralremark_index_check CHECK ((index >= 0))
);


ALTER TABLE public.companies_invoicegeneralremark OWNER TO postgres;

--
-- Name: companies_invoicegeneralremark_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.companies_invoicegeneralremark_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.companies_invoicegeneralremark_id_seq OWNER TO postgres;

--
-- Name: companies_invoicegeneralremark_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.companies_invoicegeneralremark_id_seq OWNED BY public.companies_invoicegeneralremark.id;


--
-- Name: companies_quotationgeneralremark; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.companies_quotationgeneralremark (
    id integer NOT NULL,
    index integer NOT NULL,
    content text NOT NULL,
    company_id integer NOT NULL,
    CONSTRAINT companies_quotationgeneralremark_index_check CHECK ((index >= 0))
);


ALTER TABLE public.companies_quotationgeneralremark OWNER TO postgres;

--
-- Name: companies_quotationgeneralremark_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.companies_quotationgeneralremark_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.companies_quotationgeneralremark_id_seq OWNER TO postgres;

--
-- Name: companies_quotationgeneralremark_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.companies_quotationgeneralremark_id_seq OWNED BY public.companies_quotationgeneralremark.id;


--
-- Name: companies_receiptgeneralremark; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.companies_receiptgeneralremark (
    id integer NOT NULL,
    index integer NOT NULL,
    content text NOT NULL,
    company_id integer NOT NULL,
    CONSTRAINT companies_receiptgeneralremark_index_check CHECK ((index >= 0))
);


ALTER TABLE public.companies_receiptgeneralremark OWNER TO postgres;

--
-- Name: companies_receiptgeneralremark_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.companies_receiptgeneralremark_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.companies_receiptgeneralremark_id_seq OWNER TO postgres;

--
-- Name: companies_receiptgeneralremark_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.companies_receiptgeneralremark_id_seq OWNED BY public.companies_receiptgeneralremark.id;


--
-- Name: companies_tags; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.companies_tags (
    id integer NOT NULL,
    name character varying(20) NOT NULL,
    slug character varying(20) NOT NULL
);


ALTER TABLE public.companies_tags OWNER TO postgres;

--
-- Name: companies_tags_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.companies_tags_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.companies_tags_id_seq OWNER TO postgres;

--
-- Name: companies_tags_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.companies_tags_id_seq OWNED BY public.companies_tags.id;


--
-- Name: contacts_contact; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.contacts_contact (
    id integer NOT NULL,
    first_name character varying(255) NOT NULL,
    last_name character varying(255) NOT NULL,
    email character varying(254),
    phone character varying(128) NOT NULL,
    description text,
    created_on timestamp with time zone NOT NULL,
    is_active boolean NOT NULL,
    address_id integer,
    created_by_id integer,
    profile_pic character varying(1000)
);


ALTER TABLE public.contacts_contact OWNER TO postgres;

--
-- Name: contacts_contact_assigned_to; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.contacts_contact_assigned_to (
    id integer NOT NULL,
    contact_id integer NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.contacts_contact_assigned_to OWNER TO postgres;

--
-- Name: contacts_contact_assigned_to_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.contacts_contact_assigned_to_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.contacts_contact_assigned_to_id_seq OWNER TO postgres;

--
-- Name: contacts_contact_assigned_to_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.contacts_contact_assigned_to_id_seq OWNED BY public.contacts_contact_assigned_to.id;


--
-- Name: contacts_contact_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.contacts_contact_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.contacts_contact_id_seq OWNER TO postgres;

--
-- Name: contacts_contact_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.contacts_contact_id_seq OWNED BY public.contacts_contact.id;


--
-- Name: contacts_contact_teams; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.contacts_contact_teams (
    id integer NOT NULL,
    contact_id integer NOT NULL,
    teams_id integer NOT NULL
);


ALTER TABLE public.contacts_contact_teams OWNER TO postgres;

--
-- Name: contacts_contact_teams_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.contacts_contact_teams_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.contacts_contact_teams_id_seq OWNER TO postgres;

--
-- Name: contacts_contact_teams_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.contacts_contact_teams_id_seq OWNED BY public.contacts_contact_teams.id;


--
-- Name: customers_customer; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.customers_customer (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    company_name character varying(255),
    email character varying(254),
    phone character varying(128),
    address character varying(1024),
    created_on timestamp with time zone NOT NULL,
    created_by_id integer,
    project_id integer NOT NULL
);


ALTER TABLE public.customers_customer OWNER TO postgres;

--
-- Name: customers_customer_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.customers_customer_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.customers_customer_id_seq OWNER TO postgres;

--
-- Name: customers_customer_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.customers_customer_id_seq OWNED BY public.customers_customer.id;


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO postgres;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.django_admin_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_admin_log_id_seq OWNER TO postgres;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.django_admin_log_id_seq OWNED BY public.django_admin_log.id;


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO postgres;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.django_content_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_content_type_id_seq OWNER TO postgres;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.django_content_type_id_seq OWNED BY public.django_content_type.id;


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_migrations (
    id integer NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO postgres;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.django_migrations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_migrations_id_seq OWNER TO postgres;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.django_migrations_id_seq OWNED BY public.django_migrations.id;


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO postgres;

--
-- Name: emails_email; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.emails_email (
    id integer NOT NULL,
    from_email character varying(200) NOT NULL,
    to_email character varying(200) NOT NULL,
    subject character varying(200) NOT NULL,
    message character varying(200) NOT NULL,
    file character varying(100),
    send_time timestamp with time zone NOT NULL,
    status character varying(200) NOT NULL,
    important boolean NOT NULL
);


ALTER TABLE public.emails_email OWNER TO postgres;

--
-- Name: emails_email_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.emails_email_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.emails_email_id_seq OWNER TO postgres;

--
-- Name: emails_email_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.emails_email_id_seq OWNED BY public.emails_email.id;


--
-- Name: events_event; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.events_event (
    id integer NOT NULL,
    name character varying(64) NOT NULL,
    event_type character varying(20) NOT NULL,
    status character varying(64),
    start_date date NOT NULL,
    start_time time without time zone NOT NULL,
    end_date date NOT NULL,
    end_time time without time zone,
    description text,
    created_on timestamp with time zone NOT NULL,
    is_active boolean NOT NULL,
    disabled boolean NOT NULL,
    created_by_id integer,
    date_of_meeting date
);


ALTER TABLE public.events_event OWNER TO postgres;

--
-- Name: events_event_assigned_to; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.events_event_assigned_to (
    id integer NOT NULL,
    event_id integer NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.events_event_assigned_to OWNER TO postgres;

--
-- Name: events_event_assigned_to_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.events_event_assigned_to_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.events_event_assigned_to_id_seq OWNER TO postgres;

--
-- Name: events_event_assigned_to_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.events_event_assigned_to_id_seq OWNED BY public.events_event_assigned_to.id;


--
-- Name: events_event_contacts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.events_event_contacts (
    id integer NOT NULL,
    event_id integer NOT NULL,
    contact_id integer NOT NULL
);


ALTER TABLE public.events_event_contacts OWNER TO postgres;

--
-- Name: events_event_contacts_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.events_event_contacts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.events_event_contacts_id_seq OWNER TO postgres;

--
-- Name: events_event_contacts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.events_event_contacts_id_seq OWNED BY public.events_event_contacts.id;


--
-- Name: events_event_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.events_event_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.events_event_id_seq OWNER TO postgres;

--
-- Name: events_event_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.events_event_id_seq OWNED BY public.events_event.id;


--
-- Name: events_event_teams; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.events_event_teams (
    id integer NOT NULL,
    event_id integer NOT NULL,
    teams_id integer NOT NULL
);


ALTER TABLE public.events_event_teams OWNER TO postgres;

--
-- Name: events_event_teams_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.events_event_teams_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.events_event_teams_id_seq OWNER TO postgres;

--
-- Name: events_event_teams_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.events_event_teams_id_seq OWNED BY public.events_event_teams.id;


--
-- Name: function_items_functionitem; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.function_items_functionitem (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    created_on timestamp with time zone NOT NULL,
    created_by_id integer,
    type character varying(20) NOT NULL,
    description text,
    price numeric(12,2) NOT NULL,
    status character varying(20) NOT NULL,
    approved_by_id integer,
    approved_on timestamp with time zone,
    last_updated_by_id integer,
    last_updated_on timestamp with time zone NOT NULL
);


ALTER TABLE public.function_items_functionitem OWNER TO postgres;

--
-- Name: function_items_functionitem_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.function_items_functionitem_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.function_items_functionitem_id_seq OWNER TO postgres;

--
-- Name: function_items_functionitem_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.function_items_functionitem_id_seq OWNED BY public.function_items_functionitem.id;


--
-- Name: function_items_functionitemhistory; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.function_items_functionitemhistory (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    price numeric(12,2) NOT NULL,
    description text,
    type character varying(20) NOT NULL,
    status character varying(20) NOT NULL,
    created_on timestamp with time zone NOT NULL,
    function_item_id integer,
    updated_by_id integer,
    changed_data text
);


ALTER TABLE public.function_items_functionitemhistory OWNER TO postgres;

--
-- Name: function_items_functionitemhistory_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.function_items_functionitemhistory_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.function_items_functionitemhistory_id_seq OWNER TO postgres;

--
-- Name: function_items_functionitemhistory_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.function_items_functionitemhistory_id_seq OWNED BY public.function_items_functionitemhistory.id;


--
-- Name: function_items_subfunctionitem; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.function_items_subfunctionitem (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    price numeric(12,2) NOT NULL,
    description text,
    status character varying(20) NOT NULL,
    created_on timestamp with time zone NOT NULL,
    approved_on timestamp with time zone,
    last_updated_on timestamp with time zone NOT NULL,
    approved_by_id integer,
    created_by_id integer,
    last_updated_by_id integer,
    related_function_item_id integer NOT NULL
);


ALTER TABLE public.function_items_subfunctionitem OWNER TO postgres;

--
-- Name: function_items_subfunctionitem_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.function_items_subfunctionitem_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.function_items_subfunctionitem_id_seq OWNER TO postgres;

--
-- Name: function_items_subfunctionitem_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.function_items_subfunctionitem_id_seq OWNED BY public.function_items_subfunctionitem.id;


--
-- Name: function_items_subfunctionitemhistory; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.function_items_subfunctionitemhistory (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    price numeric(12,2) NOT NULL,
    description text,
    status character varying(20) NOT NULL,
    changed_data text,
    created_on timestamp with time zone NOT NULL,
    sub_function_item_id integer,
    updated_by_id integer
);


ALTER TABLE public.function_items_subfunctionitemhistory OWNER TO postgres;

--
-- Name: function_items_subfunctionitemhistory_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.function_items_subfunctionitemhistory_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.function_items_subfunctionitemhistory_id_seq OWNER TO postgres;

--
-- Name: function_items_subfunctionitemhistory_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.function_items_subfunctionitemhistory_id_seq OWNED BY public.function_items_subfunctionitemhistory.id;


--
-- Name: invoices_invoice; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.invoices_invoice (
    id integer NOT NULL,
    invoice_title character varying(50) NOT NULL,
    invoice_number character varying(50) NOT NULL,
    name character varying(100) NOT NULL,
    email character varying(254) NOT NULL,
    quantity integer NOT NULL,
    rate numeric(12,2) NOT NULL,
    total_amount numeric(12,2),
    currency character varying(3),
    phone character varying(128),
    created_on timestamp with time zone NOT NULL,
    amount_due numeric(12,2),
    amount_paid numeric(12,2),
    is_email_sent boolean NOT NULL,
    status character varying(15) NOT NULL,
    created_by_id integer,
    from_address_id integer,
    to_address_id integer,
    details text,
    due_date date,
    CONSTRAINT invoices_invoice_quantity_check CHECK ((quantity >= 0))
);


ALTER TABLE public.invoices_invoice OWNER TO postgres;

--
-- Name: invoices_invoice_assigned_to; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.invoices_invoice_assigned_to (
    id integer NOT NULL,
    invoice_id integer NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.invoices_invoice_assigned_to OWNER TO postgres;

--
-- Name: invoices_invoice_assigned_to_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.invoices_invoice_assigned_to_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.invoices_invoice_assigned_to_id_seq OWNER TO postgres;

--
-- Name: invoices_invoice_assigned_to_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.invoices_invoice_assigned_to_id_seq OWNED BY public.invoices_invoice_assigned_to.id;


--
-- Name: invoices_invoice_companies; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.invoices_invoice_companies (
    id integer NOT NULL,
    invoice_id integer NOT NULL,
    company_id integer NOT NULL
);


ALTER TABLE public.invoices_invoice_companies OWNER TO postgres;

--
-- Name: invoices_invoice_companies_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.invoices_invoice_companies_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.invoices_invoice_companies_id_seq OWNER TO postgres;

--
-- Name: invoices_invoice_companies_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.invoices_invoice_companies_id_seq OWNED BY public.invoices_invoice_companies.id;


--
-- Name: invoices_invoice_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.invoices_invoice_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.invoices_invoice_id_seq OWNER TO postgres;

--
-- Name: invoices_invoice_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.invoices_invoice_id_seq OWNED BY public.invoices_invoice.id;


--
-- Name: invoices_invoice_teams; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.invoices_invoice_teams (
    id integer NOT NULL,
    invoice_id integer NOT NULL,
    teams_id integer NOT NULL
);


ALTER TABLE public.invoices_invoice_teams OWNER TO postgres;

--
-- Name: invoices_invoice_teams_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.invoices_invoice_teams_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.invoices_invoice_teams_id_seq OWNER TO postgres;

--
-- Name: invoices_invoice_teams_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.invoices_invoice_teams_id_seq OWNED BY public.invoices_invoice_teams.id;


--
-- Name: invoices_invoicehistory; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.invoices_invoicehistory (
    id integer NOT NULL,
    invoice_title character varying(50) NOT NULL,
    invoice_number character varying(50) NOT NULL,
    name character varying(100) NOT NULL,
    email character varying(254) NOT NULL,
    quantity integer NOT NULL,
    rate numeric(12,2) NOT NULL,
    total_amount numeric(12,2),
    currency character varying(3),
    phone character varying(128),
    created_on timestamp with time zone NOT NULL,
    amount_due numeric(12,2),
    amount_paid numeric(12,2),
    is_email_sent boolean NOT NULL,
    status character varying(15) NOT NULL,
    details text,
    due_date date,
    from_address_id integer,
    invoice_id integer NOT NULL,
    to_address_id integer,
    updated_by_id integer,
    CONSTRAINT invoices_invoicehistory_quantity_check CHECK ((quantity >= 0))
);


ALTER TABLE public.invoices_invoicehistory OWNER TO postgres;

--
-- Name: invoices_invoicehistory_assigned_to; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.invoices_invoicehistory_assigned_to (
    id integer NOT NULL,
    invoicehistory_id integer NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.invoices_invoicehistory_assigned_to OWNER TO postgres;

--
-- Name: invoices_invoicehistory_assigned_to_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.invoices_invoicehistory_assigned_to_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.invoices_invoicehistory_assigned_to_id_seq OWNER TO postgres;

--
-- Name: invoices_invoicehistory_assigned_to_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.invoices_invoicehistory_assigned_to_id_seq OWNED BY public.invoices_invoicehistory_assigned_to.id;


--
-- Name: invoices_invoicehistory_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.invoices_invoicehistory_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.invoices_invoicehistory_id_seq OWNER TO postgres;

--
-- Name: invoices_invoicehistory_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.invoices_invoicehistory_id_seq OWNED BY public.invoices_invoicehistory.id;


--
-- Name: leads_lead; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.leads_lead (
    id integer NOT NULL,
    title character varying(64) NOT NULL,
    first_name character varying(255),
    last_name character varying(255),
    email character varying(254),
    phone character varying(128),
    status character varying(255),
    source character varying(255),
    website character varying(255),
    description text,
    company_name character varying(255),
    opportunity_amount numeric(12,2),
    created_on timestamp with time zone NOT NULL,
    is_active boolean NOT NULL,
    enquery_type character varying(255),
    created_by_id integer,
    address_line character varying(255),
    city character varying(255),
    country character varying(3),
    postcode character varying(64),
    state character varying(255),
    street character varying(55),
    created_from_site boolean NOT NULL
);


ALTER TABLE public.leads_lead OWNER TO postgres;

--
-- Name: leads_lead_assigned_to; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.leads_lead_assigned_to (
    id integer NOT NULL,
    lead_id integer NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.leads_lead_assigned_to OWNER TO postgres;

--
-- Name: leads_lead_assigned_to_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.leads_lead_assigned_to_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.leads_lead_assigned_to_id_seq OWNER TO postgres;

--
-- Name: leads_lead_assigned_to_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.leads_lead_assigned_to_id_seq OWNED BY public.leads_lead_assigned_to.id;


--
-- Name: leads_lead_contacts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.leads_lead_contacts (
    id integer NOT NULL,
    lead_id integer NOT NULL,
    contact_id integer NOT NULL
);


ALTER TABLE public.leads_lead_contacts OWNER TO postgres;

--
-- Name: leads_lead_contacts_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.leads_lead_contacts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.leads_lead_contacts_id_seq OWNER TO postgres;

--
-- Name: leads_lead_contacts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.leads_lead_contacts_id_seq OWNED BY public.leads_lead_contacts.id;


--
-- Name: leads_lead_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.leads_lead_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.leads_lead_id_seq OWNER TO postgres;

--
-- Name: leads_lead_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.leads_lead_id_seq OWNED BY public.leads_lead.id;


--
-- Name: leads_lead_teams; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.leads_lead_teams (
    id integer NOT NULL,
    lead_id integer NOT NULL,
    teams_id integer NOT NULL
);


ALTER TABLE public.leads_lead_teams OWNER TO postgres;

--
-- Name: leads_lead_teams_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.leads_lead_teams_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.leads_lead_teams_id_seq OWNER TO postgres;

--
-- Name: leads_lead_teams_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.leads_lead_teams_id_seq OWNED BY public.leads_lead_teams.id;


--
-- Name: marketing_blockeddomain; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.marketing_blockeddomain (
    id integer NOT NULL,
    domain character varying(200) NOT NULL,
    created_on timestamp with time zone NOT NULL,
    created_by_id integer
);


ALTER TABLE public.marketing_blockeddomain OWNER TO postgres;

--
-- Name: marketing_blockeddomain_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.marketing_blockeddomain_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.marketing_blockeddomain_id_seq OWNER TO postgres;

--
-- Name: marketing_blockeddomain_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.marketing_blockeddomain_id_seq OWNED BY public.marketing_blockeddomain.id;


--
-- Name: marketing_blockedemail; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.marketing_blockedemail (
    id integer NOT NULL,
    email character varying(254) NOT NULL,
    created_on timestamp with time zone NOT NULL,
    created_by_id integer
);


ALTER TABLE public.marketing_blockedemail OWNER TO postgres;

--
-- Name: marketing_blockedemail_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.marketing_blockedemail_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.marketing_blockedemail_id_seq OWNER TO postgres;

--
-- Name: marketing_blockedemail_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.marketing_blockedemail_id_seq OWNED BY public.marketing_blockedemail.id;


--
-- Name: marketing_campaign; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.marketing_campaign (
    id integer NOT NULL,
    title character varying(5000) NOT NULL,
    created_on timestamp with time zone NOT NULL,
    schedule_date_time timestamp with time zone,
    reply_to_email character varying(254),
    subject character varying(5000) NOT NULL,
    html text NOT NULL,
    html_processed text NOT NULL,
    from_email character varying(254),
    from_name character varying(254),
    sent integer NOT NULL,
    opens integer NOT NULL,
    opens_unique integer NOT NULL,
    bounced integer NOT NULL,
    status character varying(20) NOT NULL,
    created_by_id integer,
    email_template_id integer,
    updated_on timestamp with time zone NOT NULL,
    timezone character varying(100) NOT NULL,
    attachment character varying(1000)
);


ALTER TABLE public.marketing_campaign OWNER TO postgres;

--
-- Name: marketing_campaign_contact_lists; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.marketing_campaign_contact_lists (
    id integer NOT NULL,
    campaign_id integer NOT NULL,
    contactlist_id integer NOT NULL
);


ALTER TABLE public.marketing_campaign_contact_lists OWNER TO postgres;

--
-- Name: marketing_campaign_contact_lists_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.marketing_campaign_contact_lists_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.marketing_campaign_contact_lists_id_seq OWNER TO postgres;

--
-- Name: marketing_campaign_contact_lists_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.marketing_campaign_contact_lists_id_seq OWNED BY public.marketing_campaign_contact_lists.id;


--
-- Name: marketing_campaign_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.marketing_campaign_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.marketing_campaign_id_seq OWNER TO postgres;

--
-- Name: marketing_campaign_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.marketing_campaign_id_seq OWNED BY public.marketing_campaign.id;


--
-- Name: marketing_campaign_tags; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.marketing_campaign_tags (
    id integer NOT NULL,
    campaign_id integer NOT NULL,
    tag_id integer NOT NULL
);


ALTER TABLE public.marketing_campaign_tags OWNER TO postgres;

--
-- Name: marketing_campaign_tags_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.marketing_campaign_tags_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.marketing_campaign_tags_id_seq OWNER TO postgres;

--
-- Name: marketing_campaign_tags_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.marketing_campaign_tags_id_seq OWNED BY public.marketing_campaign_tags.id;


--
-- Name: marketing_campaigncompleted; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.marketing_campaigncompleted (
    id integer NOT NULL,
    is_completed boolean NOT NULL,
    campaign_id integer NOT NULL
);


ALTER TABLE public.marketing_campaigncompleted OWNER TO postgres;

--
-- Name: marketing_campaigncompleted_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.marketing_campaigncompleted_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.marketing_campaigncompleted_id_seq OWNER TO postgres;

--
-- Name: marketing_campaigncompleted_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.marketing_campaigncompleted_id_seq OWNED BY public.marketing_campaigncompleted.id;


--
-- Name: marketing_campaignlinkclick; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.marketing_campaignlinkclick (
    id integer NOT NULL,
    ip_address inet NOT NULL,
    created_on timestamp with time zone NOT NULL,
    user_agent character varying(2000),
    campaign_id integer NOT NULL,
    contact_id integer,
    link_id integer
);


ALTER TABLE public.marketing_campaignlinkclick OWNER TO postgres;

--
-- Name: marketing_campaignlinkclick_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.marketing_campaignlinkclick_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.marketing_campaignlinkclick_id_seq OWNER TO postgres;

--
-- Name: marketing_campaignlinkclick_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.marketing_campaignlinkclick_id_seq OWNED BY public.marketing_campaignlinkclick.id;


--
-- Name: marketing_campaignlog; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.marketing_campaignlog (
    id integer NOT NULL,
    created_on timestamp with time zone NOT NULL,
    message_id character varying(1000),
    campaign_id integer NOT NULL,
    contact_id integer
);


ALTER TABLE public.marketing_campaignlog OWNER TO postgres;

--
-- Name: marketing_campaignlog_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.marketing_campaignlog_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.marketing_campaignlog_id_seq OWNER TO postgres;

--
-- Name: marketing_campaignlog_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.marketing_campaignlog_id_seq OWNED BY public.marketing_campaignlog.id;


--
-- Name: marketing_campaignopen; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.marketing_campaignopen (
    id integer NOT NULL,
    ip_address inet NOT NULL,
    created_on timestamp with time zone NOT NULL,
    user_agent character varying(2000),
    campaign_id integer NOT NULL,
    contact_id integer
);


ALTER TABLE public.marketing_campaignopen OWNER TO postgres;

--
-- Name: marketing_campaignopen_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.marketing_campaignopen_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.marketing_campaignopen_id_seq OWNER TO postgres;

--
-- Name: marketing_campaignopen_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.marketing_campaignopen_id_seq OWNED BY public.marketing_campaignopen.id;


--
-- Name: marketing_contact; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.marketing_contact (
    id integer NOT NULL,
    created_on timestamp with time zone NOT NULL,
    name character varying(500) NOT NULL,
    email character varying(254) NOT NULL,
    contact_number character varying(20),
    is_unsubscribed boolean NOT NULL,
    is_bounced boolean NOT NULL,
    company_name character varying(500),
    last_name character varying(500),
    city character varying(500),
    state character varying(500),
    contry character varying(500),
    created_by_id integer,
    updated_on timestamp with time zone NOT NULL
);


ALTER TABLE public.marketing_contact OWNER TO postgres;

--
-- Name: marketing_contact_contact_list; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.marketing_contact_contact_list (
    id integer NOT NULL,
    contact_id integer NOT NULL,
    contactlist_id integer NOT NULL
);


ALTER TABLE public.marketing_contact_contact_list OWNER TO postgres;

--
-- Name: marketing_contact_contact_list_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.marketing_contact_contact_list_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.marketing_contact_contact_list_id_seq OWNER TO postgres;

--
-- Name: marketing_contact_contact_list_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.marketing_contact_contact_list_id_seq OWNED BY public.marketing_contact_contact_list.id;


--
-- Name: marketing_contact_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.marketing_contact_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.marketing_contact_id_seq OWNER TO postgres;

--
-- Name: marketing_contact_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.marketing_contact_id_seq OWNED BY public.marketing_contact.id;


--
-- Name: marketing_contactemailcampaign; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.marketing_contactemailcampaign (
    id integer NOT NULL,
    name character varying(500) NOT NULL,
    email character varying(254) NOT NULL,
    last_name character varying(500),
    created_on timestamp with time zone NOT NULL,
    created_by_id integer
);


ALTER TABLE public.marketing_contactemailcampaign OWNER TO postgres;

--
-- Name: marketing_contactemailcampaign_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.marketing_contactemailcampaign_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.marketing_contactemailcampaign_id_seq OWNER TO postgres;

--
-- Name: marketing_contactemailcampaign_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.marketing_contactemailcampaign_id_seq OWNED BY public.marketing_contactemailcampaign.id;


--
-- Name: marketing_contactlist; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.marketing_contactlist (
    id integer NOT NULL,
    created_on timestamp with time zone NOT NULL,
    name character varying(500) NOT NULL,
    created_by_id integer,
    updated_on timestamp with time zone NOT NULL
);


ALTER TABLE public.marketing_contactlist OWNER TO postgres;

--
-- Name: marketing_contactlist_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.marketing_contactlist_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.marketing_contactlist_id_seq OWNER TO postgres;

--
-- Name: marketing_contactlist_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.marketing_contactlist_id_seq OWNED BY public.marketing_contactlist.id;


--
-- Name: marketing_contactlist_tags; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.marketing_contactlist_tags (
    id integer NOT NULL,
    contactlist_id integer NOT NULL,
    tag_id integer NOT NULL
);


ALTER TABLE public.marketing_contactlist_tags OWNER TO postgres;

--
-- Name: marketing_contactlist_tags_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.marketing_contactlist_tags_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.marketing_contactlist_tags_id_seq OWNER TO postgres;

--
-- Name: marketing_contactlist_tags_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.marketing_contactlist_tags_id_seq OWNED BY public.marketing_contactlist_tags.id;


--
-- Name: marketing_contactlist_visible_to; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.marketing_contactlist_visible_to (
    id integer NOT NULL,
    contactlist_id integer NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.marketing_contactlist_visible_to OWNER TO postgres;

--
-- Name: marketing_contactlist_visible_to_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.marketing_contactlist_visible_to_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.marketing_contactlist_visible_to_id_seq OWNER TO postgres;

--
-- Name: marketing_contactlist_visible_to_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.marketing_contactlist_visible_to_id_seq OWNED BY public.marketing_contactlist_visible_to.id;


--
-- Name: marketing_contactunsubscribedcampaign; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.marketing_contactunsubscribedcampaign (
    id integer NOT NULL,
    is_unsubscribed boolean NOT NULL,
    campaigns_id integer NOT NULL,
    contacts_id integer NOT NULL
);


ALTER TABLE public.marketing_contactunsubscribedcampaign OWNER TO postgres;

--
-- Name: marketing_contactunsubscribedcampaign_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.marketing_contactunsubscribedcampaign_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.marketing_contactunsubscribedcampaign_id_seq OWNER TO postgres;

--
-- Name: marketing_contactunsubscribedcampaign_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.marketing_contactunsubscribedcampaign_id_seq OWNED BY public.marketing_contactunsubscribedcampaign.id;


--
-- Name: marketing_duplicatecontacts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.marketing_duplicatecontacts (
    id integer NOT NULL,
    contact_list_id integer,
    contacts_id integer
);


ALTER TABLE public.marketing_duplicatecontacts OWNER TO postgres;

--
-- Name: marketing_duplicatecontacts_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.marketing_duplicatecontacts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.marketing_duplicatecontacts_id_seq OWNER TO postgres;

--
-- Name: marketing_duplicatecontacts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.marketing_duplicatecontacts_id_seq OWNED BY public.marketing_duplicatecontacts.id;


--
-- Name: marketing_emailtemplate; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.marketing_emailtemplate (
    id integer NOT NULL,
    created_on timestamp with time zone NOT NULL,
    title character varying(5000) NOT NULL,
    subject character varying(5000) NOT NULL,
    html text NOT NULL,
    created_by_id integer,
    updated_on timestamp with time zone NOT NULL
);


ALTER TABLE public.marketing_emailtemplate OWNER TO postgres;

--
-- Name: marketing_emailtemplate_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.marketing_emailtemplate_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.marketing_emailtemplate_id_seq OWNER TO postgres;

--
-- Name: marketing_emailtemplate_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.marketing_emailtemplate_id_seq OWNED BY public.marketing_emailtemplate.id;


--
-- Name: marketing_failedcontact; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.marketing_failedcontact (
    id integer NOT NULL,
    created_on timestamp with time zone NOT NULL,
    name character varying(500),
    email character varying(254),
    contact_number character varying(20),
    company_name character varying(500),
    last_name character varying(500),
    city character varying(500),
    state character varying(500),
    contry character varying(500),
    created_by_id integer
);


ALTER TABLE public.marketing_failedcontact OWNER TO postgres;

--
-- Name: marketing_failedcontact_contact_list; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.marketing_failedcontact_contact_list (
    id integer NOT NULL,
    failedcontact_id integer NOT NULL,
    contactlist_id integer NOT NULL
);


ALTER TABLE public.marketing_failedcontact_contact_list OWNER TO postgres;

--
-- Name: marketing_failedcontact_contact_list_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.marketing_failedcontact_contact_list_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.marketing_failedcontact_contact_list_id_seq OWNER TO postgres;

--
-- Name: marketing_failedcontact_contact_list_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.marketing_failedcontact_contact_list_id_seq OWNED BY public.marketing_failedcontact_contact_list.id;


--
-- Name: marketing_failedcontact_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.marketing_failedcontact_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.marketing_failedcontact_id_seq OWNER TO postgres;

--
-- Name: marketing_failedcontact_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.marketing_failedcontact_id_seq OWNED BY public.marketing_failedcontact.id;


--
-- Name: marketing_link; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.marketing_link (
    id integer NOT NULL,
    original character varying(2100) NOT NULL,
    clicks integer NOT NULL,
    "unique" integer NOT NULL,
    campaign_id integer NOT NULL
);


ALTER TABLE public.marketing_link OWNER TO postgres;

--
-- Name: marketing_link_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.marketing_link_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.marketing_link_id_seq OWNER TO postgres;

--
-- Name: marketing_link_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.marketing_link_id_seq OWNED BY public.marketing_link.id;


--
-- Name: marketing_tag; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.marketing_tag (
    id integer NOT NULL,
    name character varying(500) NOT NULL,
    color character varying(20) NOT NULL,
    created_by_id integer,
    created_on timestamp with time zone NOT NULL
);


ALTER TABLE public.marketing_tag OWNER TO postgres;

--
-- Name: marketing_tag_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.marketing_tag_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.marketing_tag_id_seq OWNER TO postgres;

--
-- Name: marketing_tag_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.marketing_tag_id_seq OWNED BY public.marketing_tag.id;


--
-- Name: opportunity_opportunity; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.opportunity_opportunity (
    id integer NOT NULL,
    name character varying(64) NOT NULL,
    stage character varying(64) NOT NULL,
    currency character varying(3),
    amount numeric(12,2),
    lead_source character varying(255),
    probability integer,
    closed_on date,
    description text,
    created_on timestamp with time zone NOT NULL,
    is_active boolean NOT NULL,
    closed_by_id integer,
    created_by_id integer,
    company_id integer
);


ALTER TABLE public.opportunity_opportunity OWNER TO postgres;

--
-- Name: opportunity_opportunity_assigned_to; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.opportunity_opportunity_assigned_to (
    id integer NOT NULL,
    opportunity_id integer NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.opportunity_opportunity_assigned_to OWNER TO postgres;

--
-- Name: opportunity_opportunity_assigned_to_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.opportunity_opportunity_assigned_to_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.opportunity_opportunity_assigned_to_id_seq OWNER TO postgres;

--
-- Name: opportunity_opportunity_assigned_to_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.opportunity_opportunity_assigned_to_id_seq OWNED BY public.opportunity_opportunity_assigned_to.id;


--
-- Name: opportunity_opportunity_contacts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.opportunity_opportunity_contacts (
    id integer NOT NULL,
    opportunity_id integer NOT NULL,
    contact_id integer NOT NULL
);


ALTER TABLE public.opportunity_opportunity_contacts OWNER TO postgres;

--
-- Name: opportunity_opportunity_contacts_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.opportunity_opportunity_contacts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.opportunity_opportunity_contacts_id_seq OWNER TO postgres;

--
-- Name: opportunity_opportunity_contacts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.opportunity_opportunity_contacts_id_seq OWNED BY public.opportunity_opportunity_contacts.id;


--
-- Name: opportunity_opportunity_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.opportunity_opportunity_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.opportunity_opportunity_id_seq OWNER TO postgres;

--
-- Name: opportunity_opportunity_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.opportunity_opportunity_id_seq OWNED BY public.opportunity_opportunity.id;


--
-- Name: opportunity_opportunity_tags; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.opportunity_opportunity_tags (
    id integer NOT NULL,
    opportunity_id integer NOT NULL,
    tags_id integer NOT NULL
);


ALTER TABLE public.opportunity_opportunity_tags OWNER TO postgres;

--
-- Name: opportunity_opportunity_tags_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.opportunity_opportunity_tags_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.opportunity_opportunity_tags_id_seq OWNER TO postgres;

--
-- Name: opportunity_opportunity_tags_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.opportunity_opportunity_tags_id_seq OWNED BY public.opportunity_opportunity_tags.id;


--
-- Name: opportunity_opportunity_teams; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.opportunity_opportunity_teams (
    id integer NOT NULL,
    opportunity_id integer NOT NULL,
    teams_id integer NOT NULL
);


ALTER TABLE public.opportunity_opportunity_teams OWNER TO postgres;

--
-- Name: opportunity_opportunity_teams_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.opportunity_opportunity_teams_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.opportunity_opportunity_teams_id_seq OWNER TO postgres;

--
-- Name: opportunity_opportunity_teams_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.opportunity_opportunity_teams_id_seq OWNED BY public.opportunity_opportunity_teams.id;


--
-- Name: planner_event; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.planner_event (
    id integer NOT NULL,
    name character varying(64) NOT NULL,
    event_type character varying(7) NOT NULL,
    object_id integer,
    status character varying(64) NOT NULL,
    direction character varying(20) NOT NULL,
    start_date date NOT NULL,
    close_date date,
    duration integer,
    priority character varying(10) NOT NULL,
    updated_on timestamp with time zone NOT NULL,
    created_on timestamp with time zone NOT NULL,
    description text,
    is_active boolean NOT NULL,
    content_type_id integer,
    created_by_id integer,
    updated_by_id integer,
    CONSTRAINT planner_event_object_id_check CHECK ((object_id >= 0))
);


ALTER TABLE public.planner_event OWNER TO postgres;

--
-- Name: planner_event_assigned_to; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.planner_event_assigned_to (
    id integer NOT NULL,
    event_id integer NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.planner_event_assigned_to OWNER TO postgres;

--
-- Name: planner_event_assigned_to_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.planner_event_assigned_to_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.planner_event_assigned_to_id_seq OWNER TO postgres;

--
-- Name: planner_event_assigned_to_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.planner_event_assigned_to_id_seq OWNED BY public.planner_event_assigned_to.id;


--
-- Name: planner_event_attendees_contacts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.planner_event_attendees_contacts (
    id integer NOT NULL,
    event_id integer NOT NULL,
    contact_id integer NOT NULL
);


ALTER TABLE public.planner_event_attendees_contacts OWNER TO postgres;

--
-- Name: planner_event_attendees_contacts_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.planner_event_attendees_contacts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.planner_event_attendees_contacts_id_seq OWNER TO postgres;

--
-- Name: planner_event_attendees_contacts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.planner_event_attendees_contacts_id_seq OWNED BY public.planner_event_attendees_contacts.id;


--
-- Name: planner_event_attendees_leads; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.planner_event_attendees_leads (
    id integer NOT NULL,
    event_id integer NOT NULL,
    lead_id integer NOT NULL
);


ALTER TABLE public.planner_event_attendees_leads OWNER TO postgres;

--
-- Name: planner_event_attendees_leads_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.planner_event_attendees_leads_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.planner_event_attendees_leads_id_seq OWNER TO postgres;

--
-- Name: planner_event_attendees_leads_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.planner_event_attendees_leads_id_seq OWNED BY public.planner_event_attendees_leads.id;


--
-- Name: planner_event_attendees_user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.planner_event_attendees_user (
    id integer NOT NULL,
    event_id integer NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.planner_event_attendees_user OWNER TO postgres;

--
-- Name: planner_event_attendees_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.planner_event_attendees_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.planner_event_attendees_user_id_seq OWNER TO postgres;

--
-- Name: planner_event_attendees_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.planner_event_attendees_user_id_seq OWNED BY public.planner_event_attendees_user.id;


--
-- Name: planner_event_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.planner_event_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.planner_event_id_seq OWNER TO postgres;

--
-- Name: planner_event_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.planner_event_id_seq OWNED BY public.planner_event.id;


--
-- Name: planner_event_reminders; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.planner_event_reminders (
    id integer NOT NULL,
    event_id integer NOT NULL,
    reminder_id integer NOT NULL
);


ALTER TABLE public.planner_event_reminders OWNER TO postgres;

--
-- Name: planner_event_reminders_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.planner_event_reminders_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.planner_event_reminders_id_seq OWNER TO postgres;

--
-- Name: planner_event_reminders_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.planner_event_reminders_id_seq OWNED BY public.planner_event_reminders.id;


--
-- Name: planner_reminder; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.planner_reminder (
    id integer NOT NULL,
    reminder_type character varying(5),
    reminder_time integer
);


ALTER TABLE public.planner_reminder OWNER TO postgres;

--
-- Name: planner_reminder_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.planner_reminder_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.planner_reminder_id_seq OWNER TO postgres;

--
-- Name: planner_reminder_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.planner_reminder_id_seq OWNED BY public.planner_reminder.id;


--
-- Name: project_expenses_expensetype; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.project_expenses_expensetype (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    is_active boolean NOT NULL
);


ALTER TABLE public.project_expenses_expensetype OWNER TO postgres;

--
-- Name: project_expenses_expendtype_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.project_expenses_expendtype_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.project_expenses_expendtype_id_seq OWNER TO postgres;

--
-- Name: project_expenses_expendtype_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.project_expenses_expendtype_id_seq OWNED BY public.project_expenses_expensetype.id;


--
-- Name: project_expenses_projectexpense; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.project_expenses_projectexpense (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    price numeric(12,2) NOT NULL,
    pic character varying(50),
    remark text,
    pay_date date NOT NULL,
    project_id integer NOT NULL,
    expense_type_id integer NOT NULL,
    img character varying(100),
    img_upload_date date,
    img_height integer NOT NULL,
    img_width integer NOT NULL,
    CONSTRAINT project_expenses_projectexpense_img_height_check CHECK ((img_height >= 0)),
    CONSTRAINT project_expenses_projectexpense_img_width_check CHECK ((img_width >= 0))
);


ALTER TABLE public.project_expenses_projectexpense OWNER TO postgres;

--
-- Name: project_expenses_projectexpend_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.project_expenses_projectexpend_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.project_expenses_projectexpend_id_seq OWNER TO postgres;

--
-- Name: project_expenses_projectexpend_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.project_expenses_projectexpend_id_seq OWNED BY public.project_expenses_projectexpense.id;


--
-- Name: project_items_item; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.project_items_item (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    is_active boolean NOT NULL,
    item_type_id integer NOT NULL,
    value_based_price numeric(12,2) NOT NULL,
    item_formulas jsonb,
    item_properties_sort jsonb NOT NULL,
    index integer NOT NULL
);


ALTER TABLE public.project_items_item OWNER TO postgres;

--
-- Name: project_items_item_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.project_items_item_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.project_items_item_id_seq OWNER TO postgres;

--
-- Name: project_items_item_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.project_items_item_id_seq OWNED BY public.project_items_item.id;


--
-- Name: project_items_item_item_properties; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.project_items_item_item_properties (
    id integer NOT NULL,
    item_id integer NOT NULL,
    itemproperty_id integer NOT NULL
);


ALTER TABLE public.project_items_item_item_properties OWNER TO postgres;

--
-- Name: project_items_item_item_properties_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.project_items_item_item_properties_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.project_items_item_item_properties_id_seq OWNER TO postgres;

--
-- Name: project_items_item_item_properties_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.project_items_item_item_properties_id_seq OWNED BY public.project_items_item_item_properties.id;


--
-- Name: project_items_itemformula; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.project_items_itemformula (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    formula text NOT NULL,
    item_id integer NOT NULL,
    is_active boolean NOT NULL
);


ALTER TABLE public.project_items_itemformula OWNER TO postgres;

--
-- Name: project_items_itemformula_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.project_items_itemformula_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.project_items_itemformula_id_seq OWNER TO postgres;

--
-- Name: project_items_itemformula_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.project_items_itemformula_id_seq OWNED BY public.project_items_itemformula.id;


--
-- Name: project_items_itemproperty; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.project_items_itemproperty (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    symbol character varying(50) NOT NULL,
    index integer NOT NULL
);


ALTER TABLE public.project_items_itemproperty OWNER TO postgres;

--
-- Name: project_items_itemproperty_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.project_items_itemproperty_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.project_items_itemproperty_id_seq OWNER TO postgres;

--
-- Name: project_items_itemproperty_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.project_items_itemproperty_id_seq OWNED BY public.project_items_itemproperty.id;


--
-- Name: project_items_itemtype; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.project_items_itemtype (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    is_active boolean NOT NULL,
    item_type_materials jsonb
);


ALTER TABLE public.project_items_itemtype OWNER TO postgres;

--
-- Name: project_items_itemtype_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.project_items_itemtype_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.project_items_itemtype_id_seq OWNER TO postgres;

--
-- Name: project_items_itemtype_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.project_items_itemtype_id_seq OWNED BY public.project_items_itemtype.id;


--
-- Name: project_items_itemtypematerial; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.project_items_itemtypematerial (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    item_type_id integer NOT NULL,
    value_based_price numeric(12,2) NOT NULL,
    is_active boolean NOT NULL
);


ALTER TABLE public.project_items_itemtypematerial OWNER TO postgres;

--
-- Name: project_items_itemtypematerial_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.project_items_itemtypematerial_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.project_items_itemtypematerial_id_seq OWNER TO postgres;

--
-- Name: project_items_itemtypematerial_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.project_items_itemtypematerial_id_seq OWNED BY public.project_items_itemtypematerial.id;


--
-- Name: project_misc_misc; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.project_misc_misc (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    suggested_unit_price numeric(12,2) NOT NULL,
    is_active boolean NOT NULL
);


ALTER TABLE public.project_misc_misc OWNER TO postgres;

--
-- Name: project_misc_misc_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.project_misc_misc_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.project_misc_misc_id_seq OWNER TO postgres;

--
-- Name: project_misc_misc_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.project_misc_misc_id_seq OWNED BY public.project_misc_misc.id;


--
-- Name: project_misc_projectmisc; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.project_misc_projectmisc (
    id integer NOT NULL,
    unit_price numeric(12,2) NOT NULL,
    quantity integer NOT NULL,
    remark text,
    misc_id integer NOT NULL,
    project_id integer NOT NULL,
    CONSTRAINT project_misc_projectmisc_quantity_check CHECK ((quantity >= 0))
);


ALTER TABLE public.project_misc_projectmisc OWNER TO postgres;

--
-- Name: project_misc_projectmisc_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.project_misc_projectmisc_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.project_misc_projectmisc_id_seq OWNER TO postgres;

--
-- Name: project_misc_projectmisc_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.project_misc_projectmisc_id_seq OWNED BY public.project_misc_projectmisc.id;


--
-- Name: project_timetable_projectmilestone; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.project_timetable_projectmilestone (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    date date NOT NULL,
    remind interval,
    pic character varying(50),
    description text,
    project_id integer NOT NULL,
    img character varying(100),
    img_upload_date date,
    img_height integer NOT NULL,
    img_width integer NOT NULL,
    CONSTRAINT project_timetable_projectmilestone_img_height_check CHECK ((img_height >= 0)),
    CONSTRAINT project_timetable_projectmilestone_img_width_check CHECK ((img_width >= 0))
);


ALTER TABLE public.project_timetable_projectmilestone OWNER TO postgres;

--
-- Name: project_timetable_projectmilestone_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.project_timetable_projectmilestone_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.project_timetable_projectmilestone_id_seq OWNER TO postgres;

--
-- Name: project_timetable_projectmilestone_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.project_timetable_projectmilestone_id_seq OWNED BY public.project_timetable_projectmilestone.id;


--
-- Name: project_timetable_projectwork; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.project_timetable_projectwork (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    pic character varying(50),
    start_date date NOT NULL,
    end_date date NOT NULL,
    description text,
    project_id integer NOT NULL
);


ALTER TABLE public.project_timetable_projectwork OWNER TO postgres;

--
-- Name: project_timetable_projectwork_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.project_timetable_projectwork_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.project_timetable_projectwork_id_seq OWNER TO postgres;

--
-- Name: project_timetable_projectwork_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.project_timetable_projectwork_id_seq OWNED BY public.project_timetable_projectwork.id;


--
-- Name: projects_companyprojectcomparison; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.projects_companyprojectcomparison (
    id integer NOT NULL,
    company_id integer NOT NULL
);


ALTER TABLE public.projects_companyprojectcomparison OWNER TO postgres;

--
-- Name: projects_companyprojectcomparison_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.projects_companyprojectcomparison_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.projects_companyprojectcomparison_id_seq OWNER TO postgres;

--
-- Name: projects_companyprojectcomparison_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.projects_companyprojectcomparison_id_seq OWNED BY public.projects_companyprojectcomparison.id;


--
-- Name: projects_companyprojectcomparison_projects; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.projects_companyprojectcomparison_projects (
    id integer NOT NULL,
    companyprojectcomparison_id integer NOT NULL,
    project_id integer NOT NULL
);


ALTER TABLE public.projects_companyprojectcomparison_projects OWNER TO postgres;

--
-- Name: projects_companyprojectcomparison_projects_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.projects_companyprojectcomparison_projects_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.projects_companyprojectcomparison_projects_id_seq OWNER TO postgres;

--
-- Name: projects_companyprojectcomparison_projects_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.projects_companyprojectcomparison_projects_id_seq OWNED BY public.projects_companyprojectcomparison_projects.id;


--
-- Name: projects_project; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.projects_project (
    id integer NOT NULL,
    project_title character varying(50) NOT NULL,
    created_on timestamp with time zone NOT NULL,
    amount_due numeric(12,2),
    amount_paid numeric(12,2),
    is_email_sent boolean NOT NULL,
    status character varying(15) NOT NULL,
    details text,
    start_date date,
    due_date date,
    district character varying(50) NOT NULL,
    work_location character varying(1024),
    company_id integer NOT NULL,
    created_by_id integer,
    charging_stages jsonb NOT NULL,
    document_format jsonb NOT NULL,
    invoice_remarks jsonb,
    job_no integer NOT NULL,
    quotation_generated_on timestamp with time zone,
    quotation_no character varying(50),
    quotation_remarks jsonb,
    receipt_remarks jsonb,
    updated_on timestamp with time zone NOT NULL,
    quotation_version integer NOT NULL,
    CONSTRAINT projects_project_job_no_check CHECK ((job_no >= 0)),
    CONSTRAINT projects_project_quotation_version_check CHECK ((quotation_version >= 0))
);


ALTER TABLE public.projects_project OWNER TO postgres;

--
-- Name: projects_project_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.projects_project_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.projects_project_id_seq OWNER TO postgres;

--
-- Name: projects_project_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.projects_project_id_seq OWNED BY public.projects_project.id;


--
-- Name: projects_projecthistory; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.projects_projecthistory (
    id integer NOT NULL,
    project_title character varying(50) NOT NULL,
    project_number character varying(50) NOT NULL,
    name character varying(100) NOT NULL,
    email character varying(254) NOT NULL,
    quantity integer NOT NULL,
    rate numeric(12,2) NOT NULL,
    phone character varying(128),
    created_on timestamp with time zone NOT NULL,
    amount_due numeric(12,2),
    amount_paid numeric(12,2),
    is_email_sent boolean NOT NULL,
    status character varying(15) NOT NULL,
    details text,
    due_date date,
    from_address_id integer,
    project_id integer NOT NULL,
    to_address_id integer,
    updated_by_id integer,
    CONSTRAINT projects_projecthistory_quantity_check CHECK ((quantity >= 0))
);


ALTER TABLE public.projects_projecthistory OWNER TO postgres;

--
-- Name: projects_projecthistory_assigned_to; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.projects_projecthistory_assigned_to (
    id integer NOT NULL,
    projecthistory_id integer NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.projects_projecthistory_assigned_to OWNER TO postgres;

--
-- Name: projects_projecthistory_assigned_to_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.projects_projecthistory_assigned_to_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.projects_projecthistory_assigned_to_id_seq OWNER TO postgres;

--
-- Name: projects_projecthistory_assigned_to_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.projects_projecthistory_assigned_to_id_seq OWNED BY public.projects_projecthistory_assigned_to.id;


--
-- Name: projects_projecthistory_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.projects_projecthistory_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.projects_projecthistory_id_seq OWNER TO postgres;

--
-- Name: projects_projecthistory_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.projects_projecthistory_id_seq OWNED BY public.projects_projecthistory.id;


--
-- Name: projects_projectimage; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.projects_projectimage (
    id integer NOT NULL,
    img character varying(100) NOT NULL,
    img_width integer NOT NULL,
    img_height integer NOT NULL,
    related_project_id integer NOT NULL,
    display_id integer NOT NULL,
    CONSTRAINT projects_projectimage_img_height_check CHECK ((img_height >= 0)),
    CONSTRAINT projects_projectimage_img_width_check CHECK ((img_width >= 0))
);


ALTER TABLE public.projects_projectimage OWNER TO postgres;

--
-- Name: projects_projectimage_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.projects_projectimage_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.projects_projectimage_id_seq OWNER TO postgres;

--
-- Name: projects_projectimage_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.projects_projectimage_id_seq OWNED BY public.projects_projectimage.id;


--
-- Name: projects_projectimageset; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.projects_projectimageset (
    id integer NOT NULL,
    related_project_id integer,
    upload_date date NOT NULL,
    display_id integer NOT NULL,
    project_milestone_id integer
);


ALTER TABLE public.projects_projectimageset OWNER TO postgres;

--
-- Name: projects_projectimageset_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.projects_projectimageset_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.projects_projectimageset_id_seq OWNER TO postgres;

--
-- Name: projects_projectimageset_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.projects_projectimageset_id_seq OWNED BY public.projects_projectimageset.id;


--
-- Name: projects_projectimageset_imgs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.projects_projectimageset_imgs (
    id integer NOT NULL,
    projectimageset_id integer NOT NULL,
    projectimage_id integer NOT NULL
);


ALTER TABLE public.projects_projectimageset_imgs OWNER TO postgres;

--
-- Name: projects_projectimageset_imgs_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.projects_projectimageset_imgs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.projects_projectimageset_imgs_id_seq OWNER TO postgres;

--
-- Name: projects_projectimageset_imgs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.projects_projectimageset_imgs_id_seq OWNED BY public.projects_projectimageset_imgs.id;


--
-- Name: projects_projectinvoice; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.projects_projectinvoice (
    id integer NOT NULL,
    generated_on timestamp with time zone NOT NULL,
    invoice_id integer NOT NULL,
    project_id integer NOT NULL,
    CONSTRAINT projects_projectinvoice_invoice_id_check CHECK ((invoice_id >= 0))
);


ALTER TABLE public.projects_projectinvoice OWNER TO postgres;

--
-- Name: projects_projectinvoice_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.projects_projectinvoice_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.projects_projectinvoice_id_seq OWNER TO postgres;

--
-- Name: projects_projectinvoice_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.projects_projectinvoice_id_seq OWNED BY public.projects_projectinvoice.id;


--
-- Name: projects_projectreceipt; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.projects_projectreceipt (
    id integer NOT NULL,
    generated_on timestamp with time zone NOT NULL,
    receipt_id integer NOT NULL,
    project_id integer NOT NULL,
    CONSTRAINT projects_projectreceipt_receipt_id_check CHECK ((receipt_id >= 0))
);


ALTER TABLE public.projects_projectreceipt OWNER TO postgres;

--
-- Name: projects_projectreceipt_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.projects_projectreceipt_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.projects_projectreceipt_id_seq OWNER TO postgres;

--
-- Name: projects_projectreceipt_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.projects_projectreceipt_id_seq OWNED BY public.projects_projectreceipt.id;


--
-- Name: quotations_quotation; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.quotations_quotation (
    id integer NOT NULL,
    quotation_title character varying(50) NOT NULL,
    quotation_number character varying(50) NOT NULL,
    name character varying(100) NOT NULL,
    email character varying(254) NOT NULL,
    quantity integer NOT NULL,
    rate numeric(12,2) NOT NULL,
    phone character varying(128),
    created_on timestamp with time zone NOT NULL,
    amount_due numeric(12,2),
    amount_paid numeric(12,2),
    is_email_sent boolean NOT NULL,
    status character varying(15) NOT NULL,
    details text,
    due_date date,
    created_by_id integer,
    from_address_id integer,
    to_address_id integer,
    approved_by_id integer,
    approved_on timestamp with time zone,
    last_updated_by_id integer,
    last_updated_on timestamp with time zone NOT NULL,
    CONSTRAINT quotations_quotation_quantity_check CHECK ((quantity >= 0))
);


ALTER TABLE public.quotations_quotation OWNER TO postgres;

--
-- Name: quotations_quotation_assigned_to; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.quotations_quotation_assigned_to (
    id integer NOT NULL,
    quotation_id integer NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.quotations_quotation_assigned_to OWNER TO postgres;

--
-- Name: quotations_quotation_assigned_to_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.quotations_quotation_assigned_to_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.quotations_quotation_assigned_to_id_seq OWNER TO postgres;

--
-- Name: quotations_quotation_assigned_to_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.quotations_quotation_assigned_to_id_seq OWNED BY public.quotations_quotation_assigned_to.id;


--
-- Name: quotations_quotation_companies; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.quotations_quotation_companies (
    id integer NOT NULL,
    quotation_id integer NOT NULL,
    company_id integer NOT NULL
);


ALTER TABLE public.quotations_quotation_companies OWNER TO postgres;

--
-- Name: quotations_quotation_companies_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.quotations_quotation_companies_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.quotations_quotation_companies_id_seq OWNER TO postgres;

--
-- Name: quotations_quotation_companies_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.quotations_quotation_companies_id_seq OWNED BY public.quotations_quotation_companies.id;


--
-- Name: quotations_quotation_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.quotations_quotation_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.quotations_quotation_id_seq OWNER TO postgres;

--
-- Name: quotations_quotation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.quotations_quotation_id_seq OWNED BY public.quotations_quotation.id;


--
-- Name: quotations_quotation_teams; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.quotations_quotation_teams (
    id integer NOT NULL,
    quotation_id integer NOT NULL,
    teams_id integer NOT NULL
);


ALTER TABLE public.quotations_quotation_teams OWNER TO postgres;

--
-- Name: quotations_quotation_teams_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.quotations_quotation_teams_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.quotations_quotation_teams_id_seq OWNER TO postgres;

--
-- Name: quotations_quotation_teams_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.quotations_quotation_teams_id_seq OWNED BY public.quotations_quotation_teams.id;


--
-- Name: quotations_quotationhistory; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.quotations_quotationhistory (
    id integer NOT NULL,
    quotation_title character varying(50) NOT NULL,
    quotation_number character varying(50) NOT NULL,
    name character varying(100) NOT NULL,
    email character varying(254) NOT NULL,
    quantity integer NOT NULL,
    rate numeric(12,2) NOT NULL,
    phone character varying(128),
    created_on timestamp with time zone NOT NULL,
    amount_due numeric(12,2),
    amount_paid numeric(12,2),
    is_email_sent boolean NOT NULL,
    status character varying(15) NOT NULL,
    details text,
    due_date date,
    from_address_id integer,
    quotation_id integer NOT NULL,
    to_address_id integer,
    updated_by_id integer,
    CONSTRAINT quotations_quotationhistory_quantity_check CHECK ((quantity >= 0))
);


ALTER TABLE public.quotations_quotationhistory OWNER TO postgres;

--
-- Name: quotations_quotationhistory_assigned_to; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.quotations_quotationhistory_assigned_to (
    id integer NOT NULL,
    quotationhistory_id integer NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.quotations_quotationhistory_assigned_to OWNER TO postgres;

--
-- Name: quotations_quotationhistory_assigned_to_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.quotations_quotationhistory_assigned_to_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.quotations_quotationhistory_assigned_to_id_seq OWNER TO postgres;

--
-- Name: quotations_quotationhistory_assigned_to_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.quotations_quotationhistory_assigned_to_id_seq OWNED BY public.quotations_quotationhistory_assigned_to.id;


--
-- Name: quotations_quotationhistory_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.quotations_quotationhistory_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.quotations_quotationhistory_id_seq OWNER TO postgres;

--
-- Name: quotations_quotationhistory_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.quotations_quotationhistory_id_seq OWNED BY public.quotations_quotationhistory.id;


--
-- Name: rooms_room; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.rooms_room (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    related_project_id integer NOT NULL,
    room_type_id integer NOT NULL,
    value jsonb,
    measure_quantifier character varying(20) NOT NULL
);


ALTER TABLE public.rooms_room OWNER TO postgres;

--
-- Name: rooms_room_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.rooms_room_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.rooms_room_id_seq OWNER TO postgres;

--
-- Name: rooms_room_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.rooms_room_id_seq OWNED BY public.rooms_room.id;


--
-- Name: rooms_roomitem; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.rooms_roomitem (
    id integer NOT NULL,
    unit_price numeric(12,2) NOT NULL,
    value jsonb,
    quantity numeric(12,2) NOT NULL,
    item_id integer NOT NULL,
    room_id integer NOT NULL,
    material text,
    remark text,
    material_value_based_price numeric(12,2) NOT NULL,
    measure_quantifier character varying(20) NOT NULL,
    item_quantifier character varying(20) NOT NULL,
    value_based_price numeric(12,2) NOT NULL
);


ALTER TABLE public.rooms_roomitem OWNER TO postgres;

--
-- Name: rooms_roomitem_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.rooms_roomitem_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.rooms_roomitem_id_seq OWNER TO postgres;

--
-- Name: rooms_roomitem_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.rooms_roomitem_id_seq OWNED BY public.rooms_roomitem.id;


--
-- Name: rooms_roomproperty; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.rooms_roomproperty (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    symbol character varying(50) NOT NULL,
    data_type character varying(50) NOT NULL,
    custom_properties jsonb,
    custom_property_formulas jsonb,
    index integer NOT NULL
);


ALTER TABLE public.rooms_roomproperty OWNER TO postgres;

--
-- Name: rooms_roomproperty_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.rooms_roomproperty_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.rooms_roomproperty_id_seq OWNER TO postgres;

--
-- Name: rooms_roomproperty_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.rooms_roomproperty_id_seq OWNED BY public.rooms_roomproperty.id;


--
-- Name: rooms_roomtype; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.rooms_roomtype (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    is_active boolean NOT NULL,
    room_type_formulas jsonb,
    related_items_sort jsonb NOT NULL,
    room_properties_sort jsonb NOT NULL
);


ALTER TABLE public.rooms_roomtype OWNER TO postgres;

--
-- Name: rooms_roomtype_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.rooms_roomtype_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.rooms_roomtype_id_seq OWNER TO postgres;

--
-- Name: rooms_roomtype_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.rooms_roomtype_id_seq OWNED BY public.rooms_roomtype.id;


--
-- Name: rooms_roomtype_related_items; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.rooms_roomtype_related_items (
    id integer NOT NULL,
    roomtype_id integer NOT NULL,
    item_id integer NOT NULL
);


ALTER TABLE public.rooms_roomtype_related_items OWNER TO postgres;

--
-- Name: rooms_roomtype_related_items_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.rooms_roomtype_related_items_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.rooms_roomtype_related_items_id_seq OWNER TO postgres;

--
-- Name: rooms_roomtype_related_items_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.rooms_roomtype_related_items_id_seq OWNED BY public.rooms_roomtype_related_items.id;


--
-- Name: rooms_roomtype_room_properties; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.rooms_roomtype_room_properties (
    id integer NOT NULL,
    roomtype_id integer NOT NULL,
    roomproperty_id integer NOT NULL
);


ALTER TABLE public.rooms_roomtype_room_properties OWNER TO postgres;

--
-- Name: rooms_roomtype_room_properties_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.rooms_roomtype_room_properties_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.rooms_roomtype_room_properties_id_seq OWNER TO postgres;

--
-- Name: rooms_roomtype_room_properties_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.rooms_roomtype_room_properties_id_seq OWNED BY public.rooms_roomtype_room_properties.id;


--
-- Name: rooms_roomtypeformula; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.rooms_roomtypeformula (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    formula text NOT NULL,
    room_type_id integer NOT NULL,
    is_active boolean NOT NULL
);


ALTER TABLE public.rooms_roomtypeformula OWNER TO postgres;

--
-- Name: rooms_roomtypeformula_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.rooms_roomtypeformula_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.rooms_roomtypeformula_id_seq OWNER TO postgres;

--
-- Name: rooms_roomtypeformula_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.rooms_roomtypeformula_id_seq OWNED BY public.rooms_roomtypeformula.id;


--
-- Name: subscription_plans_companysubscribedplan; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.subscription_plans_companysubscribedplan (
    id integer NOT NULL,
    start_date date NOT NULL,
    next_billing_date date,
    company_id integer NOT NULL,
    plan_id integer NOT NULL
);


ALTER TABLE public.subscription_plans_companysubscribedplan OWNER TO postgres;

--
-- Name: subscription_plans_companysubscribedplan_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.subscription_plans_companysubscribedplan_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.subscription_plans_companysubscribedplan_id_seq OWNER TO postgres;

--
-- Name: subscription_plans_companysubscribedplan_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.subscription_plans_companysubscribedplan_id_seq OWNED BY public.subscription_plans_companysubscribedplan.id;


--
-- Name: subscription_plans_subscriptionplan; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.subscription_plans_subscriptionplan (
    id integer NOT NULL,
    plan_name character varying(256) NOT NULL,
    display_price numeric(12,2) NOT NULL,
    project_quota integer,
    function_permission jsonb NOT NULL,
    description text NOT NULL,
    is_active boolean NOT NULL,
    visible boolean NOT NULL,
    bottom_bg_color character varying(18) NOT NULL,
    top_bg_color character varying(18) NOT NULL,
    CONSTRAINT subscription_plans_subscriptionplan_project_quota_check CHECK ((project_quota >= 0))
);


ALTER TABLE public.subscription_plans_subscriptionplan OWNER TO postgres;

--
-- Name: subscription_plans_subscriptionplan_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.subscription_plans_subscriptionplan_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.subscription_plans_subscriptionplan_id_seq OWNER TO postgres;

--
-- Name: subscription_plans_subscriptionplan_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.subscription_plans_subscriptionplan_id_seq OWNED BY public.subscription_plans_subscriptionplan.id;


--
-- Name: tasks_task; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tasks_task (
    id integer NOT NULL,
    title character varying(200) NOT NULL,
    status character varying(50) NOT NULL,
    priority character varying(50) NOT NULL,
    due_date date,
    created_by_id integer,
    created_on timestamp with time zone NOT NULL,
    company_id integer
);


ALTER TABLE public.tasks_task OWNER TO postgres;

--
-- Name: tasks_task_assigned_to; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tasks_task_assigned_to (
    id integer NOT NULL,
    task_id integer NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.tasks_task_assigned_to OWNER TO postgres;

--
-- Name: tasks_task_assigned_to_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tasks_task_assigned_to_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tasks_task_assigned_to_id_seq OWNER TO postgres;

--
-- Name: tasks_task_assigned_to_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tasks_task_assigned_to_id_seq OWNED BY public.tasks_task_assigned_to.id;


--
-- Name: tasks_task_contacts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tasks_task_contacts (
    id integer NOT NULL,
    task_id integer NOT NULL,
    contact_id integer NOT NULL
);


ALTER TABLE public.tasks_task_contacts OWNER TO postgres;

--
-- Name: tasks_task_contacts_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tasks_task_contacts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tasks_task_contacts_id_seq OWNER TO postgres;

--
-- Name: tasks_task_contacts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tasks_task_contacts_id_seq OWNED BY public.tasks_task_contacts.id;


--
-- Name: tasks_task_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tasks_task_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tasks_task_id_seq OWNER TO postgres;

--
-- Name: tasks_task_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tasks_task_id_seq OWNED BY public.tasks_task.id;


--
-- Name: tasks_task_teams; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tasks_task_teams (
    id integer NOT NULL,
    task_id integer NOT NULL,
    teams_id integer NOT NULL
);


ALTER TABLE public.tasks_task_teams OWNER TO postgres;

--
-- Name: tasks_task_teams_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tasks_task_teams_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tasks_task_teams_id_seq OWNER TO postgres;

--
-- Name: tasks_task_teams_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tasks_task_teams_id_seq OWNED BY public.tasks_task_teams.id;


--
-- Name: teams_teams; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.teams_teams (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    description text NOT NULL,
    created_by_id integer,
    created_on timestamp with time zone NOT NULL
);


ALTER TABLE public.teams_teams OWNER TO postgres;

--
-- Name: teams_teams_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.teams_teams_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.teams_teams_id_seq OWNER TO postgres;

--
-- Name: teams_teams_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.teams_teams_id_seq OWNED BY public.teams_teams.id;


--
-- Name: teams_teams_users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.teams_teams_users (
    id integer NOT NULL,
    teams_id integer NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.teams_teams_users OWNER TO postgres;

--
-- Name: teams_teams_users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.teams_teams_users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.teams_teams_users_id_seq OWNER TO postgres;

--
-- Name: teams_teams_users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.teams_teams_users_id_seq OWNED BY public.teams_teams_users.id;


--
-- Name: thumbnail_kvstore; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.thumbnail_kvstore (
    key character varying(200) NOT NULL,
    value text NOT NULL
);


ALTER TABLE public.thumbnail_kvstore OWNER TO postgres;

--
-- Name: token_blacklist_blacklistedtoken; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.token_blacklist_blacklistedtoken (
    id integer NOT NULL,
    blacklisted_at timestamp with time zone NOT NULL,
    token_id integer NOT NULL
);


ALTER TABLE public.token_blacklist_blacklistedtoken OWNER TO postgres;

--
-- Name: token_blacklist_blacklistedtoken_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.token_blacklist_blacklistedtoken_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.token_blacklist_blacklistedtoken_id_seq OWNER TO postgres;

--
-- Name: token_blacklist_blacklistedtoken_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.token_blacklist_blacklistedtoken_id_seq OWNED BY public.token_blacklist_blacklistedtoken.id;


--
-- Name: token_blacklist_outstandingtoken; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.token_blacklist_outstandingtoken (
    id integer NOT NULL,
    token text NOT NULL,
    created_at timestamp with time zone,
    expires_at timestamp with time zone NOT NULL,
    user_id integer,
    jti character varying(255) NOT NULL
);


ALTER TABLE public.token_blacklist_outstandingtoken OWNER TO postgres;

--
-- Name: token_blacklist_outstandingtoken_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.token_blacklist_outstandingtoken_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.token_blacklist_outstandingtoken_id_seq OWNER TO postgres;

--
-- Name: token_blacklist_outstandingtoken_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.token_blacklist_outstandingtoken_id_seq OWNED BY public.token_blacklist_outstandingtoken.id;


--
-- Name: accounts_account id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_account ALTER COLUMN id SET DEFAULT nextval('public.accounts_account_id_seq'::regclass);


--
-- Name: accounts_account_assigned_to id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_account_assigned_to ALTER COLUMN id SET DEFAULT nextval('public.accounts_account_assigned_to_id_seq'::regclass);


--
-- Name: accounts_account_contacts id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_account_contacts ALTER COLUMN id SET DEFAULT nextval('public.accounts_account_contacts_id_seq'::regclass);


--
-- Name: accounts_account_tags id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_account_tags ALTER COLUMN id SET DEFAULT nextval('public.accounts_account_tags_id_seq'::regclass);


--
-- Name: accounts_account_teams id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_account_teams ALTER COLUMN id SET DEFAULT nextval('public.accounts_account_teams_id_seq'::regclass);


--
-- Name: accounts_email id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_email ALTER COLUMN id SET DEFAULT nextval('public.accounts_email_id_seq'::regclass);


--
-- Name: accounts_email_recipients id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_email_recipients ALTER COLUMN id SET DEFAULT nextval('public.accounts_email_recipients_id_seq'::regclass);


--
-- Name: accounts_emaillog id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_emaillog ALTER COLUMN id SET DEFAULT nextval('public.accounts_emaillog_id_seq'::regclass);


--
-- Name: accounts_tags id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_tags ALTER COLUMN id SET DEFAULT nextval('public.accounts_tags_id_seq'::regclass);


--
-- Name: auth_group id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group ALTER COLUMN id SET DEFAULT nextval('public.auth_group_id_seq'::regclass);


--
-- Name: auth_group_permissions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_group_permissions_id_seq'::regclass);


--
-- Name: auth_permission id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission ALTER COLUMN id SET DEFAULT nextval('public.auth_permission_id_seq'::regclass);


--
-- Name: cases_case id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cases_case ALTER COLUMN id SET DEFAULT nextval('public.cases_case_id_seq'::regclass);


--
-- Name: cases_case_assigned_to id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cases_case_assigned_to ALTER COLUMN id SET DEFAULT nextval('public.cases_case_assigned_to_id_seq'::regclass);


--
-- Name: cases_case_contacts id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cases_case_contacts ALTER COLUMN id SET DEFAULT nextval('public.cases_case_contacts_id_seq'::regclass);


--
-- Name: cases_case_teams id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cases_case_teams ALTER COLUMN id SET DEFAULT nextval('public.cases_case_teams_id_seq'::regclass);


--
-- Name: common_address id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.common_address ALTER COLUMN id SET DEFAULT nextval('public.common_address_id_seq'::regclass);


--
-- Name: common_apisettings id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.common_apisettings ALTER COLUMN id SET DEFAULT nextval('public.common_apisettings_id_seq'::regclass);


--
-- Name: common_apisettings_lead_assigned_to id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.common_apisettings_lead_assigned_to ALTER COLUMN id SET DEFAULT nextval('public.common_apisettings_lead_assigned_to_id_seq'::regclass);


--
-- Name: common_apisettings_tags id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.common_apisettings_tags ALTER COLUMN id SET DEFAULT nextval('public.common_apisettings_tags_id_seq'::regclass);


--
-- Name: common_attachments id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.common_attachments ALTER COLUMN id SET DEFAULT nextval('public.common_attachments_id_seq'::regclass);


--
-- Name: common_comment id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.common_comment ALTER COLUMN id SET DEFAULT nextval('public.common_comment_id_seq'::regclass);


--
-- Name: common_comment_files id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.common_comment_files ALTER COLUMN id SET DEFAULT nextval('public.common_comment_files_id_seq'::regclass);


--
-- Name: common_document id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.common_document ALTER COLUMN id SET DEFAULT nextval('public.common_document_id_seq'::regclass);


--
-- Name: common_document_shared_to id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.common_document_shared_to ALTER COLUMN id SET DEFAULT nextval('public.common_document_shared_to_id_seq'::regclass);


--
-- Name: common_document_teams id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.common_document_teams ALTER COLUMN id SET DEFAULT nextval('public.common_document_teams_id_seq'::regclass);


--
-- Name: common_google id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.common_google ALTER COLUMN id SET DEFAULT nextval('public.common_google_id_seq'::regclass);


--
-- Name: common_profile id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.common_profile ALTER COLUMN id SET DEFAULT nextval('public.common_profile_id_seq'::regclass);


--
-- Name: common_user id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.common_user ALTER COLUMN id SET DEFAULT nextval('public.common_user_id_seq'::regclass);


--
-- Name: common_user_groups id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.common_user_groups ALTER COLUMN id SET DEFAULT nextval('public.common_user_groups_id_seq'::regclass);


--
-- Name: common_user_user_permissions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.common_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('public.common_user_user_permissions_id_seq'::regclass);


--
-- Name: companies_chargingstages id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.companies_chargingstages ALTER COLUMN id SET DEFAULT nextval('public.companies_chargingstages_id_seq'::regclass);


--
-- Name: companies_company id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.companies_company ALTER COLUMN id SET DEFAULT nextval('public.companies_company_id_seq'::regclass);


--
-- Name: companies_company_tags id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.companies_company_tags ALTER COLUMN id SET DEFAULT nextval('public.companies_company_tags_id_seq'::regclass);


--
-- Name: companies_documentformat id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.companies_documentformat ALTER COLUMN id SET DEFAULT nextval('public.companies_documentformat_id_seq'::regclass);


--
-- Name: companies_documentheaderinformation id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.companies_documentheaderinformation ALTER COLUMN id SET DEFAULT nextval('public.companies_documentheaderinformation_id_seq'::regclass);


--
-- Name: companies_email id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.companies_email ALTER COLUMN id SET DEFAULT nextval('public.companies_email_id_seq'::regclass);


--
-- Name: companies_email_recipients id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.companies_email_recipients ALTER COLUMN id SET DEFAULT nextval('public.companies_email_recipients_id_seq'::regclass);


--
-- Name: companies_emaillog id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.companies_emaillog ALTER COLUMN id SET DEFAULT nextval('public.companies_emaillog_id_seq'::regclass);


--
-- Name: companies_invoicegeneralremark id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.companies_invoicegeneralremark ALTER COLUMN id SET DEFAULT nextval('public.companies_invoicegeneralremark_id_seq'::regclass);


--
-- Name: companies_quotationgeneralremark id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.companies_quotationgeneralremark ALTER COLUMN id SET DEFAULT nextval('public.companies_quotationgeneralremark_id_seq'::regclass);


--
-- Name: companies_receiptgeneralremark id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.companies_receiptgeneralremark ALTER COLUMN id SET DEFAULT nextval('public.companies_receiptgeneralremark_id_seq'::regclass);


--
-- Name: companies_tags id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.companies_tags ALTER COLUMN id SET DEFAULT nextval('public.companies_tags_id_seq'::regclass);


--
-- Name: contacts_contact id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contacts_contact ALTER COLUMN id SET DEFAULT nextval('public.contacts_contact_id_seq'::regclass);


--
-- Name: contacts_contact_assigned_to id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contacts_contact_assigned_to ALTER COLUMN id SET DEFAULT nextval('public.contacts_contact_assigned_to_id_seq'::regclass);


--
-- Name: contacts_contact_teams id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contacts_contact_teams ALTER COLUMN id SET DEFAULT nextval('public.contacts_contact_teams_id_seq'::regclass);


--
-- Name: customers_customer id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.customers_customer ALTER COLUMN id SET DEFAULT nextval('public.customers_customer_id_seq'::regclass);


--
-- Name: django_admin_log id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log ALTER COLUMN id SET DEFAULT nextval('public.django_admin_log_id_seq'::regclass);


--
-- Name: django_content_type id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type ALTER COLUMN id SET DEFAULT nextval('public.django_content_type_id_seq'::regclass);


--
-- Name: django_migrations id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_migrations ALTER COLUMN id SET DEFAULT nextval('public.django_migrations_id_seq'::regclass);


--
-- Name: emails_email id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.emails_email ALTER COLUMN id SET DEFAULT nextval('public.emails_email_id_seq'::regclass);


--
-- Name: events_event id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.events_event ALTER COLUMN id SET DEFAULT nextval('public.events_event_id_seq'::regclass);


--
-- Name: events_event_assigned_to id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.events_event_assigned_to ALTER COLUMN id SET DEFAULT nextval('public.events_event_assigned_to_id_seq'::regclass);


--
-- Name: events_event_contacts id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.events_event_contacts ALTER COLUMN id SET DEFAULT nextval('public.events_event_contacts_id_seq'::regclass);


--
-- Name: events_event_teams id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.events_event_teams ALTER COLUMN id SET DEFAULT nextval('public.events_event_teams_id_seq'::regclass);


--
-- Name: function_items_functionitem id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.function_items_functionitem ALTER COLUMN id SET DEFAULT nextval('public.function_items_functionitem_id_seq'::regclass);


--
-- Name: function_items_functionitemhistory id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.function_items_functionitemhistory ALTER COLUMN id SET DEFAULT nextval('public.function_items_functionitemhistory_id_seq'::regclass);


--
-- Name: function_items_subfunctionitem id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.function_items_subfunctionitem ALTER COLUMN id SET DEFAULT nextval('public.function_items_subfunctionitem_id_seq'::regclass);


--
-- Name: function_items_subfunctionitemhistory id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.function_items_subfunctionitemhistory ALTER COLUMN id SET DEFAULT nextval('public.function_items_subfunctionitemhistory_id_seq'::regclass);


--
-- Name: invoices_invoice id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.invoices_invoice ALTER COLUMN id SET DEFAULT nextval('public.invoices_invoice_id_seq'::regclass);


--
-- Name: invoices_invoice_assigned_to id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.invoices_invoice_assigned_to ALTER COLUMN id SET DEFAULT nextval('public.invoices_invoice_assigned_to_id_seq'::regclass);


--
-- Name: invoices_invoice_companies id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.invoices_invoice_companies ALTER COLUMN id SET DEFAULT nextval('public.invoices_invoice_companies_id_seq'::regclass);


--
-- Name: invoices_invoice_teams id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.invoices_invoice_teams ALTER COLUMN id SET DEFAULT nextval('public.invoices_invoice_teams_id_seq'::regclass);


--
-- Name: invoices_invoicehistory id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.invoices_invoicehistory ALTER COLUMN id SET DEFAULT nextval('public.invoices_invoicehistory_id_seq'::regclass);


--
-- Name: invoices_invoicehistory_assigned_to id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.invoices_invoicehistory_assigned_to ALTER COLUMN id SET DEFAULT nextval('public.invoices_invoicehistory_assigned_to_id_seq'::regclass);


--
-- Name: leads_lead id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.leads_lead ALTER COLUMN id SET DEFAULT nextval('public.leads_lead_id_seq'::regclass);


--
-- Name: leads_lead_assigned_to id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.leads_lead_assigned_to ALTER COLUMN id SET DEFAULT nextval('public.leads_lead_assigned_to_id_seq'::regclass);


--
-- Name: leads_lead_contacts id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.leads_lead_contacts ALTER COLUMN id SET DEFAULT nextval('public.leads_lead_contacts_id_seq'::regclass);


--
-- Name: leads_lead_teams id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.leads_lead_teams ALTER COLUMN id SET DEFAULT nextval('public.leads_lead_teams_id_seq'::regclass);


--
-- Name: marketing_blockeddomain id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_blockeddomain ALTER COLUMN id SET DEFAULT nextval('public.marketing_blockeddomain_id_seq'::regclass);


--
-- Name: marketing_blockedemail id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_blockedemail ALTER COLUMN id SET DEFAULT nextval('public.marketing_blockedemail_id_seq'::regclass);


--
-- Name: marketing_campaign id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_campaign ALTER COLUMN id SET DEFAULT nextval('public.marketing_campaign_id_seq'::regclass);


--
-- Name: marketing_campaign_contact_lists id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_campaign_contact_lists ALTER COLUMN id SET DEFAULT nextval('public.marketing_campaign_contact_lists_id_seq'::regclass);


--
-- Name: marketing_campaign_tags id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_campaign_tags ALTER COLUMN id SET DEFAULT nextval('public.marketing_campaign_tags_id_seq'::regclass);


--
-- Name: marketing_campaigncompleted id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_campaigncompleted ALTER COLUMN id SET DEFAULT nextval('public.marketing_campaigncompleted_id_seq'::regclass);


--
-- Name: marketing_campaignlinkclick id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_campaignlinkclick ALTER COLUMN id SET DEFAULT nextval('public.marketing_campaignlinkclick_id_seq'::regclass);


--
-- Name: marketing_campaignlog id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_campaignlog ALTER COLUMN id SET DEFAULT nextval('public.marketing_campaignlog_id_seq'::regclass);


--
-- Name: marketing_campaignopen id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_campaignopen ALTER COLUMN id SET DEFAULT nextval('public.marketing_campaignopen_id_seq'::regclass);


--
-- Name: marketing_contact id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_contact ALTER COLUMN id SET DEFAULT nextval('public.marketing_contact_id_seq'::regclass);


--
-- Name: marketing_contact_contact_list id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_contact_contact_list ALTER COLUMN id SET DEFAULT nextval('public.marketing_contact_contact_list_id_seq'::regclass);


--
-- Name: marketing_contactemailcampaign id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_contactemailcampaign ALTER COLUMN id SET DEFAULT nextval('public.marketing_contactemailcampaign_id_seq'::regclass);


--
-- Name: marketing_contactlist id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_contactlist ALTER COLUMN id SET DEFAULT nextval('public.marketing_contactlist_id_seq'::regclass);


--
-- Name: marketing_contactlist_tags id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_contactlist_tags ALTER COLUMN id SET DEFAULT nextval('public.marketing_contactlist_tags_id_seq'::regclass);


--
-- Name: marketing_contactlist_visible_to id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_contactlist_visible_to ALTER COLUMN id SET DEFAULT nextval('public.marketing_contactlist_visible_to_id_seq'::regclass);


--
-- Name: marketing_contactunsubscribedcampaign id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_contactunsubscribedcampaign ALTER COLUMN id SET DEFAULT nextval('public.marketing_contactunsubscribedcampaign_id_seq'::regclass);


--
-- Name: marketing_duplicatecontacts id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_duplicatecontacts ALTER COLUMN id SET DEFAULT nextval('public.marketing_duplicatecontacts_id_seq'::regclass);


--
-- Name: marketing_emailtemplate id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_emailtemplate ALTER COLUMN id SET DEFAULT nextval('public.marketing_emailtemplate_id_seq'::regclass);


--
-- Name: marketing_failedcontact id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_failedcontact ALTER COLUMN id SET DEFAULT nextval('public.marketing_failedcontact_id_seq'::regclass);


--
-- Name: marketing_failedcontact_contact_list id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_failedcontact_contact_list ALTER COLUMN id SET DEFAULT nextval('public.marketing_failedcontact_contact_list_id_seq'::regclass);


--
-- Name: marketing_link id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_link ALTER COLUMN id SET DEFAULT nextval('public.marketing_link_id_seq'::regclass);


--
-- Name: marketing_tag id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_tag ALTER COLUMN id SET DEFAULT nextval('public.marketing_tag_id_seq'::regclass);


--
-- Name: opportunity_opportunity id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.opportunity_opportunity ALTER COLUMN id SET DEFAULT nextval('public.opportunity_opportunity_id_seq'::regclass);


--
-- Name: opportunity_opportunity_assigned_to id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.opportunity_opportunity_assigned_to ALTER COLUMN id SET DEFAULT nextval('public.opportunity_opportunity_assigned_to_id_seq'::regclass);


--
-- Name: opportunity_opportunity_contacts id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.opportunity_opportunity_contacts ALTER COLUMN id SET DEFAULT nextval('public.opportunity_opportunity_contacts_id_seq'::regclass);


--
-- Name: opportunity_opportunity_tags id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.opportunity_opportunity_tags ALTER COLUMN id SET DEFAULT nextval('public.opportunity_opportunity_tags_id_seq'::regclass);


--
-- Name: opportunity_opportunity_teams id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.opportunity_opportunity_teams ALTER COLUMN id SET DEFAULT nextval('public.opportunity_opportunity_teams_id_seq'::regclass);


--
-- Name: planner_event id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.planner_event ALTER COLUMN id SET DEFAULT nextval('public.planner_event_id_seq'::regclass);


--
-- Name: planner_event_assigned_to id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.planner_event_assigned_to ALTER COLUMN id SET DEFAULT nextval('public.planner_event_assigned_to_id_seq'::regclass);


--
-- Name: planner_event_attendees_contacts id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.planner_event_attendees_contacts ALTER COLUMN id SET DEFAULT nextval('public.planner_event_attendees_contacts_id_seq'::regclass);


--
-- Name: planner_event_attendees_leads id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.planner_event_attendees_leads ALTER COLUMN id SET DEFAULT nextval('public.planner_event_attendees_leads_id_seq'::regclass);


--
-- Name: planner_event_attendees_user id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.planner_event_attendees_user ALTER COLUMN id SET DEFAULT nextval('public.planner_event_attendees_user_id_seq'::regclass);


--
-- Name: planner_event_reminders id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.planner_event_reminders ALTER COLUMN id SET DEFAULT nextval('public.planner_event_reminders_id_seq'::regclass);


--
-- Name: planner_reminder id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.planner_reminder ALTER COLUMN id SET DEFAULT nextval('public.planner_reminder_id_seq'::regclass);


--
-- Name: project_expenses_expensetype id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.project_expenses_expensetype ALTER COLUMN id SET DEFAULT nextval('public.project_expenses_expendtype_id_seq'::regclass);


--
-- Name: project_expenses_projectexpense id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.project_expenses_projectexpense ALTER COLUMN id SET DEFAULT nextval('public.project_expenses_projectexpend_id_seq'::regclass);


--
-- Name: project_items_item id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.project_items_item ALTER COLUMN id SET DEFAULT nextval('public.project_items_item_id_seq'::regclass);


--
-- Name: project_items_item_item_properties id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.project_items_item_item_properties ALTER COLUMN id SET DEFAULT nextval('public.project_items_item_item_properties_id_seq'::regclass);


--
-- Name: project_items_itemformula id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.project_items_itemformula ALTER COLUMN id SET DEFAULT nextval('public.project_items_itemformula_id_seq'::regclass);


--
-- Name: project_items_itemproperty id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.project_items_itemproperty ALTER COLUMN id SET DEFAULT nextval('public.project_items_itemproperty_id_seq'::regclass);


--
-- Name: project_items_itemtype id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.project_items_itemtype ALTER COLUMN id SET DEFAULT nextval('public.project_items_itemtype_id_seq'::regclass);


--
-- Name: project_items_itemtypematerial id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.project_items_itemtypematerial ALTER COLUMN id SET DEFAULT nextval('public.project_items_itemtypematerial_id_seq'::regclass);


--
-- Name: project_misc_misc id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.project_misc_misc ALTER COLUMN id SET DEFAULT nextval('public.project_misc_misc_id_seq'::regclass);


--
-- Name: project_misc_projectmisc id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.project_misc_projectmisc ALTER COLUMN id SET DEFAULT nextval('public.project_misc_projectmisc_id_seq'::regclass);


--
-- Name: project_timetable_projectmilestone id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.project_timetable_projectmilestone ALTER COLUMN id SET DEFAULT nextval('public.project_timetable_projectmilestone_id_seq'::regclass);


--
-- Name: project_timetable_projectwork id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.project_timetable_projectwork ALTER COLUMN id SET DEFAULT nextval('public.project_timetable_projectwork_id_seq'::regclass);


--
-- Name: projects_companyprojectcomparison id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects_companyprojectcomparison ALTER COLUMN id SET DEFAULT nextval('public.projects_companyprojectcomparison_id_seq'::regclass);


--
-- Name: projects_companyprojectcomparison_projects id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects_companyprojectcomparison_projects ALTER COLUMN id SET DEFAULT nextval('public.projects_companyprojectcomparison_projects_id_seq'::regclass);


--
-- Name: projects_project id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects_project ALTER COLUMN id SET DEFAULT nextval('public.projects_project_id_seq'::regclass);


--
-- Name: projects_projecthistory id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects_projecthistory ALTER COLUMN id SET DEFAULT nextval('public.projects_projecthistory_id_seq'::regclass);


--
-- Name: projects_projecthistory_assigned_to id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects_projecthistory_assigned_to ALTER COLUMN id SET DEFAULT nextval('public.projects_projecthistory_assigned_to_id_seq'::regclass);


--
-- Name: projects_projectimage id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects_projectimage ALTER COLUMN id SET DEFAULT nextval('public.projects_projectimage_id_seq'::regclass);


--
-- Name: projects_projectimageset id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects_projectimageset ALTER COLUMN id SET DEFAULT nextval('public.projects_projectimageset_id_seq'::regclass);


--
-- Name: projects_projectimageset_imgs id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects_projectimageset_imgs ALTER COLUMN id SET DEFAULT nextval('public.projects_projectimageset_imgs_id_seq'::regclass);


--
-- Name: projects_projectinvoice id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects_projectinvoice ALTER COLUMN id SET DEFAULT nextval('public.projects_projectinvoice_id_seq'::regclass);


--
-- Name: projects_projectreceipt id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects_projectreceipt ALTER COLUMN id SET DEFAULT nextval('public.projects_projectreceipt_id_seq'::regclass);


--
-- Name: quotations_quotation id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.quotations_quotation ALTER COLUMN id SET DEFAULT nextval('public.quotations_quotation_id_seq'::regclass);


--
-- Name: quotations_quotation_assigned_to id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.quotations_quotation_assigned_to ALTER COLUMN id SET DEFAULT nextval('public.quotations_quotation_assigned_to_id_seq'::regclass);


--
-- Name: quotations_quotation_companies id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.quotations_quotation_companies ALTER COLUMN id SET DEFAULT nextval('public.quotations_quotation_companies_id_seq'::regclass);


--
-- Name: quotations_quotation_teams id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.quotations_quotation_teams ALTER COLUMN id SET DEFAULT nextval('public.quotations_quotation_teams_id_seq'::regclass);


--
-- Name: quotations_quotationhistory id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.quotations_quotationhistory ALTER COLUMN id SET DEFAULT nextval('public.quotations_quotationhistory_id_seq'::regclass);


--
-- Name: quotations_quotationhistory_assigned_to id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.quotations_quotationhistory_assigned_to ALTER COLUMN id SET DEFAULT nextval('public.quotations_quotationhistory_assigned_to_id_seq'::regclass);


--
-- Name: rooms_room id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rooms_room ALTER COLUMN id SET DEFAULT nextval('public.rooms_room_id_seq'::regclass);


--
-- Name: rooms_roomitem id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rooms_roomitem ALTER COLUMN id SET DEFAULT nextval('public.rooms_roomitem_id_seq'::regclass);


--
-- Name: rooms_roomproperty id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rooms_roomproperty ALTER COLUMN id SET DEFAULT nextval('public.rooms_roomproperty_id_seq'::regclass);


--
-- Name: rooms_roomtype id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rooms_roomtype ALTER COLUMN id SET DEFAULT nextval('public.rooms_roomtype_id_seq'::regclass);


--
-- Name: rooms_roomtype_related_items id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rooms_roomtype_related_items ALTER COLUMN id SET DEFAULT nextval('public.rooms_roomtype_related_items_id_seq'::regclass);


--
-- Name: rooms_roomtype_room_properties id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rooms_roomtype_room_properties ALTER COLUMN id SET DEFAULT nextval('public.rooms_roomtype_room_properties_id_seq'::regclass);


--
-- Name: rooms_roomtypeformula id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rooms_roomtypeformula ALTER COLUMN id SET DEFAULT nextval('public.rooms_roomtypeformula_id_seq'::regclass);


--
-- Name: subscription_plans_companysubscribedplan id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subscription_plans_companysubscribedplan ALTER COLUMN id SET DEFAULT nextval('public.subscription_plans_companysubscribedplan_id_seq'::regclass);


--
-- Name: subscription_plans_subscriptionplan id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subscription_plans_subscriptionplan ALTER COLUMN id SET DEFAULT nextval('public.subscription_plans_subscriptionplan_id_seq'::regclass);


--
-- Name: tasks_task id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tasks_task ALTER COLUMN id SET DEFAULT nextval('public.tasks_task_id_seq'::regclass);


--
-- Name: tasks_task_assigned_to id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tasks_task_assigned_to ALTER COLUMN id SET DEFAULT nextval('public.tasks_task_assigned_to_id_seq'::regclass);


--
-- Name: tasks_task_contacts id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tasks_task_contacts ALTER COLUMN id SET DEFAULT nextval('public.tasks_task_contacts_id_seq'::regclass);


--
-- Name: tasks_task_teams id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tasks_task_teams ALTER COLUMN id SET DEFAULT nextval('public.tasks_task_teams_id_seq'::regclass);


--
-- Name: teams_teams id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.teams_teams ALTER COLUMN id SET DEFAULT nextval('public.teams_teams_id_seq'::regclass);


--
-- Name: teams_teams_users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.teams_teams_users ALTER COLUMN id SET DEFAULT nextval('public.teams_teams_users_id_seq'::regclass);


--
-- Name: token_blacklist_blacklistedtoken id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.token_blacklist_blacklistedtoken ALTER COLUMN id SET DEFAULT nextval('public.token_blacklist_blacklistedtoken_id_seq'::regclass);


--
-- Name: token_blacklist_outstandingtoken id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.token_blacklist_outstandingtoken ALTER COLUMN id SET DEFAULT nextval('public.token_blacklist_outstandingtoken_id_seq'::regclass);


--
-- Data for Name: accounts_account; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.accounts_account (id, name, email, phone, industry, website, description, created_on, is_active, created_by_id, status, lead_id, billing_address_line, billing_city, billing_country, billing_postcode, billing_state, billing_street, contact_name) FROM stdin;
\.


--
-- Data for Name: accounts_account_assigned_to; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.accounts_account_assigned_to (id, account_id, user_id) FROM stdin;
\.


--
-- Data for Name: accounts_account_contacts; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.accounts_account_contacts (id, account_id, contact_id) FROM stdin;
\.


--
-- Data for Name: accounts_account_tags; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.accounts_account_tags (id, account_id, tags_id) FROM stdin;
\.


--
-- Data for Name: accounts_account_teams; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.accounts_account_teams (id, account_id, teams_id) FROM stdin;
\.


--
-- Data for Name: accounts_email; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.accounts_email (id, created_on, message_subject, message_body, from_account_id, from_email, rendered_message_body, scheduled_date_time, scheduled_later, timezone) FROM stdin;
\.


--
-- Data for Name: accounts_email_recipients; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.accounts_email_recipients (id, email_id, contact_id) FROM stdin;
\.


--
-- Data for Name: accounts_emaillog; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.accounts_emaillog (id, is_sent, contact_id, email_id) FROM stdin;
\.


--
-- Data for Name: accounts_tags; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.accounts_tags (id, name, slug) FROM stdin;
\.


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_group (id, name) FROM stdin;
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add permission	1	add_permission
2	Can change permission	1	change_permission
3	Can delete permission	1	delete_permission
4	Can view permission	1	view_permission
5	Can add group	2	add_group
6	Can change group	2	change_group
7	Can delete group	2	delete_group
8	Can view group	2	view_group
9	Can add content type	3	add_contenttype
10	Can change content type	3	change_contenttype
11	Can delete content type	3	delete_contenttype
12	Can view content type	3	view_contenttype
13	Can add session	4	add_session
14	Can change session	4	change_session
15	Can delete session	4	delete_session
16	Can view session	4	view_session
17	Can add user	5	add_user
18	Can change user	5	change_user
19	Can delete user	5	delete_user
20	Can view user	5	view_user
21	Can add address	6	add_address
22	Can change address	6	change_address
23	Can delete address	6	delete_address
24	Can view address	6	view_address
25	Can add attachments	7	add_attachments
26	Can change attachments	7	change_attachments
27	Can delete attachments	7	delete_attachments
28	Can view attachments	7	view_attachments
29	Can add comment	8	add_comment
30	Can change comment	8	change_comment
31	Can delete comment	8	delete_comment
32	Can view comment	8	view_comment
33	Can add comment_ files	9	add_comment_files
34	Can change comment_ files	9	change_comment_files
35	Can delete comment_ files	9	delete_comment_files
36	Can view comment_ files	9	view_comment_files
37	Can add document	10	add_document
38	Can change document	10	change_document
39	Can delete document	10	delete_document
40	Can view document	10	view_document
41	Can add google	11	add_google
42	Can change google	11	change_google
43	Can delete google	11	delete_google
44	Can view google	11	view_google
45	Can add api settings	12	add_apisettings
46	Can change api settings	12	change_apisettings
47	Can delete api settings	12	delete_apisettings
48	Can view api settings	12	view_apisettings
49	Can add profile	13	add_profile
50	Can change profile	13	change_profile
51	Can delete profile	13	delete_profile
52	Can view profile	13	view_profile
53	Can add account	14	add_account
54	Can change account	14	change_account
55	Can delete account	14	delete_account
56	Can view account	14	view_account
57	Can add tags	15	add_tags
58	Can change tags	15	change_tags
59	Can delete tags	15	delete_tags
60	Can view tags	15	view_tags
61	Can add email	16	add_email
62	Can change email	16	change_email
63	Can delete email	16	delete_email
64	Can view email	16	view_email
65	Can add email log	17	add_emaillog
66	Can change email log	17	change_emaillog
67	Can delete email log	17	delete_emaillog
68	Can view email log	17	view_emaillog
69	Can add case	18	add_case
70	Can change case	18	change_case
71	Can delete case	18	delete_case
72	Can view case	18	view_case
73	Can add contact	19	add_contact
74	Can change contact	19	change_contact
75	Can delete contact	19	delete_contact
76	Can view contact	19	view_contact
77	Can add email	20	add_email
78	Can change email	20	change_email
79	Can delete email	20	delete_email
80	Can view email	20	view_email
81	Can add lead	21	add_lead
82	Can change lead	21	change_lead
83	Can delete lead	21	delete_lead
84	Can view lead	21	view_lead
85	Can add opportunity	22	add_opportunity
86	Can change opportunity	22	change_opportunity
87	Can delete opportunity	22	delete_opportunity
88	Can view opportunity	22	view_opportunity
89	Can add event	23	add_event
90	Can change event	23	change_event
91	Can delete event	23	delete_event
92	Can view event	23	view_event
93	Can add reminder	24	add_reminder
94	Can change reminder	24	change_reminder
95	Can delete reminder	24	delete_reminder
96	Can view reminder	24	view_reminder
97	Can add kv store	25	add_kvstore
98	Can change kv store	25	change_kvstore
99	Can delete kv store	25	delete_kvstore
100	Can view kv store	25	view_kvstore
101	Can add campaign	26	add_campaign
102	Can change campaign	26	change_campaign
103	Can delete campaign	26	delete_campaign
104	Can view campaign	26	view_campaign
105	Can add campaign link click	27	add_campaignlinkclick
106	Can change campaign link click	27	change_campaignlinkclick
107	Can delete campaign link click	27	delete_campaignlinkclick
108	Can view campaign link click	27	view_campaignlinkclick
109	Can add campaign log	28	add_campaignlog
110	Can change campaign log	28	change_campaignlog
111	Can delete campaign log	28	delete_campaignlog
112	Can view campaign log	28	view_campaignlog
113	Can add campaign open	29	add_campaignopen
114	Can change campaign open	29	change_campaignopen
115	Can delete campaign open	29	delete_campaignopen
116	Can view campaign open	29	view_campaignopen
117	Can add contact	30	add_contact
118	Can change contact	30	change_contact
119	Can delete contact	30	delete_contact
120	Can view contact	30	view_contact
121	Can add contact list	31	add_contactlist
122	Can change contact list	31	change_contactlist
123	Can delete contact list	31	delete_contactlist
124	Can view contact list	31	view_contactlist
125	Can add email template	32	add_emailtemplate
126	Can change email template	32	change_emailtemplate
127	Can delete email template	32	delete_emailtemplate
128	Can view email template	32	view_emailtemplate
129	Can add link	33	add_link
130	Can change link	33	change_link
131	Can delete link	33	delete_link
132	Can view link	33	view_link
133	Can add tag	34	add_tag
134	Can change tag	34	change_tag
135	Can delete tag	34	delete_tag
136	Can view tag	34	view_tag
137	Can add failed contact	35	add_failedcontact
138	Can change failed contact	35	change_failedcontact
139	Can delete failed contact	35	delete_failedcontact
140	Can view failed contact	35	view_failedcontact
141	Can add campaign completed	36	add_campaigncompleted
142	Can change campaign completed	36	change_campaigncompleted
143	Can delete campaign completed	36	delete_campaigncompleted
144	Can view campaign completed	36	view_campaigncompleted
145	Can add contact unsubscribed campaign	37	add_contactunsubscribedcampaign
146	Can change contact unsubscribed campaign	37	change_contactunsubscribedcampaign
147	Can delete contact unsubscribed campaign	37	delete_contactunsubscribedcampaign
148	Can view contact unsubscribed campaign	37	view_contactunsubscribedcampaign
149	Can add contact email campaign	38	add_contactemailcampaign
150	Can change contact email campaign	38	change_contactemailcampaign
151	Can delete contact email campaign	38	delete_contactemailcampaign
152	Can view contact email campaign	38	view_contactemailcampaign
153	Can add duplicate contacts	39	add_duplicatecontacts
154	Can change duplicate contacts	39	change_duplicatecontacts
155	Can delete duplicate contacts	39	delete_duplicatecontacts
156	Can view duplicate contacts	39	view_duplicatecontacts
157	Can add blocked email	40	add_blockedemail
158	Can change blocked email	40	change_blockedemail
159	Can delete blocked email	40	delete_blockedemail
160	Can view blocked email	40	view_blockedemail
161	Can add blocked domain	41	add_blockeddomain
162	Can change blocked domain	41	change_blockeddomain
163	Can delete blocked domain	41	delete_blockeddomain
164	Can view blocked domain	41	view_blockeddomain
165	Can add task	42	add_task
166	Can change task	42	change_task
167	Can delete task	42	delete_task
168	Can view task	42	view_task
169	Can add Invoice	43	add_invoice
170	Can change Invoice	43	change_invoice
171	Can delete Invoice	43	delete_invoice
172	Can view Invoice	43	view_invoice
173	Can add invoice history	44	add_invoicehistory
174	Can change invoice history	44	change_invoicehistory
175	Can delete invoice history	44	delete_invoicehistory
176	Can view invoice history	44	view_invoicehistory
177	Can add event	45	add_event
178	Can change event	45	change_event
179	Can delete event	45	delete_event
180	Can view event	45	view_event
181	Can add teams	46	add_teams
182	Can change teams	46	change_teams
183	Can delete teams	46	delete_teams
184	Can view teams	46	view_teams
185	Can add log entry	47	add_logentry
186	Can change log entry	47	change_logentry
187	Can delete log entry	47	delete_logentry
188	Can view log entry	47	view_logentry
189	Can add blacklisted token	48	add_blacklistedtoken
190	Can change blacklisted token	48	change_blacklistedtoken
191	Can delete blacklisted token	48	delete_blacklistedtoken
192	Can view blacklisted token	48	view_blacklistedtoken
193	Can add outstanding token	49	add_outstandingtoken
194	Can change outstanding token	49	change_outstandingtoken
195	Can delete outstanding token	49	delete_outstandingtoken
196	Can view outstanding token	49	view_outstandingtoken
197	Can add Quotation	50	add_quotation
198	Can change Quotation	50	change_quotation
199	Can delete Quotation	50	delete_quotation
200	Can view Quotation	50	view_quotation
201	Can add quotation history	51	add_quotationhistory
202	Can change quotation history	51	change_quotationhistory
203	Can delete quotation history	51	delete_quotationhistory
204	Can view quotation history	51	view_quotationhistory
205	Can add Function Item	52	add_functionitem
206	Can change Function Item	52	change_functionitem
207	Can delete Function Item	52	delete_functionitem
208	Can view Function Item	52	view_functionitem
209	Can add function item history	53	add_functionitemhistory
210	Can change function item history	53	change_functionitemhistory
211	Can delete function item history	53	delete_functionitemhistory
212	Can view function item history	53	view_functionitemhistory
213	Can add Sub Function Item	54	add_subfunctionitem
214	Can change Sub Function Item	54	change_subfunctionitem
215	Can delete Sub Function Item	54	delete_subfunctionitem
216	Can view Sub Function Item	54	view_subfunctionitem
217	Can add sub function item history	55	add_subfunctionitemhistory
218	Can change sub function item history	55	change_subfunctionitemhistory
219	Can delete sub function item history	55	delete_subfunctionitemhistory
220	Can view sub function item history	55	view_subfunctionitemhistory
221	Can add company	56	add_company
222	Can change company	56	change_company
223	Can delete company	56	delete_company
224	Can view company	56	view_company
225	Can add email	57	add_email
226	Can change email	57	change_email
227	Can delete email	57	delete_email
228	Can view email	57	view_email
229	Can add tags	58	add_tags
230	Can change tags	58	change_tags
231	Can delete tags	58	delete_tags
232	Can view tags	58	view_tags
233	Can add general remark	59	add_generalremark
234	Can change general remark	59	change_generalremark
235	Can delete general remark	59	delete_generalremark
236	Can view general remark	59	view_generalremark
237	Can add email log	60	add_emaillog
238	Can change email log	60	change_emaillog
239	Can delete email log	60	delete_emaillog
240	Can view email log	60	view_emaillog
241	Can add document format	61	add_documentformat
242	Can change document format	61	change_documentformat
243	Can delete document format	61	delete_documentformat
244	Can view document format	61	view_documentformat
245	Can add charging stage	62	add_chargingstage
246	Can change charging stage	62	change_chargingstage
247	Can delete charging stage	62	delete_chargingstage
248	Can view charging stage	62	view_chargingstage
249	Can add Project	63	add_project
250	Can change Project	63	change_project
251	Can delete Project	63	delete_project
252	Can view Project	63	view_project
253	Can add project history	64	add_projecthistory
254	Can change project history	64	change_projecthistory
255	Can delete project history	64	delete_projecthistory
256	Can view project history	64	view_projecthistory
257	Can add room property	65	add_roomproperty
258	Can change room property	65	change_roomproperty
259	Can delete room property	65	delete_roomproperty
260	Can view room property	65	view_roomproperty
261	Can add room type	66	add_roomtype
262	Can change room type	66	change_roomtype
263	Can delete room type	66	delete_roomtype
264	Can view room type	66	view_roomtype
265	Can add room type formula	67	add_roomtypeformula
266	Can change room type formula	67	change_roomtypeformula
267	Can delete room type formula	67	delete_roomtypeformula
268	Can view room type formula	67	view_roomtypeformula
269	Can add room	68	add_room
270	Can change room	68	change_room
271	Can delete room	68	delete_room
272	Can view room	68	view_room
273	Can add room type property	69	add_roomtypeproperty
274	Can change room type property	69	change_roomtypeproperty
275	Can delete room type property	69	delete_roomtypeproperty
276	Can view room type property	69	view_roomtypeproperty
277	Can add customer	70	add_customer
278	Can change customer	70	change_customer
279	Can delete customer	70	delete_customer
280	Can view customer	70	view_customer
281	Can add Function Item	71	add_item
282	Can change Function Item	71	change_item
283	Can delete Function Item	71	delete_item
284	Can view Function Item	71	view_item
285	Can add Sub Function Item	72	add_projectitem
286	Can change Sub Function Item	72	change_projectitem
287	Can delete Sub Function Item	72	delete_projectitem
288	Can view Sub Function Item	72	view_projectitem
289	Can add room type properties	73	add_roomtypeproperties
290	Can change room type properties	73	change_roomtypeproperties
291	Can delete room type properties	73	delete_roomtypeproperties
292	Can view room type properties	73	view_roomtypeproperties
293	Can add Room Item	74	add_roomitem
294	Can change Room Item	74	change_roomitem
295	Can delete Room Item	74	delete_roomitem
296	Can view Room Item	74	view_roomitem
297	Can add item property	75	add_itemproperty
298	Can change item property	75	change_itemproperty
299	Can delete item property	75	delete_itemproperty
300	Can view item property	75	view_itemproperty
301	Can add item type	76	add_itemtype
302	Can change item type	76	change_itemtype
303	Can delete item type	76	delete_itemtype
304	Can view item type	76	view_itemtype
305	Can add item type material	77	add_itemtypematerial
306	Can change item type material	77	change_itemtypematerial
307	Can delete item type material	77	delete_itemtypematerial
308	Can view item type material	77	view_itemtypematerial
309	Can add charging stages	78	add_chargingstages
310	Can change charging stages	78	change_chargingstages
311	Can delete charging stages	78	delete_chargingstages
312	Can view charging stages	78	view_chargingstages
313	Can add project charging stages	79	add_projectchargingstages
314	Can change project charging stages	79	change_projectchargingstages
315	Can delete project charging stages	79	delete_projectchargingstages
316	Can view project charging stages	79	view_projectchargingstages
317	Can add item formula	80	add_itemformula
318	Can change item formula	80	change_itemformula
319	Can delete item formula	80	delete_itemformula
320	Can view item formula	80	view_itemformula
350	Can add Misc	113	add_misc
351	Can change Misc	113	change_misc
352	Can delete Misc	113	delete_misc
353	Can view Misc	113	view_misc
354	Can add misc type	114	add_misctype
355	Can change misc type	114	change_misctype
356	Can delete misc type	114	delete_misctype
357	Can view misc type	114	view_misctype
358	Can add Room Item	115	add_projectmisc
359	Can change Room Item	115	change_projectmisc
360	Can delete Room Item	115	delete_projectmisc
361	Can view Room Item	115	view_projectmisc
362	Can add expend type	116	add_expendtype
363	Can change expend type	116	change_expendtype
364	Can delete expend type	116	delete_expendtype
365	Can view expend type	116	view_expendtype
366	Can add project expend	117	add_projectexpend
367	Can change project expend	117	change_projectexpend
368	Can delete project expend	117	delete_projectexpend
369	Can view project expend	117	view_projectexpend
395	Can add Project Misc	149	add_projectmisc
396	Can change Project Misc	149	change_projectmisc
397	Can delete Project Misc	149	delete_projectmisc
398	Can view Project Misc	149	view_projectmisc
399	Can add Misc	150	add_misc
400	Can change Misc	150	change_misc
401	Can delete Misc	150	delete_misc
402	Can view Misc	150	view_misc
403	Can add project expend	151	add_projectexpend
404	Can change project expend	151	change_projectexpend
405	Can delete project expend	151	delete_projectexpend
406	Can view project expend	151	view_projectexpend
407	Can add expend type	152	add_expendtype
408	Can change expend type	152	change_expendtype
409	Can delete expend type	152	delete_expendtype
410	Can view expend type	152	view_expendtype
411	Can add expense type	152	add_expensetype
412	Can change expense type	152	change_expensetype
413	Can delete expense type	152	delete_expensetype
414	Can view expense type	152	view_expensetype
415	Can add project expense	151	add_projectexpense
416	Can change project expense	151	change_projectexpense
417	Can delete project expense	151	delete_projectexpense
418	Can view project expense	151	view_projectexpense
419	Can add project mile stone	153	add_projectmilestone
420	Can change project mile stone	153	change_projectmilestone
421	Can delete project mile stone	153	delete_projectmilestone
422	Can view project mile stone	153	view_projectmilestone
423	Can add project work	154	add_projectwork
424	Can change project work	154	change_projectwork
425	Can delete project work	154	delete_projectwork
426	Can view project work	154	view_projectwork
427	Can add document header information	155	add_documentheaderinformation
428	Can change document header information	155	change_documentheaderinformation
429	Can delete document header information	155	delete_documentheaderinformation
430	Can view document header information	155	view_documentheaderinformation
431	Can add invoice general remark	156	add_invoicegeneralremark
432	Can change invoice general remark	156	change_invoicegeneralremark
433	Can delete invoice general remark	156	delete_invoicegeneralremark
434	Can view invoice general remark	156	view_invoicegeneralremark
435	Can add quotation general remark	157	add_quotationgeneralremark
436	Can change quotation general remark	157	change_quotationgeneralremark
437	Can delete quotation general remark	157	delete_quotationgeneralremark
438	Can view quotation general remark	157	view_quotationgeneralremark
439	Can add receipt general remark	158	add_receiptgeneralremark
440	Can change receipt general remark	158	change_receiptgeneralremark
441	Can delete receipt general remark	158	delete_receiptgeneralremark
442	Can view receipt general remark	158	view_receiptgeneralremark
443	Can add project invoice	159	add_projectinvoice
444	Can change project invoice	159	change_projectinvoice
445	Can delete project invoice	159	delete_projectinvoice
446	Can view project invoice	159	view_projectinvoice
447	Can add project receipt	160	add_projectreceipt
448	Can change project receipt	160	change_projectreceipt
449	Can delete project receipt	160	delete_projectreceipt
450	Can view project receipt	160	view_projectreceipt
451	Can add project comparisons	161	add_projectcomparisons
452	Can change project comparisons	161	change_projectcomparisons
453	Can delete project comparisons	161	delete_projectcomparisons
454	Can view project comparisons	161	view_projectcomparisons
455	Can add project comparison	162	add_projectcomparison
456	Can change project comparison	162	change_projectcomparison
457	Can delete project comparison	162	delete_projectcomparison
458	Can view project comparison	162	view_projectcomparison
459	Can add company project comparison	163	add_companyprojectcomparison
460	Can change company project comparison	163	change_companyprojectcomparison
461	Can delete company project comparison	163	delete_companyprojectcomparison
462	Can view company project comparison	163	view_companyprojectcomparison
463	Can add company subscribed plan	164	add_companysubscribedplan
464	Can change company subscribed plan	164	change_companysubscribedplan
465	Can delete company subscribed plan	164	delete_companysubscribedplan
466	Can view company subscribed plan	164	view_companysubscribedplan
467	Can add subscription plan	165	add_subscriptionplan
468	Can change subscription plan	165	change_subscriptionplan
469	Can delete subscription plan	165	delete_subscriptionplan
470	Can view subscription plan	165	view_subscriptionplan
471	Can add project image set	166	add_projectimageset
472	Can change project image set	166	change_projectimageset
473	Can delete project image set	166	delete_projectimageset
474	Can view project image set	166	view_projectimageset
475	Can add project image	167	add_projectimage
476	Can change project image	167	change_projectimage
477	Can delete project image	167	delete_projectimage
478	Can view project image	167	view_projectimage
\.


--
-- Data for Name: cases_case; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.cases_case (id, name, status, priority, case_type, closed_on, description, created_on, is_active, created_by_id, company_id) FROM stdin;
\.


--
-- Data for Name: cases_case_assigned_to; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.cases_case_assigned_to (id, case_id, user_id) FROM stdin;
\.


--
-- Data for Name: cases_case_contacts; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.cases_case_contacts (id, case_id, contact_id) FROM stdin;
\.


--
-- Data for Name: cases_case_teams; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.cases_case_teams (id, case_id, teams_id) FROM stdin;
\.


--
-- Data for Name: common_address; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.common_address (id, address_line, street, city, state, postcode, country, lat, lng) FROM stdin;
\.


--
-- Data for Name: common_apisettings; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.common_apisettings (id, title, apikey, created_on, created_by_id, website) FROM stdin;
\.


--
-- Data for Name: common_apisettings_lead_assigned_to; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.common_apisettings_lead_assigned_to (id, apisettings_id, user_id) FROM stdin;
\.


--
-- Data for Name: common_apisettings_tags; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.common_apisettings_tags (id, apisettings_id, tags_id) FROM stdin;
\.


--
-- Data for Name: common_attachments; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.common_attachments (id, file_name, created_on, attachment, account_id, contact_id, created_by_id, lead_id, opportunity_id, case_id, task_id, event_id, quotation_id, company_id) FROM stdin;
\.


--
-- Data for Name: common_comment; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.common_comment (id, comment, commented_on, account_id, case_id, commented_by_id, contact_id, lead_id, opportunity_id, user_id, task_id, event_id, quotation_id, company_id) FROM stdin;
\.


--
-- Data for Name: common_comment_files; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.common_comment_files (id, updated_on, comment_file, comment_id) FROM stdin;
\.


--
-- Data for Name: common_document; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.common_document (id, title, document_file, created_on, created_by_id, status) FROM stdin;
\.


--
-- Data for Name: common_document_shared_to; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.common_document_shared_to (id, document_id, user_id) FROM stdin;
\.


--
-- Data for Name: common_document_teams; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.common_document_teams (id, document_id, teams_id) FROM stdin;
\.


--
-- Data for Name: common_google; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.common_google (id, google_id, google_url, verified_email, family_name, name, gender, dob, given_name, email, user_id) FROM stdin;
\.


--
-- Data for Name: common_profile; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.common_profile (id, activation_key, key_expires, user_id) FROM stdin;
\.


--
-- Data for Name: common_user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.common_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_active, is_admin, is_staff, date_joined, role, profile_pic, has_marketing_access, has_sales_access, phone, phone_verify, verify_code, display_name, login_token, need_login_verify, new_phone, new_phone_verify_code) FROM stdin;
23	pbkdf2_sha256$150000$vnWkXMVAXyzZ$Uhyy9ESJOgHsTbmtf+COWPQQ6HJZHfu2lCCuiP0+xDw=	\N	f	+85291322902				t	f	f	2020-09-13 11:36:03.152598+00	USER		f	f	+85291322902	t	000000	Joe Lam	cZkLaRXxYfrM	f	\N	\N
18	pbkdf2_sha256$150000$17zFNirKdM83$s9pnm7VUnz6nVnwFpE+khlDbt9HSJDiO5p3DOuplDSQ=	\N	f	+85290654321				t	f	f	2020-09-06 07:52:41.909785+00	USER		f	f	+85290654321	t	000000	tester002	71z4dfCBzumE	f	\N	\N
1	pbkdf2_sha256$150000$ZOpNZ6JdiHOY$sDx81k5cSwObglY/ld5JLifC3O42shD4KdDM/dO2aUA=	2021-03-04 08:04:58.864075+00	t	Kingson Wan			kingsonwan@vidarstudio.com	t	f	t	2020-06-22 07:56:16.511092+00			f	f		f			aaaaaaaaaaaa	f	\N	\N
19	pbkdf2_sha256$150000$m9r96cJglJkq$795JbQd0yYUxgEsDLHaEt8R1/ZCo7LiaQXWu0OGFRzY=	\N	f	+85267403399				t	f	f	2020-09-06 12:45:57.730034+00	USER		f	f	+85267403399	t	000000	tester 99	aI1UZM44YTfF	f	\N	\N
24	pbkdf2_sha256$150000$U2bmCh6fU0uO$5QVYuducDkHm9I5zo6lSb623/MAOycp7mFYpwGtRAus=	\N	f	+85290123456				t	f	f	2020-09-13 12:21:44.185491+00	USER		f	f	+85290123456	t	000000	ABC Testing2	oyhAnPh9jOF7	f	\N	\N
37	pbkdf2_sha256$150000$zbMF0tTC0E3J$3va6d6A6QsPSNzRjECl4JIRSXK2whmx7Z2Mh2DeT2ng=	\N	f	+85267403305				t	f	f	2020-10-25 06:12:26.779415+00	USER		f	f	+85267403305	t	000000	fat cat	XkfIqjfVPtoX	f	\N	\N
28	pbkdf2_sha256$150000$QJG0yd1qcF4Y$Cjl4qMkiAJEi0RcY/87g9ahsEfIBJQQAdsrkO8svo3c=	\N	f	+85291234567				t	f	f	2020-09-13 12:49:03.315497+00	USER		f	f	+85291234567	t	000000	abc	FmcfNwK8xNtf	f	\N	\N
25	pbkdf2_sha256$150000$JXfBBSaXYFi4$HVxCNrfaYM50pR0AC9gy/ntvwjm5ezW7FYVG/I6B4uQ=	\N	f	+85297561195				t	f	f	2020-09-13 12:23:05.269092+00	USER		f	f	+85297561195	t	000000		tiMOUyjl1kFG	t	\N	\N
9	pbkdf2_sha256$150000$RcovjnEEbP1V$BM7jnSR6V59jq7BPxn0VVkX8IYh07mvpHdwKeSVGt+Y=	\N	t	Calvin Sung			calvinsung@vidarstudio.com	t	f	t	2020-06-22 08:38:28.716392+00			f	f	\N	f			aaaaaaaaaaaa	f	\N	\N
43	pbkdf2_sha256$150000$OKjGrED9t69b$7D+Io+sX1NBKvXRqnzhn1thMgP4+FwDYkVhoMvx2Uqs=	\N	f	+85290622891				t	f	f	2020-12-04 15:32:16.322825+00	USER		f	f	+85290622891	t	000000	小朋友	CBqB73hcgVWv	f	\N	\N
40	pbkdf2_sha256$150000$RmpwlO8jClaG$WtkiqfZmxcdxSNiDfRcT5pMQwu2IEn0319auelbYi2k=	2021-02-23 01:15:25.924698+00	f	Interiumdesign			info@interiumdesign.com	t	f	f	2020-11-02 08:04:19.393456+00	ADMIN		f	f	\N	f				f	\N	\N
70	pbkdf2_sha256$150000$E3F3Daz25TyA$AxA1JIQWKZ1/QjW3GoMI5dc/Q9A3aw4jAY/6Mi5G6ZI=	\N	f	+85297331493				t	f	f	2021-02-15 09:26:38.230504+00	USER		f	f	+85297331493	t	000000	a	Z1qf8bIHbf98	f	\N	\N
27	pbkdf2_sha256$150000$BSI5go6fdvv6$NrzKqrlznJZqlKuzYw/vikHcaXg7C0Y5egYCgYS7DU4=	\N	f	+85297654321				t	f	f	2020-09-13 12:32:11.724633+00	USER		f	f	+85297654321	f	000000		5N7Y8gs7554H	t	\N	\N
35	pbkdf2_sha256$150000$1hxq8fKV5fv6$z5teGVSQZBvcusQ5wZ+diZKn5sjBeOiByb1n9LvVv24=	\N	f	+85291322905				t	f	f	2020-09-27 13:33:47.79256+00	USER		f	f	+85291322905	f	000000		5UV9FclkNtdu	t	\N	\N
12	pbkdf2_sha256$150000$MlcV9499TnPS$z/d+X8ZRfmqpj8HYFtgOR5ivye/QIgensYmL8TIpUh0=	\N	f	+85291234568				t	f	f	2020-09-03 08:30:12.573576+00	USER		f	f	+85291234568	t	000000		VnB14HChFtQJ	f	\N	\N
21	pbkdf2_sha256$150000$qWtCX00lHkWR$OnqcIsu/M0VbRK4MBNn30Mx/Zsh4S0m5FoWoirhUI6E=	\N	f	+85264403385				t	f	f	2020-09-09 06:33:08.610963+00	USER		f	f	+85264403385	t	000000		scbGHBybuJyt	f	\N	\N
36	pbkdf2_sha256$150000$II4maWFVqgH7$ShxT5ThJjpBpEt7CbvH1GhfzBQ+vQM06RBO55PLlEC0=	\N	f	+85267408888				t	f	f	2020-10-23 10:09:56.59019+00	USER		f	f	+85267408888	t	000000	tester 1	C3LpSoMhYxNj	f	\N	\N
29	pbkdf2_sha256$150000$nH3ZKbLtmZ5s$Wz4YOAME1O7AtMpmh7jfw3NHbey7+u4knfGuoFozDt4=	\N	f	+85290622091				t	f	f	2020-09-13 13:14:01.262873+00	USER		f	f	+85290622091	f	000000		5NNTgOoDwjYO	t	\N	\N
31	pbkdf2_sha256$150000$0uDNi3Jhcbvf$AY4TjSCiH/4t4+aV0eux04fgDXchXq8MpwRsG07zbHk=	\N	f	+85267405555				t	f	f	2020-09-13 13:41:09.635796+00	USER		f	f	+85267405555	t	000000		bWVsRmKQY8CU	f	\N	\N
5	pbkdf2_sha256$150000$mJfrpbcaVKfg$KT07vebMOahyqJ3iCNp2ROIZ3X11bJKJz87FkjH0Jww=	\N	f	+85290123458			\N	t	f	f	2020-06-22 08:23:42.014365+00	USER		f	f	+85290123458	t	000000	Testing ABC	MQkKCpHSCHnr	f	\N	\N
34	pbkdf2_sha256$150000$U0cuQSyqTLlt$nipv1b72eI5RuegSEI3sOK0MKguvlKAjW1kXEN1nR9U=	\N	f	+85290621111				t	f	f	2020-09-22 09:41:47.974864+00	USER		f	f	+85290621111	t	000000	tester 3	YYmGp81dSVvO	f	\N	\N
32	pbkdf2_sha256$150000$DZncvVl6fzP6$LAFsOXagrCBDrF+rOpKmwnZ8WEHbc4L+aA/7hQqmULo=	\N	f	+85267401111				t	f	f	2020-09-13 13:41:28.499316+00	USER		f	f	+85267401111	t	000000	tester2	m7iwlkYZnA3L	f	\N	\N
14	pbkdf2_sha256$150000$3GIUQnj5EZch$D3vuSwHAhBIkgeoAg0sKnluyzF7WVbNfLoa+S4Mh/bI=	2020-09-09 09:45:51+00	f	admin			test@test.com	t	f	f	2020-09-04 17:50:34.59887+00	ADMIN		f	f	+85230624700	f			000000	f	\N	\N
38	pbkdf2_sha256$150000$6I1Qw65uS9TS$sIbYH8Dyr9dRZJMAyT5izSfup6A+gh2nyIxQQl0e66k=	\N	f	+85267402222				t	f	f	2020-10-27 03:36:44.103109+00	USER		f	f	+85267402222	t	000000	tester 2	DiPPSKEep7Xe	f	\N	\N
26	pbkdf2_sha256$150000$oZcb861KVFNL$uTIM4Xsnl5Yf0OyDhNXkkSelxba5Q0BwsWCDAc7YEtE=	\N	f	+85290789456				t	f	f	2020-09-13 12:27:36.26208+00	USER		f	f	+85290789456	f	000000		0upAkpgp66gL	t	\N	\N
11	pbkdf2_sha256$150000$cmZBJ3ooVvge$wzBrHvEon09jArn4Skp2QPATU45Vnk7dQwPtmWxUNKg=	\N	f	+85267403385				t	f	f	2020-09-02 15:53:57.651511+00	USER		f	f	+85267403385	t	000000	Fat Cat	gEfx3vhX8ely	f	\N	\N
22	pbkdf2_sha256$150000$g5RojCBnQOoC$xg8FK8V1k/6Z0uIpoCfhQJHvKzsYjXiGYfq60ytZc1I=	\N	f	+85290123789				t	f	f	2020-09-10 04:36:25.677732+00	USER		f	f	+85290123789	t	000000	fatdog	E9RjuHXMFge0	f	\N	\N
41	pbkdf2_sha256$150000$pAam8TvnB8Oz$9tL770mvFG2UEpwWi79nmRaJn6ok6SjBXlj+6mNb0/Y=	\N	f	+85290987654				t	f	f	2020-12-04 12:13:12.590984+00	USER		f	f	+85290987654	t	000000		F5Ka6ZHtHEv6	f	\N	\N
39	pbkdf2_sha256$150000$fM48b4zAwm4d$rsnUerDLIsdSvJmD0+e0L7DrkCVIx1Inc6Eo9XtOmLE=	\N	f	+85264703385				t	f	f	2020-11-01 15:45:22.903843+00	USER		f	f	+85264703385	t	000000	a	akfLsa6tsLAX	f	\N	\N
20	pbkdf2_sha256$150000$cnnuWf8A6ach$9b2x1TE7R+4qbFl3YQcPUSmXhCapacHir0CnNE5Ivto=	\N	f	+85267403388				t	f	f	2020-09-08 14:52:25.33415+00	USER		f	f	+85267403388	t	000000		ppXpfT9r3dOk	f	\N	\N
42	pbkdf2_sha256$150000$4mWqrcJqiyql$FwalDnO2Glzl0I8A5JPIvlxW6O5B3RuzR2mmhxSiUBw=	\N	f	+85290622890				t	f	f	2020-12-04 12:22:16.713414+00	USER		f	f	+85290622890	t	000000	A	Qq4QlX8nKQTF	f	\N	\N
30	pbkdf2_sha256$150000$opPn1tDU1G1o$1bsCfzVNia6A77YLXkiBYzBL9K4FVl2txzDvi8d132k=	\N	f	+85268415885				t	f	f	2020-09-13 13:15:52.187766+00	USER		f	f	+85268415885	t	000000	小朋友	yektzFRTrdZb	f	\N	\N
44	pbkdf2_sha256$150000$L3QdsU6SaRJY$6c7GTjI11u+XqIyVfcU/Z+Dnobd3kxkTuXWsAaIePv8=	\N	f	+85267722254				t	f	f	2020-12-04 17:50:03.940491+00	USER		f	f	+85267722254	t	000000	test	YeIhU3OLQmcB	f	\N	\N
45	pbkdf2_sha256$150000$B45yNKoGgB8s$fM3dpQkSt0OTHoIq6YUpfdsWn/PeajdR9jFz/Pf58cI=	\N	f	+85267711154				t	f	f	2020-12-04 18:20:34.450782+00	USER		f	f	+85267711154	t	000000	test 2	ZPPFk8YAqAUY	f	\N	\N
46	pbkdf2_sha256$150000$F7zC5z1m1jvn$ZFljt239AQdSGCDOrc3MoY+CcQc834z532mUA3zgv8U=	\N	f	+85267733354				t	f	f	2020-12-04 18:28:03.494625+00	USER		f	f	+85267733354	t	000000	test 3	V9NQ7wJgK8VR	f	\N	\N
10	pbkdf2_sha256$150000$39AggD9nC3hi$qHmZw7ztpiju1CULkJUZgxg8MZRelOWglT7k4n89Azs=	2020-12-04 18:37:56.053844+00	t	Loi Cheung			def@hij.com	t	f	t	2020-09-02 15:48:59.308166+00	USER		f	f	\N	f				f	\N	\N
47	pbkdf2_sha256$150000$KwOZTIpYcUxl$tjR+4HvZdMk6zACXUvg7fiHdXemJWSsgMEScKjRFaUw=	\N	f	+85268415895				t	f	f	2020-12-04 18:48:14.148743+00	USER		f	f	+85268415895	t	000000	a	Aty9H9tqaE6q	f	\N	\N
48	pbkdf2_sha256$150000$IaCc1QSaXzDS$pbnbaRiQp7TOlcv3E9YU6kdaQylGfBeqxueSmj+U+hs=	\N	f	+85292657977				t	f	f	2020-12-04 22:36:42.882148+00	USER		f	f	+85292657977	f	000000		wqPdLHbK0rXz	t	\N	\N
77	pbkdf2_sha256$150000$rJVBtKoUWK2V$8MPV8GKxJVNRBFGl4OybExEcAgxNrt3GBbEUI5ljvS8=	\N	f	+85290123465				t	f	f	2021-02-24 09:04:08.541315+00	USER		f	f	+85290123465	f	000000		spMFbnlZIV5i	t	\N	\N
49	pbkdf2_sha256$150000$geCWRqSbl0WC$fdxIf6ruZ0IsNQFV7HEb4Lmr/ZQ9VE5RF7wGjD6VJlc=	\N	f	+85293265789				t	f	f	2020-12-04 22:37:03.083268+00	USER		f	f	+85293265789	t	000000	test lam	HAISi1wWnx4W	f	\N	\N
59	pbkdf2_sha256$150000$33McXljo9bta$0jAJROkEYbZRW2UxnZ7srLX8PRX85R+UsykyriXkkYY=	\N	f	+85290674033				t	f	f	2021-02-09 09:48:20.281707+00	USER		f	f	+85290674033	t	000000	123123	a2WKz8Wj8IX0	f	\N	\N
60	pbkdf2_sha256$150000$mt013yJE9IlY$oAmQE5YEjPrDZiGNpupKXWMGaPHVCUtDUD9q3DSCxDg=	\N	f	test			\N	t	f	f	2021-02-10 03:40:22.917512+00	ADMIN		f	f	\N	f				f	\N	\N
52	pbkdf2_sha256$150000$vl8MxyAipinN$aWd4C35ASHbejLs6Mo7ntRww6KzRfkDue7Z8h/Xi96s=	\N	f	+85295486484				t	f	f	2020-12-06 18:03:05.290501+00	USER		f	f	+85295486484	t	000000	bsbsjs	k9wJSrU0E4AO	f	\N	\N
71	pbkdf2_sha256$150000$iVkkvgBTL9Cg$YxcrpL255YL2CvyB87RTBecRVePUPge8F8fGieZI+uU=	\N	f	+85298876543				t	f	f	2021-02-16 03:58:40.141558+00	USER		f	f	+85298876543	t	000000		OgxEioOivBX3	f	\N	\N
50	pbkdf2_sha256$150000$ynFW1h20tOdU$NhH7jZQa3lGvMOczYyjmUm1Ri/FpTjhXtC4XWv8euKs=	\N	f	+85267744454				t	f	f	2020-12-05 05:59:54.626833+00	USER		f	f	+85267744454	t	000000	test 4	nFDmCXrOeMFP	f	\N	\N
53	pbkdf2_sha256$150000$eSQNwx6tB0JD$CpDVtlxv8Hma8DYblroGzbbudiRBcN50zknNK4T7shk=	\N	f	+85290123459				t	f	f	2020-12-11 14:44:48.122734+00	USER		f	f	+85290123459	t	000000		nOgi2L9u01FR	f	\N	\N
51	pbkdf2_sha256$150000$mpPtSfl7F3it$CM86H2U1Z2ycaLfO6v+NZPMdpXfpaYLCTtGu5MlmCUY=	\N	f	+85236914746				t	f	f	2020-12-06 01:01:28.455241+00	USER		f	f	+85236914746	t	000000	abc hen dkalwoi	KGTgxJqH5Jnt	f	\N	\N
74	pbkdf2_sha256$150000$DMXv0MlrFZkg$iTE4EwZ0ZkD8TXTCl4bmtFCYHpxMPnEXigRILbsK+yc=	\N	f	+85292021089				t	f	f	2021-02-23 06:32:46.534684+00	USER		f	f	+85292021089	f	000000		qusfJ2uaY8jU	t	\N	\N
67	pbkdf2_sha256$150000$QitR8rSv3ueb$i3ZX3218f45Ux6jw80ULm653YiFoKYwIwdMpW9oJcFk=	\N	f	test1234			\N	t	f	f	2021-02-15 06:04:34.395953+00	USER		f	f	+85298765432	t	000000	test1234	U1HOjSjBYyjk	f	\N	\N
75	pbkdf2_sha256$150000$cgSiBxdSY6pq$nI/37ECxVDrDLsyL541KQGGxMOXJvQVj8wJl1oXmkT0=	\N	f	+85292017302				t	f	f	2021-02-23 06:38:57.332488+00	USER		f	f	+85292017302	t	000000	Testing Owner Name	LfP9m5o9MzUi	f	\N	\N
76	pbkdf2_sha256$150000$z407byw3Dnu1$d2r63oIIauauiOIiYx6+BvXfZquh+PhEQLY+B3yqqW8=	\N	f	+85297331499				t	f	f	2021-02-24 08:29:29.344537+00	USER		f	f	+85297331499	t	000000	abc	bG9MNCAX3t44	f	\N	\N
\.


--
-- Data for Name: common_user_groups; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.common_user_groups (id, user_id, group_id) FROM stdin;
\.


--
-- Data for Name: common_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.common_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- Data for Name: companies_chargingstages; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.companies_chargingstages (id, quantity, "values", descriptions, company_id) FROM stdin;
6	2	{50,50}	{"",""}	15
22	3	{5,80,15}	{"","",""}	35
11	5	{20,20,20,20,20}	{"","","","",""}	20
25	5	{20,20,20,20,20}	{"Before contract","After first meeting","After Painting","After Construction",Final}	60
2	2	{50,50}	{"test 1","test 2"}	2
5	3	{25,25,50}	{"","",""}	11
12	1	{100}	{""}	23
13	2	{50,50}	{"",""}	24
14	3	{40,30,30}	{"","",""}	25
15	1	{100}	{""}	26
16	1	{100}	{""}	27
20	3	{10,20,70}	{"","",""}	31
21	3	{20,10,70}	{"","",""}	34
23	3	{50,25,25}	{"","",""}	36
\.


--
-- Data for Name: companies_company; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.companies_company (id, name, email, phone, industry, billing_address_line, billing_street, billing_city, billing_state, billing_postcode, billing_country, website, description, created_on, is_active, status, logo_pic, br_pic, created_by_id, owner_id, br_approved, job_no, sign, br_pic_height, br_pic_width, logo_pic_height, logo_pic_width, sign_height, sign_width, gen_invoice_count, gen_invoice_date, gen_quot_count, gen_quot_date, gen_receipt_count, gen_receipt_date) FROM stdin;
60	Testing Company Limited	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	2021-02-23 06:42:08.243394+00	f	open	companies/60/logos/fca921e0-9af.jpg	companies/60/brs/c888b3ad-947.jpg	75	75	f	1	companies/60/signs/a6bf412d-da6.jpg	1	1	1	1	1	1	0	2021-02-24	0	2021-02-24	0	2021-02-24
34	tezt co	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	2020-12-06 01:02:52.620093+00	f	open	companies/34/logos/da9836e0-30c.png	companies/34/brs/b89f7ebb-52f.png	51	51	t	1	companies/34/signs/fd3b5181-9e7.png	1	1	1	1	1	1	0	2021-02-24	0	2021-02-24	0	2021-02-24
32	test 4	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N		2020-12-05 06:01:35.019124+00	t	open	companies/32/logos/695b16cd-f43.jpg	companies/32/brs/87004479-b5b.jpg	50	50	f	1	companies/32/signs/3a6f1552-994.jpg	1	1	1	1	1	1	0	2021-02-24	0	2021-02-24	0	2021-02-24
23	小朋友有限公司	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	2020-12-04 14:28:18.82957+00	f	open	companies/23/logos/b2bb8c1e-3f7.jpg	companies/23/brs/2abc39db-d45.jpg	30	30	f	1	companies/23/signs/82a7ab53-5cb.jpg	1	1	1	1	1	1	0	2021-02-24	0	2021-02-24	0	2021-02-24
25	test	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	2020-12-04 17:52:57.701086+00	f	open	companies/25/logos/4121eb78-4bb.jpg	companies/25/brs/eba29375-5f3.jpg	44	44	f	1	companies/25/signs/fc4af291-9a8.jpg	1	1	1	1	1	1	0	2021-02-24	0	2021-02-24	0	2021-02-24
26	test 2	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	2020-12-04 18:21:02.599802+00	f	open	companies/26/logos/9598b7fa-23c.jpg	companies/26/brs/98357a42-380.jpg	45	45	f	1	companies/26/signs/ff8a6a87-ed8.jpg	1	1	1	1	1	1	0	2021-02-24	0	2021-02-24	0	2021-02-24
20	interium design &contracting ltd	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	2020-11-26 17:15:35.074947+00	f	open	companies/20/logos/cf01a3a0-e1b.jpg	companies/20/brs/0583e01d-3cd.jpg	23	23	t	14	companies/20/signs/783a80cf-8c5.jpg	1	1	1	1	1	1	0	2021-02-24	0	2021-02-24	0	2021-02-24
2	Fat Cat company	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N		2020-09-02 15:54:39.311777+00	f	open	companies/2/logos/9766ffc6-8b5.jpg	companies/2/brs/427b0540-0ac.jpg	11	11	t	75	companies/2/signs/e40d9037-010.jpg	480	480	480	480	480	480	0	2021-02-24	0	2021-02-24	0	2021-02-24
27	test 3	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N		2020-12-04 18:28:34.411449+00	f	open	companies/27/logos/c7b9a53f-525.jpg	companies/27/brs/966116e5-e5a.jpg	46	46	t	1	companies/27/signs/a3706c2d-315.jpg	1	1	1	1	1	1	0	2021-02-24	0	2021-02-24	0	2021-02-24
63	a	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	2021-02-24 08:28:44.88986+00	f	open	companies/63/logos/48b375b8-36e.jpg	companies/63/brs/458a9c1c-66a.jpg	70	70	f	1	companies/63/signs/346ffb5d-4e3.jpg	1	1	1	1	1	1	0	2021-02-24	0	2021-02-24	0	2021-02-24
64	abc	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	2021-02-24 08:29:56.096216+00	f	open	companies/64/logos/d16583b2-988.jpg	companies/64/brs/50143866-852.jpg	76	76	f	1	companies/64/signs/a817ebcc-07c.jpg	1	1	1	1	1	1	0	2021-02-24	0	2021-02-24	0	2021-02-24
31	test co.	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	2020-12-04 22:38:49.007622+00	f	open	companies/31/logos/0e7c7bba-da6.png	companies/31/brs/c8dc4798-7b6.png	49	49	f	1	companies/31/signs/de68e1a5-192.png	1	1	1	1	1	1	0	2021-02-24	0	2021-02-24	0	2021-02-24
15	ABC Co., Ltd2	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N		2020-10-22 10:16:03.014009+00	f	open	companies/15/logos/4315eba5-138.jpg	companies/15/brs/8bdee8db-f97.jpg	24	24	t	63	companies/15/signs/bd7d6c3c-140.jpg	1	1	1280	960	1280	960	6	2021-02-26	4	2021-03-04	0	2021-02-26
11	abc	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	2020-09-13 12:58:51.667371+00	f	open	companies/11/logos/c311d41b-1c8.jpg	companies/11/brs/245a2a8e-2f8.jpg	28	28	t	13	companies/11/signs/09380789-c29.jpg	2560	1440	2560	1440	2560	1440	0	2021-02-24	0	2021-03-04	0	2021-02-24
35	小朋友公司	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	2020-12-06 17:33:21.312708+00	f	open	companies/35/logos/640a004d-593.jpg	companies/35/brs/42e8b235-ff6.jpg	43	43	t	7	companies/35/signs/fe6049dd-5f7.jpg	1	1	1	1	1	1	0	2021-02-24	0	2021-03-04	0	2021-02-24
33	a	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	2020-12-05 06:31:03.58989+00	f	open	companies/33/logos/158400f7-cf1.jpg	companies/33/brs/70c25011-06f.jpg	47	47	f	1	companies/33/signs/7a94caf3-b81.jpg	1	1	1	1	1	1	0	2021-02-24	0	2021-02-24	0	2021-02-24
36	hshsh	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	2020-12-06 18:03:32.029253+00	f	open	companies/36/logos/730616ae-af0.jpg	companies/36/brs/c8986a16-037.jpg	52	52	t	1	companies/36/signs/7fb49b14-2fa.jpg	1	1	1	1	1	1	0	2021-02-24	0	2021-02-24	0	2021-02-24
38	123123	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	2021-02-09 09:48:51.019948+00	f	open	companies/38/logos/8c297df4-6b1.jpg	companies/38/brs/044b844c-cee.jpg	59	59	t	1	companies/38/signs/ba4a5574-a49.jpg	1	1	1	1	1	1	0	2021-02-24	0	2021-02-24	0	2021-02-24
24	A	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	2020-12-04 15:44:09.79776+00	f	open	companies/24/logos/5f1bc250-90f.jpg	companies/24/brs/2efe7088-a21.jpg	42	42	t	1	companies/24/signs/3af3832f-366.jpg	1	1	1	1	1	1	0	2021-02-24	0	2021-02-24	0	2021-02-24
\.


--
-- Data for Name: companies_company_tags; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.companies_company_tags (id, company_id, tags_id) FROM stdin;
\.


--
-- Data for Name: companies_documentformat; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.companies_documentformat (id, quot_upper_format, quot_middle_format, quot_lower_format, invoice_upper_format, invoice_middle_format, invoice_lower_format, receipt_upper_format, receipt_middle_format, receipt_lower_format, company_id, project_upper_format, project_lower_format, project_based_number) FROM stdin;
14	A	Date	Alphabet	A	Date	Alphabet	A	Date	Alphabet	23	I	Number	0
15	A	Date	Alphabet	A	Date	Alphabet	A	Date	Alphabet	24	A	Number	0
16	A	Date	Alphabet	A	Date	Alphabet	A	Date	Alphabet	25	A	Number	0
17	A	Date	Alphabet	A	Date	Alphabet	A	Date	Alphabet	26	A	Number	0
18	A	Date	Alphabet	A	Date	Alphabet	A	Date	Alphabet	27	A	Number	0
2	Q	Date	Number	I	Date	Number	R	Date	Number	2	P	Number	0
22	A	Date	Alphabet	A	Date	Alphabet	A	Date	Alphabet	31	A	Number	0
23	J	Date	Alphabet	L	Date	Alphabet	A	Number	Number	34	A	Number	0
25	A	Date	Alphabet	A	Date	Alphabet	A	Date	Alphabet	36	A	Number	0
6	A	Date	Alphabet	A	Date	Alphabet	A	Date	Alphabet	11	A	Number	0
24	H	Alphabet	Number	A	Date	Alphabet	A	Date	Alphabet	35	A	Number	1
13	Q	Date	Alphabet	I	Date	Alphabet	R	Date	Alphabet	20	J	Number	3
27	Q	Number	Alphabet	I	Number	Alphabet	R	Number	Alphabet	60	P	Number	1
8	A	Date	Number	A	Date	Alphabet	A	Date	Alphabet	15	asda	Number	0
\.


--
-- Data for Name: companies_documentheaderinformation; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.companies_documentheaderinformation (id, tel, email, fax, address, company_id) FROM stdin;
1	+85267403385	cat@fatcat.com	+85267403385	fat cat building	2
19	+85212345678	snsi@jei.com	+852null	null	31
20	+85246207888	dgbv@dk.com			34
22					33
23	+85290876648	hshs@jdj.com	+85299494994		36
11	+85227499974	joe.lam@interiumdesign.com	+85234604852	Room 9, 12/F, Corporation park A,11 On Lai Street, Shuk Mun	20
6	+85290123456	1231@123.com	+85290123456	abc	15
21	+85290558888	calvinsung@vidarstudio.com			35
25	+85255554444	testing@email.com	+85228384545	Company Address	60
5	+85291234567	abc@def.com	+85291234567	abc	11
12	+85290622891	hshshs@jsj.com	+852null	null	23
13					25
14	+85267711154	test2@test.com	+85267711154		26
15					27
\.


--
-- Data for Name: companies_email; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.companies_email (id, message_subject, message_body, timezone, scheduled_date_time, scheduled_later, created_on, from_email, rendered_message_body, from_company_id) FROM stdin;
\.


--
-- Data for Name: companies_email_recipients; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.companies_email_recipients (id, email_id, contact_id) FROM stdin;
\.


--
-- Data for Name: companies_emaillog; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.companies_emaillog (id, is_sent, contact_id, email_id) FROM stdin;
\.


--
-- Data for Name: companies_invoicegeneralremark; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.companies_invoicegeneralremark (id, index, content, company_id) FROM stdin;
\.


--
-- Data for Name: companies_quotationgeneralremark; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.companies_quotationgeneralremark (id, index, content, company_id) FROM stdin;
63	1	qq	35
\.


--
-- Data for Name: companies_receiptgeneralremark; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.companies_receiptgeneralremark (id, index, content, company_id) FROM stdin;
\.


--
-- Data for Name: companies_tags; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.companies_tags (id, name, slug) FROM stdin;
\.


--
-- Data for Name: contacts_contact; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.contacts_contact (id, first_name, last_name, email, phone, description, created_on, is_active, address_id, created_by_id, profile_pic) FROM stdin;
\.


--
-- Data for Name: contacts_contact_assigned_to; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.contacts_contact_assigned_to (id, contact_id, user_id) FROM stdin;
\.


--
-- Data for Name: contacts_contact_teams; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.contacts_contact_teams (id, contact_id, teams_id) FROM stdin;
\.


--
-- Data for Name: customers_customer; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.customers_customer (id, name, company_name, email, phone, address, created_on, created_by_id, project_id) FROM stdin;
121	Client Name	Company Name	testing@email.com	+85291325687	Address	2021-02-23 04:11:53.571161+00	\N	179
91	sbne	\N	\N	\N	Pending	2020-11-21 05:33:15.113068+00	\N	147
122	Client 2	Company Name 2	\N	+85291993523	Pending	2021-02-23 04:31:20.976435+00	\N	180
93	gay client	gay limited	testing@gay.com	+85290909090	Pending	2020-12-06 17:45:23.759159+00	\N	149
95	god me	god company	sjsjs@jdjs.com	+85298550000	test	2020-12-06 17:57:56.383702+00	\N	151
58	a	a	a@a.com	+85290123456	a	2020-11-19 16:10:41.213052+00	\N	81
96	a	a	a@a.com	+85290123456	a	2020-12-06 18:00:05.735977+00	\N	152
101	a	\N	\N	\N	Pending	2020-12-07 10:13:46.001448+00	\N	160
47	a	assssssssssssssssssssssssssssssssssssssssssssss	a@a.co	+85290123456	123\n123\n123	2020-10-23 10:32:55.659468+00	\N	78
104	bjj	\N	\N	\N	Pending	2020-12-31 03:18:06.371758+00	\N	163
107	test	\N	\N	\N	Pending	2021-01-07 11:34:26.118339+00	\N	166
108	asdas	\N	\N	\N	Pending	2021-01-18 14:36:25.83753+00	\N	167
109	jsjsjsjs	dhdhhs	hshshsj@jxjd.com	+85264646464	jsjsjwjw	2021-01-19 04:44:40.240836+00	\N	168
110	jdkdk	\N	\N	\N	Pending	2021-01-20 08:00:57.760169+00	\N	169
102	林先生	\N	\N	\N	Pending	2020-12-11 17:51:54.440546+00	\N	161
111	鄧先生	鄧先生	\N	+85296067525	Pending	2021-01-23 12:28:04.013696+00	\N	170
106	太平有限公司	太平有限公司	pacific@nglhk.com	+85223230000	德輔道中11號	2021-01-05 16:10:44.42718+00	\N	165
92	J2601港景峰	ADB company	testing@gmail.com	+85291383013	Pending	2020-11-26 17:30:35.854209+00	\N	148
112	怡保有限公司	怡保有限公司	yipo@yahoo.com.hk	+85228332833	Pending	2021-01-30 16:16:37.878801+00	\N	171
114	陸先生	太平洋有限公司	andrewluk@yahoo.com.hk	+85228300283	香港西灣河太康街鲤景灣安明閣16樓G室	2021-02-03 03:43:43.499453+00	\N	173
115	鄭先生	新興有限公司	cheng@gmail.com	+85224326855	太子道西250號2樓	2021-02-03 07:27:57.859561+00	\N	174
116	陳先生	日材有限公司	\N	+85228283535	Pending	2021-02-04 04:04:11.127625+00	\N	175
117	J.M. Chan	JM Company Holdings Ltd.	jmchan@jm.com	+85297842138	Tai Po, HK	2021-02-15 11:32:13.902054+00	\N	176
118	a	\N	\N	\N	Pending	2021-02-15 15:08:33.978936+00	\N	97
73	def	hfxhxf	\N	\N	Pending	2020-11-20 17:05:44.448782+00	\N	123
119	q	q	\N	\N	q	2021-02-15 17:52:14.470324+00	\N	177
120	a	\N	\N	\N	Pending	2021-02-16 04:54:15.298955+00	\N	178
66	nsjdk	\N	\N	\N	Pending	2020-11-20 12:45:44.585917+00	\N	117
67	sjsn	\N	\N	\N	Pending	2020-11-20 12:50:34.143315+00	\N	96
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
1	2020-06-23 10:55:59.596407+00	1	Toilet	1	[{"added": {}}]	66	1
2	2020-06-23 10:56:05.692706+00	2	Kitchen	1	[{"added": {}}]	66	1
3	2020-06-23 10:56:12.746385+00	3	Living Room	1	[{"added": {}}]	66	1
4	2020-06-23 10:56:19.012056+00	4	Dinning Room	1	[{"added": {}}]	66	1
5	2020-06-23 10:56:25.288972+00	5	1 Person Bed Room	1	[{"added": {}}]	66	1
6	2020-06-23 10:56:33.678067+00	6	2 Persons Bed Room	1	[{"added": {}}]	66	1
7	2020-06-23 11:19:54.476601+00	1	Height	1	[{"added": {}}]	65	1
8	2020-06-23 11:20:06.120196+00	2	Length	1	[{"added": {}}]	65	1
9	2020-06-23 11:20:14.463687+00	3	Width	1	[{"added": {}}]	65	1
10	2020-06-23 11:20:32.13185+00	1	RoomTypeProperties object (1)	1	[{"added": {}}]	73	1
11	2020-06-23 11:21:28.83565+00	1	Toilet's Properties	2	[]	73	1
12	2020-06-23 11:22:11.505015+00	1	RoomTypeFormula object (1)	1	[{"added": {}}]	67	1
13	2020-06-23 11:46:46.500255+00	4	Testing	1	[{"added": {}}]	65	1
14	2020-06-23 11:47:02.089734+00	1	Toilet's Properties	2	[{"changed": {"fields": ["room_properties"]}}]	73	1
15	2020-06-23 11:57:00.413065+00	1	Testing: ABC	2	[{"changed": {"fields": ["value"]}}]	68	1
16	2020-06-23 11:58:34.874047+00	1	Toilet: Floor Area	2	[{"changed": {"fields": ["formula"]}}]	67	1
17	2020-06-23 12:28:19.96976+00	1	Toilet: Floor Area	2	[{"changed": {"fields": ["formula"]}}]	67	1
18	2020-06-23 12:49:40.931005+00	2	Toilet: Wall Area	1	[{"added": {}}]	67	1
19	2020-06-26 07:50:00.915215+00	1	Length	1	[{"added": {}}]	75	1
20	2020-06-26 07:50:17.984486+00	2	Width	1	[{"added": {}}]	75	1
21	2020-06-26 08:06:00.048311+00	1	Lighting	1	[{"added": {}}]	76	1
22	2020-06-26 08:07:15.648403+00	2	Furniture	1	[{"added": {}}]	76	1
23	2020-06-26 08:08:22.416973+00	2	Furniture: Wood	1	[{"added": {}}]	77	1
24	2020-06-26 08:08:56.255579+00	3	Furniture: Steel	1	[{"added": {}}]	77	1
25	2020-06-26 08:22:36.132621+00	3	Hose	1	[{"added": {}}]	76	1
26	2020-06-26 08:31:45.52682+00	1	Living Room Chair	1	[{"added": {}}]	71	1
27	2020-06-26 08:35:36.403698+00	1	Testing: ABC: Living Room Chair	1	[{"added": {}}]	74	1
28	2020-06-26 10:11:50.256922+00	4	Testing	3		65	1
29	2020-06-26 10:12:04.110402+00	1	Toilet: Floor Area	2	[{"changed": {"fields": ["formula"]}}]	67	1
30	2020-06-26 10:20:33.910058+00	2	Kitchen's Properties	1	[{"added": {}}]	73	1
31	2020-06-26 11:11:04.869808+00	3	Living Room	2	[{"changed": {"fields": ["related_items"]}}]	66	1
32	2020-06-26 11:12:00.856175+00	2	Hose	1	[{"added": {}}]	71	1
33	2020-06-26 11:12:17.265718+00	1	Toilet	2	[{"changed": {"fields": ["related_items"]}}]	66	1
66	2020-06-29 07:31:38.53045+00	1	Living Room Chair: Living Room Chair Price	1	[{"added": {}}]	80	1
67	2020-06-29 07:31:53.123033+00	1	Living Room Chair: Suggested Quantity	2	[{"changed": {"fields": ["name"]}}]	80	1
68	2020-06-29 07:32:14.708141+00	2	Living Room Chair: Suggested Price	1	[{"added": {}}]	80	1
69	2020-06-29 10:48:16.533192+00	2	Living Room Chair: Suggested Unit Price	2	[{"changed": {"fields": ["name", "formula"]}}]	80	1
70	2020-06-29 11:26:23.894603+00	2	Living Room Chair: Suggested Unit Price	2	[]	80	1
71	2020-06-29 11:30:20.961685+00	1	Living Room Chair	2	[{"changed": {"fields": ["value_based_price"]}}]	71	1
72	2020-06-29 11:38:23.482867+00	2	Living Room Chair: Suggested Unit Price	2	[{"changed": {"fields": ["formula"]}}]	80	1
73	2020-07-03 06:19:05.80439+00	1	Living Room Chair	2	[{"changed": {"fields": ["value_based_price"]}}]	71	1
74	2020-07-03 07:03:29.636927+00	3	Furniture: Steel	2	[{"changed": {"fields": ["value_based_price"]}}]	77	1
75	2020-07-03 07:35:10.377413+00	3	Furniture: Steel	2	[{"changed": {"fields": ["value_based_price"]}}]	77	1
76	2020-07-03 07:35:18.426308+00	3	Furniture: Steel	2	[{"changed": {"fields": ["value_based_price"]}}]	77	1
77	2020-07-03 07:36:17.201551+00	1	Living Room Chair	2	[{"changed": {"fields": ["item_type"]}}]	71	1
78	2020-07-03 07:37:45.730995+00	1	Living Room Chair	2	[{"changed": {"fields": ["item_type"]}}]	71	1
79	2020-07-03 07:39:57.108909+00	2	Furniture: Wood	2	[{"changed": {"fields": ["value_based_price"]}}]	77	1
80	2020-07-03 08:08:42.427923+00	1	Testing: ABC: Living Room Chair	2	[{"changed": {"fields": ["quantity"]}}]	74	1
81	2020-07-03 08:52:56.026105+00	1	Third-Party Liability Insurance	1	[{"added": {}}]	114	1
82	2020-07-03 08:55:24.925641+00	2	Cleaning after Decoration	1	[{"added": {}}]	114	1
83	2020-07-03 09:03:49.51329+00	1	Third-Party Liability Insurance	1	[{"added": {}}]	113	1
84	2020-07-03 09:04:03.377373+00	2	Cleaning after Decoration	1	[{"added": {}}]	113	1
85	2020-07-03 09:04:23.365014+00	1	testing1: Testing: Third-Party Liability Insurance	1	[{"added": {}}]	115	1
86	2020-07-06 09:12:32.591745+00	2	testing1: Testing	3		63	1
87	2020-07-06 09:13:59.307214+00	1	testing1: Testing	2	[{"changed": {"fields": ["created_by", "charging_stages"]}}]	63	1
88	2020-07-06 09:14:05.566163+00	1	testing1: Testing	2	[]	63	1
89	2020-07-06 09:22:50.185706+00	1	testing1 Document Format	1	[{"added": {}}]	61	1
90	2020-07-06 09:58:31.248556+00	1	testing1: Testing	2	[{"changed": {"fields": ["document_format"]}}]	63	1
91	2020-07-09 12:14:21.889715+00	1	testing1	2	[{"changed": {"fields": ["created_by", "logo_pic", "br_pic"]}}]	56	1
92	2020-07-10 11:13:42.353391+00	1	testing1	2	[{"changed": {"fields": ["phone", "billing_address_line"]}}]	56	1
93	2020-09-02 15:51:48.770913+00	5	+85290123458	2	[{"changed": {"fields": ["role"]}}]	5	1
94	2020-09-02 15:56:07.816418+00	2	傢俬	2	[{"changed": {"fields": ["name"]}}]	76	1
95	2020-09-02 15:56:27.669799+00	1	照明	2	[{"changed": {"fields": ["name"]}}]	76	1
96	2020-09-02 15:56:44.9796+00	3	水管	2	[{"changed": {"fields": ["name"]}}]	76	1
97	2020-09-02 15:56:58.420309+00	2	水管	2	[{"changed": {"fields": ["name"]}}]	71	1
98	2020-09-02 15:57:20.955988+00	1	第三者保險	1	[{"added": {}}]	150	10
99	2020-09-02 15:57:44.693424+00	2	施工期間清除垃圾	1	[{"added": {}}]	150	10
100	2020-09-02 15:57:49.096727+00	1	客廳櫈	2	[{"changed": {"fields": ["name"]}}]	71	1
101	2020-09-02 15:57:59.163753+00	3	裝修完工清潔	1	[{"added": {}}]	150	10
102	2020-09-02 15:58:10.918368+00	3	傢俬: 鋼	2	[{"changed": {"fields": ["name"]}}]	77	1
103	2020-09-02 15:58:13.444915+00	4	清拆厨房磁磚	1	[{"added": {}}]	150	10
104	2020-09-02 15:58:15.321718+00	2	傢俬: 木	2	[{"changed": {"fields": ["name"]}}]	77	1
105	2020-09-02 15:58:27.63674+00	5	清拆厠所磁磚	1	[{"added": {}}]	150	10
106	2020-09-02 15:58:38.60468+00	6	清拆客廳地板	1	[{"added": {}}]	150	10
107	2020-09-02 15:58:39.205178+00	1	廁所	2	[{"changed": {"fields": ["name"]}}]	66	1
108	2020-09-02 15:58:46.763273+00	2	廚房	2	[{"changed": {"fields": ["name"]}}]	66	1
109	2020-09-02 15:59:04.028785+00	3	客廳	2	[{"changed": {"fields": ["name"]}}]	66	1
110	2020-09-02 15:59:46.460131+00	4	飯廳	2	[{"changed": {"fields": ["name"]}}]	66	1
111	2020-09-02 15:59:52.11041+00	5	1	2	[{"changed": {"fields": ["name"]}}]	66	1
112	2020-09-02 16:00:18.052163+00	5	1人睡房	2	[{"changed": {"fields": ["name"]}}]	66	1
113	2020-09-02 16:00:23.358654+00	6	2人睡房	2	[{"changed": {"fields": ["name"]}}]	66	1
114	2020-09-02 16:49:17.354977+00	2	cat company	2	[{"changed": {"fields": ["br_approved"]}}]	56	10
115	2020-09-03 08:21:25.538595+00	1	廁所	2	[{"changed": {"fields": ["room_properties"]}}]	66	1
116	2020-09-03 08:21:30.047431+00	2	廚房	2	[{"changed": {"fields": ["room_properties"]}}]	66	1
117	2020-09-03 08:21:34.85225+00	3	客廳	2	[{"changed": {"fields": ["room_properties"]}}]	66	1
118	2020-09-03 08:21:39.764532+00	4	飯廳	2	[{"changed": {"fields": ["room_properties"]}}]	66	1
119	2020-09-03 08:21:49.998236+00	5	1人睡房	2	[{"changed": {"fields": ["room_properties"]}}]	66	1
120	2020-09-03 08:21:53.226736+00	6	2人睡房	2	[{"changed": {"fields": ["room_properties"]}}]	66	1
121	2020-09-03 10:52:59.444668+00	7	自定義房間	1	[{"added": {}}]	66	1
122	2020-09-03 10:54:01.821931+00	5	地台數目	1	[{"added": {}}]	65	1
123	2020-09-03 10:54:19.361788+00	6	牆身數目	1	[{"added": {}}]	65	1
124	2020-09-03 10:54:24.408967+00	5	地台數目	2	[{"changed": {"fields": ["symbol"]}}]	65	1
125	2020-09-03 15:42:55.637352+00	2	cat company's Charging Stage	2	[{"changed": {"fields": ["descriptions"]}}]	78	10
126	2020-09-03 15:54:21.326395+00	2	cat company's Charging Stage	2	[{"changed": {"fields": ["descriptions"]}}]	78	10
127	2020-09-03 15:54:57.405118+00	2	cat company's Charging Stage	2	[{"changed": {"fields": ["descriptions"]}}]	78	10
128	2020-09-03 16:01:38.406179+00	7	cat company: test1	3		63	10
129	2020-09-03 16:01:45.276065+00	6	cat company: test1	3		63	10
130	2020-09-03 16:01:52.216848+00	5	cat company: test1	3		63	10
131	2020-09-03 16:03:52.465807+00	8	cat company: test1	3		63	10
132	2020-09-03 16:14:18.830133+00	10	cat company: test1	3		63	10
133	2020-09-03 16:14:23.077796+00	9	cat company: test1	3		63	10
134	2020-09-04 03:55:11.134113+00	1	fat cat	3		70	10
135	2020-09-04 05:11:02.974605+00	2	testing project1: Kitchen	2	[{"changed": {"fields": ["related_project"]}}]	68	1
136	2020-09-04 05:11:06.861587+00	1	testing project1: ABC	2	[{"changed": {"fields": ["related_project"]}}]	68	1
137	2020-09-04 07:33:43.301684+00	6	cat company: testing project1: 施工期間清除垃圾	3		149	10
138	2020-09-04 07:33:46.366219+00	5	cat company: testing project1: 第三者保險	3		149	10
139	2020-09-04 10:37:18.698931+00	1	客廳櫈	2	[{"changed": {"fields": ["value_based_price"]}}]	71	10
140	2020-09-04 12:55:11.738582+00	5	testing project1: 客廳	3		68	10
141	2020-09-04 12:55:36.474373+00	3	testing project1: ABC	3		68	10
142	2020-09-04 12:55:43.327211+00	2	testing project1: Kitchen	3		68	10
143	2020-09-04 12:55:46.901324+00	1	testing project1: ABC	3		68	10
144	2020-09-04 17:51:29.607483+00	14	admin	2	[{"changed": {"fields": ["phone", "login_token", "role"]}}]	5	1
145	2020-09-05 08:41:16.902418+00	1	cat company Document Header	2	[{"changed": {"fields": ["tel", "email", "fax", "address"]}}]	155	10
146	2020-09-05 09:07:33.940245+00	11	cat company: testing project1	3		63	10
147	2020-09-05 09:07:40.522825+00	12	cat company: test2	3		63	10
148	2020-09-05 09:07:44.846314+00	13	cat company: test3	3		63	10
149	2020-09-07 11:02:51.652933+00	2	company 99 Document Header	2	[]	155	1
150	2020-09-07 11:03:16.077719+00	3	testing1 Document Header	1	[{"added": {}}]	155	1
151	2020-09-07 11:05:26.471524+00	17	Testing: 客廳	2	[{"changed": {"fields": ["related_project"]}}]	68	1
152	2020-09-07 11:05:38.795503+00	17	testing project 3: 客廳	2	[{"changed": {"fields": ["related_project"]}}]	68	1
153	2020-09-07 11:08:55.560219+00	1	testing1	2	[{"changed": {"fields": ["sign"]}}]	56	1
154	2020-09-07 11:10:37.772488+00	1	testing1	2	[{"changed": {"fields": ["logo_pic"]}}]	56	1
155	2020-09-07 11:23:57.98846+00	9	ABC	1	[{"added": {}}]	70	1
156	2020-09-07 11:25:48.741535+00	5	+85290123458	2	[{"changed": {"fields": ["display_name"]}}]	5	1
157	2020-09-10 08:10:05.969035+00	9	dog company	2	[{"changed": {"fields": ["br_approved"]}}]	56	10
158	2020-09-13 12:48:54.042568+00	14	admin	2	[{"changed": {"fields": ["phone"]}}]	5	1
159	2020-09-18 09:41:58.450555+00	15	fat cat company: cat project milestone 15 test milestone 1	2	[{"changed": {"fields": ["img"]}}]	153	1
160	2020-09-20 07:25:01.066492+00	1	泥水及瓷磚	1	[{"added": {}}]	152	1
161	2020-09-20 10:36:56.278483+00	2	fat cat company: cat project expense: test expense 1	3		151	10
162	2020-09-20 10:36:59.438824+00	3	fat cat company: cat project expense: test expense 1	3		151	10
163	2020-09-20 10:37:02.145467+00	4	fat cat company: cat project expense: test expense 1	3		151	10
164	2020-09-20 10:37:04.631644+00	5	fat cat company: cat project expense: test expense 1	3		151	10
165	2020-09-20 10:37:09.787213+00	1	fat cat company: cat project expense: test expense 1	2	[{"changed": {"fields": ["price"]}}]	151	10
166	2020-09-24 10:31:31.074055+00	36	fat cat company: dog project	2	[{"changed": {"fields": ["document_format"]}}]	63	1
167	2020-09-24 10:31:39.596402+00	35	dog company: TESTING	2	[{"changed": {"fields": ["document_format"]}}]	63	1
168	2020-09-24 10:31:44.660628+00	34	dog company: TESTING	2	[{"changed": {"fields": ["document_format"]}}]	63	1
169	2020-09-24 10:31:51.784396+00	33	dog company: TESTING	2	[{"changed": {"fields": ["document_format"]}}]	63	1
170	2020-09-24 10:32:03.403467+00	32	fat cat company: cat project	2	[{"changed": {"fields": ["document_format"]}}]	63	1
171	2020-09-24 10:32:11.803881+00	25	dog company: test project1	2	[{"changed": {"fields": ["document_format"]}}]	63	1
172	2020-09-24 10:32:16.627142+00	4	testing1: Testing	2	[{"changed": {"fields": ["document_format"]}}]	63	1
173	2020-09-24 10:32:21.415265+00	1	testing1: Testing	2	[{"changed": {"fields": ["document_format"]}}]	63	1
174	2020-09-24 10:50:56.186213+00	36	fat cat company: dog project	2	[{"changed": {"fields": ["document_format"]}}]	63	1
175	2020-09-24 10:51:09.731961+00	35	dog company: TESTING	2	[{"changed": {"fields": ["document_format"]}}]	63	1
176	2020-09-24 10:51:14.373117+00	34	dog company: TESTING	2	[{"changed": {"fields": ["document_format"]}}]	63	1
177	2020-09-24 10:51:18.730808+00	33	dog company: TESTING	2	[{"changed": {"fields": ["document_format"]}}]	63	1
178	2020-09-24 10:51:22.958698+00	32	fat cat company: cat project	2	[{"changed": {"fields": ["document_format"]}}]	63	1
179	2020-09-24 10:51:26.552309+00	25	dog company: test project1	2	[{"changed": {"fields": ["document_format"]}}]	63	1
180	2020-09-24 10:51:30.404723+00	4	testing1: Testing	2	[{"changed": {"fields": ["document_format"]}}]	63	1
181	2020-09-24 10:51:34.728692+00	1	testing1: Testing	2	[{"changed": {"fields": ["document_format"]}}]	63	1
182	2020-09-25 07:51:27.544103+00	3	傢俬	1	[{"added": {}}]	152	10
183	2020-09-25 08:15:09.871333+00	7	fat cat company: cat project expense: test expense 2	2	[{"changed": {"fields": ["expense_type"]}}]	151	10
184	2020-09-26 11:00:43.59887+00	37	fat cat company: testing project 3	3		63	10
185	2020-09-26 11:02:21.551266+00	38	fat cat company: project 3	3		63	10
186	2020-09-26 11:22:58.786517+00	39	fat cat company: 123	3		63	10
187	2020-09-26 20:02:34.018753+00	7	fat cat company: cat test project expense: test expense 2	2	[{"changed": {"fields": ["remark"]}}]	151	1
188	2020-09-26 20:02:41.376312+00	1	fat cat company: cat test project expense: test expense 1	2	[{"changed": {"fields": ["remark"]}}]	151	1
189	2020-09-27 06:00:34.327325+00	1	fat cat company: cat test project expense: test expense 1	2	[{"changed": {"fields": ["img"]}}]	151	10
190	2020-09-27 15:01:47.030197+00	3	餐桌	1	[{"added": {}}]	71	10
191	2020-09-27 15:09:41.579733+00	4	吊燈	1	[{"added": {}}]	71	10
192	2020-09-27 15:09:46.789552+00	4	吊燈	2	[{"changed": {"fields": ["value_based_price"]}}]	71	10
193	2020-09-27 15:10:07.821838+00	5	水晶吊燈	1	[{"added": {}}]	71	10
194	2020-09-27 15:12:00.911296+00	3	客廳	2	[{"changed": {"fields": ["related_items"]}}]	66	10
195	2020-09-27 15:13:53.685304+00	3	餐桌	2	[{"changed": {"fields": ["item_properties"]}}]	71	10
196	2020-09-27 15:16:33.729209+00	5	照明: 慳電膽	1	[{"added": {}}]	77	10
197	2020-09-27 15:17:03.217213+00	6	照明: LED 燈膽	1	[{"added": {}}]	77	10
198	2020-09-28 08:57:28.124578+00	7	自訂窗台	2	[{"changed": {"fields": ["custom_properties", "property_formulas"]}}]	65	1
199	2020-09-28 08:59:28.601102+00	6	自定義房間: 窗台面積	1	[{"added": {}}]	67	1
200	2020-09-28 09:00:22.121932+00	7	自定義房間	2	[{"changed": {"fields": ["is_active"]}}]	66	1
201	2020-09-28 09:10:07.618075+00	7	自訂窗台	2	[]	65	1
202	2020-09-28 09:17:31.693801+00	7	自訂窗台	2	[{"changed": {"fields": ["data_type"]}}]	65	1
203	2020-09-28 09:17:36.187194+00	6	自訂牆身	2	[{"changed": {"fields": ["data_type"]}}]	65	1
204	2020-09-28 09:17:42.681107+00	5	自訂地台	2	[{"changed": {"fields": ["data_type"]}}]	65	1
205	2020-09-28 09:17:46.394906+00	3	闊度	2	[{"changed": {"fields": ["data_type"]}}]	65	1
206	2020-09-28 09:17:49.824541+00	2	長度	2	[{"changed": {"fields": ["data_type"]}}]	65	1
207	2020-09-28 09:17:53.247967+00	1	高度	2	[{"changed": {"fields": ["data_type"]}}]	65	1
208	2020-09-29 11:49:18.0917+00	64	cat test project: 客廳: 客廳櫈	3		74	1
209	2020-09-29 11:49:26.562375+00	63	cat test project: 客廳: 客廳櫈	3		74	1
210	2020-09-29 11:49:26.563972+00	62	cat test project: 客廳: 客廳櫈	3		74	1
211	2020-09-29 11:49:26.564902+00	61	cat test project: 客廳: 客廳櫈	3		74	1
212	2020-09-29 11:49:26.565827+00	60	cat test project: 客廳: 客廳櫈	3		74	1
213	2020-09-29 11:57:30.09577+00	66	cat test project: 客廳: 客廳櫈	3		74	1
214	2020-09-29 11:57:30.107814+00	65	cat test project: 客廳: 客廳櫈	3		74	1
215	2020-09-29 11:57:30.108948+00	59	cat test project: 客廳: 客廳櫈	3		74	1
216	2020-10-06 09:49:42.474712+00	7	自訂窗台	2	[{"changed": {"fields": ["custom_property_formulas"]}}]	65	1
217	2020-10-07 07:18:19.274894+00	64	test: Testing	1	[{"added": {}}]	68	1
218	2020-10-07 07:18:30.272116+00	64	test: Testing Custom Room	2	[{"changed": {"fields": ["name"]}}]	68	1
219	2020-10-07 11:53:18.709268+00	4	客廳: Floor Area	2	[{"changed": {"fields": ["formula"]}}]	67	1
220	2020-10-08 05:36:53.205457+00	5	客廳: 牆身面積	2	[{"changed": {"fields": ["name"]}}]	67	10
221	2020-10-08 05:37:05.832287+00	4	客廳: 地板面積	2	[{"changed": {"fields": ["name"]}}]	67	10
222	2020-10-08 05:37:18.245022+00	2	廁所: 牆身面積	2	[{"changed": {"fields": ["name"]}}]	67	10
223	2020-10-08 05:37:29.041243+00	1	廁所: 地板面積	2	[{"changed": {"fields": ["name"]}}]	67	10
224	2020-10-08 20:33:23.035965+00	7	自訂窗台	2	[{"changed": {"fields": ["custom_properties", "custom_property_formulas"]}}]	65	1
225	2020-10-08 20:34:37.059895+00	6	自訂牆身	2	[{"changed": {"fields": ["custom_properties", "custom_property_formulas"]}}]	65	1
226	2020-10-08 20:36:05.528016+00	5	自訂地台	2	[{"changed": {"fields": ["custom_properties", "custom_property_formulas"]}}]	65	1
227	2020-10-08 20:56:52.469638+00	6	自訂牆身	2	[{"changed": {"fields": ["custom_properties"]}}]	65	1
228	2020-10-12 11:03:07.722028+00	13	fat cat company: test 1 expense: test expense 1	3		151	1
229	2020-10-14 07:11:54.431134+00	1	SubscriptionPlan object (1)	1	[{"added": {}}]	165	1
230	2020-10-14 07:22:18.951031+00	3	fat cat company Free Plan	1	[{"added": {}}]	164	1
231	2020-10-14 09:00:05.954142+00	2	Standard Plan	1	[{"added": {}}]	165	1
232	2020-10-14 09:01:27.52328+00	3	Advanced Plan	1	[{"added": {}}]	165	1
233	2020-10-14 09:02:57.665311+00	4	Professional Plan	1	[{"added": {}}]	165	1
234	2020-10-14 09:19:51.463297+00	2	Standard Plan	2	[{"changed": {"fields": ["top_bg_color", "bottom_bg_color"]}}]	165	1
235	2020-10-14 09:20:10.073795+00	3	Advanced Plan	2	[{"changed": {"fields": ["top_bg_color", "bottom_bg_color"]}}]	165	1
236	2020-10-14 09:20:21.63257+00	4	Professional Plan	2	[{"changed": {"fields": ["top_bg_color", "bottom_bg_color"]}}]	165	1
237	2020-10-19 09:17:12.011167+00	4	Professional Plan	2	[{"changed": {"fields": ["price"]}}]	165	1
238	2020-10-23 11:19:06.752059+00	16	test ac 1	2	[{"changed": {"fields": ["br_approved"]}}]	56	10
239	2020-10-25 06:22:15.169387+00	17	fat cat company	3		56	10
240	2020-10-27 03:36:05.223115+00	443	Token for +85267403305 (0ff0cebce43241b29b066c2e67648c3b)	2	[]	49	10
241	2020-10-27 03:36:12.188747+00	443	Token for +85267403305 (0ff0cebce43241b29b066c2e67648c3b)	2	[]	49	10
242	2020-10-27 03:43:52.861783+00	18	test 2	2	[{"changed": {"fields": ["br_approved"]}}]	56	10
243	2020-10-27 08:03:15.078575+00	15	ABC	2	[{"changed": {"fields": ["logo_pic"]}}]	56	1
244	2020-10-27 08:04:20.376237+00	15	ABC	2	[{"changed": {"fields": ["logo_pic"]}}]	56	1
245	2020-10-28 08:02:31.891656+00	3	水管	2	[{"changed": {"fields": ["item_type_materials"]}}]	76	1
246	2020-10-28 08:02:37.268983+00	2	傢俬	2	[{"changed": {"fields": ["item_type_materials"]}}]	76	1
247	2020-10-28 08:02:41.82915+00	1	照明	2	[{"changed": {"fields": ["item_type_materials"]}}]	76	1
248	2020-10-28 10:40:37.687509+00	1	照明	2	[{"changed": {"fields": ["item_type_materials"]}}]	76	1
249	2020-10-29 16:10:43.953467+00	85	a: 客廳: 客廳櫈	3		74	1
250	2020-10-29 16:10:48.657434+00	84	a: 客廳: 客廳櫈	3		74	1
251	2020-10-29 16:49:37.510848+00	89	a: 客廳: 吊燈	2	[{"changed": {"fields": ["remark"]}}]	74	1
252	2020-11-03 08:43:16.64305+00	6	2人睡房	2	[{"changed": {"fields": ["room_type_formulas"]}}]	66	1
253	2020-11-03 08:44:16.867193+00	6	2人睡房	2	[{"changed": {"fields": ["room_type_formulas"]}}]	66	1
254	2020-11-03 08:44:26.858739+00	5	1人睡房	2	[{"changed": {"fields": ["room_type_formulas"]}}]	66	1
255	2020-11-03 08:44:30.443541+00	4	飯廳	2	[{"changed": {"fields": ["room_type_formulas"]}}]	66	1
256	2020-11-03 08:44:34.396321+00	3	客廳	2	[{"changed": {"fields": ["room_type_formulas"]}}]	66	1
257	2020-11-03 08:44:37.476602+00	2	廚房	2	[{"changed": {"fields": ["room_type_formulas"]}}]	66	1
258	2020-11-03 08:44:41.011114+00	1	廁所	2	[{"changed": {"fields": ["room_type_formulas"]}}]	66	1
259	2020-11-03 09:32:21.797063+00	6	2人睡房	2	[{"changed": {"fields": ["room_type_formulas"]}}]	66	1
260	2020-11-03 09:32:29.302139+00	5	1人睡房	2	[{"changed": {"fields": ["room_type_formulas"]}}]	66	1
261	2020-11-03 09:32:33.473626+00	4	飯廳	2	[{"changed": {"fields": ["room_type_formulas"]}}]	66	1
262	2020-11-03 09:32:36.644216+00	3	客廳	2	[{"changed": {"fields": ["room_type_formulas"]}}]	66	1
263	2020-11-03 09:32:40.121866+00	2	廚房	2	[{"changed": {"fields": ["room_type_formulas"]}}]	66	1
264	2020-11-03 09:32:43.308131+00	1	廁所	2	[{"changed": {"fields": ["room_type_formulas"]}}]	66	1
265	2020-11-03 10:36:58.128917+00	81	test: 客廳	2	[{"changed": {"fields": ["value"]}}]	68	1
266	2020-11-05 07:56:35.261544+00	5	水晶吊燈	2	[{"changed": {"fields": ["item_formulas"]}}]	71	1
267	2020-11-05 07:57:05.023651+00	5	水晶吊燈	2	[{"changed": {"fields": ["item_formulas"]}}]	71	1
268	2020-11-05 07:57:19.231476+00	5	水晶吊燈	2	[{"changed": {"fields": ["item_formulas"]}}]	71	1
269	2020-11-05 07:59:06.837368+00	1	客廳櫈	2	[{"changed": {"fields": ["item_formulas"]}}]	71	1
270	2020-11-05 08:42:25.650024+00	1	客廳櫈	2	[{"changed": {"fields": ["item_formulas"]}}]	71	1
271	2020-11-05 08:42:36.575563+00	5	水晶吊燈	2	[{"changed": {"fields": ["item_formulas"]}}]	71	1
272	2020-11-06 08:07:14.373397+00	15	ABC	2	[{"changed": {"fields": ["br_pic_width", "br_pic_height"]}}]	56	1
273	2020-11-13 11:45:11.156413+00	31	ABC Co., Ltd2: a milestone 31 Test	2	[{"changed": {"fields": ["img_upload_date"]}}]	153	1
274	2020-11-20 13:25:12.701356+00	19	a	3		56	1
275	2020-11-20 13:25:12.716316+00	18	test 2	3		56	1
276	2020-11-20 13:25:12.721456+00	16	test ac 1	3		56	1
277	2020-11-20 13:25:12.722935+00	14	test ac 3	3		56	1
278	2020-11-20 13:25:12.723835+00	13	test2	3		56	1
279	2020-11-20 13:25:12.724719+00	12	abc	3		56	1
280	2020-11-20 13:25:12.725888+00	10	test	3		56	1
281	2020-11-20 13:25:12.726687+00	9	dog company	3		56	1
282	2020-11-20 13:25:12.728859+00	8	company 99	3		56	1
283	2020-11-20 13:25:12.730815+00	7	ABC Co., Ltd2	3		56	1
284	2020-11-20 13:25:12.731695+00	6	testing company2	3		56	1
285	2020-11-20 13:25:12.732502+00	5	Testing	3		56	1
286	2020-11-20 13:25:12.733704+00	1	testing1	3		56	1
287	2020-12-04 12:37:20.142949+00	22	a	3		56	1
288	2020-12-04 12:37:20.15226+00	21	小朋友公司	3		56	1
289	2020-12-04 18:38:22.045931+00	27	test 3	2	[{"changed": {"fields": ["br_approved"]}}]	56	10
290	2020-12-04 19:06:37.81012+00	28	a	3		56	1
291	2020-12-04 19:11:20.561704+00	29	a	3		56	1
292	2020-12-06 17:57:27.80997+00	32	test 4	2	[{"changed": {"fields": ["br_approved"]}}]	56	10
293	2020-12-06 18:00:08.216395+00	32	test 4	2	[{"changed": {"fields": ["br_approved"]}}]	56	10
294	2020-12-06 18:00:39.236465+00	32	test 4	2	[{"changed": {"fields": ["br_approved"]}}]	56	10
295	2020-12-06 18:01:23.941792+00	32	test 4	2	[{"changed": {"fields": ["br_approved"]}}]	56	10
296	2020-12-06 18:07:47.917237+00	32	test 4	2	[{"changed": {"fields": ["is_active"]}}]	56	10
297	2020-12-06 18:08:15.318473+00	32	test 4	2	[{"changed": {"fields": ["br_approved"]}}]	56	10
298	2020-12-07 05:06:44.416966+00	32	test 4	2	[{"changed": {"fields": ["br_approved"]}}]	56	10
299	2020-12-07 05:16:54.229217+00	32	test 4	2	[{"changed": {"fields": ["br_approved"]}}]	56	10
300	2020-12-07 10:36:03.503735+00	32	test 4	2	[{"changed": {"fields": ["br_approved"]}}]	56	10
301	2020-12-11 09:40:50.11228+00	2	水管	2	[{"changed": {"fields": ["item_formulas"]}}]	71	1
302	2020-12-11 09:40:55.360151+00	3	餐桌	2	[{"changed": {"fields": ["item_formulas"]}}]	71	1
303	2020-12-11 09:40:59.387272+00	4	吊燈	2	[{"changed": {"fields": ["item_formulas"]}}]	71	1
304	2020-12-11 09:44:29.74413+00	7	單人床	2	[{"changed": {"fields": ["item_formulas"]}}]	71	1
305	2020-12-11 09:44:35.340319+00	8	雙人床	2	[{"changed": {"fields": ["item_formulas"]}}]	71	1
306	2020-12-11 09:44:40.996433+00	10	洗手盤	2	[{"changed": {"fields": ["item_formulas"]}}]	71	1
307	2020-12-11 09:44:47.220368+00	11	座廁	2	[{"changed": {"fields": ["item_formulas"]}}]	71	1
308	2020-12-11 09:44:57.482682+00	14	代工安裝浴室寶 - 天花式	2	[{"changed": {"fields": ["item_formulas"]}}]	71	1
309	2020-12-11 09:45:01.944114+00	15	代工安裝浴室寶 - 窗口式	2	[{"changed": {"fields": ["item_formulas"]}}]	71	1
310	2020-12-11 09:45:07.369041+00	6	鋅盤	2	[{"changed": {"fields": ["item_formulas"]}}]	71	1
311	2020-12-11 09:45:24.330648+00	5	天花項目	2	[{"changed": {"fields": ["item_type_materials"]}}]	76	1
312	2020-12-11 09:45:28.130776+00	6	油漆項目	2	[{"changed": {"fields": ["item_type_materials"]}}]	76	1
313	2020-12-11 09:45:32.017485+00	7	鋁窗項目	2	[{"changed": {"fields": ["item_type_materials"]}}]	76	1
314	2020-12-12 06:43:28.682508+00	9	電燈項目: test 1	1	[{"added": {}}]	77	10
315	2020-12-12 06:44:57.89359+00	9	電燈項目: test 1	2	[]	77	10
316	2020-12-12 06:46:59.334849+00	22	test 2	1	[{"added": {}}]	71	10
317	2020-12-12 06:47:23.917677+00	22	test 2	2	[]	71	10
318	2020-12-12 06:47:44.051706+00	22	test 2	3		71	10
319	2021-01-13 06:38:53.750592+00	2	ABC Co., Ltd2: test image (1)	3		167	1
320	2021-01-13 06:39:33.368842+00	5	ABC Co., Ltd2: test image (1)	3		167	1
321	2021-01-13 06:39:49.826627+00	1	ABC Co., Ltd2: test image set (1)	3		166	1
322	2021-01-13 06:39:53.259619+00	2	ABC Co., Ltd2: test image set (1)	3		166	1
323	2021-01-13 06:40:00.701448+00	4	ABC Co., Ltd2: test image (1)	3		167	1
324	2021-01-13 06:40:00.702881+00	3	ABC Co., Ltd2: test image (1)	3		167	1
325	2021-01-13 06:40:00.703785+00	1	ABC Co., Ltd2: test image (1)	3		167	1
326	2021-01-13 06:47:34.624371+00	3	ABC Co., Ltd2: test image set (1)	3		166	1
327	2021-01-13 06:49:49.438648+00	15	ABC Co., Ltd2: test image (10)	3		167	1
328	2021-01-13 06:49:49.451524+00	14	ABC Co., Ltd2: test image (9)	3		167	1
329	2021-01-13 06:49:49.452681+00	13	ABC Co., Ltd2: test image (8)	3		167	1
330	2021-01-13 06:49:49.453615+00	12	ABC Co., Ltd2: test image (7)	3		167	1
331	2021-01-13 06:49:49.454476+00	11	ABC Co., Ltd2: test image (6)	3		167	1
332	2021-01-13 06:49:49.455536+00	10	ABC Co., Ltd2: test image (5)	3		167	1
333	2021-01-13 06:49:49.456388+00	9	ABC Co., Ltd2: test image (4)	3		167	1
334	2021-01-13 06:49:49.457228+00	8	ABC Co., Ltd2: test image (3)	3		167	1
335	2021-01-13 06:49:49.458084+00	7	ABC Co., Ltd2: test image (2)	3		167	1
336	2021-01-13 06:49:49.458926+00	6	ABC Co., Ltd2: test image (1)	3		167	1
337	2021-01-13 06:50:35.340643+00	4	ABC Co., Ltd2: test image set (1)	3		166	1
338	2021-01-13 06:51:25.04402+00	4	ABC Co., Ltd2: test image set (1)	3		166	1
339	2021-01-13 07:00:18.804316+00	5	ABC Co., Ltd2: test image set (1)	1	[{"added": {}}]	166	1
340	2021-01-13 07:00:25.336355+00	5	ABC Co., Ltd2: test image set (1)	3		166	1
341	2021-01-13 07:06:24.799048+00	35	ABC Co., Ltd2: test image (20)	3		167	1
342	2021-01-13 07:06:24.807955+00	34	ABC Co., Ltd2: test image (19)	3		167	1
343	2021-01-13 07:06:24.808922+00	33	ABC Co., Ltd2: test image (18)	3		167	1
344	2021-01-13 07:06:24.809839+00	32	ABC Co., Ltd2: test image (17)	3		167	1
345	2021-01-13 07:06:24.810699+00	31	ABC Co., Ltd2: test image (16)	3		167	1
346	2021-01-13 07:06:24.81153+00	30	ABC Co., Ltd2: test image (15)	3		167	1
347	2021-01-13 07:06:24.812436+00	29	ABC Co., Ltd2: test image (14)	3		167	1
348	2021-01-13 07:06:24.813296+00	28	ABC Co., Ltd2: test image (13)	3		167	1
349	2021-01-13 07:06:24.81402+00	27	ABC Co., Ltd2: test image (12)	3		167	1
350	2021-01-13 07:06:24.814737+00	26	ABC Co., Ltd2: test image (11)	3		167	1
351	2021-01-13 07:06:24.815447+00	25	ABC Co., Ltd2: test image (10)	3		167	1
352	2021-01-13 07:06:24.816175+00	24	ABC Co., Ltd2: test image (9)	3		167	1
353	2021-01-13 07:06:24.81688+00	23	ABC Co., Ltd2: test image (8)	3		167	1
354	2021-01-13 07:06:24.817595+00	22	ABC Co., Ltd2: test image (7)	3		167	1
355	2021-01-13 07:06:24.818338+00	21	ABC Co., Ltd2: test image (6)	3		167	1
356	2021-01-13 07:06:24.819264+00	20	ABC Co., Ltd2: test image (5)	3		167	1
357	2021-01-13 07:06:24.82012+00	19	ABC Co., Ltd2: test image (4)	3		167	1
358	2021-01-13 07:06:24.820865+00	18	ABC Co., Ltd2: test image (3)	3		167	1
359	2021-01-13 07:06:24.821574+00	17	ABC Co., Ltd2: test image (2)	3		167	1
360	2021-01-13 07:06:24.822287+00	16	ABC Co., Ltd2: test image (1)	3		167	1
361	2021-01-13 07:06:37.216443+00	8	ABC Co., Ltd2: test image set (3)	3		166	1
362	2021-01-13 07:06:37.217864+00	7	ABC Co., Ltd2: test image set (2)	3		166	1
363	2021-01-13 07:06:37.21876+00	6	ABC Co., Ltd2: test image set (1)	3		166	1
364	2021-01-13 07:07:34.478824+00	9	ABC Co., Ltd2: test image set (1)	2	[{"changed": {"fields": ["imgs"]}}]	166	1
365	2021-01-13 07:07:43.036101+00	9	ABC Co., Ltd2: test image set (1)	3		166	1
366	2021-01-13 07:13:49.2068+00	10	ABC Co., Ltd2: test image set (1)	1	[{"added": {}}]	166	1
367	2021-01-13 07:13:53.869039+00	10	ABC Co., Ltd2: test image set (1)	3		166	1
368	2021-01-13 07:14:51.054521+00	11	ABC Co., Ltd2: test image set (1)	1	[{"added": {}}]	166	1
369	2021-01-13 07:14:57.059879+00	11	ABC Co., Ltd2: test image set (1)	3		166	1
370	2021-01-13 07:16:13.493167+00	12	ABC Co., Ltd2: test image set (1)	1	[{"added": {}}]	166	1
371	2021-01-13 07:16:22.27173+00	12	ABC Co., Ltd2: test image set (1)	3		166	1
372	2021-01-13 07:19:14.566356+00	13	ABC Co., Ltd2: test image set (1)	1	[{"added": {}}]	166	1
373	2021-01-13 07:19:22.512502+00	13	ABC Co., Ltd2: test image set (1)	3		166	1
374	2021-01-13 07:19:51.253556+00	13	ABC Co., Ltd2: test image set (1)	3		166	1
375	2021-01-13 07:24:12.178535+00	47	ABC Co., Ltd2: test image (7)	3		167	1
376	2021-01-13 07:24:12.191637+00	46	ABC Co., Ltd2: test image (6)	3		167	1
377	2021-01-13 07:24:12.192608+00	45	ABC Co., Ltd2: test image (5)	3		167	1
378	2021-01-13 07:24:12.193471+00	44	ABC Co., Ltd2: test image (4)	3		167	1
379	2021-01-13 07:24:12.194345+00	43	ABC Co., Ltd2: test image (3)	3		167	1
380	2021-01-13 07:24:12.195234+00	42	ABC Co., Ltd2: test image (2)	3		167	1
381	2021-01-13 07:24:12.196146+00	36	ABC Co., Ltd2: test image (1)	3		167	1
382	2021-01-13 07:24:52.316155+00	14	ABC Co., Ltd2: test image set (1)	3		166	1
383	2021-01-13 11:51:49.701347+00	59	ABC Co., Ltd2: test image (7)	3		167	1
384	2021-01-13 11:51:49.710153+00	58	ABC Co., Ltd2: test image (6)	3		167	1
385	2021-01-13 11:54:09.36506+00	26	ABC Co., Ltd2: a111111111 milestone 26 testing	3		153	1
386	2021-01-13 11:55:30.635155+00	101	ABC Co., Ltd2: test milestone 101 testing	3		153	1
387	2021-01-13 12:50:53.773745+00	18	ABC Co., Ltd2: test milestone 102 test milestone 1 image set (1)	2	[{"changed": {"fields": ["project_milestone"]}}]	166	1
388	2021-01-13 14:18:03.801144+00	18	ABC Co., Ltd2: test milestone 102 test milestone 1 image set (1)	2	[{"changed": {"fields": ["project_milestone"]}}]	166	1
389	2021-01-20 09:22:11.080811+00	36	A	3		71	1
390	2021-01-20 09:22:11.082404+00	35	Testing	3		71	1
391	2021-01-20 09:22:18.531204+00	2	新造來水及去水 (暗喉)	2	[{"changed": {"fields": ["item_formulas"]}}]	71	1
392	2021-01-20 09:22:25.490007+00	4	吊燈	2	[{"changed": {"fields": ["item_formulas"]}}]	71	1
393	2021-01-20 09:22:36.789915+00	6	鋅盤	2	[{"changed": {"fields": ["item_formulas"]}}]	71	1
394	2021-01-20 09:22:40.928549+00	7	單人床	2	[{"changed": {"fields": ["item_formulas"]}}]	71	1
395	2021-01-20 09:22:48.954659+00	8	雙人床	2	[{"changed": {"fields": ["item_formulas"]}}]	71	1
396	2021-01-20 09:22:59.853591+00	9	磁磚	2	[{"changed": {"fields": ["item_formulas"]}}]	71	1
397	2021-01-20 09:23:03.075147+00	10	洗手盤	2	[{"changed": {"fields": ["item_formulas"]}}]	71	1
398	2021-01-20 09:23:17.350655+00	11	座廁	2	[{"changed": {"fields": ["item_formulas"]}}]	71	1
399	2021-01-20 09:23:34.213987+00	14	代工安裝浴室寶 - 天花式	2	[{"changed": {"fields": ["item_formulas"]}}]	71	1
400	2021-01-20 09:23:38.254653+00	15	代工安裝浴室寶 - 窗口式	2	[{"changed": {"fields": ["item_formulas"]}}]	71	1
401	2021-01-20 09:23:43.648614+00	17	新造全高衣櫃	2	[{"changed": {"fields": ["item_formulas"]}}]	71	1
402	2021-01-20 09:23:47.085103+00	18	新造床頭櫃	2	[{"changed": {"fields": ["item_formulas"]}}]	71	1
403	2021-01-20 09:23:49.813205+00	20	新造13A雙位制	2	[{"changed": {"fields": ["item_formulas"]}}]	71	1
404	2021-01-20 09:23:53.682313+00	21	新造13A單位制	2	[{"changed": {"fields": ["item_formulas"]}}]	71	1
405	2021-01-20 09:23:59.89646+00	25	新造泥水腳座	2	[{"changed": {"fields": ["item_formulas"]}}]	71	1
406	2021-01-20 09:24:03.341449+00	26	新砌泥水企缸	2	[{"changed": {"fields": ["item_formulas"]}}]	71	1
407	2021-01-20 09:24:06.332407+00	27	新造企缸位連地台及牆身防水	2	[{"changed": {"fields": ["item_formulas"]}}]	71	1
408	2021-01-20 09:24:09.848363+00	28	新造雲石吸咀	2	[{"changed": {"fields": ["item_formulas"]}}]	71	1
409	2021-01-20 09:24:28.885602+00	31	修葺拆牆後泥水批當	2	[{"changed": {"fields": ["item_formulas"]}}]	71	1
410	2021-01-20 09:24:32.616792+00	32	新造窗口窗邊雲石	2	[{"changed": {"fields": ["item_formulas"]}}]	71	1
411	2021-01-20 09:24:35.17641+00	34	/	2	[{"changed": {"fields": ["item_formulas"]}}]	71	1
412	2021-01-29 04:14:20.788943+00	57	代工安裝浴室潔具	2	[{"changed": {"fields": ["item_formulas"]}}]	71	1
413	2021-01-29 04:16:58.387478+00	56	新造來去水喉(浴室)	2	[{"changed": {"fields": ["item_formulas"]}}]	71	1
414	2021-01-29 04:17:32.386109+00	56	新造來去水喉(浴室)	2	[{"changed": {"fields": ["item_formulas"]}}]	71	1
415	2021-01-29 04:17:43.385692+00	55	新造來去水喉(廚房)	2	[{"changed": {"fields": ["item_formulas"]}}]	71	1
416	2021-01-29 13:22:41.092757+00	60	新造假天花	2	[{"changed": {"fields": ["item_formulas"]}}]	71	1
417	2021-01-30 06:55:23.634554+00	61	新造假天花燈槽	2	[{"changed": {"fields": ["item_formulas"]}}]	71	1
418	2021-01-30 06:56:54.622597+00	61	新造假天花燈槽	2	[{"changed": {"fields": ["item_formulas"]}}]	71	1
419	2021-02-01 09:49:02.498372+00	1	長度	2	[{"changed": {"fields": ["index"]}}]	75	1
420	2021-02-01 09:49:25.755563+00	1	長度	2	[{"changed": {"fields": ["index"]}}]	75	1
421	2021-02-01 09:49:31.276075+00	2	闊度	2	[{"changed": {"fields": ["index"]}}]	75	1
422	2021-02-01 09:49:36.604366+00	3	高度	2	[{"changed": {"fields": ["index"]}}]	75	1
423	2021-02-01 10:43:22.815024+00	10	睡房(有窗台)	2	[{"changed": {"fields": ["room_type_formulas"]}}]	66	1
424	2021-02-01 10:53:43.679486+00	9	備注	2	[{"changed": {"fields": ["custom_properties", "custom_property_formulas"]}}]	65	1
425	2021-02-01 10:53:54.919355+00	8	有窗台	2	[{"changed": {"fields": ["custom_properties", "custom_property_formulas"]}}]	65	1
426	2021-02-01 10:54:03.038109+00	3	闊度	2	[{"changed": {"fields": ["custom_properties", "custom_property_formulas"]}}]	65	1
427	2021-02-01 10:54:08.644985+00	2	長度	2	[{"changed": {"fields": ["custom_properties", "custom_property_formulas"]}}]	65	1
428	2021-02-01 10:54:14.648855+00	1	高度	2	[{"changed": {"fields": ["custom_properties", "custom_property_formulas"]}}]	65	1
429	2021-02-02 09:07:01.634364+00	1	高度	2	[{"changed": {"fields": ["index"]}}]	65	1
430	2021-02-02 09:07:09.411561+00	3	闊度	2	[{"changed": {"fields": ["index"]}}]	65	1
431	2021-02-02 09:07:18.872539+00	2	長度	2	[{"changed": {"fields": ["index"]}}]	65	1
432	2021-02-11 03:55:13.429676+00	199	a111111111: 1人睡房: 新造床頭櫃	2	[{"changed": {"fields": ["value"]}}]	74	1
433	2021-02-15 13:01:49.38235+00	471	職熱權口業: 飯廳: Test	3		74	1
434	2021-02-15 13:02:22.199591+00	221	a111111111: Test	3		68	1
435	2021-02-15 13:03:00.236966+00	16	Test	3		66	1
436	2021-02-15 13:05:00.440223+00	466	123: 飯廳: Test	3		74	1
437	2021-02-16 05:53:03.49297+00	39	新造牆身乳膠漆(包括由防潮油批灰打磨)	2	[{"changed": {"fields": ["item_properties"]}}]	71	1
438	2021-02-24 04:32:36.605218+00	94	ABC Co., Ltd2: a111111111: 清拆客廳地板	2	[{"changed": {"fields": ["remark"]}}]	149	1
439	2021-02-24 04:44:45.272333+00	95	ABC Co., Ltd2: a111111111: 第三者保險	2	[{"changed": {"fields": ["remark"]}}]	149	1
440	2021-02-24 04:55:57.044377+00	130	ABC Co., Ltd2: test: 清拆客廳地板	2	[{"changed": {"fields": ["remark"]}}]	149	1
441	2021-02-24 05:05:37.65186+00	179	ABC Co., Ltd2: test: 清拆客廳地板	2	[{"changed": {"fields": ["remark"]}}]	149	1
442	2021-02-24 09:20:53.9835+00	1	浴室	2	[{"changed": {"fields": ["room_properties_sort"]}}]	66	1
443	2021-02-24 09:21:27.604496+00	1	浴室	2	[{"changed": {"fields": ["room_properties_sort"]}}]	66	1
444	2021-02-24 09:28:30.918059+00	1	浴室	2	[{"changed": {"fields": ["room_properties_sort"]}}]	66	1
445	2021-02-24 09:43:38.148734+00	1	浴室	2	[{"changed": {"fields": ["room_properties_sort"]}}]	66	1
446	2021-02-24 09:52:47.926598+00	1	浴室	2	[{"changed": {"fields": ["room_properties_sort"]}}]	66	1
447	2021-02-24 10:24:59.877952+00	10	睡房(有窗台)	2	[{"changed": {"fields": ["room_properties_sort"]}}]	66	1
448	2021-02-24 11:18:43.698964+00	1	浴室	2	[{"changed": {"fields": ["related_items_sort"]}}]	66	1
449	2021-02-24 11:19:10.22266+00	1	浴室	2	[{"changed": {"fields": ["related_items_sort"]}}]	66	1
450	2021-02-24 12:33:13.932678+00	1	浴室	2	[{"changed": {"fields": ["related_items_sort"]}}]	66	1
451	2021-02-24 12:33:28.266024+00	1	浴室	2	[{"changed": {"fields": ["related_items_sort"]}}]	66	1
452	2021-02-25 10:37:45.043606+00	178	ABC Co., Ltd2: test	2	[{"changed": {"fields": ["document_format"]}}]	63	1
453	2021-02-25 10:38:43.860837+00	178	ABC Co., Ltd2: test	2	[{"changed": {"fields": ["document_format"]}}]	63	1
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	auth	permission
2	auth	group
3	contenttypes	contenttype
4	sessions	session
5	common	user
6	common	address
7	common	attachments
8	common	comment
9	common	comment_files
10	common	document
11	common	google
12	common	apisettings
13	common	profile
14	accounts	account
15	accounts	tags
16	accounts	email
17	accounts	emaillog
18	cases	case
19	contacts	contact
20	emails	email
21	leads	lead
22	opportunity	opportunity
23	planner	event
24	planner	reminder
25	thumbnail	kvstore
26	marketing	campaign
27	marketing	campaignlinkclick
28	marketing	campaignlog
29	marketing	campaignopen
30	marketing	contact
31	marketing	contactlist
32	marketing	emailtemplate
33	marketing	link
34	marketing	tag
35	marketing	failedcontact
36	marketing	campaigncompleted
37	marketing	contactunsubscribedcampaign
38	marketing	contactemailcampaign
39	marketing	duplicatecontacts
40	marketing	blockedemail
41	marketing	blockeddomain
42	tasks	task
43	invoices	invoice
44	invoices	invoicehistory
45	events	event
46	teams	teams
47	admin	logentry
48	token_blacklist	blacklistedtoken
49	token_blacklist	outstandingtoken
50	quotations	quotation
51	quotations	quotationhistory
52	function_items	functionitem
53	function_items	functionitemhistory
54	function_items	subfunctionitem
55	function_items	subfunctionitemhistory
56	companies	company
57	companies	email
58	companies	tags
59	companies	generalremark
60	companies	emaillog
61	companies	documentformat
62	companies	chargingstage
63	projects	project
64	projects	projecthistory
65	rooms	roomproperty
66	rooms	roomtype
67	rooms	roomtypeformula
68	rooms	room
69	rooms	roomtypeproperty
70	customers	customer
71	project_items	item
72	project_items	projectitem
73	rooms	roomtypeproperties
74	rooms	roomitem
75	project_items	itemproperty
76	project_items	itemtype
77	project_items	itemtypematerial
78	companies	chargingstages
79	projects	projectchargingstages
80	project_items	itemformula
113	project_items	misc
114	project_items	misctype
115	project_items	projectmisc
116	project_items	expendtype
117	project_items	projectexpend
149	project_misc	projectmisc
150	project_misc	misc
152	project_expenses	expensetype
151	project_expenses	projectexpense
153	project_timetable	projectmilestone
154	project_timetable	projectwork
155	companies	documentheaderinformation
156	companies	invoicegeneralremark
157	companies	quotationgeneralremark
158	companies	receiptgeneralremark
159	projects	projectinvoice
160	projects	projectreceipt
161	projects	projectcomparisons
162	projects	projectcomparison
163	projects	companyprojectcomparison
164	subscription_plans	companysubscribedplan
165	subscription_plans	subscriptionplan
166	projects	projectimageset
167	projects	projectimage
\.


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	accounts	0001_initial	2020-06-22 07:28:58.686441+00
2	cases	0001_initial	2020-06-22 07:28:58.706667+00
3	common	0001_initial	2020-06-22 07:28:58.761346+00
4	teams	0001_initial	2020-06-22 07:28:58.793186+00
5	teams	0002_auto_20190624_1250	2020-06-22 07:28:58.821456+00
6	teams	0003_auto_20190909_1621	2020-06-22 07:28:58.86799+00
7	contacts	0001_initial	2020-06-22 07:28:58.894527+00
8	contacts	0002_auto_20190212_1334	2020-06-22 07:28:58.983858+00
9	contacts	0002_auto_20190210_1810	2020-06-22 07:28:58.997553+00
10	contacts	0003_merge_20190214_1427	2020-06-22 07:28:58.999163+00
11	leads	0001_initial	2020-06-22 07:28:59.028468+00
12	accounts	0002_auto_20190128_1237	2020-06-22 07:28:59.155313+00
13	accounts	0003_auto_20190201_1840	2020-06-22 07:28:59.202994+00
14	leads	0002_lead_tags	2020-06-22 07:28:59.239173+00
15	leads	0003_auto_20190211_1142	2020-06-22 07:28:59.269999+00
16	leads	0004_auto_20190212_1334	2020-06-22 07:28:59.387104+00
17	accounts	0004_account_status	2020-06-22 07:28:59.446335+00
18	accounts	0005_auto_20190212_1334	2020-06-22 07:28:59.602774+00
19	accounts	0006_auto_20190212_1708	2020-06-22 07:28:59.964085+00
20	accounts	0007_email	2020-06-22 07:28:59.997119+00
21	accounts	0008_account_assigned_to	2020-06-22 07:29:00.033375+00
22	accounts	0009_auto_20190809_1659	2020-06-22 07:29:00.302628+00
23	accounts	0010_account_teams	2020-06-22 07:29:00.346282+00
24	contenttypes	0001_initial	2020-06-22 07:29:00.363027+00
25	contenttypes	0002_remove_content_type_name	2020-06-22 07:29:00.406112+00
26	auth	0001_initial	2020-06-22 07:29:00.433856+00
27	auth	0002_alter_permission_name_max_length	2020-06-22 07:29:00.450273+00
28	auth	0003_alter_user_email_max_length	2020-06-22 07:29:00.459841+00
29	auth	0004_alter_user_username_opts	2020-06-22 07:29:00.470966+00
30	auth	0005_alter_user_last_login_null	2020-06-22 07:29:00.480951+00
31	auth	0006_require_contenttypes_0002	2020-06-22 07:29:00.482532+00
32	auth	0007_alter_validators_add_error_messages	2020-06-22 07:29:00.491838+00
33	auth	0008_alter_user_username_max_length	2020-06-22 07:29:00.501332+00
34	auth	0009_alter_user_last_name_max_length	2020-06-22 07:29:00.511068+00
35	auth	0010_alter_group_name_max_length	2020-06-22 07:29:00.520317+00
36	auth	0011_update_proxy_permissions	2020-06-22 07:29:00.557191+00
37	cases	0002_auto_20190128_1237	2020-06-22 07:29:00.702187+00
38	cases	0003_auto_20190212_1334	2020-06-22 07:29:00.850097+00
39	cases	0004_case_teams	2020-06-22 07:29:00.888681+00
40	events	0001_initial	2020-06-22 07:29:00.940504+00
41	events	0002_event_date_of_meeting	2020-06-22 07:29:00.988639+00
42	tasks	0001_initial	2020-06-22 07:29:01.039522+00
43	tasks	0002_task_created_by	2020-06-22 07:29:01.094263+00
44	opportunity	0001_initial	2020-06-22 07:29:01.155738+00
45	common	0002_auto_20190128_1237	2020-06-22 07:29:01.758967+00
46	planner	0001_initial	2020-06-22 07:29:02.070454+00
47	planner	0002_auto_20190212_1334	2020-06-22 07:29:02.308316+00
48	opportunity	0002_opportunity_tags	2020-06-22 07:29:02.442421+00
49	opportunity	0003_auto_20190212_1334	2020-06-22 07:29:02.651486+00
50	common	0003_document	2020-06-22 07:29:02.720194+00
51	common	0004_attachments_case	2020-06-22 07:29:02.793404+00
52	common	0005_auto_20190204_1400	2020-06-22 07:29:02.973976+00
53	common	0006_comment_user	2020-06-22 07:29:03.042144+00
54	common	0007_auto_20190212_1334	2020-06-22 07:29:03.301689+00
55	common	0008_google	2020-06-22 07:29:03.367723+00
56	common	0009_document_shared_to	2020-06-22 07:29:03.437056+00
57	common	0010_apisettings	2020-06-22 07:29:03.515363+00
58	common	0011_auto_20190218_1230	2020-06-22 07:29:03.588234+00
59	common	0012_apisettings_website	2020-06-22 07:29:03.651713+00
60	common	0013_auto_20190508_1540	2020-06-22 07:29:03.796622+00
61	invoices	0001_initial	2020-06-22 07:29:03.943+00
62	invoices	0002_auto_20190524_1113	2020-06-22 07:29:04.018719+00
63	common	0014_auto_20190524_1113	2020-06-22 07:29:04.175163+00
64	common	0015_auto_20190604_1830	2020-06-22 07:29:04.337008+00
65	common	0016_auto_20190624_1816	2020-06-22 07:29:04.558888+00
66	common	0017_auto_20190722_1443	2020-06-22 07:29:04.830226+00
67	common	0018_document_teams	2020-06-22 07:29:04.908093+00
68	contacts	0004_contact_teams	2020-06-22 07:29:04.991513+00
69	emails	0001_initial	2020-06-22 07:29:05.006091+00
70	events	0003_event_teams	2020-06-22 07:29:05.08599+00
71	invoices	0003_auto_20190527_1620	2020-06-22 07:29:05.238313+00
72	invoices	0004_auto_20190603_1844	2020-06-22 07:29:05.312497+00
73	invoices	0005_invoicehistory	2020-06-22 07:29:05.467061+00
74	invoices	0006_invoice_account	2020-06-22 07:29:05.562484+00
75	invoices	0007_auto_20190909_1621	2020-06-22 07:29:05.644264+00
76	invoices	0008_invoice_teams	2020-06-22 07:29:05.731383+00
77	leads	0005_auto_20190212_1708	2020-06-22 07:29:06.358515+00
78	leads	0006_auto_20190218_1217	2020-06-22 07:29:06.439928+00
79	leads	0007_auto_20190306_1226	2020-06-22 07:29:06.521248+00
80	leads	0008_auto_20190315_1503	2020-06-22 07:29:06.756765+00
81	leads	0009_lead_created_from_site	2020-06-22 07:29:06.902809+00
82	leads	0010_lead_teams	2020-06-22 07:29:06.992646+00
83	marketing	0001_initial	2020-06-22 07:29:08.52114+00
84	marketing	0002_auto_20190307_1227	2020-06-22 07:29:09.01448+00
85	marketing	0003_failedcontact	2020-06-22 07:29:09.183612+00
86	marketing	0004_auto_20190315_1443	2020-06-22 07:29:09.377367+00
87	marketing	0005_campaign_timezone	2020-06-22 07:29:09.472114+00
88	marketing	0006_campaign_attachment	2020-06-22 07:29:09.567245+00
89	marketing	0007_auto_20190611_1226	2020-06-22 07:29:09.865496+00
90	marketing	0008_auto_20190612_1905	2020-06-22 07:29:10.668306+00
91	marketing	0009_auto_20190618_1144	2020-06-22 07:29:10.990029+00
92	marketing	0010_auto_20190805_1038	2020-06-22 07:29:11.528358+00
93	marketing	0011_auto_20190904_1143	2020-06-22 07:29:11.734637+00
94	marketing	0012_auto_20190909_1621	2020-06-22 07:29:11.764786+00
95	marketing	0013_blockeddomain_blockedemail	2020-06-22 07:29:11.96842+00
96	opportunity	0004_opportunity_teams	2020-06-22 07:29:12.163502+00
97	sessions	0001_initial	2020-06-22 07:29:12.177984+00
98	tasks	0003_task_created_on	2020-06-22 07:29:12.277616+00
99	tasks	0004_task_teams	2020-06-22 07:29:12.387556+00
100	thumbnail	0001_initial	2020-06-22 07:29:12.402149+00
101	accounts	0011_auto_20200504_1823	2020-06-22 07:54:32.378175+00
102	admin	0001_initial	2020-06-22 07:54:32.506084+00
103	admin	0002_logentry_remove_auto_add	2020-06-22 07:54:32.615637+00
104	admin	0003_logentry_add_action_flag_choices	2020-06-22 07:54:32.719604+00
105	contacts	0005_auto_20200429_1746	2020-06-22 07:54:33.332629+00
106	contacts	0006_contact_profile_pic	2020-06-22 07:54:33.439602+00
107	contacts	0007_auto_20200622_1554	2020-06-22 07:54:33.557551+00
108	companies	0001_initial	2020-06-22 07:54:34.793877+00
109	cases	0005_remove_case_account	2020-06-22 07:54:34.957768+00
110	cases	0006_case_company	2020-06-22 07:54:35.08642+00
111	quotations	0001_initial	2020-06-22 07:54:35.371446+00
112	common	0019_auto_20200429_1746	2020-06-22 07:54:35.464343+00
113	common	0020_auto_20200504_1823	2020-06-22 07:54:35.719563+00
114	common	0021_auto_20200506_1732	2020-06-22 07:54:36.290168+00
115	common	0022_auto_20200622_1554	2020-06-22 07:54:37.559578+00
116	function_items	0001_initial	2020-06-22 07:54:37.692347+00
117	function_items	0002_auto_20200507_1601	2020-06-22 07:54:38.284669+00
118	function_items	0003_auto_20200507_1642	2020-06-22 07:54:38.525475+00
119	function_items	0004_functionitem_price	2020-06-22 07:54:38.659888+00
120	function_items	0005_auto_20200508_1758	2020-06-22 07:54:38.783597+00
121	function_items	0006_functionitem_status	2020-06-22 07:54:39.0115+00
122	function_items	0007_auto_20200514_1544	2020-06-22 07:54:39.19817+00
123	function_items	0008_functionitem_approved_by	2020-06-22 07:54:39.377072+00
124	function_items	0009_auto_20200514_1759	2020-06-22 07:54:39.871441+00
125	function_items	0010_auto_20200514_1812	2020-06-22 07:54:39.99356+00
126	function_items	0011_auto_20200514_1837	2020-06-22 07:54:40.137816+00
127	function_items	0012_functionitemhistory_changed_data	2020-06-22 07:54:40.267217+00
128	function_items	0013_auto_20200622_1554	2020-06-22 07:54:40.875856+00
129	projects	0001_initial	2020-06-22 07:54:41.198875+00
130	customers	0001_initial	2020-06-22 07:54:41.41328+00
131	customers	0002_customer_project	2020-06-22 07:54:41.766424+00
132	invoices	0009_auto_20200622_1554	2020-06-22 07:54:42.078143+00
133	leads	0011_auto_20200622_1554	2020-06-22 07:54:42.506411+00
134	opportunity	0005_auto_20200622_1554	2020-06-22 07:54:43.067329+00
135	planner	0003_auto_20200622_1554	2020-06-22 07:54:43.226211+00
136	project_items	0001_initial	2020-06-22 07:54:43.64718+00
137	quotations	0002_auto_20200508_1653	2020-06-22 07:54:44.024344+00
138	quotations	0003_auto_20200513_1817	2020-06-22 07:54:44.432469+00
139	quotations	0004_remove_quotationhistory_currency	2020-06-22 07:54:44.579081+00
140	quotations	0005_auto_20200514_1555	2020-06-22 07:54:44.878955+00
141	quotations	0006_auto_20200514_1751	2020-06-22 07:54:45.357684+00
142	quotations	0007_auto_20200515_1420	2020-06-22 07:54:45.523182+00
143	quotations	0008_auto_20200515_1434	2020-06-22 07:54:45.686635+00
144	quotations	0009_auto_20200515_1442	2020-06-22 07:54:45.938272+00
145	quotations	0010_remove_quotationhistory_total_amount	2020-06-22 07:54:46.082507+00
146	quotations	0011_auto_20200518_1800	2020-06-22 07:54:46.868552+00
147	quotations	0012_auto_20200622_1554	2020-06-22 07:54:47.989972+00
148	rooms	0001_initial	2020-06-22 07:54:48.209526+00
149	tasks	0005_auto_20200622_1554	2020-06-22 07:54:48.684322+00
150	token_blacklist	0001_initial	2020-06-22 07:54:49.099769+00
151	token_blacklist	0002_outstandingtoken_jti_hex	2020-06-22 07:54:49.345323+00
152	token_blacklist	0003_auto_20171017_2007	2020-06-22 07:54:49.520195+00
153	token_blacklist	0004_auto_20171017_2013	2020-06-22 07:54:49.67115+00
154	token_blacklist	0005_remove_outstandingtoken_jti	2020-06-22 07:54:49.81975+00
155	token_blacklist	0006_auto_20171017_2113	2020-06-22 07:54:50.172467+00
156	token_blacklist	0007_auto_20171017_2214	2020-06-22 07:54:50.477744+00
157	common	0023_auto_20200622_1555	2020-06-22 07:55:45.292292+00
158	common	0024_auto_20200622_1635	2020-06-22 08:35:42.177516+00
159	rooms	0002_auto_20200623_1748	2020-06-23 09:48:36.56696+00
160	rooms	0003_auto_20200623_1748	2020-06-23 09:48:36.639218+00
161	rooms	0004_auto_20200623_1935	2020-06-23 11:35:10.853542+00
162	project_items	0002_auto_20200624_1609	2020-06-24 08:09:59.27418+00
163	rooms	0005_roomitem	2020-06-24 08:09:59.509009+00
164	companies	0002_auto_20200624_1701	2020-06-24 09:01:58.283605+00
165	companies	0003_auto_20200624_1711	2020-06-24 09:12:03.99178+00
166	projects	0002_projectchargingstages	2020-06-24 09:16:01.115502+00
167	project_items	0003_itemformula	2020-06-24 11:08:36.914746+00
200	project_items	0004_auto_20200626_1549	2020-06-26 07:49:31.76183+00
201	project_items	0005_item_preset_unit_price	2020-06-26 08:18:58.347737+00
202	rooms	0006_roomitem_material	2020-06-26 08:34:06.923877+00
203	rooms	0007_roomitem_remark	2020-06-26 09:23:01.341477+00
204	rooms	0008_auto_20200626_1744	2020-06-26 09:44:36.932217+00
205	rooms	0009_roomtype_related_items	2020-06-26 11:05:03.108072+00
206	project_items	0006_auto_20200629_1609	2020-06-29 08:11:51.32963+00
207	project_items	0007_itemtypematerial_value_based_price	2020-06-29 08:11:51.367323+00
208	rooms	0010_auto_20200629_1723	2020-06-29 09:23:26.375958+00
209	project_items	0008_auto_20200629_1930	2020-06-29 11:35:08.785308+00
210	project_items	0009_auto_20200703_1644	2020-07-03 08:44:19.967403+00
211	rooms	0011_auto_20200703_1644	2020-07-03 08:44:20.283728+00
212	project_items	0010_auto_20200703_1657	2020-07-03 08:57:23.176563+00
213	project_items	0011_auto_20200703_1838	2020-07-03 10:38:41.47585+00
214	project_items	0012_auto_20200703_1907	2020-07-03 11:07:32.798357+00
247	project_items	0013_auto_20200706_1631	2020-07-06 08:31:57.087763+00
248	project_expenses	0001_initial	2020-07-06 08:33:48.460618+00
249	project_misc	0001_initial	2020-07-06 08:33:48.716227+00
250	project_expenses	0002_auto_20200706_1637	2020-07-06 08:37:42.856554+00
251	projects	0003_project_charging_stages	2020-07-06 08:57:40.215941+00
252	projects	0004_auto_20200706_1713	2020-07-06 09:13:54.574305+00
253	projects	0005_project_document_format	2020-07-06 09:18:37.944325+00
254	project_timetable	0001_initial	2020-07-06 11:04:21.603158+00
255	companies	0004_auto_20200709_1950	2020-07-09 11:50:13.275251+00
256	common	0025_auto_20200902_2340	2020-09-02 15:41:03.214466+00
257	companies	0005_auto_20200902_2340	2020-09-02 15:41:04.769991+00
258	project_expenses	0003_auto_20200902_2340	2020-09-02 15:41:05.694163+00
259	project_items	0014_auto_20200902_2340	2020-09-02 15:41:06.143676+00
260	projects	0006_auto_20200902_2340	2020-09-02 15:41:08.192536+00
261	project_timetable	0002_auto_20200902_2340	2020-09-02 15:41:08.4885+00
262	quotations	0013_auto_20200902_2340	2020-09-02 15:41:09.399257+00
263	rooms	0012_auto_20200902_2340	2020-09-02 15:41:09.554288+00
264	rooms	0013_auto_20200903_1620	2020-09-03 08:21:02.454896+00
265	rooms	0014_auto_20200904_0030	2020-09-03 16:30:42.132511+00
266	rooms	0015_auto_20200904_0334	2020-09-03 19:34:28.459689+00
267	rooms	0016_auto_20200904_0433	2020-09-03 20:34:03.731789+00
268	common	0026_auto_20200905_0443	2020-09-04 20:43:35.713256+00
269	common	0027_auto_20200905_1821	2020-09-05 10:21:15.293821+00
270	project_timetable	0003_projectmilestone_img	2020-09-16 09:11:35.707273+00
271	rooms	0017_auto_20200918_1523	2020-09-18 07:23:57.777963+00
272	rooms	0018_auto_20200918_1840	2020-09-18 10:40:53.454469+00
273	project_expenses	0004_projectexpense_img	2020-09-20 07:22:37.368282+00
274	projects	0007_auto_20200922_1737	2020-09-22 09:37:20.308248+00
275	companies	0006_auto_20200924_1830	2020-09-24 10:30:20.729606+00
276	companies	0007_documentformat_project_lower_format	2020-09-24 10:48:16.182471+00
277	project_expenses	0005_auto_20200927_0403	2020-09-26 20:03:49.522084+00
278	rooms	0019_auto_20200929_1857	2020-09-29 10:57:37.759794+00
279	rooms	0020_remove_roomproperty_property_formulas	2020-10-06 06:17:44.07123+00
280	projects	0008_projectcomparisons	2020-10-12 09:15:54.289565+00
281	rooms	0021_auto_20201012_1715	2020-10-12 09:15:54.33372+00
282	projects	0009_auto_20201012_1719	2020-10-12 09:19:32.535617+00
283	projects	0010_auto_20201012_1832	2020-10-12 10:32:19.28233+00
284	project_expenses	0006_projectexpense_img_upload_date	2020-10-12 11:00:41.176564+00
285	project_timetable	0004_projectmilestone_img_upload_date	2020-10-12 11:00:41.226537+00
286	projects	0011_auto_20201013_1835	2020-10-13 10:35:22.724989+00
287	subscription_plans	0001_initial	2020-10-14 06:54:00.452885+00
288	subscription_plans	0002_auto_20201014_1520	2020-10-14 07:20:41.61501+00
289	subscription_plans	0003_auto_20201014_1522	2020-10-14 07:22:15.436278+00
290	subscription_plans	0004_auto_20201014_1658	2020-10-14 08:58:44.622613+00
291	subscription_plans	0005_auto_20201014_1700	2020-10-14 09:00:52.756374+00
292	subscription_plans	0006_auto_20201014_1702	2020-10-14 09:02:40.24875+00
293	subscription_plans	0007_subscriptionplan_bg_color	2020-10-14 09:13:35.574442+00
294	subscription_plans	0008_auto_20201014_1718	2020-10-14 09:18:29.183351+00
295	subscription_plans	0009_auto_20201015_1830	2020-10-15 10:31:10.225005+00
296	subscription_plans	0010_auto_20201019_1718	2020-10-19 09:19:00.560981+00
297	subscription_plans	0011_auto_20201021_1744	2020-10-21 09:44:13.946879+00
298	subscription_plans	0012_auto_20201021_1812	2020-10-21 10:12:29.55726+00
299	companies	0008_auto_20201027_1404	2020-10-27 06:36:52.707118+00
300	companies	0009_auto_20201027_1436	2020-10-27 06:49:19.948234+00
301	companies	0010_auto_20201027_1440	2020-10-27 06:49:20.477293+00
302	companies	0011_auto_20201027_1441	2020-10-27 06:49:20.480376+00
303	companies	0012_auto_20201027_1445	2020-10-27 06:49:21.13161+00
304	companies	0013_auto_20201027_1452	2020-10-27 06:52:30.969982+00
305	companies	0014_auto_20201027_1646	2020-10-27 08:47:00.45894+00
306	project_items	0015_itemtype_item_materials	2020-10-27 13:31:04.754848+00
307	project_items	0016_auto_20201027_2130	2020-10-27 13:31:04.784519+00
308	project_items	0017_auto_20201027_2137	2020-10-27 13:37:48.113992+00
309	project_items	0018_auto_20201028_1601	2020-10-28 08:02:28.96497+00
310	rooms	0022_auto_20201029_2348	2020-10-29 15:49:06.427246+00
311	rooms	0023_remove_roomitem_material_s	2020-10-29 15:49:52.926534+00
312	rooms	0024_auto_20201103_1620	2020-11-03 08:20:17.716392+00
313	project_items	0019_auto_20201105_1536	2020-11-05 07:36:45.898615+00
314	project_items	0020_auto_20201105_1709	2020-11-05 09:09:43.314918+00
315	project_items	0021_auto_20201105_1714	2020-11-05 09:14:11.844469+00
316	project_items	0022_auto_20201105_1852	2020-11-05 10:52:37.857446+00
317	project_expenses	0007_auto_20201105_1858	2020-11-05 10:58:43.048373+00
318	companies	0015_auto_20201106_1556	2020-11-06 07:56:44.632265+00
319	project_timetable	0005_auto_20201106_1556	2020-11-06 07:56:44.808738+00
320	companies	0016_auto_20201106_1608	2020-11-06 08:08:24.468477+00
321	project_expenses	0008_auto_20201106_1608	2020-11-06 08:08:24.550511+00
322	project_timetable	0006_auto_20201106_1608	2020-11-06 08:08:24.622287+00
323	project_expenses	0009_auto_20201116_1810	2020-11-16 10:11:00.369824+00
324	project_timetable	0007_auto_20201116_1810	2020-11-16 10:11:00.426024+00
325	project_expenses	0010_auto_20201120_0223	2020-11-19 18:23:50.108545+00
326	project_timetable	0008_auto_20201120_0223	2020-11-19 18:23:50.165392+00
327	project_expenses	0011_auto_20201120_0256	2020-11-19 18:56:55.017038+00
328	project_misc	0002_auto_20201120_0256	2020-11-19 18:56:55.072685+00
329	project_timetable	0009_auto_20201120_0256	2020-11-19 18:56:55.15201+00
330	rooms	0025_auto_20201120_0256	2020-11-19 18:56:55.202114+00
331	customers	0003_auto_20201120_1952	2020-11-20 11:53:01.331471+00
332	customers	0004_auto_20201120_1956	2020-11-20 11:57:17.833135+00
333	project_expenses	0012_auto_20201211_1216	2020-12-11 04:16:55.056212+00
334	project_items	0023_auto_20201211_1329	2020-12-11 05:29:21.236701+00
335	project_items	0024_auto_20201211_1743	2020-12-11 09:43:54.834535+00
336	project_misc	0003_auto_20201211_1756	2020-12-11 09:56:18.155944+00
337	companies	0017_auto_20210107_1611	2021-01-07 08:11:16.066535+00
338	rooms	0026_auto_20210107_1926	2021-01-07 11:26:24.280483+00
339	rooms	0027_roomitem_item_quantifier	2021-01-07 13:06:36.172911+00
340	rooms	0028_auto_20210108_1521	2021-01-08 07:21:49.740925+00
341	projects	0012_projectimage_projectimageset	2021-01-12 11:11:57.148577+00
342	projects	0013_auto_20210112_2010	2021-01-12 12:10:44.574313+00
343	projects	0014_auto_20210113_1436	2021-01-13 06:36:29.127802+00
344	projects	0015_auto_20210113_1642	2021-01-13 08:42:16.431892+00
345	projects	0016_auto_20210113_2031	2021-01-13 12:31:23.977351+00
346	projects	0017_auto_20210113_2045	2021-01-13 12:45:58.378538+00
347	projects	0018_auto_20210113_2047	2021-01-13 12:47:49.091802+00
348	projects	0019_remove_projectimageset_project_milestone	2021-01-13 12:49:38.474728+00
349	projects	0020_projectimageset_project_milestone	2021-01-13 12:50:39.0746+00
350	projects	0021_auto_20210113_2051	2021-01-13 12:56:37.216958+00
351	projects	0022_auto_20210113_2056	2021-01-13 12:56:37.435734+00
352	projects	0023_auto_20210113_2056	2021-01-13 13:00:22.700736+00
353	projects	0024_remove_projectimageset_project_milestone	2021-01-13 13:02:54.721812+00
354	projects	0025_projectimageset_project_milestone	2021-01-13 13:44:10.891249+00
355	projects	0026_auto_20210113_2104	2021-01-13 13:44:11.115823+00
356	projects	0027_auto_20210113_2104	2021-01-13 13:44:11.385194+00
357	projects	0028_auto_20210113_2105	2021-01-13 13:44:11.591093+00
358	projects	0029_auto_20210113_2105	2021-01-13 13:44:11.809152+00
359	projects	0030_auto_20210113_2106	2021-01-13 13:44:12.137274+00
360	projects	0031_auto_20210113_2106	2021-01-13 13:44:12.438205+00
361	projects	0032_auto_20210113_2106	2021-01-13 13:44:12.64407+00
362	projects	0033_auto_20210113_2137	2021-01-13 13:44:12.84631+00
363	projects	0034_auto_20210113_2138	2021-01-13 13:44:13.238447+00
364	projects	0035_auto_20210113_2138	2021-01-13 13:44:13.468607+00
365	projects	0036_auto_20210113_2138	2021-01-13 13:44:13.671746+00
366	projects	0037_auto_20210113_2143	2021-01-13 13:44:13.873504+00
367	projects	0038_auto_20210113_2143	2021-01-13 13:44:14.166538+00
368	projects	0039_auto_20210113_2144	2021-01-13 13:44:14.674413+00
369	projects	0040_auto_20210113_2144	2021-01-13 13:52:00.069274+00
370	projects	0041_auto_20210113_2145	2021-01-13 13:52:00.289254+00
371	projects	0042_auto_20210113_2150	2021-01-13 13:52:00.565655+00
372	projects	0043_auto_20210113_2150	2021-01-13 13:52:00.769336+00
373	projects	0044_auto_20210113_2150	2021-01-13 13:52:00.996588+00
374	projects	0045_auto_20210113_2151	2021-01-13 13:52:01.473523+00
375	projects	0046_auto_20210113_2200	2021-01-13 14:00:33.321939+00
376	projects	0047_auto_20210113_2202	2021-01-13 14:02:26.312274+00
377	projects	0048_auto_20210113_2215	2021-01-13 14:15:24.994452+00
378	projects	0049_auto_20210113_2221	2021-01-13 14:21:53.757433+00
379	projects	0050_auto_20210118_1810	2021-01-18 10:10:40.670055+00
380	project_items	0025_auto_20210201_1747	2021-02-01 09:47:38.988366+00
381	projects	0051_auto_20210201_1747	2021-02-01 09:47:39.256309+00
382	rooms	0029_auto_20210201_1747	2021-02-01 09:47:39.388839+00
383	projects	0052_auto_20210201_1852	2021-02-01 10:52:52.759093+00
384	rooms	0030_auto_20210201_1852	2021-02-01 10:52:52.828429+00
385	projects	0053_auto_20210202_1612	2021-02-02 08:12:25.723784+00
386	rooms	0031_auto_20210202_1612	2021-02-02 08:12:25.791188+00
387	common	0028_auto_20210210_1236	2021-02-10 04:36:24.331611+00
388	projects	0054_auto_20210210_1236	2021-02-10 04:36:24.579773+00
389	common	0029_auto_20210210_1245	2021-02-10 04:45:12.084112+00
390	projects	0055_auto_20210210_1245	2021-02-10 04:45:12.300301+00
391	companies	0018_auto_20210224_1313	2021-02-24 05:13:47.439835+00
392	project_items	0026_auto_20210224_1313	2021-02-24 05:13:47.472407+00
393	projects	0056_auto_20210224_1313	2021-02-24 05:13:47.681039+00
394	rooms	0032_auto_20210224_1313	2021-02-24 05:13:47.724675+00
395	companies	0019_auto_20210224_1501	2021-02-24 07:01:53.539337+00
396	projects	0057_auto_20210224_1501	2021-02-24 07:01:53.852039+00
397	project_items	0027_item_item_properties_sort	2021-02-24 08:01:20.38186+00
398	projects	0058_auto_20210224_1601	2021-02-24 08:01:20.606476+00
399	rooms	0033_auto_20210224_1601	2021-02-24 08:01:20.664195+00
400	projects	0059_auto_20210224_1958	2021-02-24 11:58:34.638312+00
401	project_items	0028_auto_20210225_1236	2021-02-25 04:36:42.084392+00
402	projects	0060_auto_20210225_1236	2021-02-25 04:36:42.315235+00
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
6qmz0emgiq71mklu08xlu0ynj48z7kr8	MmM0YzFlZmYwNzkyMDk1YzIzZDdjOWExN2VmOWYzMzA2MjU1NTM1Njp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5YzM5ZWM4NGM1MTU5NDU0MGU4M2NiMjcxZGQzMDVmYzJjMGE3Y2NlIn0=	2020-07-06 07:56:27.116237+00
nsvox2ctrfcdgf89zk46xvd5quq6zoi0	MmM0YzFlZmYwNzkyMDk1YzIzZDdjOWExN2VmOWYzMzA2MjU1NTM1Njp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5YzM5ZWM4NGM1MTU5NDU0MGU4M2NiMjcxZGQzMDVmYzJjMGE3Y2NlIn0=	2020-07-06 07:57:23.50054+00
7dsnxpx9gwt6j706g8ms7kabksdx8upy	MmM0YzFlZmYwNzkyMDk1YzIzZDdjOWExN2VmOWYzMzA2MjU1NTM1Njp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5YzM5ZWM4NGM1MTU5NDU0MGU4M2NiMjcxZGQzMDVmYzJjMGE3Y2NlIn0=	2020-07-06 07:58:06.513698+00
38patnsblaloopipr55lt10psuv413z0	MmM0YzFlZmYwNzkyMDk1YzIzZDdjOWExN2VmOWYzMzA2MjU1NTM1Njp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5YzM5ZWM4NGM1MTU5NDU0MGU4M2NiMjcxZGQzMDVmYzJjMGE3Y2NlIn0=	2020-07-20 07:59:24.390747+00
j2y0addgfvbtbexarlyegccxf73un3un	MmM0YzFlZmYwNzkyMDk1YzIzZDdjOWExN2VmOWYzMzA2MjU1NTM1Njp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5YzM5ZWM4NGM1MTU5NDU0MGU4M2NiMjcxZGQzMDVmYzJjMGE3Y2NlIn0=	2020-09-16 15:38:12.00527+00
ydzihmrcgxj9u4zqhdznwmrok4e8mw6v	MmM0YzFlZmYwNzkyMDk1YzIzZDdjOWExN2VmOWYzMzA2MjU1NTM1Njp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5YzM5ZWM4NGM1MTU5NDU0MGU4M2NiMjcxZGQzMDVmYzJjMGE3Y2NlIn0=	2020-09-16 15:47:38.411358+00
gu1m8r2n3fefo36juh5daj22pxai2hp5	Y2M2NzM1MmYxNGUzMWVkMzcxMmZhMTI3ODA1OTUwYWRiZWYzMWE1OTp7Il9hdXRoX3VzZXJfaWQiOiIxMCIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiZWNmMDliNjMzMzg4NjAxNWFlZTNkYmRjYzgwMDZjY2UwMjE4YjA2NyJ9	2020-09-16 15:56:10.613508+00
t33wb2odvsn72yiuvj4hbu8thl5u60nb	MmM0YzFlZmYwNzkyMDk1YzIzZDdjOWExN2VmOWYzMzA2MjU1NTM1Njp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5YzM5ZWM4NGM1MTU5NDU0MGU4M2NiMjcxZGQzMDVmYzJjMGE3Y2NlIn0=	2020-09-17 08:10:21.588415+00
h7iu6atvjj37gbfnv9evnarvlmnh1cmn	MmM0YzFlZmYwNzkyMDk1YzIzZDdjOWExN2VmOWYzMzA2MjU1NTM1Njp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5YzM5ZWM4NGM1MTU5NDU0MGU4M2NiMjcxZGQzMDVmYzJjMGE3Y2NlIn0=	2020-09-17 17:23:57.225109+00
gr7w7q5tmuhw4hecfi59g2e1g2v8j9oc	MmM0YzFlZmYwNzkyMDk1YzIzZDdjOWExN2VmOWYzMzA2MjU1NTM1Njp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5YzM5ZWM4NGM1MTU5NDU0MGU4M2NiMjcxZGQzMDVmYzJjMGE3Y2NlIn0=	2020-09-18 07:38:42.878097+00
vdo6l76yie80d4c4s6vxhn7qgwab5smx	MmM0YzFlZmYwNzkyMDk1YzIzZDdjOWExN2VmOWYzMzA2MjU1NTM1Njp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5YzM5ZWM4NGM1MTU5NDU0MGU4M2NiMjcxZGQzMDVmYzJjMGE3Y2NlIn0=	2020-09-18 08:05:01.070979+00
l32s3woxuovvysd1our5nv7i2kfut5vv	Y2M2NzM1MmYxNGUzMWVkMzcxMmZhMTI3ODA1OTUwYWRiZWYzMWE1OTp7Il9hdXRoX3VzZXJfaWQiOiIxMCIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiZWNmMDliNjMzMzg4NjAxNWFlZTNkYmRjYzgwMDZjY2UwMjE4YjA2NyJ9	2020-09-18 17:46:14.774542+00
a3prf3d5o9a363rpuecgjdji8anqqch6	MzQwMDE1YTBlYWRiYWFkYmU3N2M3N2Y5Y2QzMWUzM2U2NTAxYjZlNzp7Il9hdXRoX3VzZXJfaWQiOiIxNCIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiZWNhZmI3Njc5MGUxZmI0ZTZhYWZmYWNlNWM5ZWU3OThhYWFjNWIyNCJ9	2020-09-18 17:51:59.016815+00
t0p22g27n7a1krxgv6nwf900rpbhmafr	MmM0YzFlZmYwNzkyMDk1YzIzZDdjOWExN2VmOWYzMzA2MjU1NTM1Njp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5YzM5ZWM4NGM1MTU5NDU0MGU4M2NiMjcxZGQzMDVmYzJjMGE3Y2NlIn0=	2020-09-19 05:00:03.975894+00
wkr1nwy4eykkg1v7lyg2bn1kw6og50dk	MzQwMDE1YTBlYWRiYWFkYmU3N2M3N2Y5Y2QzMWUzM2U2NTAxYjZlNzp7Il9hdXRoX3VzZXJfaWQiOiIxNCIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiZWNhZmI3Njc5MGUxZmI0ZTZhYWZmYWNlNWM5ZWU3OThhYWFjNWIyNCJ9	2020-09-23 09:45:51.405283+00
dti9nw3ai5xqyf7r9m5lty2m0wfnaef4	Y2M2NzM1MmYxNGUzMWVkMzcxMmZhMTI3ODA1OTUwYWRiZWYzMWE1OTp7Il9hdXRoX3VzZXJfaWQiOiIxMCIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiZWNmMDliNjMzMzg4NjAxNWFlZTNkYmRjYzgwMDZjY2UwMjE4YjA2NyJ9	2020-09-29 03:22:50.921184+00
z06s7jizt5pd8jn71brht8u1l8ynw0g4	MmM0YzFlZmYwNzkyMDk1YzIzZDdjOWExN2VmOWYzMzA2MjU1NTM1Njp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5YzM5ZWM4NGM1MTU5NDU0MGU4M2NiMjcxZGQzMDVmYzJjMGE3Y2NlIn0=	2020-09-30 10:18:29.655925+00
lhlwogkrsi63trhpmllss10k94nvvuyw	MmM0YzFlZmYwNzkyMDk1YzIzZDdjOWExN2VmOWYzMzA2MjU1NTM1Njp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5YzM5ZWM4NGM1MTU5NDU0MGU4M2NiMjcxZGQzMDVmYzJjMGE3Y2NlIn0=	2020-10-04 07:24:02.252102+00
hw77mnixo3oiwouv1pepnwgn5uu01q2w	Y2M2NzM1MmYxNGUzMWVkMzcxMmZhMTI3ODA1OTUwYWRiZWYzMWE1OTp7Il9hdXRoX3VzZXJfaWQiOiIxMCIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiZWNmMDliNjMzMzg4NjAxNWFlZTNkYmRjYzgwMDZjY2UwMjE4YjA2NyJ9	2020-10-04 07:25:36.19362+00
pjcdz7umcm5tgo12ul6lpvy9y3bkfp9m	MmM0YzFlZmYwNzkyMDk1YzIzZDdjOWExN2VmOWYzMzA2MjU1NTM1Njp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5YzM5ZWM4NGM1MTU5NDU0MGU4M2NiMjcxZGQzMDVmYzJjMGE3Y2NlIn0=	2020-10-16 08:22:49.066047+00
papael6ygtbhift71x32e43tbfl4y6sq	MmM0YzFlZmYwNzkyMDk1YzIzZDdjOWExN2VmOWYzMzA2MjU1NTM1Njp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5YzM5ZWM4NGM1MTU5NDU0MGU4M2NiMjcxZGQzMDVmYzJjMGE3Y2NlIn0=	2020-10-17 16:13:35.48981+00
1v6v20en9i0ie3q76hw0rm50pd875um6	MmM0YzFlZmYwNzkyMDk1YzIzZDdjOWExN2VmOWYzMzA2MjU1NTM1Njp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5YzM5ZWM4NGM1MTU5NDU0MGU4M2NiMjcxZGQzMDVmYzJjMGE3Y2NlIn0=	2020-10-19 07:44:57.40708+00
is2abs1hmlvpl30brrv9jsho8whjcvuc	MmM0YzFlZmYwNzkyMDk1YzIzZDdjOWExN2VmOWYzMzA2MjU1NTM1Njp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5YzM5ZWM4NGM1MTU5NDU0MGU4M2NiMjcxZGQzMDVmYzJjMGE3Y2NlIn0=	2020-10-21 11:52:46.88374+00
zxyg9g2m1xw2gksdefp4s4o47vbsfxup	Y2M2NzM1MmYxNGUzMWVkMzcxMmZhMTI3ODA1OTUwYWRiZWYzMWE1OTp7Il9hdXRoX3VzZXJfaWQiOiIxMCIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiZWNmMDliNjMzMzg4NjAxNWFlZTNkYmRjYzgwMDZjY2UwMjE4YjA2NyJ9	2020-10-22 05:36:14.50988+00
zzsg7ips8iasxd72e4wme16d9h3ew70n	MmM0YzFlZmYwNzkyMDk1YzIzZDdjOWExN2VmOWYzMzA2MjU1NTM1Njp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5YzM5ZWM4NGM1MTU5NDU0MGU4M2NiMjcxZGQzMDVmYzJjMGE3Y2NlIn0=	2020-10-22 08:03:45.449042+00
25tinee8fvsmm1qwluatzncimmfplhoc	MmM0YzFlZmYwNzkyMDk1YzIzZDdjOWExN2VmOWYzMzA2MjU1NTM1Njp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5YzM5ZWM4NGM1MTU5NDU0MGU4M2NiMjcxZGQzMDVmYzJjMGE3Y2NlIn0=	2020-11-02 09:17:03.800307+00
cnq05uc8dndrblje1mh0giu1wkfa9iz2	MmM0YzFlZmYwNzkyMDk1YzIzZDdjOWExN2VmOWYzMzA2MjU1NTM1Njp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5YzM5ZWM4NGM1MTU5NDU0MGU4M2NiMjcxZGQzMDVmYzJjMGE3Y2NlIn0=	2020-11-04 09:49:00.943321+00
fcbj7sv0wuicpy4osfwiwno77siadayr	Y2M2NzM1MmYxNGUzMWVkMzcxMmZhMTI3ODA1OTUwYWRiZWYzMWE1OTp7Il9hdXRoX3VzZXJfaWQiOiIxMCIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiZWNmMDliNjMzMzg4NjAxNWFlZTNkYmRjYzgwMDZjY2UwMjE4YjA2NyJ9	2020-11-06 11:18:05.750846+00
uzjvuqgttmbvdh8ys5d8yylm90l7n6qe	MmM0YzFlZmYwNzkyMDk1YzIzZDdjOWExN2VmOWYzMzA2MjU1NTM1Njp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5YzM5ZWM4NGM1MTU5NDU0MGU4M2NiMjcxZGQzMDVmYzJjMGE3Y2NlIn0=	2020-11-11 10:32:31.158137+00
aw3vmef9r4987ql1u9mymenwrnyfxzs1	MmM0YzFlZmYwNzkyMDk1YzIzZDdjOWExN2VmOWYzMzA2MjU1NTM1Njp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5YzM5ZWM4NGM1MTU5NDU0MGU4M2NiMjcxZGQzMDVmYzJjMGE3Y2NlIn0=	2020-11-12 16:04:54.988408+00
167qvdw4nzyvchjxzch4d9rqrd849olh	MmM0YzFlZmYwNzkyMDk1YzIzZDdjOWExN2VmOWYzMzA2MjU1NTM1Njp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5YzM5ZWM4NGM1MTU5NDU0MGU4M2NiMjcxZGQzMDVmYzJjMGE3Y2NlIn0=	2020-11-15 14:20:20.956834+00
u9oktbhszxf42ijgm8lsrq71k2yewls4	MmM0YzFlZmYwNzkyMDk1YzIzZDdjOWExN2VmOWYzMzA2MjU1NTM1Njp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5YzM5ZWM4NGM1MTU5NDU0MGU4M2NiMjcxZGQzMDVmYzJjMGE3Y2NlIn0=	2020-11-17 12:45:22.456519+00
2yfwxpvfqzwclsxb1utodwbq1d3tp6lg	MmM0YzFlZmYwNzkyMDk1YzIzZDdjOWExN2VmOWYzMzA2MjU1NTM1Njp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5YzM5ZWM4NGM1MTU5NDU0MGU4M2NiMjcxZGQzMDVmYzJjMGE3Y2NlIn0=	2020-11-19 07:17:34.494353+00
tmm2sqkpqruvdsp5jjx2r2zd6arma6gz	MmM0YzFlZmYwNzkyMDk1YzIzZDdjOWExN2VmOWYzMzA2MjU1NTM1Njp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5YzM5ZWM4NGM1MTU5NDU0MGU4M2NiMjcxZGQzMDVmYzJjMGE3Y2NlIn0=	2020-12-03 10:15:57.244721+00
02gb2kycuf4u1uaxgtsi91oefkrpitl7	OWNjN2Y3OGVmMTgxZTViOTkxNTlhOWQwYmE5NWI1ZDk1MDkxZWMwOTp7Il9hdXRoX3VzZXJfaWQiOiI0MCIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiNmI2YzIxMTNiMDMxNTBiMDMyMWZiMGUxZGExOWNkYTc0NWYxMDI3OCJ9	2020-12-03 10:17:34.015158+00
l3tipcq4705a8kdduzird3753qvbjza4	NjA0OWM3NjVlMGMwNDdmNzY5ZGUxYmFiMjQ3NWJhZWI2ZjI4OTlhZjp7Il9hdXRoX3VzZXJfaWQiOiI0MCIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiZDYyODliMGM3MTI3YmIwYjJhMjU3ZGUyZmJiMmJlMDA3OWYxNTVhMiJ9	2020-12-10 17:16:14.434771+00
lg0mt63ebbiq34i0rtdjhtto7ej0oaft	MmM0YzFlZmYwNzkyMDk1YzIzZDdjOWExN2VmOWYzMzA2MjU1NTM1Njp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5YzM5ZWM4NGM1MTU5NDU0MGU4M2NiMjcxZGQzMDVmYzJjMGE3Y2NlIn0=	2020-12-18 12:37:06.990612+00
67dfuslh0xk3aazrzs0dpf2c47dx2r2f	Y2M2NzM1MmYxNGUzMWVkMzcxMmZhMTI3ODA1OTUwYWRiZWYzMWE1OTp7Il9hdXRoX3VzZXJfaWQiOiIxMCIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiZWNmMDliNjMzMzg4NjAxNWFlZTNkYmRjYzgwMDZjY2UwMjE4YjA2NyJ9	2020-12-18 18:37:56.056155+00
543wrzqek5cjyuhrjcu688t5dqntgmcp	NjA0OWM3NjVlMGMwNDdmNzY5ZGUxYmFiMjQ3NWJhZWI2ZjI4OTlhZjp7Il9hdXRoX3VzZXJfaWQiOiI0MCIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiZDYyODliMGM3MTI3YmIwYjJhMjU3ZGUyZmJiMmJlMDA3OWYxNTVhMiJ9	2020-12-24 18:03:29.959979+00
qni2xphvnezwrnvb2aqgr85lwgl68y10	YzkzNjhhNTQ3MDI4NGRhNjMzNDgyMmZhMDBmZTJlYjc3OTZiNWQzNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5YzM5ZWM4NGM1MTU5NDU0MGU4M2NiMjcxZGQzMDVmYzJjMGE3Y2NlIiwicHJvdGVjdGVkRXJyb3IiOmZhbHNlfQ==	2020-12-25 05:38:42.88498+00
o30fufilf4ey3lxy658v5mg1yjn2jwlj	YzkzNjhhNTQ3MDI4NGRhNjMzNDgyMmZhMDBmZTJlYjc3OTZiNWQzNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5YzM5ZWM4NGM1MTU5NDU0MGU4M2NiMjcxZGQzMDVmYzJjMGE3Y2NlIiwicHJvdGVjdGVkRXJyb3IiOmZhbHNlfQ==	2020-12-25 06:34:19.734306+00
p67w0yi3xo126bbp36m3jqoworgqo3sr	NjA0OWM3NjVlMGMwNDdmNzY5ZGUxYmFiMjQ3NWJhZWI2ZjI4OTlhZjp7Il9hdXRoX3VzZXJfaWQiOiI0MCIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiZDYyODliMGM3MTI3YmIwYjJhMjU3ZGUyZmJiMmJlMDA3OWYxNTVhMiJ9	2020-12-28 03:41:29.182019+00
f3x35hap19ebmguyjfzeh17dtpr8v8m5	NjA0OWM3NjVlMGMwNDdmNzY5ZGUxYmFiMjQ3NWJhZWI2ZjI4OTlhZjp7Il9hdXRoX3VzZXJfaWQiOiI0MCIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiZDYyODliMGM3MTI3YmIwYjJhMjU3ZGUyZmJiMmJlMDA3OWYxNTVhMiJ9	2021-01-19 04:25:19.874179+00
l1j7f6ualtoji9npy3qji2wfsiwx83rl	MmM0YzFlZmYwNzkyMDk1YzIzZDdjOWExN2VmOWYzMzA2MjU1NTM1Njp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5YzM5ZWM4NGM1MTU5NDU0MGU4M2NiMjcxZGQzMDVmYzJjMGE3Y2NlIn0=	2021-01-21 07:54:42.407086+00
x7hr8p29miqjhawitvdmgmd4umdbutsb	MmM0YzFlZmYwNzkyMDk1YzIzZDdjOWExN2VmOWYzMzA2MjU1NTM1Njp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5YzM5ZWM4NGM1MTU5NDU0MGU4M2NiMjcxZGQzMDVmYzJjMGE3Y2NlIn0=	2021-01-25 06:07:27.8685+00
m03neeaowd1be5yw5qdwhpf33z9e8k5m	MmM0YzFlZmYwNzkyMDk1YzIzZDdjOWExN2VmOWYzMzA2MjU1NTM1Njp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5YzM5ZWM4NGM1MTU5NDU0MGU4M2NiMjcxZGQzMDVmYzJjMGE3Y2NlIn0=	2021-01-25 07:44:22.903357+00
d12x25huxf03a2x4p9qxt8btes1okoja	MmM0YzFlZmYwNzkyMDk1YzIzZDdjOWExN2VmOWYzMzA2MjU1NTM1Njp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5YzM5ZWM4NGM1MTU5NDU0MGU4M2NiMjcxZGQzMDVmYzJjMGE3Y2NlIn0=	2021-02-01 09:17:04.859344+00
wrcbpswc0v9qhhtr2n8qlhwh6jfx5yru	Mjg2OWE0NjQwMTk1MDQwZDg3NDNiNmUyODVmYjBmZDFjMmQwYjNmZjp7Il9hdXRoX3VzZXJfaWQiOiI0MCIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiZDYyODliMGM3MTI3YmIwYjJhMjU3ZGUyZmJiMmJlMDA3OWYxNTVhMiIsInByb3RlY3RlZEVycm9yIjpmYWxzZX0=	2021-03-05 08:21:01.945214+00
8ra6h3e8m8214l3dki37mvknce0yzg11	NzZjODczNjBiNzZmMGJjYTkyODgzMjZkYWVkYzllMTI0ODRhNjk0Zjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJiYjA1YThmOWFhNmJiNjk1ZWRiNjc3ZjA0NjY2Y2RmYjA3NzBiNzM1In0=	2021-03-08 01:47:29.313589+00
uixy4i3flac5ob6dyt57f0zv04vwgom0	NjA0OWM3NjVlMGMwNDdmNzY5ZGUxYmFiMjQ3NWJhZWI2ZjI4OTlhZjp7Il9hdXRoX3VzZXJfaWQiOiI0MCIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiZDYyODliMGM3MTI3YmIwYjJhMjU3ZGUyZmJiMmJlMDA3OWYxNTVhMiJ9	2021-03-08 02:04:41.139733+00
e3pqc1odgrm8652ydjk5qjmrhd29h3ze	NzZjODczNjBiNzZmMGJjYTkyODgzMjZkYWVkYzllMTI0ODRhNjk0Zjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJiYjA1YThmOWFhNmJiNjk1ZWRiNjc3ZjA0NjY2Y2RmYjA3NzBiNzM1In0=	2021-03-08 04:56:43.754153+00
khmrcj3yft7xrc8ho8g8l1gslb90k7ui	NjA0OWM3NjVlMGMwNDdmNzY5ZGUxYmFiMjQ3NWJhZWI2ZjI4OTlhZjp7Il9hdXRoX3VzZXJfaWQiOiI0MCIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiZDYyODliMGM3MTI3YmIwYjJhMjU3ZGUyZmJiMmJlMDA3OWYxNTVhMiJ9	2021-03-08 06:28:19.147302+00
1u63tw8d2bqhou2557xknmqltkj2kjnh	NjA0OWM3NjVlMGMwNDdmNzY5ZGUxYmFiMjQ3NWJhZWI2ZjI4OTlhZjp7Il9hdXRoX3VzZXJfaWQiOiI0MCIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiZDYyODliMGM3MTI3YmIwYjJhMjU3ZGUyZmJiMmJlMDA3OWYxNTVhMiJ9	2021-03-09 01:15:25.926989+00
rzp05p7opwa8f6jul65clj9btt4r3zkv	MmM0YzFlZmYwNzkyMDk1YzIzZDdjOWExN2VmOWYzMzA2MjU1NTM1Njp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5YzM5ZWM4NGM1MTU5NDU0MGU4M2NiMjcxZGQzMDVmYzJjMGE3Y2NlIn0=	2021-02-11 16:13:17.928376+00
becde7s0jzbfuv3a5a6bmzj4re9rivza	Mjg2OWE0NjQwMTk1MDQwZDg3NDNiNmUyODVmYjBmZDFjMmQwYjNmZjp7Il9hdXRoX3VzZXJfaWQiOiI0MCIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiZDYyODliMGM3MTI3YmIwYjJhMjU3ZGUyZmJiMmJlMDA3OWYxNTVhMiIsInByb3RlY3RlZEVycm9yIjpmYWxzZX0=	2021-02-12 12:49:36.841785+00
rljj9ogtffkvssqin7ba3e6tvlx1rn9m	NjA0OWM3NjVlMGMwNDdmNzY5ZGUxYmFiMjQ3NWJhZWI2ZjI4OTlhZjp7Il9hdXRoX3VzZXJfaWQiOiI0MCIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiZDYyODliMGM3MTI3YmIwYjJhMjU3ZGUyZmJiMmJlMDA3OWYxNTVhMiJ9	2021-02-12 13:04:58.611338+00
rbgxdic1yxhhsrmkrnxxcrkg10mhds0y	MmM0YzFlZmYwNzkyMDk1YzIzZDdjOWExN2VmOWYzMzA2MjU1NTM1Njp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5YzM5ZWM4NGM1MTU5NDU0MGU4M2NiMjcxZGQzMDVmYzJjMGE3Y2NlIn0=	2021-02-12 18:00:02.066858+00
ow64vbinxf7qiak48olzb3lbwoqaiz1g	YzkzNjhhNTQ3MDI4NGRhNjMzNDgyMmZhMDBmZTJlYjc3OTZiNWQzNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5YzM5ZWM4NGM1MTU5NDU0MGU4M2NiMjcxZGQzMDVmYzJjMGE3Y2NlIiwicHJvdGVjdGVkRXJyb3IiOmZhbHNlfQ==	2021-02-13 07:13:40.605947+00
cahk7fth1ky7qytc8h16f6vdt663djwt	MmM0YzFlZmYwNzkyMDk1YzIzZDdjOWExN2VmOWYzMzA2MjU1NTM1Njp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5YzM5ZWM4NGM1MTU5NDU0MGU4M2NiMjcxZGQzMDVmYzJjMGE3Y2NlIn0=	2021-02-15 09:02:58.955689+00
6neh36yrw2pgvaqnv086tvaawnivofr7	MmM0YzFlZmYwNzkyMDk1YzIzZDdjOWExN2VmOWYzMzA2MjU1NTM1Njp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5YzM5ZWM4NGM1MTU5NDU0MGU4M2NiMjcxZGQzMDVmYzJjMGE3Y2NlIn0=	2021-02-15 09:35:08.677851+00
7mcgwkkv9ehf23ug91s8fdnkv1hg63ld	NjA0OWM3NjVlMGMwNDdmNzY5ZGUxYmFiMjQ3NWJhZWI2ZjI4OTlhZjp7Il9hdXRoX3VzZXJfaWQiOiI0MCIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiZDYyODliMGM3MTI3YmIwYjJhMjU3ZGUyZmJiMmJlMDA3OWYxNTVhMiJ9	2021-02-17 02:09:43.95909+00
uuhmv7446zriinm1ncr01s6e9q7ba3oe	MmM0YzFlZmYwNzkyMDk1YzIzZDdjOWExN2VmOWYzMzA2MjU1NTM1Njp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5YzM5ZWM4NGM1MTU5NDU0MGU4M2NiMjcxZGQzMDVmYzJjMGE3Y2NlIn0=	2021-02-17 03:05:10.012962+00
fih4om7inod48lifa5eqn8upkk3ckjps	NzZjODczNjBiNzZmMGJjYTkyODgzMjZkYWVkYzllMTI0ODRhNjk0Zjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJiYjA1YThmOWFhNmJiNjk1ZWRiNjc3ZjA0NjY2Y2RmYjA3NzBiNzM1In0=	2021-02-23 04:59:50.818774+00
h02buvzk7ay72bu33g219o2byf0gqz0q	NzZjODczNjBiNzZmMGJjYTkyODgzMjZkYWVkYzllMTI0ODRhNjk0Zjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJiYjA1YThmOWFhNmJiNjk1ZWRiNjc3ZjA0NjY2Y2RmYjA3NzBiNzM1In0=	2021-02-25 09:02:59.353969+00
bl0xn8b6xya9vi0a9tt57o2k4bebj03a	OGVkZGNjMDJhZTBlNjk5NGQxMTRkYWIyMzZjNzQ2NzZiMjdjYzY2Mzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJiYjA1YThmOWFhNmJiNjk1ZWRiNjc3ZjA0NjY2Y2RmYjA3NzBiNzM1IiwicHJvdGVjdGVkRXJyb3IiOmZhbHNlfQ==	2021-02-25 10:05:40.766663+00
rxf23mco3ql9a18k0bqnpb9r6e1b8o7b	OGVkZGNjMDJhZTBlNjk5NGQxMTRkYWIyMzZjNzQ2NzZiMjdjYzY2Mzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJiYjA1YThmOWFhNmJiNjk1ZWRiNjc3ZjA0NjY2Y2RmYjA3NzBiNzM1IiwicHJvdGVjdGVkRXJyb3IiOmZhbHNlfQ==	2021-02-28 10:38:09.83672+00
39yp7dvqwgdj7wotwyg8dmqyyhxd48tq	OGVkZGNjMDJhZTBlNjk5NGQxMTRkYWIyMzZjNzQ2NzZiMjdjYzY2Mzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJiYjA1YThmOWFhNmJiNjk1ZWRiNjc3ZjA0NjY2Y2RmYjA3NzBiNzM1IiwicHJvdGVjdGVkRXJyb3IiOmZhbHNlfQ==	2021-03-01 13:03:52.968692+00
5kj2nnq7fgzayrpdcc193udsy0lyvng3	NjA0OWM3NjVlMGMwNDdmNzY5ZGUxYmFiMjQ3NWJhZWI2ZjI4OTlhZjp7Il9hdXRoX3VzZXJfaWQiOiI0MCIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiZDYyODliMGM3MTI3YmIwYjJhMjU3ZGUyZmJiMmJlMDA3OWYxNTVhMiJ9	2021-03-04 17:58:06.857573+00
5laql70kep5342au1f6lo9grtukvwyzm	NzZjODczNjBiNzZmMGJjYTkyODgzMjZkYWVkYzllMTI0ODRhNjk0Zjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJiYjA1YThmOWFhNmJiNjk1ZWRiNjc3ZjA0NjY2Y2RmYjA3NzBiNzM1In0=	2021-03-09 06:54:27.382164+00
s7reexfuplb1opbohmv3z4d5zce5hj9o	NzZjODczNjBiNzZmMGJjYTkyODgzMjZkYWVkYzllMTI0ODRhNjk0Zjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJiYjA1YThmOWFhNmJiNjk1ZWRiNjc3ZjA0NjY2Y2RmYjA3NzBiNzM1In0=	2021-03-10 04:32:10.801208+00
3quhsoczj4kbwfke1skjgev9g9ki31hs	NzZjODczNjBiNzZmMGJjYTkyODgzMjZkYWVkYzllMTI0ODRhNjk0Zjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJiYjA1YThmOWFhNmJiNjk1ZWRiNjc3ZjA0NjY2Y2RmYjA3NzBiNzM1In0=	2021-03-11 02:38:23.268011+00
qr5lr6q83i4huuj4ffnu6qipnme74wh3	NzZjODczNjBiNzZmMGJjYTkyODgzMjZkYWVkYzllMTI0ODRhNjk0Zjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJiYjA1YThmOWFhNmJiNjk1ZWRiNjc3ZjA0NjY2Y2RmYjA3NzBiNzM1In0=	2021-03-17 05:19:14.01584+00
v11o3n6r32nn6ui81ebud5qc8puh90qf	NzZjODczNjBiNzZmMGJjYTkyODgzMjZkYWVkYzllMTI0ODRhNjk0Zjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJiYjA1YThmOWFhNmJiNjk1ZWRiNjc3ZjA0NjY2Y2RmYjA3NzBiNzM1In0=	2021-03-18 08:04:58.866147+00
\.


--
-- Data for Name: emails_email; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.emails_email (id, from_email, to_email, subject, message, file, send_time, status, important) FROM stdin;
\.


--
-- Data for Name: events_event; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.events_event (id, name, event_type, status, start_date, start_time, end_date, end_time, description, created_on, is_active, disabled, created_by_id, date_of_meeting) FROM stdin;
\.


--
-- Data for Name: events_event_assigned_to; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.events_event_assigned_to (id, event_id, user_id) FROM stdin;
\.


--
-- Data for Name: events_event_contacts; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.events_event_contacts (id, event_id, contact_id) FROM stdin;
\.


--
-- Data for Name: events_event_teams; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.events_event_teams (id, event_id, teams_id) FROM stdin;
\.


--
-- Data for Name: function_items_functionitem; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.function_items_functionitem (id, name, created_on, created_by_id, type, description, price, status, approved_by_id, approved_on, last_updated_by_id, last_updated_on) FROM stdin;
\.


--
-- Data for Name: function_items_functionitemhistory; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.function_items_functionitemhistory (id, name, price, description, type, status, created_on, function_item_id, updated_by_id, changed_data) FROM stdin;
\.


--
-- Data for Name: function_items_subfunctionitem; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.function_items_subfunctionitem (id, name, price, description, status, created_on, approved_on, last_updated_on, approved_by_id, created_by_id, last_updated_by_id, related_function_item_id) FROM stdin;
\.


--
-- Data for Name: function_items_subfunctionitemhistory; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.function_items_subfunctionitemhistory (id, name, price, description, status, changed_data, created_on, sub_function_item_id, updated_by_id) FROM stdin;
\.


--
-- Data for Name: invoices_invoice; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.invoices_invoice (id, invoice_title, invoice_number, name, email, quantity, rate, total_amount, currency, phone, created_on, amount_due, amount_paid, is_email_sent, status, created_by_id, from_address_id, to_address_id, details, due_date) FROM stdin;
\.


--
-- Data for Name: invoices_invoice_assigned_to; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.invoices_invoice_assigned_to (id, invoice_id, user_id) FROM stdin;
\.


--
-- Data for Name: invoices_invoice_companies; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.invoices_invoice_companies (id, invoice_id, company_id) FROM stdin;
\.


--
-- Data for Name: invoices_invoice_teams; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.invoices_invoice_teams (id, invoice_id, teams_id) FROM stdin;
\.


--
-- Data for Name: invoices_invoicehistory; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.invoices_invoicehistory (id, invoice_title, invoice_number, name, email, quantity, rate, total_amount, currency, phone, created_on, amount_due, amount_paid, is_email_sent, status, details, due_date, from_address_id, invoice_id, to_address_id, updated_by_id) FROM stdin;
\.


--
-- Data for Name: invoices_invoicehistory_assigned_to; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.invoices_invoicehistory_assigned_to (id, invoicehistory_id, user_id) FROM stdin;
\.


--
-- Data for Name: leads_lead; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.leads_lead (id, title, first_name, last_name, email, phone, status, source, website, description, company_name, opportunity_amount, created_on, is_active, enquery_type, created_by_id, address_line, city, country, postcode, state, street, created_from_site) FROM stdin;
\.


--
-- Data for Name: leads_lead_assigned_to; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.leads_lead_assigned_to (id, lead_id, user_id) FROM stdin;
\.


--
-- Data for Name: leads_lead_contacts; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.leads_lead_contacts (id, lead_id, contact_id) FROM stdin;
\.


--
-- Data for Name: leads_lead_teams; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.leads_lead_teams (id, lead_id, teams_id) FROM stdin;
\.


--
-- Data for Name: marketing_blockeddomain; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.marketing_blockeddomain (id, domain, created_on, created_by_id) FROM stdin;
\.


--
-- Data for Name: marketing_blockedemail; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.marketing_blockedemail (id, email, created_on, created_by_id) FROM stdin;
\.


--
-- Data for Name: marketing_campaign; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.marketing_campaign (id, title, created_on, schedule_date_time, reply_to_email, subject, html, html_processed, from_email, from_name, sent, opens, opens_unique, bounced, status, created_by_id, email_template_id, updated_on, timezone, attachment) FROM stdin;
\.


--
-- Data for Name: marketing_campaign_contact_lists; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.marketing_campaign_contact_lists (id, campaign_id, contactlist_id) FROM stdin;
\.


--
-- Data for Name: marketing_campaign_tags; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.marketing_campaign_tags (id, campaign_id, tag_id) FROM stdin;
\.


--
-- Data for Name: marketing_campaigncompleted; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.marketing_campaigncompleted (id, is_completed, campaign_id) FROM stdin;
\.


--
-- Data for Name: marketing_campaignlinkclick; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.marketing_campaignlinkclick (id, ip_address, created_on, user_agent, campaign_id, contact_id, link_id) FROM stdin;
\.


--
-- Data for Name: marketing_campaignlog; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.marketing_campaignlog (id, created_on, message_id, campaign_id, contact_id) FROM stdin;
\.


--
-- Data for Name: marketing_campaignopen; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.marketing_campaignopen (id, ip_address, created_on, user_agent, campaign_id, contact_id) FROM stdin;
\.


--
-- Data for Name: marketing_contact; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.marketing_contact (id, created_on, name, email, contact_number, is_unsubscribed, is_bounced, company_name, last_name, city, state, contry, created_by_id, updated_on) FROM stdin;
\.


--
-- Data for Name: marketing_contact_contact_list; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.marketing_contact_contact_list (id, contact_id, contactlist_id) FROM stdin;
\.


--
-- Data for Name: marketing_contactemailcampaign; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.marketing_contactemailcampaign (id, name, email, last_name, created_on, created_by_id) FROM stdin;
\.


--
-- Data for Name: marketing_contactlist; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.marketing_contactlist (id, created_on, name, created_by_id, updated_on) FROM stdin;
\.


--
-- Data for Name: marketing_contactlist_tags; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.marketing_contactlist_tags (id, contactlist_id, tag_id) FROM stdin;
\.


--
-- Data for Name: marketing_contactlist_visible_to; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.marketing_contactlist_visible_to (id, contactlist_id, user_id) FROM stdin;
\.


--
-- Data for Name: marketing_contactunsubscribedcampaign; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.marketing_contactunsubscribedcampaign (id, is_unsubscribed, campaigns_id, contacts_id) FROM stdin;
\.


--
-- Data for Name: marketing_duplicatecontacts; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.marketing_duplicatecontacts (id, contact_list_id, contacts_id) FROM stdin;
\.


--
-- Data for Name: marketing_emailtemplate; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.marketing_emailtemplate (id, created_on, title, subject, html, created_by_id, updated_on) FROM stdin;
\.


--
-- Data for Name: marketing_failedcontact; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.marketing_failedcontact (id, created_on, name, email, contact_number, company_name, last_name, city, state, contry, created_by_id) FROM stdin;
\.


--
-- Data for Name: marketing_failedcontact_contact_list; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.marketing_failedcontact_contact_list (id, failedcontact_id, contactlist_id) FROM stdin;
\.


--
-- Data for Name: marketing_link; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.marketing_link (id, original, clicks, "unique", campaign_id) FROM stdin;
\.


--
-- Data for Name: marketing_tag; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.marketing_tag (id, name, color, created_by_id, created_on) FROM stdin;
\.


--
-- Data for Name: opportunity_opportunity; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.opportunity_opportunity (id, name, stage, currency, amount, lead_source, probability, closed_on, description, created_on, is_active, closed_by_id, created_by_id, company_id) FROM stdin;
\.


--
-- Data for Name: opportunity_opportunity_assigned_to; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.opportunity_opportunity_assigned_to (id, opportunity_id, user_id) FROM stdin;
\.


--
-- Data for Name: opportunity_opportunity_contacts; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.opportunity_opportunity_contacts (id, opportunity_id, contact_id) FROM stdin;
\.


--
-- Data for Name: opportunity_opportunity_tags; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.opportunity_opportunity_tags (id, opportunity_id, tags_id) FROM stdin;
\.


--
-- Data for Name: opportunity_opportunity_teams; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.opportunity_opportunity_teams (id, opportunity_id, teams_id) FROM stdin;
\.


--
-- Data for Name: planner_event; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.planner_event (id, name, event_type, object_id, status, direction, start_date, close_date, duration, priority, updated_on, created_on, description, is_active, content_type_id, created_by_id, updated_by_id) FROM stdin;
\.


--
-- Data for Name: planner_event_assigned_to; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.planner_event_assigned_to (id, event_id, user_id) FROM stdin;
\.


--
-- Data for Name: planner_event_attendees_contacts; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.planner_event_attendees_contacts (id, event_id, contact_id) FROM stdin;
\.


--
-- Data for Name: planner_event_attendees_leads; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.planner_event_attendees_leads (id, event_id, lead_id) FROM stdin;
\.


--
-- Data for Name: planner_event_attendees_user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.planner_event_attendees_user (id, event_id, user_id) FROM stdin;
\.


--
-- Data for Name: planner_event_reminders; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.planner_event_reminders (id, event_id, reminder_id) FROM stdin;
\.


--
-- Data for Name: planner_reminder; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.planner_reminder (id, reminder_type, reminder_time) FROM stdin;
\.


--
-- Data for Name: project_expenses_expensetype; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.project_expenses_expensetype (id, name, is_active) FROM stdin;
5	泥水項目	t
3	訂造傢俬	t
7	訂造木門/玻璃門	t
8	油漆項目	t
9	鋁窗項目	t
10	地台項目	t
11	天花項目	t
4	電燈項目	t
1	水喉項目	t
12	其他項目	t
\.


--
-- Data for Name: project_expenses_projectexpense; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.project_expenses_projectexpense (id, name, price, pic, remark, pay_date, project_id, expense_type_id, img, img_upload_date, img_height, img_width) FROM stdin;
55	a	20.55	d		2021-02-15	110	11		2021-02-15	1	1
33	sfsd	1000.00	123		2020-11-20	78	1		2020-11-20	1	1
53	a	20.22	d		2021-02-15	167	11	companies/15/expense/189bdf5d-b0e.jpg	2021-02-16	1	1
36	1345	24773.00	DC xc		2020-11-25	117	1	companies/11/expense/85687506-0be.png	2020-11-20	1	1
37	1684	4994.00	＃		2020-11-21	147	1		2020-11-21	1	1
38	完成	3497976.00	！		2020-11-21	147	1		2020-11-21	1	1
39	testing	100000.00	ghost		2020-12-07	149	1	companies/35/expense/5fa117b0-f30.jpg	2020-12-07	1	1
40	新造泥水項目	25000.00	冮耀輝		2020-12-15	148	1	companies/20/expense/37fa7424-91b.jpg	2020-12-10	1	1
41	加改水喉	5000.00	龍		2020-12-07	148	4	companies/20/expense/0e4c9f69-163.jpg	2020-12-10	1	1
56	test	100.99	a		2021-02-16	178	12		2021-02-16	1	1
57	s	123.44	s		2021-02-16	178	12		2021-02-16	1	1
58	牆身髹油	8000.00	榮仔	全屋牆身	2021-02-18	165	8	companies/20/expense/de2289b5-5b7.jpg	2021-02-18	1	1
27	test	1.00	a		2020-11-19	78	1	companies/15/expense/689196ad-748.jpg	\N	1	1
28	test	10000.00	test		2020-11-20	78	1	companies/15/expense/889f1c5d-63d.jpg	\N	1	1
35	test111111111111111111111111111111111111	100.55	test111111111111111111111111111111111111	123\n123	2020-11-20	78	1	companies/15/expense/93a4de1d-dc6.jpg	2020-11-20	1	1
59	天花髹底油	2000.00	榮仔	只髹底油	2021-02-18	165	11	companies/20/expense/3802abb3-cbd.jpg	2021-02-18	1	1
34	test	5000.00	tester	123\n123\nasd	2020-11-20	78	5		2020-11-20	1	1
42	新造泥水腳	5000.00	漢哥	防水	2021-02-03	173	12	companies/20/expense/42baca83-ad2.jpg	2021-02-03	1	1
43	買白泥	5.00	東哥	新威記	2021-02-03	173	12	companies/20/expense/681c4473-a40.jpg	2021-02-03	1	1
60	Testing	5896.00	Mr. X		2021-02-19	171	12		2021-02-19	1	1
61	Testing 2	78598.60	Mr.X		2021-02-19	171	1		2021-02-19	1	1
29	運費	500.00	PIC		2020-11-19	78	3	companies/15/expense/a4b410aa-b87.jpg	2020-11-20	1	1
30	水管工人	5000.00	PIC		2020-11-19	78	4	companies/15/expense/9e5d1b70-950.jpg	2020-11-20	1	1
31	464319	1000.00	sn dbej	O:) &(%/%	2020-11-28	96	1	companies/11/expense/2c12b729-39d.png	2020-11-20	1	1
32	a	465.00	djs	null	2020-11-20	97	1	companies/15/expense/80cd1d09-098.jpg	2020-11-20	1	1
47	test	2000.00	test		2021-02-15	97	12	companies/15/expense/085cada5-5f6.jpg	2021-02-15	1	1
46	a	300.00	a		2021-02-15	78	12	companies/15/expense/7a008f33-c07.jpg	2021-02-15	1	1
52	20	3890.00	Chan		2021-02-15	176	9	companies/11/expense/8ffb8972-68e.png	2021-02-15	1	1
51	test2	1234.11	teset		2021-02-15	97	12		2021-02-15	1	1
54	asweda	11.14	asdasd		2021-02-15	78	11		2021-02-15	1	1
\.


--
-- Data for Name: project_items_item; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.project_items_item (id, name, is_active, item_type_id, value_based_price, item_formulas, item_properties_sort, index) FROM stdin;
27	新造地台防水	t	4	3000.00	[{"name": "Suggested Unit Price", "formula": "\\"value_based_price\\"+\\"material.value_based_price\\"", "is_active": "True"}, {"name": "Suggested Quantity", "formula": "1", "is_active": "True"}]	[]	0
1	新造電視地櫃	t	2	1500.00	[{"name": "Suggested Unit Price", "formula": "\\"value_based_price\\"+\\"material.value_based_price\\"", "is_active": "True"}, {"name": "Suggested Quantity", "formula": "1", "is_active": "True"}]	[1, 2]	0
42	新造瓷磚地台	f	4	85.00	[{"name": "Suggested Unit Price", "formula": "\\"value_based_price\\"+\\"material.value_based_price\\"", "is_active": "True"}, {"name": "Suggested Quantity", "formula": "\\"L\\"*\\"W\\"", "is_active": "True"}, {"name": "Area", "formula": "\\"L\\"*\\"W\\"", "is_active": "True"}]	[2, 1]	0
37	新造DATA制位	t	1	850.00	[{"name": "Suggested Unit Price", "formula": "\\"value_based_price\\"+\\"material.value_based_price\\"", "is_active": "True"}, {"name": "Suggested Quantity", "formula": "1", "is_active": "True"}]	[]	0
10	洗手盤	t	3	2000.00	[{"name": "Suggested Unit Price", "formula": "\\"value_based_price\\"+\\"material.value_based_price\\"", "is_active": "True"}, {"name": "Suggested Quantity", "formula": "1", "is_active": "True"}]	[2, 1]	0
21	新造13A單位制	t	1	850.00	[{"name": "Suggested Unit Price", "formula": "\\"value_based_price\\"+\\"material.value_based_price\\"", "is_active": "True"}, {"name": "Suggested Quantity", "formula": "1", "is_active": "True"}]	[]	0
18	新造床頭櫃	t	2	1500.00	[{"name": "Suggested Unit Price", "formula": "\\"value_based_price\\"+\\"material.value_based_price\\"", "is_active": "True"}, {"name": "Suggested Quantity", "formula": "1", "is_active": "True"}]	[2, 1]	0
40	新造單人床	t	2	0.00	[{"name": "Suggested Quantity", "formula": "1", "is_active": "True"}, {"name": "Suggested Unit Price", "formula": "\\"value_based_price\\"+\\"material.value_based_price\\"", "is_active": "True"}]	[2, 1]	0
17	新造全高衣櫃	t	2	2700.00	[{"name": "Suggested Unit Price", "formula": "\\"value_based_price\\"+\\"material.value_based_price\\"", "is_active": "True"}, {"name": "Suggested Quantity", "formula": "1", "is_active": "True"}]	[2, 1]	0
4	新造開關燈制位	t	1	850.00	[{"name": "Suggested Unit Price", "formula": "\\"value_based_price\\"+\\"material.value_based_price\\"", "is_active": "True"}, {"name": "Suggested Quantity", "formula": "1", "is_active": "True"}]	[]	0
26	新砌泥水企缸	t	4	3000.00	[{"name": "Suggested Unit Price", "formula": "\\"value_based_price\\"+\\"material.value_based_price\\"", "is_active": "True"}, {"name": "Suggested Quantity", "formula": "1", "is_active": "True"}]	[]	0
28	新造雲石吸咀	t	4	1000.00	[{"name": "Suggested Unit Price", "formula": "\\"value_based_price\\"+\\"material.value_based_price\\"", "is_active": "True"}, {"name": "Suggested Quantity", "formula": "1", "is_active": "True"}]	[]	0
30	新造窗台雲石	t	4	1000.00	[{"name": "Suggested Unit Price", "formula": "\\"value_based_price\\"+\\"material.value_based_price\\"", "is_active": "True"}, {"name": "Suggested Quantity", "formula": "1", "is_active": "True"}, {"name": "窗台雲石", "formula": "\\"L\\"*1000", "is_active": "True"}]	[1]	0
2	新造來水及去水(每一個位計算)	t	3	3000.00	[{"name": "Suggested Unit Price", "formula": "\\"value_based_price\\"+\\"material.value_based_price\\"", "is_active": "True"}, {"name": "Suggested Quantity", "formula": "1", "is_active": "True"}]	[2, 1]	0
14	代工安裝浴室寶 - 天花式	t	1	1000.00	[{"name": "Suggested Unit Price", "formula": "\\"value_based_price\\"+\\"material.value_based_price\\"", "is_active": "True"}, {"name": "Suggested Quantity", "formula": "1", "is_active": "True"}]	[]	0
31	修葺拆牆後泥水批當	t	4	1000.00	[{"name": "Suggested Unit Price", "formula": "\\"value_based_price\\"+\\"material.value_based_price\\"", "is_active": "True"}, {"name": "Suggested Quantity", "formula": "1", "is_active": "True"}]	[]	0
7	新造地櫃	t	2	1500.00	[{"name": "Suggested Unit Price", "formula": "\\"value_based_price\\"+\\"material.value_based_price\\"", "is_active": "True"}, {"name": "Suggested Quantity", "formula": "1", "is_active": "True"}]	[2, 1]	0
8	新造鏡櫃	t	2	1200.00	[{"name": "Suggested Unit Price", "formula": "\\"value_based_price\\"+\\"material.value_based_price\\"", "is_active": "True"}, {"name": "Suggested Quantity", "formula": "1", "is_active": "True"}]	[1]	0
9	磁磚	t	5	20.00	[{"name": "Suggested Unit Price", "formula": "\\"value_based_price\\"+\\"material.value_based_price\\"", "is_active": "True"}, {"name": "Suggested Quantity", "formula": "1", "is_active": "True"}]	[2, 1]	0
32	新造窗口窗邊雲石	t	4	1000.00	[{"name": "Suggested Unit Price", "formula": "\\"value_based_price\\"+\\"material.value_based_price\\"", "is_active": "True"}, {"name": "Suggested Quantity", "formula": "1", "is_active": "True"}]	[]	0
24	新造地台磁磚	t	4	100.00	[{"name": "地台面積", "formula": "\\"L\\"*\\"W\\"", "is_active": "True"}, {"name": "Suggested Unit Price", "formula": "\\"value_based_price\\"+\\"material.value_based_price\\"", "is_active": "True"}, {"name": "Suggested Quantity", "formula": "1", "is_active": "True"}]	[2, 1]	0
11	座廁	t	3	2000.00	[{"name": "Suggested Unit Price", "formula": "\\"value_based_price\\"+\\"material.value_based_price\\"", "is_active": "True"}, {"name": "Suggested Quantity", "formula": "1", "is_active": "True"}]	[2, 1]	0
15	代工安裝浴室寶 - 窗口式	t	1	1000.00	[{"name": "Suggested Unit Price", "formula": "\\"value_based_price\\"+\\"material.value_based_price\\"", "is_active": "True"}, {"name": "Suggested Quantity", "formula": "1", "is_active": "True"}]	[]	0
5	新造天花燈位	t	1	850.00	[{"name": "Suggested Unit Price", "formula": "\\"value_based_price\\"+\\"material.value_based_price\\"", "is_active": "True"}, {"name": "Suggested Quantity", "formula": "1", "is_active": "True"}]	[2, 1]	0
68	新造地櫃枱面雲石或仿石	t	2	1100.00	[{"name": "Suggested Unit Price", "formula": "\\"value_based_price\\"+\\"material.value_based_price\\"", "is_active": "True"}, {"name": "Suggested Quantity", "formula": "1", "is_active": "True"}]	[]	0
62	新造窗簾殻	t	5	150.00	[{"name": "Suggested Unit Price", "formula": "\\"value_based_price\\"+\\"material.value_based_price\\"", "is_active": "True"}, {"name": "Suggested Quantity", "formula": "1", "is_active": "True"}]	[]	0
53	新造冷氣開關掣	t	1	1200.00	[{"name": "Suggested Unit Price", "formula": "\\"value_based_price\\"+\\"material.value_based_price\\"", "is_active": "True"}, {"name": "Suggested Quantity", "formula": "1", "is_active": "True"}]	[]	0
55	新造來去水喉(廚房)	t	3	15000.00	[{"name": "Suggested Unit Price", "formula": "\\"value_based_price\\"+\\"material.value_based_price\\"", "is_active": "True"}, {"name": "Suggested Quantity", "formula": "1", "is_active": "True"}]	[]	0
51	新造傢俬燈槽供電位	t	1	850.00	[{"name": "Suggested Unit Price", "formula": "\\"value_based_price\\"+\\"material.value_based_price\\"", "is_active": "True"}, {"name": "Suggested Quantity", "formula": "1", "is_active": "True"}]	[]	0
49	新造天花射燈	t	1	850.00	[{"name": "Suggested Unit Price", "formula": "\\"value_based_price\\"+\\"material.value_based_price\\"", "is_active": "True"}, {"name": "Suggested Quantity", "formula": "1", "is_active": "True"}]	[]	0
48	新造牆身壁燈	t	1	850.00	[{"name": "Suggested Unit Price", "formula": "\\"value_based_price\\"+\\"material.value_based_price\\"", "is_active": "True"}, {"name": "Suggested Quantity", "formula": "1", "is_active": "True"}]	[]	0
47	新造15A以上電掣位	t	1	1200.00	[{"name": "Suggested Unit Price", "formula": "\\"value_based_price\\"+\\"material.value_based_price\\"", "is_active": "True"}, {"name": "Suggested Quantity", "formula": "1", "is_active": "True"}]	[]	0
46	新造AV長方膠糟	t	1	1200.00	[{"name": "Suggested Unit Price", "formula": "\\"value_based_price\\"+\\"material.value_based_price\\"", "is_active": "True"}, {"name": "Suggested Quantity", "formula": "1", "is_active": "True"}]	[]	0
45	新造TV天線位	t	1	850.00	[{"name": "Suggested Unit Price", "formula": "\\"value_based_price\\"+\\"material.value_based_price\\"", "is_active": "True"}, {"name": "Suggested Quantity", "formula": "1", "is_active": "True"}]	[]	0
44	新造雙人床	t	2	0.00	[{"name": "Suggested Unit Price", "formula": "\\"value_based_price\\"+\\"material.value_based_price\\"", "is_active": "True"}, {"name": "Suggested Quantity", "formula": "1", "is_active": "True"}]	[2, 1]	0
25	新造泥水腳座	t	4	1500.00	[{"name": "Suggested Unit Price", "formula": "\\"value_based_price\\"+\\"material.value_based_price\\"", "is_active": "True"}, {"name": "Suggested Quantity", "formula": "1", "is_active": "True"}]	[]	0
57	代工安裝浴室潔具	t	3	2000.00	[{"name": "Suggested Unit Price", "formula": "\\"value_based_price\\"+\\"material.value_based_price\\"", "is_active": "True"}, {"name": "Suggested Quantity", "formula": "1", "is_active": "True"}]	[]	0
50	新造天花燈槽供電位	t	1	850.00	[{"name": "Suggested Unit Price", "formula": "\\"value_based_price\\"+\\"material.value_based_price\\"", "is_active": "True"}, {"name": "Suggested Quantity", "formula": "1", "is_active": "True"}]	[]	0
16	新造天花乳膠漆(包括由防潮油批灰打磨)	t	6	30.00	[{"name": "天花面積", "formula": "\\"L\\"*\\"W\\"", "is_active": "True"}, {"name": "Suggested Unit Price", "formula": "\\"value_based_price\\"+\\"material.value_based_price\\"", "is_active": "True"}, {"name": "Suggested Quantity", "formula": "1", "is_active": "True"}]	[2, 1]	0
56	新造來去水喉(浴室)	t	3	15000.00	[{"name": "Suggested Unit Price", "formula": "\\"value_based_price\\"+\\"material.value_based_price\\"", "is_active": "True"}, {"name": "Suggested Quantity", "formula": "1", "is_active": "True"}]	[]	0
52	新造冷氣供電位	t	1	1200.00	[{"name": "Suggested Unit Price", "formula": "\\"value_based_price\\"+\\"material.value_based_price\\"", "is_active": "True"}, {"name": "Suggested Quantity", "formula": "1", "is_active": "True"}]	[]	0
61	新造假天花燈槽	t	5	550.00	[{"name": "Suggested Unit Price", "formula": "\\"value_based_price\\"+\\"material.value_based_price\\"", "is_active": "True"}, {"name": "Suggested Quantity", "formula": "1", "is_active": "True"}]	[]	0
60	新造假天花	t	5	50.00	[{"name": "Suggested Unit Price", "formula": "\\"value_based_price\\"+\\"material.value_based_price\\"", "is_active": "True"}, {"name": "Suggested Quantity", "formula": "1", "is_active": "True"}]	[2, 1]	0
54	新造燈曲	t	1	1200.00	[{"name": "Suggested Unit Price", "formula": "\\"value_based_price\\"+\\"material.value_based_price\\"", "is_active": "True"}, {"name": "Suggested Quantity", "formula": "1", "is_active": "True"}]	[]	0
65	新造牆身防水	t	4	3000.00	[{"name": "Suggested Unit Price", "formula": "\\"value_based_price\\"+\\"material.value_based_price\\"", "is_active": "True"}, {"name": "Suggested Quantity", "formula": "1", "is_active": "True"}]	[]	0
66	新造企缸或浴缸防水	t	4	3000.00	[{"name": "Suggested Unit Price", "formula": "\\"value_based_price\\"+\\"material.value_based_price\\"", "is_active": "True"}, {"name": "Suggested Quantity", "formula": "1", "is_active": "True"}]	[]	0
63	新造冷氣機木殻	t	5	250.00	[{"name": "Suggested Unit Price", "formula": "\\"value_based_price\\"+\\"material.value_based_price\\"", "is_active": "True"}, {"name": "Suggested Quantity", "formula": "1", "is_active": "True"}]	[]	0
20	新造13A雙位制	t	1	1200.00	[{"name": "Suggested Unit Price", "formula": "\\"value_based_price\\"+\\"material.value_based_price\\"", "is_active": "True"}, {"name": "Suggested Quantity", "formula": "1", "is_active": "True"}]	[]	0
6	鋅盤	t	3	0.00	[{"name": "Suggested Unit Price", "formula": "\\"value_based_price\\"+\\"material.value_based_price\\"", "is_active": "True"}, {"name": "Suggested Quantity", "formula": "1", "is_active": "True"}]	[2, 1]	0
83	新造子母大門	t	12	9000.00	[{"name": "Suggested Unit Price", "formula": "\\"value_based_price\\"+\\"material.value_based_price\\"", "is_active": "True"}, {"name": "Suggested Quantity", "formula": "1", "is_active": "True"}]	[]	0
81	外牆棚架連第三者保險	t	7	5000.00	[{"name": "Suggested Unit Price", "formula": "\\"value_based_price\\"+\\"material.value_based_price\\"", "is_active": "True"}, {"name": "Suggested Quantity", "formula": "1", "is_active": "True"}]	[]	0
79	新造電力總制箱	t	1	1.00	[{"name": "Suggested Unit Price", "formula": "\\"value_based_price\\"+\\"material.value_based_price\\"", "is_active": "True"}, {"name": "Suggested Quantity", "formula": "1", "is_active": "True"}]	[]	0
80	新造全屋50料鋁窗	t	7	250.00	[{"name": "Suggested Unit Price", "formula": "\\"value_based_price\\"+\\"material.value_based_price\\"", "is_active": "True"}, {"name": "Suggested Quantity", "formula": "1", "is_active": "True"}]	[]	0
78	新造儲物地台床	t	2	420.00	[{"name": "Suggested Unit Price", "formula": "\\"value_based_price\\"+\\"material.value_based_price\\"", "is_active": "True"}, {"name": "Suggested Quantity", "formula": "1", "is_active": "True"}]	[]	0
77	新造全高陳列櫃	t	2	2550.00	[{"name": "Suggested Unit Price", "formula": "\\"value_based_price\\"+\\"material.value_based_price\\"", "is_active": "True"}, {"name": "Suggested Quantity", "formula": "1", "is_active": "True"}]	[]	0
76	新造全高儲物櫃	t	2	2550.00	[{"name": "Suggested Unit Price", "formula": "\\"value_based_price\\"+\\"material.value_based_price\\"", "is_active": "True"}, {"name": "Suggested Quantity", "formula": "1", "is_active": "True"}]	[]	0
75	新造書枱/梳妝台	t	2	1500.00	[{"name": "Suggested Unit Price", "formula": "\\"value_based_price\\"+\\"material.value_based_price\\"", "is_active": "True"}, {"name": "Suggested Quantity", "formula": "1", "is_active": "True"}]	[]	0
39	新造牆身乳膠漆(包括由防潮油批灰打磨)	t	6	30.00	[{"name": "牆身面積", "formula": "\\"W\\"*\\"H\\"*2+\\"L\\"*\\"H\\"*2", "is_active": "True"}, {"name": "Suggested Quantity", "formula": "1", "is_active": "True"}, {"name": "Suggested Unit Price", "formula": "\\"value_based_price\\"+\\"material.value_based_price\\"", "is_active": "True"}]	[3, 2, 1]	0
82	新造單掩大門	t	12	7000.00	[{"name": "Suggested Unit Price", "formula": "\\"value_based_price\\"+\\"material.value_based_price\\"", "is_active": "True"}, {"name": "Suggested Quantity", "formula": "1", "is_active": "True"}]	[]	0
84	新造空心木門	t	12	5500.00	[{"name": "Suggested Unit Price", "formula": "\\"value_based_price\\"+\\"material.value_based_price\\"", "is_active": "True"}, {"name": "Suggested Quantity", "formula": "1", "is_active": "True"}]	[]	0
85	新造空心木趟門	t	12	6000.00	[{"name": "Suggested Unit Price", "formula": "\\"value_based_price\\"+\\"material.value_based_price\\"", "is_active": "True"}, {"name": "Suggested Quantity", "formula": "1", "is_active": "True"}]	[]	0
23	新造牆身磁磚	t	4	100.00	[{"name": "Suggested Unit Price", "formula": "\\"value_based_price\\"+\\"material.value_based_price\\"", "is_active": "True"}, {"name": "牆身面積", "formula": "\\"W\\"*\\"H\\"*2+\\"L\\"*\\"H\\"*2", "is_active": "True"}, {"name": "Suggested Quantity", "formula": "1", "is_active": "True"}]	[3, 2, 1]	0
3	新造吊櫃	t	2	1200.00	[{"name": "Suggested Unit Price", "formula": "\\"value_based_price\\"+\\"material.value_based_price\\"", "is_active": "True"}, {"name": "Suggested Quantity", "formula": "1", "is_active": "True"}]	[2, 1]	0
86	代工安裝實心大門	t	12	2500.00	[{"name": "Suggested Unit Price", "formula": "\\"value_based_price\\"+\\"material.value_based_price\\"", "is_active": "True"}, {"name": "Suggested Quantity", "formula": "1", "is_active": "True"}]	[]	0
87	代工安代裝空心房門	t	12	2000.00	[{"name": "Suggested Unit Price", "formula": "\\"value_based_price\\"+\\"material.value_based_price\\"", "is_active": "True"}, {"name": "Suggested Quantity", "formula": "1", "is_active": "True"}]	[]	0
\.


--
-- Data for Name: project_items_item_item_properties; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.project_items_item_item_properties (id, item_id, itemproperty_id) FROM stdin;
1	1	1
3	2	1
4	3	1
5	3	2
6	6	1
7	6	2
9	7	1
10	7	2
12	8	1
15	2	2
16	9	1
17	9	2
18	10	1
19	10	2
21	11	1
22	11	2
24	5	1
25	5	2
27	17	1
28	17	2
30	18	1
31	18	2
33	16	1
34	16	2
35	23	1
36	23	2
37	30	1
47	39	1
48	39	2
50	40	1
51	40	2
54	42	1
55	42	2
58	44	1
59	44	2
62	60	1
63	60	2
66	24	1
67	24	2
78	23	3
81	39	3
86	1	2
\.


--
-- Data for Name: project_items_itemformula; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.project_items_itemformula (id, name, formula, item_id, is_active) FROM stdin;
1	Suggested Quantity	1	1	t
2	Suggested Unit Price	"L"*"W"*"value_based_price"	1	t
4	Suggested Quantity	1	5	t
5	Suggested Unit Price	"value_based_price"+5*"material.value_based_price"	5	t
\.


--
-- Data for Name: project_items_itemproperty; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.project_items_itemproperty (id, name, symbol, index) FROM stdin;
4	深度	D	0
1	長度	L	1
2	闊度	W	2
5	備註	R	0
3	高度	H	3
10	半徑	RD	0
\.


--
-- Data for Name: project_items_itemtype; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.project_items_itemtype (id, name, is_active, item_type_materials) FROM stdin;
5	天花項目	t	[{"name": "石膏板", "is_active": "True", "value_based_price": "50"}, {"name": "防潮石膏板", "is_active": "True", "value_based_price": "60"}, {"name": "鋁質長條天花", "is_active": "True", "value_based_price": "60"}]
4	泥水項目	t	[]
9	地台項目	t	[]
8	其他項目	t	[]
1	電燈項目	t	[{"name": "藏牆喉管", "is_active": "True", "value_based_price": "0"}, {"name": "明喉", "is_active": "True", "value_based_price": "0"}, {"name": "外牆防水制", "is_active": "True", "value_based_price": "300"}]
12	造門項目	t	\N
6	油漆項目	t	[]
7	鋁窗項目	t	[]
2	傢俬項目	t	[{"name": "木紋膠板", "is_active": "True", "value_based_price": "0"}, {"name": "玻璃櫃門", "is_active": "True", "value_based_price": "300"}]
3	水喉項目	t	[{"name": "藏牆喉管", "is_active": "True", "value_based_price": "0"}, {"name": "明喉", "is_active": "True", "value_based_price": "0"}]
\.


--
-- Data for Name: project_items_itemtypematerial; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.project_items_itemtypematerial (id, name, item_type_id, value_based_price, is_active) FROM stdin;
3	鋼	2	1.50	t
2	木	2	1.00	t
4	鋼	3	500.00	t
5	慳電膽	1	1.00	t
6	LED 燈膽	1	1.00	t
8	a	1	111.00	t
9	test 1	1	1.00	t
\.


--
-- Data for Name: project_misc_misc; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.project_misc_misc (id, name, suggested_unit_price, is_active) FROM stdin;
2	施工期間清除垃圾	500.00	t
4	清拆厨房磁磚	8000.00	t
5	清拆厠所磁磚	8000.00	t
3	裝修完工清潔	1000.00	t
6	清拆客廳地板	10000.00	t
1	第三者保險	5000.00	t
9	提供公共地方走廊保護板	2000.00	t
10	提供室內原有門及窗保護	3000.00	t
11	室內設計費用	20000.00	t
\.


--
-- Data for Name: project_misc_projectmisc; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.project_misc_projectmisc (id, unit_price, quantity, remark, misc_id, project_id) FROM stdin;
162	5000.00	1	abctest	1	97
163	8000.00	1	aaaaaa	4	97
176	5000.00	1	test\ngg	1	178
180	20000.00	1	test2\nrow2	11	78
205	3000.00	1	123456	10	178
164	8000.00	1	qwaa ah hh!!ed=d ju HD a DC VT CD web VT f vm be 3rd xt VA avg	5	176
119	8000.00	100	\N	4	147
120	3000.00	1	\N	1	148
121	6000.00	1	\N	2	148
122	2500.00	1	\N	3	148
123	500.00	1	\N	2	147
125	5000.00	1	\N	1	152
126	5000.00	1	\N	1	149
127	5000.00	1	\N	1	161
128	1200.00	6	\N	2	161
131	8000.00	1	\N	5	166
132	1000.00	1	\N	3	168
133	10000.00	1	\N	6	147
134	5000.00	1	\N	3	165
135	10000.00	1	\N	6	165
136	2000.00	1	\N	2	165
137	10000.00	1	\N	6	170
138	8000.00	1	\N	5	170
139	8000.00	1	\N	4	170
140	3000.00	1	\N	3	170
141	5000.00	1	\N	1	170
142	5000.00	1	\N	2	170
143	10000.00	1	\N	6	171
144	5000.00	2	\N	5	171
145	8000.00	1	\N	4	171
146	500.00	1	\N	3	171
147	500.00	1	\N	2	171
148	8000.00	1	\N	1	171
155	3500.00	1	\N	1	173
156	10000.00	1	\N	6	173
157	10000.00	1	\N	5	173
158	10000.00	1	\N	4	173
160	3000.00	1	\N	3	173
159	7500.00	1	\N	2	173
161	400.00	1	\N	2	174
165	10.00	1	\N	6	176
167	8200.00	1	\N	3	176
168	18000.00	1	\N	4	176
169	500.11	1	\N	2	176
171	10000.55	1	\N	6	167
172	10000.88	1	\N	6	177
173	10000.00	1	\N	6	175
174	5000.00	1	\N	1	175
175	20000.00	1	\N	11	170
177	8000.00	3	\N	4	180
178	8000.00	1	\N	5	180
130	10000.00	1	全屋清拆	6	166
\.


--
-- Data for Name: project_timetable_projectmilestone; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.project_timetable_projectmilestone (id, name, date, remind, pic, description, project_id, img, img_upload_date, img_height, img_width) FROM stdin;
69	test 2	2020-11-18	00:00:01			78		2020-11-20	1	1
113	簽署合約	2021-02-04	00:00:05	我	第一期	175		2021-02-04	1	1
114	Qww	2021-02-15	00:00:01			176		2021-02-15	1	1
116	gdfgdf	2021-02-15	00:00:01			110		2021-02-16	1	1
117	木工	2021-01-18	00:00:01	榮仔		165		2021-02-18	1	1
67	hello	2020-11-14	00:00:01			78		2020-11-20	1	1
31	Test	2020-11-02	00:00:01	a	a	78	companies/15/milestone/5558d022-9a1.jpg	2020-10-30	1280	960
51	test	2020-11-18	00:00:01	test		78		2020-11-13	1	1
118	完工	2021-02-18	00:00:01	Joe		165		2021-02-18	1	1
71	shsnd	2020-11-17	00:00:07	vsnsb	sjmms	96		2020-11-20	1	1
93	123	2020-12-11	00:00:01		123\n123	78		2020-12-11	1	1
72	ftf	2020-11-30	00:00:01			117	companies/11/milestone/9a215284-884.png	2020-11-20	1	1
55	test	2020-11-25	00:00:01	test		78		2020-11-15	1	1
94	djdm	2020-12-21	00:00:01			147	companies/11/milestone/e432657e-540.png	2020-12-21	1	1
56	test	2020-11-17	00:00:01			78		2020-11-16	1	1
95	nsnd	2020-12-21	00:00:01			147	companies/11/milestone/439a46f5-3c6.jpg	2020-12-21	1	1
78	test 2	2020-11-27	00:00:01			78		2020-11-21	1	1
96	checking	2021-01-05	00:00:01	abc		148		2021-01-05	1	1
59	b	2020-10-07	00:00:01			78		2020-11-16	1	1
80	miles 26	2020-11-26	00:00:01			78		2020-11-21	1	1
81	miles 26 2	2020-11-26	00:00:01			78		2020-11-21	1	1
64	a	2020-11-11	00:00:01			78		2020-11-16	1	1
82	miles 26 3	2020-11-26	00:00:01			78		2020-11-21	1	1
66	b	2020-11-09	00:00:01			78		2020-11-16	1	1
83	test	2020-11-15	00:00:01			78		2020-11-21	1	1
84	aa	2020-11-05	00:00:01			78		2020-11-21	1	1
85	bb	2020-11-07	00:00:01			78		2020-11-21	1	1
97	testing	2020-09-30	00:00:01	who	hello	166		2021-01-13	1	1
98	testing	2020-09-30	00:00:01	who	hello	166		2021-01-13	1	1
99	testing	2020-09-30	00:00:01	who	hello	166		2021-01-13	1	1
87	ｌ	2020-11-21	00:00:01			96		2020-11-21	1	1
88	＾	2020-11-21	00:00:01			96		2020-11-21	1	1
89	？	2020-11-21	00:00:01			96		2020-11-21	1	1
90	testing done	2020-12-17	00:00:07	ghost	done	149	companies/35/milestone/483f5726-fb6.jpg	2020-12-07	1	1
100	testing	2020-09-30	00:00:01	who	hello	166		2021-01-13	1	1
91	checking socket	2020-12-11	00:00:01	Derek	checking window	148	companies/20/milestone/33571e6b-4cf.jpg	2020-12-10	1	1
92	checking lighting	2020-12-11	00:00:01			148	companies/20/milestone/aad78cf0-dd2.jpg	2020-12-10	1	1
120	Testing 2	2021-02-25	00:00:05	Test Name	NA	175		2021-02-23	1	1
122	Test Milestone	2021-02-24	00:00:01	Name	NA	175		2021-02-23	1	1
119	Testing	2021-02-24	00:00:05	YL	NA	175		2021-02-23	1	1
104	milestone 2	2021-01-22	00:00:01			78		2021-01-14	1	1
125	test 2	2021-03-05	00:00:01			78		2021-03-05	1	1
105	milestone 3	2021-01-16	00:00:01			78		2021-01-15	1	1
102	test milestone 1	2020-09-30	00:00:01	tester 2	hello	166		2021-01-13	1	1
106	ffff	2021-01-19	00:00:01	ffff	ddd	168		2021-01-19	1	1
103	milestone 1	2021-01-22	00:00:01	asd		78		2021-01-14	1	1
108	a	2021-01-21	00:00:01			147		2021-01-21	1	1
107	dndndm	2021-01-20	00:00:01			147		2021-01-20	1	1
110	與客人會面	2021-02-03	00:00:01	Kevin	第一次	173		2021-02-03	1	1
109	新造泥水腳	2021-02-03	00:00:05	漢哥	連防水	173		2021-02-03	1	1
\.


--
-- Data for Name: project_timetable_projectwork; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.project_timetable_projectwork (id, name, pic, start_date, end_date, description, project_id) FROM stdin;
56	work 2		2020-11-27	2020-11-28		78
58	work 26		2020-11-26	2020-11-27		78
59	work 26 2		2020-11-26	2020-11-27		78
60	work 26 3		2020-11-26	2020-11-27		78
61	test		2020-11-12	2020-11-15		78
62	aa		2020-11-05	2020-11-06		78
63	a		2020-11-06	2020-11-07		78
64	bb		2020-11-07	2020-11-08		78
66	4655		2020-11-21	2020-11-22		96
67	Ｐ		2020-11-21	2020-11-22		96
39	dffdf		2020-11-26	2020-11-28		117
69	testing	ghost	2020-12-17	2021-01-23	hea	149
71	testing 2	ghost	2020-12-17	2020-12-26		149
72	work 1		2020-12-17	2020-12-18		78
73	a		2020-12-07	2020-12-08		152
19	aa		2020-10-30	2020-10-31		78
74	meeting with clients		2020-12-10	2020-12-11	discuss window	148
25	a		2020-10-07	2020-10-07		78
27	d		2020-10-31	2020-10-31		78
29	test	test	2020-10-30	2020-10-31		78
79	123		2020-12-11	2020-12-12	123\n123\n123	78
80	sndmd	sdd	2020-12-21	2020-12-22		147
26	test		2020-11-13	2020-11-13		78
81	dndmd		2020-12-21	2020-12-22		147
68	window sill		2020-12-07	2020-12-11		148
22	TEST	test	2020-11-03	2020-11-03		78
82	工作一	林	2021-01-13	2021-01-19	髹油	148
83	work 1		2021-01-21	2021-01-22		78
84	ghhj	hhj	2021-01-19	2021-01-20	ghhj	168
86	更改座廁盆	東哥	2021-02-03	2021-02-04	加大	173
37	test 3	test 3	2020-11-02	2020-11-03		78
87	牆身髹油	漢哥	2021-02-03	2021-02-05	底油	173
38	scjcf	SD vc	2020-11-17	2020-11-18	s,;-)	96
40	cghj		2020-11-26	2020-11-27		117
88	檢查	逸名	2018-02-06	2021-04-28	檢查及執漏	175
42	hsbs		2020-11-29	2020-11-30		117
89	wos	jjj	2021-02-18	2021-02-19	kks	176
91	hfgdh		2021-02-17	2021-02-18		97
92	fgdgf		2021-02-15	2021-02-16		110
93	第三次會議	Miu	2021-02-18	2021-02-26		165
94	Testing	I	2021-02-22	2021-02-28	NA	165
95	Test Job Task	Name	2021-02-26	2021-02-27	NA	175
\.


--
-- Data for Name: projects_companyprojectcomparison; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.projects_companyprojectcomparison (id, company_id) FROM stdin;
1	2
4	20
3	11
2	15
\.


--
-- Data for Name: projects_companyprojectcomparison_projects; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.projects_companyprojectcomparison_projects (id, companyprojectcomparison_id, project_id) FROM stdin;
66	2	78
67	2	81
73	4	148
75	4	173
76	4	161
77	3	176
78	3	163
79	2	166
80	2	167
81	2	178
\.


--
-- Data for Name: projects_project; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.projects_project (id, project_title, created_on, amount_due, amount_paid, is_email_sent, status, details, start_date, due_date, district, work_location, company_id, created_by_id, charging_stages, document_format, invoice_remarks, job_no, quotation_generated_on, quotation_no, quotation_remarks, receipt_remarks, updated_on, quotation_version) FROM stdin;
168	abcjshs	2021-01-19 04:44:27.567949+00	\N	\N	f	In Progress	\N	2020-09-15	2021-02-27	Central and Western	jsjsjjdjs	35	43	[{"value": 98}, {"value": 1}, {"value": 1}]	{"quot_lower_format": "Alphabet", "quot_upper_format": "A", "quot_middle_format": "Date", "invoice_lower_format": "Alphabet", "invoice_upper_format": "A", "project_lower_format": "Number", "project_upper_format": "A", "receipt_lower_format": "Alphabet", "receipt_upper_format": "A", "invoice_middle_format": "Date", "receipt_middle_format": "Date"}	[]	5	2021-03-04 10:50:15.247829+00	\N	[{"index": 1, "content": "comment 1"}]	[]	2021-03-04 10:49:44.920769+00	2
151	testing 2	2020-12-06 17:54:01.680311+00	\N	\N	f	Early Stage	\N	2020-12-07	2020-12-14	Central and Western	大浦	35	43	[{"value": 98}, {"value": 1}, {"value": 1}]	{"quot_lower_format": "Alphabet", "quot_upper_format": "A", "quot_middle_format": "Date", "invoice_lower_format": "Alphabet", "invoice_upper_format": "A", "project_lower_format": "Number", "project_upper_format": "A", "receipt_lower_format": "Alphabet", "receipt_upper_format": "A", "invoice_middle_format": "Date", "receipt_middle_format": "Date"}	[]	2	\N	\N	[{"index": 1, "content": "comment 1"}]	[]	2020-12-06 17:54:01.680351+00	0
81	221testing	2020-10-27 08:55:49.220264+00	\N	\N	f	Finished	\N	2020-10-27	2020-11-03	Central and Western	abc	15	24	[{"value": 100}]	{"quot_lower_format": "Alphabet", "quot_upper_format": "A", "quot_middle_format": "Date", "invoice_lower_format": "Alphabet", "invoice_upper_format": "A", "project_lower_format": "Number", "project_upper_format": "A", "receipt_lower_format": "Alphabet", "receipt_upper_format": "A", "invoice_middle_format": "Date", "receipt_middle_format": "Date"}	[{"index": 1, "content": "sadsadsadsad"}]	4	2020-12-06 18:14:49.228784+00	\N	[{"index": 1, "content": "asdasdsads"}]	[{"index": 1, "content": "dsadasdasdsa"}]	2020-11-21 05:39:54.9181+00	0
160	test	2020-12-07 10:13:42.536956+00	\N	\N	f	Early Stage	\N	2020-12-07	2020-12-14	Central and Western	a	35	43	[{"value": 98}, {"value": 1}, {"value": 1}]	{"quot_lower_format": "Alphabet", "quot_upper_format": "A", "quot_middle_format": "Date", "invoice_lower_format": "Alphabet", "invoice_upper_format": "A", "project_lower_format": "Number", "project_upper_format": "A", "receipt_lower_format": "Alphabet", "receipt_upper_format": "A", "invoice_middle_format": "Date", "receipt_middle_format": "Date"}	[]	4	\N	\N	[{"index": 1, "content": "comment 1"}]	[]	2020-12-07 10:13:42.536992+00	0
163	bsnns	2020-12-31 03:18:02.251317+00	\N	\N	f	Early Stage	\N	2020-12-31	2021-01-07	Central and Western	zhjsn	11	28	[{"value": 25}, {"value": 25}, {"value": 50}]	{"quot_lower_format": "Alphabet", "quot_upper_format": "A", "quot_middle_format": "Date", "invoice_lower_format": "Alphabet", "invoice_upper_format": "A", "project_lower_format": "Number", "project_upper_format": "A", "receipt_lower_format": "Alphabet", "receipt_upper_format": "A", "invoice_middle_format": "Date", "receipt_middle_format": "Date"}	[]	10	\N	\N	[{"index": 1, "content": "jdiekn1263"}]	[]	2020-12-31 03:18:02.251365+00	0
179	Testing	2021-02-23 04:10:49.761455+00	\N	\N	f	Finished	\N	2021-02-01	2021-02-22	Central and Western	Location	20	23	[{"value": 40}, {"value": 30}, {"value": 30}]	{"quot_lower_format": "Alphabet", "quot_upper_format": "Q", "quot_middle_format": "Date", "invoice_lower_format": "Alphabet", "invoice_upper_format": "I", "project_lower_format": "Number", "project_upper_format": "J", "receipt_lower_format": "Alphabet", "receipt_upper_format": "R", "invoice_middle_format": "Date", "receipt_middle_format": "Date"}	[{"index": 1, "content": "請於三十日內"}]	15	2021-02-23 04:13:23.092342+00	\N	[{"index": 1, "content": "此報價單有效日期為30天"}]	[]	2021-02-23 04:12:55.641514+00	1
176	Test Project A	2021-02-15 11:31:12.257821+00	\N	\N	f	In Progress	\N	2020-09-09	2021-05-29	Kwai Tsing	Tai Po, HK	11	28	[{"value": 25}, {"value": 25}, {"value": 50}]	{"quot_lower_format": "Alphabet", "quot_upper_format": "A", "quot_middle_format": "Date", "invoice_lower_format": "Alphabet", "invoice_upper_format": "A", "project_lower_format": "Number", "project_upper_format": "A", "receipt_lower_format": "Alphabet", "receipt_upper_format": "A", "invoice_middle_format": "Date", "receipt_middle_format": "Date"}	[]	12	2021-03-04 10:01:37.597796+00	\N	[{"index": 1, "content": "jdiekn1263"}]	[]	2021-03-04 09:59:59.159715+00	2
147	snsks	2020-11-21 05:33:12.300537+00	\N	\N	f	Finished	\N	2020-11-26	2020-11-29	Kwun Tong	sndnso	11	28	[{"value": 25}, {"value": 25}, {"value": 50}]	{"quot_lower_format": "Alphabet", "quot_upper_format": "A", "quot_middle_format": "Date", "invoice_lower_format": "Alphabet", "invoice_upper_format": "A", "project_lower_format": "Number", "project_upper_format": "A", "receipt_lower_format": "Alphabet", "receipt_upper_format": "A", "invoice_middle_format": "Date", "receipt_middle_format": "Date"}	[]	9	2021-02-23 01:53:35.481849+00	\N	[{"index": 1, "content": "jdiekn1263"}]	[]	2021-02-15 10:58:37.368342+00	4
117	testing1	2020-11-20 12:45:36.220995+00	\N	\N	f	Finished	\N	2020-11-20	2020-11-27	Kowloon City	null	11	28	[{"value": 25}, {"value": 25}, {"value": 50}]	{"quot_lower_format": "Alphabet", "quot_upper_format": "A", "quot_middle_format": "Date", "invoice_lower_format": "Alphabet", "invoice_upper_format": "A", "project_lower_format": "Number", "project_upper_format": "A", "receipt_lower_format": "Alphabet", "receipt_upper_format": "A", "invoice_middle_format": "Date", "receipt_middle_format": "Date"}	[]	7	2020-11-21 05:32:14.243929+00	\N	[]	[]	2020-11-21 05:40:12.571461+00	0
166	test	2021-01-07 11:34:21.999615+00	\N	\N	f	Early Stage	\N	2021-01-07	2021-01-14	Central and Western	test	15	24	[{"value": 50}, {"value": 25}, {"value": 25}]	{"quot_lower_format": "Alphabet", "quot_upper_format": "A", "quot_middle_format": "Date", "invoice_lower_format": "Alphabet", "invoice_upper_format": "A", "project_lower_format": "Number", "project_upper_format": "QQQ", "receipt_lower_format": "Alphabet", "receipt_upper_format": "A", "invoice_middle_format": "Date", "receipt_middle_format": "Date"}	[{"index": 1, "content": "invoice"}]	60	2021-02-26 04:17:11.575899+00	\N	[{"index": 1, "content": "quote1"}]	[{"index": 1, "content": "receipt1"}]	2021-03-04 06:30:36.613263+00	1
149	testing	2020-12-06 17:45:03.72618+00	\N	\N	f	In Progress	\N	2020-12-07	2046-02-22	Central and Western	大西灣	35	43	[{"value": 98}, {"value": 1}, {"value": 1}]	{"quot_lower_format": "Alphabet", "quot_upper_format": "A", "quot_middle_format": "Date", "invoice_lower_format": "Alphabet", "invoice_upper_format": "A", "project_lower_format": "Number", "project_upper_format": "A", "receipt_lower_format": "Alphabet", "receipt_upper_format": "A", "invoice_middle_format": "Date", "receipt_middle_format": "Date"}	[]	1	2020-12-06 17:52:06.77792+00	\N	[{"index": 1, "content": "comment 1"}]	[]	2020-12-06 17:45:03.726217+00	0
110	test777	2020-11-20 10:05:36.299842+00	\N	\N	f	Early Stage	\N	2020-11-20	2020-11-27	Central and Western	null	15	24	[{"value": 50}, {"value": 25}, {"value": 25}]	{"quot_lower_format": "Alphabet", "quot_upper_format": "A", "quot_middle_format": "Date", "invoice_lower_format": "Alphabet", "invoice_upper_format": "A", "project_lower_format": "Number", "project_upper_format": "Q", "receipt_lower_format": "Alphabet", "receipt_upper_format": "A", "invoice_middle_format": "Date", "receipt_middle_format": "Date"}	[{"index": 1, "content": "invoice"}, {"index": 2, "content": "invoice 2"}, {"index": 3, "content": "invoice 3"}]	20	\N	\N	[{"index": 1, "content": "quote1"}, {"index": 2, "content": "quote2"}]	[{"index": 1, "content": "receipt1"}]	2020-11-20 18:07:52.023683+00	0
152	testing 3	2020-12-06 17:59:39.928201+00	\N	\N	f	Early Stage	\N	2020-12-07	2020-12-14	Central and Western	hshsjjsa	35	43	[{"value": 98}, {"value": 1}, {"value": 1}]	{"quot_lower_format": "Alphabet", "quot_upper_format": "A", "quot_middle_format": "Date", "invoice_lower_format": "Alphabet", "invoice_upper_format": "A", "project_lower_format": "Number", "project_upper_format": "A", "receipt_lower_format": "Alphabet", "receipt_upper_format": "A", "invoice_middle_format": "Date", "receipt_middle_format": "Date"}	[]	3	2020-12-06 18:00:45.050616+00	\N	[{"index": 1, "content": "comment 1"}]	[]	2021-01-19 04:43:33.571785+00	0
178	test	2021-02-16 04:54:12.879838+00	\N	\N	f	Early Stage		2021-02-16	2021-02-23	Central and Western	null	15	24	[{"value": 50}, {"value": 50}]	{"quot_lower_format": "Alphabet", "quot_upper_format": "A", "quot_middle_format": "Date", "invoice_lower_format": "Alphabet", "invoice_upper_format": "A", "project_lower_format": "Number", "project_upper_format": "asda", "receipt_lower_format": "Alphabet", "receipt_upper_format": "A", "invoice_middle_format": "Date", "receipt_middle_format": "Date"}	[{"index": 1, "content": "invoice"}]	62	2021-03-04 08:16:30.006766+00	\N	[{"index": 1, "content": "tetsy"}]	[{"index": 1, "content": "receipt 1"}]	2021-03-04 08:09:14.521328+00	10
148	J2601_ 港景峰	2020-11-26 17:29:32.216595+00	\N	\N	f	In Progress	\N	2020-11-01	2021-02-11	Yau Tsim Mong	港景峰3座28樓c室	20	23	[{"value": 5, "description": "簽定合約"}, {"value": 10, "description": "工程展開"}, {"value": 20, "description": "完成水電項目"}, {"value": 20, "description": "完成泥水項目"}, {"value": 20, "description": "訂購傢俬前"}, {"value": 20, "description": "完成工程"}, {"value": 5, "description": "完成工程三十日後"}]	{"quot_lower_format": "Alphabet", "quot_upper_format": "A", "quot_middle_format": "Date", "invoice_lower_format": "Alphabet", "invoice_upper_format": "A", "project_lower_format": "Number", "project_upper_format": "A", "receipt_lower_format": "Alphabet", "receipt_upper_format": "A", "invoice_middle_format": "Date", "receipt_middle_format": "Date"}	[{"index": 1, "content": "請於三十日內"}]	1	2021-01-04 17:08:59.867139+00	\N	[{"index": 1, "content": "此報價單有效日期為30天"}]	[]	2021-01-29 13:45:14.16113+00	0
169	dndndn	2021-01-20 08:00:54.082605+00	\N	\N	f	In Progress	\N	2021-01-23	2021-01-27	Central and Western	skdkoe	11	28	[{"value": 25}, {"value": 25}, {"value": 50}]	{"quot_lower_format": "Alphabet", "quot_upper_format": "A", "quot_middle_format": "Date", "invoice_lower_format": "Alphabet", "invoice_upper_format": "A", "project_lower_format": "Number", "project_upper_format": "A", "receipt_lower_format": "Alphabet", "receipt_upper_format": "A", "invoice_middle_format": "Date", "receipt_middle_format": "Date"}	[]	11	2021-01-20 08:53:12.694114+00	\N	[{"index": 1, "content": "jdiekn1263"}]	[]	2021-02-24 03:42:08.048775+00	3
96	abdhd	2020-11-20 06:06:15.950431+00	\N	\N	f	In Progress	\N	2020-11-20	2020-11-27	Central and Western	svdmdbd	11	28	[{"value": 50}, {"value": 25}, {"value": 25}]	{"quot_lower_format": "Alphabet", "quot_upper_format": "A", "quot_middle_format": "Date", "invoice_lower_format": "Alphabet", "invoice_upper_format": "A", "project_lower_format": "Number", "project_upper_format": "A", "receipt_lower_format": "Alphabet", "receipt_upper_format": "A", "invoice_middle_format": "Date", "receipt_middle_format": "Date"}	[]	3	2020-11-20 13:18:33.120338+00	\N	[]	[]	2020-11-21 09:41:51.242466+00	0
177	t	2021-02-15 17:50:32.341188+00	\N	\N	f	Early Stage	\N	2021-02-16	2021-02-23	Central and Western	null	35	43	[{"value": 5}, {"value": 80}, {"value": 15}]	{"quot_lower_format": "Number", "quot_upper_format": "H", "quot_middle_format": "Alphabet", "invoice_lower_format": "Alphabet", "invoice_upper_format": "A", "project_lower_format": "Number", "project_upper_format": "A", "receipt_lower_format": "Alphabet", "receipt_upper_format": "A", "invoice_middle_format": "Date", "receipt_middle_format": "Date"}	[{"index": 1, "content": "hhh"}]	7	2021-02-16 03:13:55.799973+00	\N	[{"index": 1, "content": "comment 1"}]	[{"index": 1, "content": "uuu"}]	2021-03-04 10:48:03.747944+00	1
180	Testing 2	2021-02-23 04:30:55.930998+00	\N	\N	f	Early Stage	\N	2021-02-23	2021-03-02	Central and Western	Address	20	23	[{"value": 20}, {"value": 20}, {"value": 20}, {"value": 20}, {"value": 20}]	{"quot_lower_format": "Alphabet", "quot_upper_format": "Q", "quot_middle_format": "Date", "invoice_lower_format": "Alphabet", "invoice_upper_format": "I", "project_lower_format": "Number", "project_upper_format": "J", "receipt_lower_format": "Alphabet", "receipt_upper_format": "R", "invoice_middle_format": "Date", "receipt_middle_format": "Date"}	[{"index": 1, "content": "請於三十日內"}]	16	2021-02-23 04:31:41.674906+00	\N	[{"index": 1, "content": "此報價單有效日期為30天"}]	[]	2021-02-23 04:34:56.279067+00	1
165	明輝閣	2021-01-05 16:10:07.380918+00	\N	\N	f	In Progress	\N	2021-01-06	2021-02-28	Central and Western	null	20	23	[{"value": 10}, {"value": 10}, {"value": 20}, {"value": 20}, {"value": 20}, {"value": 10}, {"value": 10}]	{"quot_lower_format": "Alphabet", "quot_upper_format": "Q", "quot_middle_format": "Date", "invoice_lower_format": "Alphabet", "invoice_upper_format": "I", "project_lower_format": "Number", "project_upper_format": "A", "receipt_lower_format": "Alphabet", "receipt_upper_format": "R", "invoice_middle_format": "Date", "receipt_middle_format": "Date"}	[{"index": 1, "content": "請於三十日內"}]	5	2021-02-23 02:01:07.391382+00	\N	[{"index": 1, "content": "此報價單有效日期為30天"}]	[]	2021-02-23 03:07:57.8838+00	5
167	123	2021-01-18 14:35:58.076298+00	\N	\N	f	Early Stage	\N	2021-01-18	2021-01-25	Central and Western	null	15	24	[{"value": 50}, {"value": 25}, {"value": 25}]	{"quot_lower_format": "Alphabet", "quot_upper_format": "A", "quot_middle_format": "Date", "invoice_lower_format": "Alphabet", "invoice_upper_format": "A", "project_lower_format": "Number", "project_upper_format": "QQQ", "receipt_lower_format": "Alphabet", "receipt_upper_format": "A", "invoice_middle_format": "Date", "receipt_middle_format": "Date"}	[{"index": 1, "content": "invoice"}]	1060	2021-02-16 11:02:14.657111+00	\N	[{"index": 1, "content": "quote1"}]	[{"index": 1, "content": "receipt1"}]	2021-02-26 09:29:15.455463+00	4
170	J2722 黃埔花園	2021-01-23 12:27:32.126099+00	\N	\N	f	In Progress	\N	2021-03-01	2021-03-01	Yau Tsim Mong	黃埔花園H室	20	23	[{"value": 10, "description": "簽署合約"}, {"value": 20, "description": "工程開工"}, {"value": 30, "description": "泥水項目完成"}, {"value": 30, "description": "傢俬項目完成"}, {"value": 10, "description": "完成執漏後"}]	{"quot_lower_format": "Alphabet", "quot_upper_format": "Q", "quot_middle_format": "Date", "invoice_lower_format": "Alphabet", "invoice_upper_format": "I", "project_lower_format": "Number", "project_upper_format": "A", "receipt_lower_format": "Alphabet", "receipt_upper_format": "R", "invoice_middle_format": "Date", "receipt_middle_format": "Date"}	[{"index": 1, "content": "請於三十日內"}]	6	2021-02-03 06:00:24.354919+00	\N	[{"index": 1, "content": "此報價單有效日期為30天"}, {"index": 2, "content": "工程進行期間客人不可以存放任何私人物品家電電器於工程地盤內如有任何損壞或損失本公司不會負責"}, {"index": 3, "content": "以上工程價格已包括現場傢俬收口"}, {"index": 4, "content": "木器傢俬用實木夾板 外皮 木紋飾面內籠用布紋膠板"}, {"index": 5, "content": "所有傳高傢俬木器 到天花地"}, {"index": 6, "content": "完工後有一年的維修保養 不包括 人為損壞樓宇結構問題"}, {"index": 7, "content": "所有木器家具包出師公圖及3d效果圖"}, {"index": 8, "content": "3d效果圖的家具 燈飾不能作交貨標準只供參考之用"}, {"index": 9, "content": "所有木器傢俬不包燈飾配件 所有燈飾則需額外報價"}, {"index": 10, "content": "所有代買物料及工具如有任何問題本公司不會負責"}, {"index": 11, "content": "在工程進行中與客人沒有 如客人沒有要求指定物料細節則日本公司設計師代為作最終決定"}, {"index": 12, "content": "天然夾板木材 關係所有一米以上櫃門都有可能會有輕微彎曲的情況"}, {"index": 13, "content": "在裝修前後由樓宇外牆結構引致的任何流水問題本公司 本公司一概不負責任"}, {"index": 14, "content": "左右電燈原有製為改動不包保養"}, {"index": 15, "content": "所有更換鋁窗項目不包修補外牆紙皮石或磁磚"}]	[]	2021-02-18 18:41:21.214927+00	6
171	麗晶花園	2021-01-30 16:14:46.286056+00	\N	\N	f	In Progress	\N	2021-01-31	2021-02-07	Kwun Tong	null	20	23	[{"value": 10, "description": "簽署合約"}, {"value": 20, "description": "工程開工"}, {"value": 30, "description": "泥水項目完成"}, {"value": 30, "description": "傢俬項目完成"}, {"value": 10, "description": "完成執漏後"}]	{"quot_lower_format": "Alphabet", "quot_upper_format": "Q", "quot_middle_format": "Date", "invoice_lower_format": "Alphabet", "invoice_upper_format": "I", "project_lower_format": "Number", "project_upper_format": "A", "receipt_lower_format": "Alphabet", "receipt_upper_format": "R", "invoice_middle_format": "Date", "receipt_middle_format": "Date"}	[{"index": 1, "content": "請於三十日內"}]	7	2021-01-30 18:16:48.340689+00	\N	[{"index": 1, "content": "此報價單有效日期為30天"}, {"index": 2, "content": "工程進行期間客人不可以存放任何私人物品家電電器於工程地盤內如有任何損壞或損失本公司不會負責"}, {"index": 3, "content": "以上工程價格已包括現場傢俬收口"}, {"index": 4, "content": "木器傢俬用實木夾板 外皮 木紋飾面內籠用布紋膠板"}, {"index": 5, "content": "所有傳高傢俬木器 到天花地"}, {"index": 6, "content": "完工後有一年的維修保養 不包括 人為損壞樓宇結構問題"}, {"index": 7, "content": "所有木器家具包出師公圖及3d效果圖"}, {"index": 8, "content": "3d效果圖的家具 燈飾不能作交貨標準只供參考之用"}, {"index": 9, "content": "所有木器傢俬不包燈飾配件 所有燈飾則需額外報價"}, {"index": 10, "content": "所有代買物料及工具如有任何問題本公司不會負責"}, {"index": 11, "content": "在工程進行中與客人沒有 如客人沒有要求指定物料細節則日本公司設計師代為作最終決定"}, {"index": 12, "content": "天然夾板木材 關係所有一米以上櫃門都有可能會有輕微彎曲的情況"}, {"index": 13, "content": "在裝修前後由樓宇外牆結構引致的任何流水問題本公司 本公司一概不負責任"}, {"index": 14, "content": "左右電燈原有製為改動不包保養"}, {"index": 15, "content": "所有更換鋁窗項目不包修補外牆紙皮石或磁磚"}]	[]	2021-02-22 06:23:50.975947+00	1
161	滿輝大廈	2020-12-11 17:51:29.506952+00	\N	\N	f	In Progress	\N	2020-11-16	2021-02-26	Wan Chai	灣仔肇輝臺滿輝大廈b座4樓b室	20	23	[{"value": 5, "description": "簽定合約"}, {"value": 10, "description": "工程展開"}, {"value": 20, "description": "完成水電項目"}, {"value": 20, "description": "完成泥水項目"}, {"value": 20, "description": "訂購傢俬前"}, {"value": 20, "description": "完成工程"}, {"value": 5, "description": "完成工程三十日後"}]	{"quot_lower_format": "Alphabet", "quot_upper_format": "A", "quot_middle_format": "Date", "invoice_lower_format": "Alphabet", "invoice_upper_format": "A", "project_lower_format": "Number", "project_upper_format": "A", "receipt_lower_format": "Alphabet", "receipt_upper_format": "A", "invoice_middle_format": "Date", "receipt_middle_format": "Date"}	[{"index": 1, "content": "請於三十日內"}]	2	2021-02-19 09:57:53.529055+00	\N	[{"index": 1, "content": "此報價單有效日期為30天"}, {"index": 2, "content": "工程進行期間，客人不可存放任何私人物品， 家具，電器等於工程地盤內。如有任何損壞或遺失本公司一概不負責。"}, {"index": 3, "content": "以上工程價目已包括現場傢俬收口。"}, {"index": 4, "content": "所有傢俬用 18mm木夾板， 外用 富米加畫或西德防火膠板。"}, {"index": 5, "content": "所有掩門用緩衝油壓門較，櫃桶用三截緩衝路軌。"}, {"index": 6, "content": "所有全高傢俬包括8.5呎高如額外增加一呎需另收$300/呎"}, {"index": 7, "content": "所有木器傢俬包括3d效果圖及私工圖"}, {"index": 8, "content": "完工後有一年維修保養責任不包括人為損壞或樓宇結構問題"}]	[]	2021-01-23 12:22:31.869048+00	1
173	華都中心	2021-02-03 03:41:17.824626+00	\N	\N	f	Finished	\N	2019-06-17	2019-07-31	Tsuen Wan	荃灣荃灣華都中心02室	20	23	[{"value": 10, "description": "簽署合約"}, {"value": 20, "description": "工程開工"}, {"value": 30, "description": "泥水項目完成"}, {"value": 30, "description": "傢俬項目完成"}, {"value": 10, "description": "完成執漏後"}]	{"quot_lower_format": "Alphabet", "quot_upper_format": "Q", "quot_middle_format": "Date", "invoice_lower_format": "Alphabet", "invoice_upper_format": "I", "project_lower_format": "Number", "project_upper_format": "A", "receipt_lower_format": "Alphabet", "receipt_upper_format": "R", "invoice_middle_format": "Date", "receipt_middle_format": "Date"}	[{"index": 1, "content": "請於三十日內"}]	9	2021-02-03 08:48:41.085815+00	\N	[{"index": 1, "content": "此報價單有效日期為30天"}, {"index": 2, "content": "工程進行期間客人不可以存放任何私人物品家電電器於工程地盤內如有任何損壞或損失本公司不會負責"}, {"index": 3, "content": "以上工程價格已包括現場傢俬收口"}, {"index": 4, "content": "木器傢俬用實木夾板 外皮 木紋飾面內籠用布紋膠板"}, {"index": 5, "content": "所有傳高傢俬木器 到天花地"}, {"index": 6, "content": "完工後有一年的維修保養 不包括 人為損壞樓宇結構問題"}, {"index": 7, "content": "所有木器家具包出師公圖及3d效果圖"}, {"index": 8, "content": "3d效果圖的家具 燈飾不能作交貨標準只供參考之用"}, {"index": 9, "content": "所有木器傢俬不包燈飾配件 所有燈飾則需額外報價"}, {"index": 10, "content": "所有代買物料及工具如有任何問題本公司不會負責"}, {"index": 11, "content": "在工程進行中與客人沒有 如客人沒有要求指定物料細節則日本公司設計師代為作最終決定"}, {"index": 12, "content": "天然夾板木材 關係所有一米以上櫃門都有可能會有輕微彎曲的情況"}, {"index": 13, "content": "在裝修前後由樓宇外牆結構引致的任何流水問題本公司 本公司一概不負責任"}, {"index": 14, "content": "左右電燈原有製為改動不包保養"}, {"index": 15, "content": "所有更換鋁窗項目不包修補外牆紙皮石或磁磚"}]	[]	2021-02-19 03:50:58.506189+00	3
174	太子道西	2021-02-03 07:26:09.138361+00	\N	\N	f	Early Stage	\N	2021-02-03	2021-03-31	Yau Tsim Mong	太子道太子道西 250 號 2 樓	20	23	[{"value": 10}, {"value": 30}, {"value": 30}, {"value": 20}, {"value": 10}]	{"quot_lower_format": "Alphabet", "quot_upper_format": "Q", "quot_middle_format": "Date", "invoice_lower_format": "Alphabet", "invoice_upper_format": "I", "project_lower_format": "Number", "project_upper_format": "A", "receipt_lower_format": "Alphabet", "receipt_upper_format": "R", "invoice_middle_format": "Date", "receipt_middle_format": "Date"}	[{"index": 1, "content": "請於三十日內"}]	10	2021-02-04 03:35:17.48504+00	\N	[{"index": 1, "content": "此報價單有效日期為30天"}, {"index": 2, "content": "工程進行期間客人不可以存放任何私人物品家電電器於工程地盤內如有任何損壞或損失本公司不會負責"}, {"index": 3, "content": "以上工程價格已包括現場傢俬收口"}, {"index": 4, "content": "木器傢俬用實木夾板 外皮 木紋飾面內籠用布紋膠板"}, {"index": 5, "content": "所有傳高傢俬木器 到天花地"}, {"index": 6, "content": "完工後有一年的維修保養 不包括 人為損壞樓宇結構問題"}, {"index": 7, "content": "所有木器家具包出師公圖及3d效果圖"}, {"index": 8, "content": "3d效果圖的家具 燈飾不能作交貨標準只供參考之用"}, {"index": 9, "content": "所有木器傢俬不包燈飾配件 所有燈飾則需額外報價"}, {"index": 10, "content": "所有代買物料及工具如有任何問題本公司不會負責"}, {"index": 11, "content": "在工程進行中與客人沒有 如客人沒有要求指定物料細節則日本公司設計師代為作最終決定"}, {"index": 12, "content": "天然夾板木材 關係所有一米以上櫃門都有可能會有輕微彎曲的情況"}, {"index": 13, "content": "在裝修前後由樓宇外牆結構引致的任何流水問題本公司 本公司一概不負責任"}, {"index": 14, "content": "左右電燈原有製為改動不包保養"}, {"index": 15, "content": "所有更換鋁窗項目不包修補外牆紙皮石或磁磚"}]	[]	2021-02-22 06:26:48.066643+00	1
175	駿發花園	2021-02-04 04:03:23.868512+00	\N	\N	f	In Progress	\N	2021-02-04	2021-03-31	Yau Tsim Mong	油麻地	20	23	[{"value": 10}, {"value": 20}, {"value": 30}, {"value": 20}, {"value": 20}]	{"quot_lower_format": "Alphabet", "quot_upper_format": "Q", "quot_middle_format": "Number", "invoice_lower_format": "Alphabet", "invoice_upper_format": "I", "project_lower_format": "Number", "project_upper_format": "J", "receipt_lower_format": "Alphabet", "receipt_upper_format": "R", "invoice_middle_format": "Date", "receipt_middle_format": "Date"}	[{"index": 1, "content": "請於三十日內"}]	14	2021-02-23 02:03:34.285107+00	\N	[{"index": 1, "content": "此報價單有效日期為30天"}, {"index": 2, "content": "工程進行期間客人不可以存放任何私人物品家電電器於工程地盤內如有任何損壞或損失本公司不會負責"}, {"index": 3, "content": "以上工程價格已包括現場傢俬收口"}, {"index": 4, "content": "木器傢俬用實木夾板 外皮 木紋飾面內籠用布紋膠板"}, {"index": 5, "content": "所有傳高傢俬木器 到天花地"}, {"index": 6, "content": "完工後有一年的維修保養 不包括 人為損壞樓宇結構問題"}, {"index": 7, "content": "所有木器家具包出師公圖及3d效果圖"}, {"index": 8, "content": "3d效果圖的家具 燈飾不能作交貨標準只供參考之用"}, {"index": 9, "content": "所有木器傢俬不包燈飾配件 所有燈飾則需額外報價"}, {"index": 10, "content": "所有代買物料及工具如有任何問題本公司不會負責"}, {"index": 11, "content": "在工程進行中與客人沒有 如客人沒有要求指定物料細節則日本公司設計師代為作最終決定"}, {"index": 12, "content": "天然夾板木材 關係所有一米以上櫃門都有可能會有輕微彎曲的情況"}, {"index": 13, "content": "在裝修前後由樓宇外牆結構引致的任何流水問題本公司 本公司一概不負責任"}, {"index": 14, "content": "左右電燈原有製為改動不包保養"}, {"index": 15, "content": "所有更換鋁窗項目不包修補外牆紙皮石或磁磚"}]	[]	2021-02-23 07:58:28.337957+00	2
97	職熱權口業	2020-11-20 06:10:26.437341+00	\N	\N	f	In Progress	\N	2020-11-20	2020-11-27	Central and Western	null	15	24	[{"value": 50}, {"value": 25}, {"value": 25}]	{"quot_lower_format": "Alphabet", "quot_upper_format": "A", "quot_middle_format": "Date", "invoice_lower_format": "Alphabet", "invoice_upper_format": "A", "project_lower_format": "Number", "project_upper_format": "Q", "receipt_lower_format": "Alphabet", "receipt_upper_format": "A", "invoice_middle_format": "Date", "receipt_middle_format": "Date"}	[{"index": 1, "content": "invoice"}, {"index": 2, "content": "invoice 2"}, {"index": 3, "content": "invoice 3"}]	7	2021-02-16 07:45:46.347556+00	\N	[{"index": 1, "content": "quote1"}, {"index": 2, "content": "quote2"}]	[{"index": 1, "content": "receipt1"}]	2021-02-24 08:46:36.267327+00	2
78	a111111111	2020-10-23 10:32:24.788816+00	\N	\N	f	In Progress	\N	2020-10-22	2020-10-29	Central and Western	destination	15	24	[{"value": 50}, {"value": 25}, {"value": 25}]	{"quot_lower_format": "Alphabet", "quot_upper_format": "A", "quot_middle_format": "Date", "invoice_lower_format": "Alphabet", "invoice_upper_format": "A", "project_lower_format": "Number", "project_upper_format": "A", "receipt_lower_format": "Alphabet", "receipt_upper_format": "A", "invoice_middle_format": "Date", "receipt_middle_format": "Date"}	[{"index": 1, "content": "invoice testing 1"}, {"index": 2, "content": "2"}]	3	2021-02-16 08:12:14.482312+00	\N	[{"index": 1, "content": "quote 1"}]	[{"index": 1, "content": "testing receipt 2"}]	2021-03-05 03:04:06.304386+00	2
123	abc	2020-11-20 17:05:41.628058+00	\N	\N	f	Early Stage	\N	2020-11-20	2020-11-27	Tuen Mun	null	15	24	[{"value": 50}, {"value": 25}, {"value": 25}]	{"quot_lower_format": "Alphabet", "quot_upper_format": "A", "quot_middle_format": "Date", "invoice_lower_format": "Alphabet", "invoice_upper_format": "A", "project_lower_format": "Number", "project_upper_format": "Q", "receipt_lower_format": "Alphabet", "receipt_upper_format": "A", "invoice_middle_format": "Date", "receipt_middle_format": "Date"}	[{"index": 1, "content": "invoice"}, {"index": 2, "content": "invoice 2"}, {"index": 3, "content": "invoice 3"}]	29	2020-11-20 17:05:47.80746+00	\N	[{"index": 1, "content": "quote1"}, {"index": 2, "content": "quote2"}]	[{"index": 1, "content": "receipt1"}]	2021-03-03 08:32:20.194577+00	0
\.


--
-- Data for Name: projects_projecthistory; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.projects_projecthistory (id, project_title, project_number, name, email, quantity, rate, phone, created_on, amount_due, amount_paid, is_email_sent, status, details, due_date, from_address_id, project_id, to_address_id, updated_by_id) FROM stdin;
\.


--
-- Data for Name: projects_projecthistory_assigned_to; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.projects_projecthistory_assigned_to (id, projecthistory_id, user_id) FROM stdin;
\.


--
-- Data for Name: projects_projectimage; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.projects_projectimage (id, img, img_width, img_height, related_project_id, display_id) FROM stdin;
53	companies/15/images/632a818b-2e1.png	1	1	166	1
54	companies/15/images/5a85e485-1ce.png	1	1	166	2
55	companies/15/images/e62586fc-0fb.png	1	1	166	3
56	companies/15/images/334effbe-f66.png	1	1	166	4
57	companies/15/images/918e344b-cf9.png	1	1	166	5
68	companies/15/images/c3b711bb-56e.png	1	1	166	6
69	companies/15/images/bac099a3-c15.png	1	1	166	7
305	companies/11/images/24c7416d-ae7.png	1	1	147	23
306	companies/11/images/333efea0-5bd.jpg	1	1	147	24
72	companies/15/images/af11b0c3-5a8.jpg	1	1	78	3
73	companies/15/images/a3cbd938-295.jpg	1	1	78	4
307	companies/11/images/7cfb936c-345.png	1	1	147	25
242	companies/11/images/af686743-e49.png	1	1	147	7
76	companies/15/images/60fa905e-81d.jpg	1	1	78	5
308	companies/11/images/2a8f1200-31b.png	1	1	147	26
424	companies/11/images/06945077-88b.png	1	1	147	27
425	companies/11/images/69192315-081.png	1	1	147	28
427	companies/20/images/e0a8826f-4be.jpg	1	1	165	1
428	companies/20/images/9902aabd-07b.jpg	1	1	173	1
429	companies/20/images/261dc5e0-1c8.jpg	1	1	173	2
430	companies/20/images/d1e4d687-212.jpg	1	1	173	3
431	companies/20/images/96a2bab9-dff.jpg	1	1	173	4
432	companies/20/images/ec7281b0-01b.jpg	1	1	173	5
149	companies/15/images/591f64db-d2b.png	1	1	166	8
434	companies/20/images/7f2e69de-a85.jpg	1	1	173	6
435	companies/20/images/3a13811c-e69.jpg	1	1	173	7
436	companies/20/images/164cd8e1-85d.jpg	1	1	173	8
153	companies/35/images/73bb3e45-92a.jpg	1	1	168	1
154	companies/35/images/5f2154a0-6fe.jpg	1	1	168	2
155	companies/35/images/ee610858-dfe.jpg	1	1	168	3
156	companies/35/images/acd493a4-211.jpg	1	1	168	4
157	companies/35/images/6a857cf8-985.jpg	1	1	168	5
437	companies/20/images/f849fa23-224.jpg	1	1	173	9
438	companies/20/images/584566d0-28d.jpg	1	1	173	10
439	companies/20/images/1ca59ce7-d1e.jpg	1	1	173	11
440	companies/20/images/61c2f670-c9a.jpg	1	1	173	12
441	companies/20/images/0372ab0f-b8d.jpg	1	1	173	13
275	companies/11/images/7a91cf10-674.png	1	1	147	13
276	companies/11/images/ac806033-e10.png	1	1	147	14
277	companies/11/images/a9afbb55-027.jpg	1	1	147	15
278	companies/11/images/42f96179-917.jpg	1	1	147	16
279	companies/11/images/06e57a71-c10.png	1	1	147	17
448	companies/20/images/2140990e-ec8.jpg	1	1	175	1
449	companies/11/images/15896df7-22b.png	1	1	176	1
450	companies/11/images/07dfe1e5-6d5.jpg	1	1	176	2
451	companies/11/images/3ffde962-f6e.jpg	1	1	176	3
453	companies/20/images/c0893790-bec.jpg	1	1	165	2
454	companies/20/images/4542faa6-7e3.jpg	1	1	165	3
\.


--
-- Data for Name: projects_projectimageset; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.projects_projectimageset (id, related_project_id, upload_date, display_id, project_milestone_id) FROM stdin;
60	\N	2021-01-19	1	106
16	166	2021-01-13	1	\N
18	\N	2021-01-13	1	102
19	\N	2021-01-14	1	103
20	\N	2021-01-14	1	104
21	\N	2021-01-15	1	105
146	147	2021-01-21	1	\N
147	147	2021-01-21	2	\N
149	165	2021-01-25	1	\N
150	\N	2021-02-03	1	109
152	173	2021-02-03	1	\N
153	173	2021-02-03	2	\N
154	173	2021-02-03	3	\N
99	\N	2021-01-20	1	107
155	\N	2021-02-03	1	110
158	\N	2021-02-04	1	113
159	176	2021-02-15	1	\N
160	\N	2021-02-15	1	114
162	\N	2021-02-16	1	116
109	\N	2021-01-21	1	108
164	\N	2021-02-18	1	117
165	\N	2021-02-18	1	118
166	\N	2021-02-23	1	119
167	\N	2021-02-23	1	120
169	\N	2021-02-23	1	122
172	\N	2021-03-05	1	125
\.


--
-- Data for Name: projects_projectimageset_imgs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.projects_projectimageset_imgs (id, projectimageset_id, projectimage_id) FROM stdin;
174	60	153
175	60	154
176	60	155
177	60	156
178	60	157
296	109	275
297	109	276
298	109	277
299	109	278
300	109	279
76	16	53
77	16	54
78	16	55
79	16	56
80	16	57
445	146	424
89	18	68
90	18	69
446	147	425
93	20	72
94	20	73
448	149	427
449	150	428
97	19	76
450	150	429
263	99	242
451	150	430
452	150	431
453	150	432
455	152	434
456	153	435
326	99	305
327	99	306
328	99	307
329	99	308
457	154	436
458	155	437
459	155	438
460	155	439
461	155	440
462	155	441
170	18	149
469	158	448
470	159	449
471	160	450
472	160	451
474	164	453
475	165	454
\.


--
-- Data for Name: projects_projectinvoice; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.projects_projectinvoice (id, generated_on, invoice_id, project_id) FROM stdin;
7	2020-10-30 11:07:53.535073+00	0	78
8	2020-11-20 13:29:39.969509+00	0	117
9	2020-11-20 13:35:55.24122+00	0	96
10	2020-11-26 17:42:39.451672+00	0	148
11	2020-11-26 17:43:39.087857+00	4	148
12	2020-12-06 17:53:34.338996+00	0	149
13	2020-12-06 17:53:38.966083+00	2	149
14	2020-12-06 18:15:34.044137+00	0	152
15	2020-12-09 18:00:14.361699+00	1	148
16	2020-12-09 18:00:29.756449+00	6	148
17	2021-01-16 11:04:48.997972+00	0	166
18	2021-02-03 04:53:55.734481+00	0	173
19	2021-02-15 12:03:55.574908+00	0	176
20	2021-02-16 08:04:34.894291+00	2	97
21	2021-02-16 08:04:48.492761+00	0	97
22	2021-02-16 08:11:55.813156+00	1	78
23	2021-02-16 08:26:21.27762+00	1	97
24	2021-02-16 08:51:55.704916+00	0	178
25	2021-02-16 08:52:31.779974+00	1	178
26	2021-02-16 11:02:30.837674+00	0	167
27	2021-02-16 11:02:39.563418+00	1	167
28	2021-02-18 09:30:39.791037+00	2	175
29	2021-02-22 09:45:01.048103+00	0	175
30	2021-02-23 01:54:45.355258+00	0	165
31	2021-02-23 08:03:37.159669+00	0	169
36	2021-02-26 04:10:27.818277+00	1	166
\.


--
-- Data for Name: projects_projectreceipt; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.projects_projectreceipt (id, generated_on, receipt_id, project_id) FROM stdin;
3	2020-10-30 11:08:56.586799+00	0	78
4	2020-11-20 13:29:53.325701+00	0	117
5	2020-11-20 13:36:36.643582+00	0	96
6	2020-12-09 17:52:02.189586+00	0	148
7	2021-01-05 15:50:22.970842+00	6	148
8	2021-01-18 15:39:28.93711+00	0	166
9	2021-02-03 04:54:07.847335+00	0	173
10	2021-02-15 12:04:11.428107+00	0	176
11	2021-02-16 08:11:17.88233+00	2	97
12	2021-02-16 08:47:25.587875+00	0	97
13	2021-02-16 08:47:38.061391+00	1	97
14	2021-02-16 08:52:07.577828+00	0	178
15	2021-02-16 08:52:39.992682+00	1	178
16	2021-02-22 09:45:11.663647+00	0	175
17	2021-02-23 01:55:00.524881+00	0	165
18	2021-02-23 08:03:43.67623+00	0	169
19	2021-02-26 04:14:57.137141+00	1	166
\.


--
-- Data for Name: quotations_quotation; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.quotations_quotation (id, quotation_title, quotation_number, name, email, quantity, rate, phone, created_on, amount_due, amount_paid, is_email_sent, status, details, due_date, created_by_id, from_address_id, to_address_id, approved_by_id, approved_on, last_updated_by_id, last_updated_on) FROM stdin;
\.


--
-- Data for Name: quotations_quotation_assigned_to; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.quotations_quotation_assigned_to (id, quotation_id, user_id) FROM stdin;
\.


--
-- Data for Name: quotations_quotation_companies; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.quotations_quotation_companies (id, quotation_id, company_id) FROM stdin;
\.


--
-- Data for Name: quotations_quotation_teams; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.quotations_quotation_teams (id, quotation_id, teams_id) FROM stdin;
\.


--
-- Data for Name: quotations_quotationhistory; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.quotations_quotationhistory (id, quotation_title, quotation_number, name, email, quantity, rate, phone, created_on, amount_due, amount_paid, is_email_sent, status, details, due_date, from_address_id, quotation_id, to_address_id, updated_by_id) FROM stdin;
\.


--
-- Data for Name: quotations_quotationhistory_assigned_to; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.quotations_quotationhistory_assigned_to (id, quotationhistory_id, user_id) FROM stdin;
\.


--
-- Data for Name: rooms_room; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.rooms_room (id, name, related_project_id, room_type_id, value, measure_quantifier) FROM stdin;
166	自定義房間	167	7	{"R": null, "CP": [{"A": 25.0, "R": ""}], "CW": [{"H": 5.0, "W": 5.0}, {"H": 5.0, "W": 5.0}, {"H": 5.0, "W": 5.0}, {"H": 5.0, "W": 5.0}], "CWS": [], "HWS": false}	mm
77	廚房	78	2	{}	mm
78	飯廳	78	4	{}	mm
93	1人睡房	78	5	{}	mm
95	2人睡房	78	6	{}	mm
96	自定義房間	78	7	{"R": null, "CP": [{"A": 50.0, "R": "三角形地台"}], "CW": [{"H": 50.0, "W": 50.0}, {"H": 50.0, "W": 50.0}, {"H": 50.0, "W": 50.0}], "CWS": [{"C": false, "L": 5.0, "R": "", "W": 2.0, "C2": false, "R2": ""}], "HWS": false}	mm
101	客廳	117	3	{}	mm
103	廚房	147	2	{}	mm
104	自定義房間	147	7	{"R": "ajns", "CP": [{"A": 192.0, "R": "qllkkdk"}, {"A": 880.0, "R": "jsbwns"}], "CW": [{"H": 2883.0, "W": 992.0}, {"H": 39937.0, "W": 9003.0}, {"H": 399.0, "W": 2782.0}], "CWS": [{"C": false, "L": 28992.0, "R": "ajjs", "W": 2783.0, "C2": false, "R2": "sn cj天"}], "HWS": true}	mm
204	自定義房間	173	7	{"R": null, "CP": [{"A": 20.0, "R": ""}], "CW": [{"H": 2.89, "W": 5.0}, {"H": 2.89, "W": 4.0}, {"H": 2.89, "W": 5.0}, {"H": 2.89, "W": 4.0}], "CWS": [{"C": true, "D": 0.6, "H": 1.2, "L": 2.0, "R": ""}], "HWS": true}	m
108	2人睡房	152	6	{}	mm
113	1人睡房	149	5	{}	mm
114	自定義房間	149	7	{"R": null, "CP": [{"A": "", "R": ""}], "CW": [{"H": "", "W": ""}], "CWS": [{"C": false, "L": "", "R": "", "W": "", "C2": false, "R2": ""}], "HWS": false}	mm
115	自定義房間	152	7	{"R": null, "CP": [{"A": "", "R": ""}], "CW": [{"H": "", "W": ""}], "CWS": [{"C": false, "L": "", "R": "", "W": "", "C2": false, "R2": ""}], "HWS": false}	mm
116	2人睡房	161	6	{}	mm
117	1人睡房	161	5	{}	mm
118	浴室	161	1	{}	mm
120	廚房	161	2	{}	mm
127	客廳	165	3	{}	mm
132	testing	166	7	{"R": null, "CP": [{"A": "", "R": ""}], "CW": [{"H": "", "W": ""}], "CWS": [{"C": false, "L": "", "R": "", "W": ""}], "HWS": false}	mm
138	廚房2	168	2	{"H": 45.0, "L": 454.0, "W": 45.0}	mm
139	2人睡房	147	6	{"H": 2902.0, "L": 2893.0, "W": 193.0}	mm
142	2人睡房	169	1	{"H": 789.0, "L": 456.0, "W": 123.0}	mm
143	廚房	169	2	{"H": 2992.0, "L": 283.0, "W": 283.0}	mm
146	浴室A	169	1	{"H": 33.0, "L": 27.0, "W": 18.0}	mm
148	飯廳XD	169	4	{"H": null, "L": null, "W": null}	mm
151	廚房a	147	2	{"H": "0", "L": "0", "W": "0"}	mm
154	偏飯廳	165	4	{"H": "3.0", "L": "3.0", "W": "2.5"}	m
155	主人房	165	6	{"H": "3000.0", "L": "3000.0", "W": "2500.0"}	mm
156	廚房	165	2	{"H": "3000.0", "L": "2500.0", "W": "2000.0"}	mm
157	浴室	165	1	{"H": "3000.0", "L": "2500.0", "W": "2500.0"}	mm
162	2人睡房	167	6	{"H": "5.0", "L": "5.0", "W": "5.0"}	mm
168	浴室	167	1	{"H": "5.0", "L": "5.0", "W": "5.0"}	mm
169	1人睡房	167	5	{"H": "5.0", "L": "5.0", "W": "5.0"}	mm
173	1人睡房	165	5	{"H": "3.0", "L": "4.0", "W": "4.0"}	m
174	主人浴室	170	1	{"H": "8.5", "L": "7.5", "W": "5.0"}	mm
178	工人房	170	5	{"H": "9.0", "L": "9.0", "W": "4.5"}	mm
179	客人浴室	170	1	{"H": "8.5", "L": "9.0", "W": "5.0"}	mm
184	主人房	171	6	{"H": "3.0", "L": "3.5", "W": "3.0"}	m
186	睡房(有窗台)	171	10	{"H": "1.2", "L": "2.5", "W": "2.0", "CWS": "2.0"}	m
188	廚房	171	2	{"H": "3.0", "L": "2.2", "W": "1.8"}	m
189	浴室	171	1	{"H": "3.0", "L": "2.2", "W": "1.8"}	m
196	1人睡房	173	5	{"H": "2.89", "L": "5.21", "W": "3.56"}	m
197	主客廳	173	3	{"H": "2.89", "L": "5.53", "W": "3.0"}	m
198	偏飯廳	173	4	{"H": "2.89", "L": "6.89", "W": "4.28"}	ft
199	主人房	173	6	{"H": "2.89", "L": "5.01", "W": "3.67"}	m
205	書房	173	9	{"H": "2.89", "L": "3.5", "W": "2.5"}	mm
206	1人睡房	173	5	{"H": "2.89", "L": "4.0", "W": "3.0"}	m
208	書房	174	9	{"H": "3.2", "L": "4.0", "W": "3.0"}	mm
209	浴室	174	1	{"H": "3.2", "L": "3.0", "W": "2.0"}	mm
210	客廳	174	3	{"H": "3.2", "L": "4.5", "W": "2.6"}	mm
255	飯廳	175	4	{"H": "3.0", "L": "4.0", "W": "2.0"}	m
215	1人睡房	167	5	{"H": "2.89", "L": "5.21", "W": "3.56"}	mm
217	飯廳	167	4	{"H": "5.0", "L": "5.0", "W": "5.0"}	mm
220	飯廳	97	4	{"H": "5.0", "L": "5.0", "W": "5.0"}	mm
228	書房	97	9	{"H": "5.0", "L": "7.0", "W": "6.0"}	mm
263	浴室	78	1	{"H": "5.0", "L": "5.0", "W": "5.0"}	mm
268	書房2	123	9	{"H": "3.0", "L": "5.0", "W": "4.0"}	m
276	書房	166	9	{"H": "3.0", "L": "5.0", "W": "4.0"}	mm
183	偏飯廳	171	4	{"H": "3.0", "L": "2.5", "W": "2.0"}	m
212	客廳	175	3	{"H": "3.1", "L": "4.2", "W": "2.4"}	mm
258	1人睡房	174	5	{"H": "2.89", "L": "3.22", "W": "4.88", "CWS": "0"}	m
224	書房A	176	9	{"H": "20.0", "L": "2.0", "W": "40.0"}	mm
225	1人睡房@%	176	5	{"H": "10.0", "L": "27.0", "W": "2.0"}	mm
226	書房	177	7	{"R": null, "CP": [{"A": "", "R": ""}], "CW": [{"H": "", "W": ""}], "CWS": [{"C": true, "D": "", "H": "", "L": "", "R": "a"}], "HWS": true}	mm
227	1人睡房	167	5	{"H": "5.0", "L": "9.0", "W": "5.0"}	ft
229	飯廳	167	4	{"H": "5.12", "L": "6.37", "W": "5.33"}	mm
267	自定義房間1	78	7	{"R": null, "CP": [{"A": 10.0, "L": 3.0, "R": "", "W": 2.0}, {"A": 12.0, "L": 4.0, "R": "", "W": 3.0}], "CW": [{"H": 4.0, "R": "", "W": 3.0}, {"H": 6.0, "R": "", "W": 5.0}, {"H": 2.0, "R": "", "W": 1.0}], "CWS": [{"C": false, "D": 3.0, "H": 2.0, "L": 1.0, "R": ""}, {"C": true, "D": 9.0, "H": 8.0, "L": 7.0, "R": ""}], "HWS": true}	ft
232	自定義房間	165	7	{"R": null, "CP": [{"A": 24.0, "R": ""}], "CW": [{"H": 3.0, "R": "", "W": 4.0}], "CWS": [{"C": false, "D": 1.0, "H": 1.0, "L": 6.0, "R": ""}], "HWS": true}	mm
233	五角形房間	165	7	{"R": null, "CP": [{"A": 16.0, "R": ""}], "CW": [{"H": 4.0, "R": "", "W": 4.27}, {"H": 4.0, "R": "", "W": 4.27}, {"H": 4.0, "R": "", "W": 4.03}, {"H": 4.0, "R": "", "W": 4.03}, {"H": 4.0, "R": "", "W": 2.0}], "CWS": [{"C": false, "D": 1.5, "H": 1.0, "L": 4.27, "R": ""}], "HWS": false}	m
234	兩長方房間	165	7	{"R": null, "CP": [{"A": 14.96, "R": ""}], "CW": [{"H": 3.1, "R": "", "W": 4.3}, {"H": 3.1, "R": "", "W": 4.3}, {"H": 3.1, "R": "", "W": 2.6}, {"H": 3.1, "R": "", "W": 2.6}, {"H": 1.2, "R": "", "W": 1.8}, {"H": 1.2, "R": "", "W": 1.8}, {"H": 1.2, "R": "", "W": 2.1}], "CWS": [{"C": false, "D": 1.8, "H": 1.2, "L": 2.1, "R": ""}], "HWS": true}	m
235	廚房	175	2	{"H": "3.24", "L": "4.65", "W": "2.82"}	m
236	書房	171	9	{"H": "3.25", "L": "4.69", "W": "2.48"}	m
237	客廳	171	3	{"H": "3.25", "L": "4.69", "W": "2.48"}	m
238	飯廳	175	4	{"H": "3.25", "L": "4.69", "W": "2.48"}	m
241	1人睡房	170	5	{"H": "8.0", "L": "8.0", "W": "8.0"}	ft
242	自定義房間	170	7	{"R": null, "CP": [{"A": 50.0, "R": ""}, {"A": "", "R": ""}], "CW": [{"H": "", "R": "", "W": ""}], "CWS": [{"C": false, "D": 2.0, "H": 5.0, "L": 7.0, "R": ""}, {"C": false, "D": "", "H": "", "L": "", "R": ""}], "HWS": false}	ft
244	自定義房間	170	7	{"R": null, "CP": [{"A": 50.0, "L": "", "R": "", "W": ""}], "CW": [{"H": "", "R": "", "W": ""}], "CWS": [{"C": false, "D": "", "H": "", "L": "", "R": ""}], "HWS": false}	mm
249	2人睡房	175	6	{"H": "3.0", "L": "6.0", "W": "5.0"}	m
250	2人睡房	173	6	{"H": "3.25", "L": "4.69", "W": "2.48"}	m
251	1人睡房	175	5	{"H": "4.69", "L": "7.0", "W": "2.99"}	mm
254	廚房	171	2	{"H": "3.25", "L": "4.69", "W": "2.48"}	m
259	廚房	179	2	{"H": "3.22", "L": "4.22", "W": "2.22"}	m
260	1人睡房	180	5	{"H": "3.0", "L": "4.0", "W": "2.0", "CWS": "0"}	mm
261	飯廳	180	4	{"H": "3.22", "L": "4.22", "W": "2.22"}	m
230	浴室testing	178	1	{"H": "5.12", "L": "4.33", "W": "5.24"}	m
273	自定義房間	166	7	{"R": "test2", "CP": [{"A": 10.0, "L": 5.0, "R": "test", "W": 2.0}], "CW": [{"H": 4.0, "R": "", "W": 3.0}], "CWS": [], "HWS": false}	ft
284	自定義房間2	178	7	{"R": null, "CP": [], "CW": [{"H": 4.0, "R": "", "W": 3.0}, {"H": 5.0, "R": "", "W": 4.0}], "CWS": [], "HWS": false}	m
282	1人睡房	176	5	{"H": "122.0", "L": "484.0", "W": "363.0", "CWS": "0"}	ft
223	自定義房間aa	176	7	{"R": "This is a room that somehow has 8 floors.", "CP": [{"A": 600.0, "R": "a"}, {"A": 900.0, "R": "b"}, {"A": 500.0, "R": "c"}, {"A": 2000.0, "R": "d"}, {"A": 680.0, "R": "e"}, {"A": 100.0, "R": "f"}, {"A": 333.0, "R": "g"}, {"A": 0.0, "R": "h"}], "CW": [{"H": 300.0, "W": 100.0}, {"H": 100.0, "W": 390.0}], "CWS": [{"C": false, "D": 31.0, "H": 20.0, "L": 20.0, "R": ""}], "HWS": false}	ft
283	1人睡房	176	5	{"H": "234.0", "L": "45.0", "W": "35.0", "CWS": "0"}	ft
285	自定義房間	177	7	{"R": null, "CP": [], "CW": [], "CWS": [{"C": false, "D": 10.0, "H": 10.0, "L": 10.0, "R": ""}], "HWS": false}	mm
286	睡房(有窗台)	168	10	{"H": "0", "L": "0", "W": "0", "CWS": "0"}	mm
\.


--
-- Data for Name: rooms_roomitem; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.rooms_roomitem (id, unit_price, value, quantity, item_id, room_id, material, remark, material_value_based_price, measure_quantifier, item_quantifier, value_based_price) FROM stdin;
205	1000.00	{}	1.00	28	120	null	\N	0.00	mm	單	1000.00
206	1500.00	{}	1.00	25	120	null	\N	0.00	mm	單	1500.00
207	100.00	{"L": 7.0, "W": 12.5}	1.00	23	120	null	\N	0.00	mm	單	100.00
173	15100.00	{"L": 5.0, "W": 5.0}	1.00	2	114	新造來去水喉	aaa	0.00	mm	單	15100.00
156	20.00	{"L": 1.0, "W": 1.0}	100.00	9	96	null		0.00	mm	單	20.00
347	1500.00	{}	1.00	25	179	null	\N	0.00	mm	單	1500.00
349	2000.00	{}	1.00	57	179	藏牆喉管	\N	0.00	mm	單	2000.00
351	850.00	{}	4.00	21	179	藏牆喉管		0.00	mm	單	850.00
353	1000.00	{}	1.00	14	179	藏牆喉管		0.00	mm	單	1000.00
355	1200.00	{}	1.00	54	179	藏牆喉管		0.00	mm	單	1200.00
359	3000.00	{}	1.00	66	174	null	\N	0.00	mm	單	3000.00
361	1000.00	{}	1.00	28	174	null	\N	0.00	mm	單	1000.00
363	100.00	{"L": "7.5", "W": "5.0"}	37.50	24	174	null	\N	0.00	mm	單	100.00
180	2500.00	{"L": 5.0, "W": 5.0}	1.00	1	113	null	\N	0.00	mm	單	2500.00
365	1100.00	{}	5.00	68	179	木紋膠板	\N	0.00	mm	單	1100.00
391	1020.50	{}	1.20	32	184	null	\N	0.00	mm	單	1020.50
403	1500.00	{}	4.00	47	188	外牆防水制	\N	300.00	mm	單	1200.00
377	55.00	{"L": "2.5", "W": "2.0"}	8.00	60	183	石膏板		50.00	m	個	5.00
379	100.00	{"L": "2.5", "W": "2.0"}	36.50	24	183	null	\N	0.00	m	單	100.00
381	1200.00	{"L": 1.3, "W": 1.0}	1.00	3	183	木紋膠板	\N	0.00	m	單	1200.00
245	30.00	{"L": 5.0, "W": 5.0}	1.00	16	132	null	\N	0.00	mm	單	30.00
243	20.00	{"L": 5.0, "W": 5.0}	1.00	9	132	null	\N	0.00	mm	單	20.00
244	30000.00	{"L": 4.0, "W": 4.0}	1.00	2	132	新造來去水喉	\N	15000.00	mm	單	15000.00
255	1400.00	{}	1.00	15	142	13 A雙位制		200.00	mm	單	1200.00
252	30.00	{"L": 2893.0, "W": 193.0}	2.00	16	139	null		0.00	mm	單	30.00
383	1200.00	{}	1.00	46	183	藏牆喉管	\N	0.00	mm	個	1200.00
256	3000.00	{}	1.00	27	146	null		0.00	mm	個	3000.00
254	16500.00	{"L": "0", "W": "0"}	1.00	2	142	代工安裝項目		500.00	mm	單	16000.00
385	30.00	{"L": "3.5", "W": "3.0"}	10.50	16	184	null	\N	0.00	m	單	30.00
346	3000.00	{}	1.00	27	179	null	\N	0.00	mm	單	3000.00
348	110.00	{"L": "0", "W": "0"}	45.00	60	179	鋁質長條天花	\N	60.00	mm	單	50.00
350	15000.00	{}	1.00	56	179	藏牆喉管	\N	0.00	mm	單	15000.00
265	2000.00	{"L": 900.0, "W": 900.0}	1.00	3	127	木紋膠板	圓桌	1000.00	mm	個	1000.00
352	850.00	{}	1.00	37	179	藏牆喉管		0.00	mm	單	850.00
332	1000.00	{}	1.00	14	174	藏牆喉管	\N	0.00	mm	個	1000.00
266	1000.00	{"L": 500.0, "W": 500.0}	4.00	1	127	木紋膠板	有椅背	500.00	mm	個	500.00
268	2000.00	{"L": 800.0, "W": 800.0}	1.00	3	154	木紋膠板	方桌	1000.00	mm	個	1000.00
270	1000.00	{}	1.00	4	154	藏牆喉管	LED	500.00	mm	個	500.00
388	1000.00	{}	1.00	31	184	null	\N	0.00	mm	單	1000.00
269	1000.00	{"L": 500.0, "W": 500.0}	2.00	1	154	木紋膠板	無椅背	500.00	mm	個	500.00
375	30.00	{"H": "3.0", "L": "2.5", "W": "2.0"}	27.00	39	183	null	\N	0.00	m	單	30.00
354	850.00	{"H": "0", "L": "0", "W": "0"}	3.00	5	179	藏牆喉管	\N	0.00	mm	單	850.00
201	3000.00	{"H": 10.0, "L": 10.0, "W": 10.0}	1.00	7	108	木紋膠板	\N	0.00	mm	單	3000.00
172	17000.00	{"H": 5.0, "L": 5.0, "W": 5.0}	1.00	6	114	新造來去水喉	testing	0.00	mm	單	17000.00
202	2000.00	{"H": 5.0, "L": 5.0, "W": 5.0}	1.00	5	96	13 A單位制	testing	0.00	mm	單	2000.00
204	2006.00	{"H": 5.0, "L": 5.0, "W": 5.0}	1.00	5	96	test 1	\N	0.00	mm	單	2006.00
176	17000.00	{"H": 1.0, "L": 1.0, "W": 1.0}	1.00	6	115	新造來去水喉	test	0.00	mm	單	17000.00
177	5850.00	{"H": 5.0, "L": 5.0, "W": 5.0}	1.00	5	115	13 A單位制	testing	0.00	mm	單	5850.00
179	17000.00	{"H": 1.0, "L": 1.0, "W": 1.0}	1.00	6	114	新造來去水喉	\N	0.00	mm	單	17000.00
181	7100.00	{"H": 5.0, "L": 5.0, "W": 5.0}	1.00	5	114	13 A單位制	\N	0.00	mm	單	7100.00
174	17000.00	{"H": 3.0, "L": 3.0, "W": 3.0}	1.00	6	77	新造來去水喉	123\n123\n123	0.00	mm	單	17000.00
253	623.00	{"H": 789.0, "L": 123.0, "W": 456.0}	1.00	6	103	代工安裝項目		500.00	m	單	123.00
257	17000.00	{"H": "0", "L": "0", "W": "0"}	1.00	11	146	新造來去水喉		15000.00	mm	個	2000.00
267	10000.00	{"H": 500.0, "L": 500.0, "W": 500.0}	1.00	5	127	外牆防水制	\N	5000.00	mm	個	5000.00
367	1500.00	{"H": "0", "L": "0", "W": "0"}	5.00	7	179	木紋膠板	\N	0.00	mm	單	1500.00
342	100.00	{"L": "9.0", "W": "5.0"}	45.00	24	179	null	\N	0.00	mm	單	100.00
344	3000.00	{}	1.00	66	179	null	\N	0.00	mm	單	3000.00
272	5000.00	{}	1.00	31	155	null	\N	0.00	mm	單	5000.00
273	20000.00	{"L": "3000.0"}	1.00	30	155	null		0.00	mm	單	20000.00
271	1000.00	{"L": "3000.0", "W": "2500.0"}	1.00	16	155	null		0.00	mm	單	1000.00
276	500.00	{}	3.00	20	155	外牆防水制	\N	500.00	mm	個	0.00
277	600.00	{}	1.00	25	156	null	\N	0.00	mm	單	600.00
279	1000.00	{}	1.00	21	156	藏牆喉管	\N	500.00	mm	個	500.00
280	2000.00	{}	1.00	26	157	null	\N	0.00	mm	單	2000.00
282	600.00	{}	2.00	21	157	藏牆喉管		300.00	mm	單	300.00
356	850.00	{}	1.00	51	179	藏牆喉管		0.00	mm	單	850.00
333	1200.00	{}	1.00	20	174	藏牆喉管	\N	0.00	mm	個	1200.00
326	30.00	{"L": "7.5", "W": "5.0"}	37.50	16	174	null		0.00	mm	單	30.00
310	1010.00	{}	2.00	56	168	藏牆喉管	\N	10.00	mm	單	1000.00
358	120.00	{"L": "7.5", "W": "5.0"}	37.50	60	174	鋁質長條天花	\N	60.00	mm	單	60.00
360	3000.00	{}	1.00	65	174	null	\N	0.00	mm	單	3000.00
362	3000.00	{}	1.00	27	174	null	\N	0.00	mm	單	3000.00
311	2500.00	{}	1.00	57	168	藏牆喉管	\N	500.00	mm	單	2000.00
389	100.00	{"L": "3.5", "W": "3.0"}	10.50	24	184	null	\N	0.00	m	單	100.00
366	1200.00	{"L": 5.0}	5.00	8	179	木紋膠板	不包括 所有特別 五金	0.00	ft	單	1200.00
376	30.00	{"L": "2.5", "W": "2.0"}	5.00	16	183	null	\N	0.00	m	單	30.00
378	600.00	{}	8.00	61	183	石膏板	\N	50.00	mm	單	550.00
380	2550.00	{"L": 1.5, "W": 1.0}	1.00	1	183	玻璃櫃門	\N	300.00	m	單	2250.00
390	1000.00	{"L": "3.5"}	1.00	30	184	null	\N	0.00	m	單	1000.00
415	100.00	{"L": "0", "W": "0"}	1.00	24	162	null	\N	0.00	mm	單	100.00
416	1200.00	{}	1.00	54	162	藏牆喉管	\N	0.00	mm	單	1200.00
417	1200.00	{}	1.00	53	162	藏牆喉管	\N	0.00	mm	單	1200.00
418	1200.00	{}	1.00	52	162	藏牆喉管	\N	0.00	mm	單	1200.00
419	850.00	{}	1.00	49	162	藏牆喉管	\N	0.00	mm	單	850.00
420	1200.00	{}	1.00	46	162	藏牆喉管	\N	0.00	mm	單	1200.00
421	1200.00	{}	1.00	20	162	藏牆喉管	\N	0.00	mm	單	1200.00
296	3.30	{"L": 3.3, "W": 3.3}	3.30	16	162	null		0.00	mm	單	3.30
422	1100.00	{}	4.00	54	93	外牆防水制	\N	304.00	mm	單	1100.00
426	30.00	{"L": "5.21", "W": "3.56"}	18.55	16	196	null	\N	0.00	m	單	30.00
430	100.00	{"L": "5.21", "W": "3.56"}	150.00	40	196	木紋膠板	\N	50.00	m	單	100.00
434	550.00	{}	5.00	61	197	鋁質長條天花	\N	60.00	mm	單	550.00
438	30.00	{"L": "6.89", "W": "4.28"}	29.49	16	198	null	白色	0.00	ft	單	30.00
446	1000.00	{}	1.00	31	199	null	\N	0.00	mm	項	1000.00
454	850.00	{}	4.40	21	210	外牆防水制	\N	300.00	mm	單	850.00
382	1150.00	{"H": "3.0", "L": "2.5", "W": "2.0"}	2.00	5	183	外牆防水制	\N	300.00	m	單	850.00
384	30.00	{"H": "3.0", "L": "3.5", "W": "3.0"}	39.00	39	184	null	\N	0.00	m	單	30.00
501	30.00	{"H": "0", "L": "0", "W": "0"}	1.00	39	233	\N	\N	0.00	mm	單	30.00
477	30.00	{"L": 30.0, "W": 120.0}	1.00	16	223	null	\N	0.00	ft	單	30.00
275	6000.00	{"H": 3000.0, "L": 3000.0, "W": 50.0}	1.00	17	155	木紋膠板	\N	3000.00	mm	個	3000.00
274	10000.00	{"H": 0.5, "L": 2.0, "W": 1.5}	1.00	8	155	木紋膠板		5000.00	ft	個	5000.00
521	300.00	{}	8.00	63	241	石膏板	\N	50.00	mm	直呎	250.00
364	100.00	{"H": "8.5", "L": "7.5", "W": "5.0"}	212.00	23	174	null	\N	0.00	mm	單	100.00
525	850.00	{}	1.00	45	241	藏牆喉管	\N	0.00	mm	單	850.00
442	1500.00	{"H": 1.2, "L": 2.0, "W": 2.0}	1.00	18	199	玻璃櫃門	\N	300.00	m	個	1500.00
459	2700.00	{"H": "5.0", "L": "5.0", "W": "5.0"}	1.00	17	169	玻璃櫃門	\N	300.00	mm	單	2700.00
450	100.00	{"H": "3.2", "L": "4.0", "W": "3.0"}	44.80	23	208	null	\N	0.00	mm	單	100.00
469	1500.00	{}	1.00	54	220	外牆防水制	\N	300.00	mm	單	1200.00
485	100.00	{"L": "0", "W": "0"}	1.00	24	225	null		0.00	mm	單	100.00
462	5000.00	{"L": 5.0}	1.00	8	96	木紋膠板		0.00	mm	單	5000.00
489	0.00	{"L": "0", "W": "0"}	80.00	16	226	\N	\N	0.00	mm	單	30.00
505	30.00	{"H": "3.25", "L": "4.69", "W": "2.48"}	46.60	39	237	\N	\N	0.00	m	單	30.00
529	100.00	{"L": 5.0, "T": 5.0, "W": 5.0}	125.00	60	238	石膏板	\N	50.00	m	單	50.00
509	3000.00	{"L": "2500.0", "W": "2000.0"}	2.00	2	156	明喉	\N	0.00	mm	單	3000.00
513	60.50	{"L": 3.0, "W": 3.5}	1.55	60	157	石膏板	\N	50.00	mm	單	10.50
541	2000.00	{}	1.00	87	254	\N	\N	0.00	mm	單	2000.00
545	4501.11	{}	3.22	55	254	明喉	\N	3000.22	mm	單	1500.89
549	100.00	{"L": "4.0", "W": "4.0"}	15.71	24	173	\N	\N	0.00	m	單	100.00
553	5500.00	{}	5.00	84	259	\N	\N	0.00	mm	單	5500.00
497	300.00	{}	1.00	63	77	石膏板	497	50.00	mm	單	250.00
569	600.00	{}	1.00	61	78	石膏板	row 1\nrow 2	50.00	mm	單	550.00
561	2000.00	{}	1.00	87	77	\N	row 1\nrow 2	0.00	mm	單	2000.00
577	30.00	{"L": "0", "W": "0"}	1.00	16	223	\N	\N	0.00	mm	單	30.00
595	40.00	{"H": 3.0, "L": 5.0, "W": 4.0}	1.00	39	267	\N		0.00	m	單	40.00
599	30.00	{"L": "4.33", "W": "5.24"}	1.00	16	230	\N	\N	0.00	m	單	30.00
603	30.00	{"L": "5.0", "W": "5.0"}	1.00	16	263	\N	\N	0.00	mm	單	30.00
402	3050.00	{"L": "2.2", "W": "1.8"}	3.00	2	188	藏牆喉管	\N	50.00	m	單	3000.00
341	30.00	{"L": "9.0", "W": "5.0"}	45.00	16	179	null	\N	0.00	mm	單	30.00
596	100.00	{"H": "3.0", "L": "5.0", "W": "4.0"}	1.00	23	268	\N		0.00	ft	平方米	100.00
189	300.00	{"L": "0", "W": "0"}	30.00	16	116	null	\N	0.00	mm	單	300.00
191	850.00	{}	3.00	21	117	暗喉	\N	0.00	mm	單	850.00
192	1200.00	{}	1.00	20	117	暗喉	\N	0.00	mm	單	1200.00
193	850.00	{}	6.00	21	116		\N	0.00	mm	單	850.00
494	98.00	{"H": 3.0, "L": 6.0, "W": 5.0}	50.00	23	226	\N	494	0.00	mm	單	100.00
194	1000.00	{}	1.00	15	118		\N	0.00	mm	單	1000.00
574	2000.00	{}	1.00	87	263	\N	row 1\nrow 2	0.00	mm	單	2000.00
604	600.00	{}	1.00	61	267	石膏板	\N	50.00	mm	單	550.00
198	1000.00	{"L": 5.0, "W": 5.0}	1.00	3	78	木紋膠板	\N	0.00	mm	單	1000.00
578	5500.00	{}	1.00	84	230	\N	\N	0.00	mm	單	5500.00
345	1000.00	{}	1.00	28	179	null	\N	0.00	mm	單	1000.00
423	1300.10	{"L": "5.0", "W": "5.0"}	1.30	18	162	玻璃櫃門	423	400.00	mm	單	900.00
427	500.00	{"L": "5.21", "W": "3.56"}	18.55	60	196	石膏板	按尺寸計	50.00	m	項	500.00
439	55.80	{}	8.00	61	198	鋁質長條天花	\N	60.30	mm	項	55.80
443	850.00	{}	2.00	4	199	外牆防水制	\N	300.00	mm	項	850.00
447	1000.00	{"L": 3.2}	3.20	30	199	null	\N	0.00	m	直呎	1000.00
451	30.00	{"L": "3.0", "W": "2.0"}	6.00	16	209	null	\N	0.00	mm	單	30.00
502	110.00	{"L": "4.65", "W": "2.82"}	13.11	60	235	防潮石膏板	\N	60.00	m	單	50.00
506	1500.00	{"L": "4.69", "W": "2.48"}	11.64	7	237	木紋膠板	\N	0.00	m	單	1500.00
510	20000.00	{}	1.00	56	157	明喉	\N	5000.00	mm	單	15000.00
514	100.00	{"L": 3.0, "W": 3.5}	10.20	24	157	\N	\N	0.00	m	單	100.00
200	5000.00	{"H": 5.0, "L": 5.0, "W": 5.0}	1.00	8	95	木紋膠板	\N	0.00	mm	單	5000.00
188	2700.00	{"H": 2700.0, "L": 1500.0, "W": 600.0}	5.00	17	116	null		0.00	mm	單	2700.00
190	2700.00	{"H": 2700.0, "L": 1050.0, "W": 600.0}	3.00	17	117	null	\N	0.00	mm	單	2700.00
187	1500.00	{"H": 350.0, "L": 350.0, "W": 350.0}	1.00	18	116	木紋膠板		0.00	mm	單	1500.00
195	17000.00	{"H": "0", "L": "0", "W": "0"}	1.00	11	118	新造來去水喉	\N	0.00	mm	單	17000.00
196	17000.00	{"H": 5.0, "L": 5.0, "W": 5.0}	1.00	6	96	新造來去水喉	\N	0.00	mm	單	17000.00
522	600.00	{}	8.00	61	241	石膏板	\N	50.00	mm	單	550.00
343	100.00	{"H": "8.5", "L": "9.0", "W": "5.0"}	238.00	23	179	null	\N	0.00	mm	單	100.00
431	50.00	{"H": "2.89", "L": "5.21", "W": 2.0}	20.58	17	196	木紋膠板	\N	30.00	m	平方呎	50.00
435	1500.00	{"H": "2.89", "L": "5.53", "W": "3.0"}	2.00	7	197	玻璃櫃門	\N	300.00	m	個	1500.00
199	1500.00	{"L": 5.0, "W": 5.0, "H (MM)": 5.0}	1.00	18	93	木紋膠板		0.00	mm	單	1500.00
246	40.00	{"L": 5.0, "W": 6.0}	40.00	16	93	null	\N	0.00	m	單	40.00
478	960.00	{"L": 300.0, "W": 100.0}	2.00	60	223	鋁質長條天花	\N	60.00	ft	單	900.00
526	1200.00	{}	2.00	20	241	藏牆喉管	\N	0.00	mm	單	1200.00
482	30.00	{}	2.00	49	223	明喉		20.00	mm	單	0.00
470	0.00	{}	1.00	54	220	明喉		0.00	mm	單	1200.00
486	0.00	{}	1.00	54	220	藏牆喉管	\N	0.00	mm	單	0.00
490	100.00	{"L": "7.0", "W": "6.0"}	1.00	24	228	\N	\N	0.00	mm	直呎	100.00
534	100.00	{"H": "3.25", "L": "4.69", "W": "2.48"}	46.60	23	250	\N	\N	0.00	m	單	100.00
538	2000.00	{}	1.00	87	249	\N	主人房門	0.00	mm	單	2000.00
542	30.00	{"L": "4.69", "W": "2.48"}	11.63	16	254	\N	\N	0.00	m	單	30.00
546	100.00	{"L": 3.22, "W": 4.88}	15.71	24	238	\N	\N	0.00	m	單	100.00
550	1500.00	{}	3.00	47	173	外牆防水制	\N	300.00	mm	單	1200.00
554	30.00	{"H": "3.0", "L": "4.0", "W": "2.0"}	36.00	39	260	\N	\N	0.00	mm	單	30.00
558	2000.00	{}	1.00	87	142	\N	\N	0.00	mm	單	2000.00
594	4000.00	{}	1.00	87	162	\N		0.00	mm	單	4000.00
424	1300.00	{"L": "0", "W": "0"}	1.00	3	162	玻璃櫃門	\N	300.00	mm	單	1300.00
428	3000.00	{}	1.00	31	196	null	\N	0.00	mm	項	3000.00
432	850.00	{}	5.50	4	196	外牆防水制	\N	300.00	mm	個	850.00
436	1200.00	{}	3.00	47	197	外牆防水制	\N	300.00	mm	個	1200.00
440	1500.00	{"L": 2.0, "W": 1.8}	3.60	1	198	木紋膠板	\N	0.00	m	平方呎	1500.00
448	1000.00	{}	1.00	32	199	null	\N	0.00	mm	單	1000.00
452	3000.00	{}	1.00	66	209	null	\N	0.00	mm	項	3000.00
456	100.00	{"L": "4.2", "W": "2.4"}	10.08	60	212	防潮石膏板	\N	60.00	mm	單	100.00
460	100.00	{"L": "5.21", "W": "3.56"}	100.00	40	215	木紋膠板	\N	0.00	mm	單	100.00
579	2000.00	{}	1.00	87	230	\N	\N	0.00	mm	單	2000.00
444	30.00	{"H": "2.89", "L": "5.01", "W": "3.67"}	50.17	39	199	null	\N	0.00	m	項	30.00
479	0.00	{"H": 20.0, "L": 50.0, "W": 3.0}	1.00	23	223	null		0.00	mm	單	0.00
483	0.00	{"H": "20.0", "L": "2.0", "W": "40.0"}	1.00	23	224	null		0.00	mm	單	0.00
487	1500.00	{"L": 3.0, "W": 3.0}	1.00	3	78	玻璃櫃門	487	300.00	mm	單	1200.00
597	1398.00	{"H": 3.25, "L": 2.48, "W": 4.69}	1.00	39	273	\N	\N	0.00	mm	單	1398.00
495	50.37	{"L": "4.33", "W": "5.24"}	133.61	60	230	石膏板	495	10.00	mm	單	40.37
499	200.66	{}	1.33	37	77	藏牆喉管	499	100.33	mm	單	100.33
503	100.00	{"L": "3.5", "W": "3.0"}	10.50	60	184	石膏板	\N	50.00	m	單	50.00
507	100.00	{"L": "4.69", "W": "2.48"}	11.63	60	237	石膏板	\N	50.00	m	單	50.00
511	1000.00	{}	3.00	20	157	藏牆喉管	\N	500.00	mm	個	500.00
519	30.00	{"H": "8.0", "L": "8.0", "W": "8.0"}	256.00	39	241	\N	519	0.00	ft	單	30.00
523	0.00	{"L": "8.0", "W": "8.0"}	1.00	40	241	木紋膠板	\N	1.00	ft	單	15000.00
527	30.00	{"H": 8.0, "L": 8.0, "W": 8.0}	64.00	39	242	\N	527	0.00	ft	單	30.00
531	50.00	{"H": 3.25, "L": 4.69, "W": 2.48}	46.60	39	249	\N	\N	0.00	m	單	50.00
535	10.65	{"L": 4.9, "W": 3.2}	15.68	60	250	石膏板	\N	4.76	mm	單	5.89
539	1200.00	{}	1.00	45	249	藏牆喉管	\N	350.00	mm	單	850.00
543	100.00	{"L": "4.69", "W": "2.48"}	11.63	24	254	\N	\N	0.00	m	單	100.00
547	100.00	{"L": 4.88, "W": 3.22}	15.71	24	236	\N	\N	0.00	m	單	100.00
551	100.00	{"L": "4.0", "W": "4.0"}	16.00	60	173	石膏板	\N	50.00	m	單	50.00
555	100.00	{"L": "4.22", "W": "2.22"}	9.37	60	261	石膏板	\N	50.00	m	單	50.00
567	5500.00	{}	1.00	84	95	\N	\N	0.00	mm	單	5500.00
429	100.00	{"L": "5.21", "W": "3.56"}	18.55	24	196	null	平方米	0.00	m	項	100.00
433	50.00	{"L": "5.53", "W": "3.0"}	16.59	16	197	null	\N	0.00	m	平方呎	50.00
441	1200.00	{}	6.00	20	198	外牆防水制	\N	300.00	mm	單	1200.00
445	50.00	{"L": "5.01", "W": "3.67"}	18.39	60	199	防潮石膏板	\N	60.00	m	單	50.00
449	100.00	{"L": "3.5", "W": "2.5"}	8.75	24	205	null	\N	0.00	mm	單	100.00
453	1200.00	{}	5.50	54	210	外牆防水制	\N	300.00	mm	單	1200.00
548	100.00	{"L": 3.22, "W": 4.88}	15.71	24	258	\N	\N	0.00	mm	單	100.00
394	1500.00	{}	1.00	53	184	外牆防水制	\N	300.00	mm	單	1200.00
395	1200.00	{}	1.00	52	184	藏牆喉管	\N	0.00	mm	單	1200.00
396	1150.00	{}	2.00	48	184	外牆防水制	\N	300.00	mm	單	850.00
484	1200.00	{}	1.00	20	225	藏牆喉管	\N	0.00	mm	單	1200.00
316	30.00	{"L": 5.0, "W": 7.0}	35.00	16	169	null		0.00	mm	單	30.00
336	30.00	{"L": "9.0", "W": "4.5"}	40.50	16	178	null	\N	0.00	mm	單	30.00
297	5000.00	{"L": 10.0}	1.00	30	162	null		0.00	m	單	5000.00
319	1150.00	{}	1.00	50	166	藏牆喉管	\N	300.00	mm	單	850.00
397	30.00	{"L": "2.2", "W": "1.8"}	3.96	16	188	null	\N	0.00	m	單	30.00
398	100.00	{"L": "2.2", "W": "1.8"}	8.00	60	188	石膏板	\N	50.00	m	單	50.00
400	100.00	{"L": "2.2", "W": "1.8"}	8.20	24	188	null	\N	0.00	m	單	100.00
401	15000.00	{}	1.00	55	188	明喉	\N	0.00	mm	單	15000.00
327	2000.00	{}	1.00	57	174	藏牆喉管	\N	0.00	mm	單	2000.00
328	15000.00	{}	1.00	56	174	藏牆喉管	\N	0.00	mm	單	15000.00
330	850.00	{}	2.00	50	174	藏牆喉管		0.00	mm	單	850.00
329	850.00	{}	4.00	49	174	藏牆喉管		0.00	mm	單	850.00
331	850.00	{}	2.00	21	174	藏牆喉管	\N	0.00	mm	個	850.00
337	200.00	{}	4.50	62	178	石膏板	\N	50.00	mm	單	150.00
338	200.00	{}	4.50	61	178	石膏板	\N	50.00	mm	單	150.00
404	30.00	{"L": "2.2", "W": "1.8"}	3.96	16	189	null	\N	0.00	m	單	30.00
405	610.00	{}	1.00	61	189	鋁質長條天花	\N	60.00	mm	單	550.00
406	3000.00	{}	1.00	27	189	null	\N	0.00	mm	單	3000.00
407	3500.00	{}	1.00	66	189	null	\N	0.00	mm	個	3500.00
408	2400.00	{}	1.00	57	189	明喉	\N	0.00	mm	單	2400.00
409	3025.00	{"L": "2.2", "W": "1.8"}	3.00	2	189	明喉	\N	25.00	m	單	3000.00
410	1500.00	{"L": "2.2"}	1.00	8	189	玻璃櫃門	\N	300.00	m	單	1200.00
411	1300.00	{}	1.00	15	189	外牆防水制	\N	300.00	mm	單	1000.00
488	0.00	{"L": 800.0, "W": 500.0}	80.00	39	226	\N	\N	0.00	mm	單	30.00
414	100.00	{"L": 5.0, "W": 5.0}	1.00	24	162	null	\N	0.00	mm	單	100.00
412	1000.00	{}	1.00	32	162	null	\N	0.00	mm	單	1000.00
457	850.00	{}	3.00	50	212	外牆防水制	\N	300.00	mm	單	850.00
461	1000.00	{}	10.00	32	215	null	\N	0.00	mm	單	1000.00
465	5300.00	{"L": 5.0}	1.00	8	95	玻璃櫃門	\N	300.00	mm	單	5000.00
500	30.33	{"H": "5.0", "L": "5.0", "W": "5.0"}	1.33	39	220	\N	\N	0.00	mm	單	30.33
504	1150.00	{"L": "4.69", "W": "2.48"}	11.63	5	237	外牆防水制	\N	300.00	m	單	850.00
508	30.00	{"H": "3.25", "L": "4.69", "W": "2.48"}	46.60	39	238	\N	\N	0.00	m	單	30.00
512	2000.00	{"L": 500.0, "W": 500.0}	2.00	7	210	木紋膠板	\N	500.00	mm	個	1500.00
437	30.00	{"H": "2.89", "L": "6.89", "W": "4.28"}	64.56	39	198	null	米色	0.00	ft	平方呎	30.00
392	1500.00	{"H": 0.6, "L": 0.6, "W": 0.4}	1.00	18	184	木紋膠板	\N	0.00	m	單	1500.00
393	2700.00	{"H": 3.0, "L": "3.5", "W": 0.6}	1.00	17	184	木紋膠板	\N	0.00	m	單	2700.00
335	30.00	{"H": 9.0, "L": "9.0", "W": 4.5}	243.00	39	178	null	\N	0.00	ft	單	30.00
399	52.50	{"H": "3.0", "L": "2.2", "W": "1.8"}	13.50	23	188	null	\N	0.00	m	個	52.50
413	100.00	{"H": "5.0", "L": "5.0", "W": "5.0"}	1.00	23	162	null	\N	0.00	mm	單	100.00
476	132.00	{"L": 12.0, "W": 39.0}	3.00	16	103	null		0.00	mm	單	133.00
520	30.00	{"L": "8.0", "W": "8.0"}	64.00	16	241	\N	\N	0.00	ft	單	30.00
524	1500.00	{"L": "0", "W": "0"}	5.00	3	241	玻璃櫃門	\N	300.00	mm	直呎	1200.00
532	100.00	{"L": 4.8, "W": 3.2}	10.20	24	204	\N	532	0.00	m	單	100.00
552	2000.00	{"L": "4.0", "W": "4.0"}	16.00	40	173	木紋膠板	552	1000.00	m	單	1000.00
536	30.00	{"L": 5.0, "W": 7.0}	35.00	16	249	\N	\N	0.00	m	單	30.00
540	30.00	{"H": "4.69", "L": "7.0", "W": "2.99"}	93.71	39	251	\N	\N	0.00	mm	單	30.00
544	1700.00	{}	2.00	52	254	外牆防水制	\N	500.00	mm	單	1200.00
576	2030.00	{"H": "0", "L": "0", "W": "0"}	1.00	39	223	\N	576	0.00	mm	單	2030.00
602	30.00	{"H": 3.25, "L": 2.48, "W": 4.69}	1.00	39	226	\N		0.00	mm	單	30.00
\.


--
-- Data for Name: rooms_roomproperty; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.rooms_roomproperty (id, name, symbol, data_type, custom_properties, custom_property_formulas, index) FROM stdin;
6	自訂牆身	CW	custom property	[{"name": "闊", "symbol": "W", "group_id": "1", "data_type": "num"}, {"name": "高", "symbol": "H", "group_id": "1", "data_type": "num"}, {"name": "備註", "symbol": "R", "group_id": "2", "data_type": "string"}]	[{"name": "AREA", "formula": "\\"H\\"*\\"W\\""}]	0
8	有窗台	HWS	bool	[]	[]	0
9	備註	R	string	[]	[]	0
5	自訂地台	CP	custom property	[{"name": "面積", "symbol": "A", "group_id": "1", "data_type": "num"}, {"name": "備註", "symbol": "R", "group_id": "2", "data_type": "string"}, {"name": "闊度", "symbol": "W", "group_id": "3", "data_type": "num"}, {"name": "長度", "symbol": "L", "group_id": "3", "data_type": "num"}]	[{"name": "AREA", "formula": "\\"A\\""}, {"name": "Area", "formula": "\\"L\\"*\\"W\\""}, {"name": "Test", "formula": "\\"A\\"+\\"W\\"+\\"L\\""}]	0
7	自訂窗台	CWS	custom property	[{"name": "長", "symbol": "L", "group_id": "1", "data_type": "num"}, {"name": "高", "symbol": "H", "group_id": "1", "data_type": "num"}, {"name": "深", "symbol": "D", "group_id": "1", "data_type": "num"}, {"name": "備註", "symbol": "R", "group_id": "2", "data_type": "string"}, {"name": "檢查", "symbol": "C", "group_id": "3", "data_type": "bool"}]	[{"name": "AREA", "formula": "\\"L\\"*\\"H\\"*2+\\"D\\"*\\"H\\"*2"}]	0
3	闊度	W	num	[]	[]	2
2	長度	L	num	[]	[]	1
1	高度	H	num	[]	[]	3
\.


--
-- Data for Name: rooms_roomtype; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.rooms_roomtype (id, name, is_active, room_type_formulas, related_items_sort, room_properties_sort) FROM stdin;
3	客廳	t	[{"name": "地台面積", "formula": "\\"L\\"*\\"W\\"", "is_active": "True"}, {"name": "牆身面積", "formula": "\\"W\\"*\\"H\\"*2+\\"L\\"*\\"H\\"*2", "is_active": "True"}]	[77, 76, 75, 61, 60, 54, 53, 52, 51, 50, 49, 48, 47, 46, 45, 39, 37, 21, 20, 16, 7, 5, 4, 3, 1]	[1, 3, 2]
2	廚房	t	[{"name": "地台面積", "formula": "\\"L\\"*\\"W\\"", "is_active": "True"}, {"name": "牆身面積", "formula": "\\"W\\"*\\"H\\"*2+\\"L\\"*\\"H\\"*2", "is_active": "True"}]	[87, 85, 84, 79, 65, 63, 62, 61, 60, 57, 55, 54, 53, 52, 51, 50, 49, 47, 37, 27, 25, 24, 23, 21, 20, 16, 4, 2]	[1, 3, 2]
10	睡房(有窗台)	t	[{"name": "地台面積", "formula": "\\"L\\"*\\"W\\"", "is_active": "True"}]	[87, 85, 84, 78, 77, 76, 75, 44, 40, 18, 17, 7, 3]	[1, 2, 3, 7]
9	書房	t	[{"name": "地台面積", "formula": "\\"L\\"*\\"W\\"", "is_active": "True"}, {"name": "牆身面積", "formula": "\\"W\\"*\\"H\\"*2+\\"L\\"*\\"H\\"*2", "is_active": "True"}]	[24, 23]	[1, 3, 2]
7	自定義房間	t	[{"name": "總地台面積", "formula": "sum(\\"CP.AREA\\")", "is_active": "True"}, {"name": "總牆身面積", "formula": "sum(\\"CW.AREA\\")", "is_active": "True"}, {"name": "總窗台面積", "formula": "sum(\\"CWS.AREA\\")", "is_active": "True"}]	[61, 60, 54, 53, 52, 51, 50, 49, 48, 47, 46, 45, 39, 37, 24, 23, 21, 20, 16, 5, 4]	[5, 6, 7, 8, 9]
6	2人睡房	t	[{"name": "地台面積", "formula": "\\"L\\"*\\"W\\"", "is_active": "True"}, {"name": "牆身面積", "formula": "\\"W\\"*\\"H\\"*2+\\"L\\"*\\"H\\"*2", "is_active": "True"}]	[87, 85, 84, 61, 60, 54, 53, 52, 51, 50, 49, 48, 47, 46, 45, 39, 37, 32, 31, 30, 24, 23, 21, 20, 18, 17, 16, 8, 7, 4, 3]	[1, 3, 2]
5	1人睡房	t	[{"name": "地台面積", "formula": "\\"L\\"*\\"W\\"", "is_active": "True"}, {"name": "牆身面積", "formula": "\\"W\\"*\\"H\\"*2+\\"L\\"*\\"H\\"*2", "is_active": "True"}]	[63, 62, 61, 60, 54, 53, 52, 51, 50, 49, 48, 47, 46, 45, 40, 39, 37, 32, 31, 24, 23, 21, 20, 18, 17, 16, 7, 5, 4, 3]	[1, 3, 2, 7]
4	飯廳	t	[{"name": "地台面積", "formula": "\\"L\\"*\\"W\\"", "is_active": "True"}, {"name": "牆身面積", "formula": "\\"W\\"*\\"H\\"*2+\\"L\\"*\\"H\\"*2", "is_active": "True"}]	[61, 60, 54, 53, 52, 51, 50, 49, 48, 47, 46, 45, 39, 37, 24, 23, 21, 20, 16, 5, 4, 3, 1]	[1, 3, 2]
1	浴室	t	[{"name": "地台面積", "formula": "\\"L\\"*\\"W\\"", "is_active": "True"}, {"name": "牆身面積", "formula": "\\"W\\"*\\"H\\"+\\"L\\"*\\"H\\"+\\"W\\"*\\"H\\"+\\"L\\"*\\"H\\"", "is_active": "True"}]	[87, 85, 84, 68, 66, 65, 61, 60, 57, 56, 54, 53, 52, 51, 50, 49, 48, 47, 37, 28, 27, 25, 24, 23, 21, 20, 16, 15, 14, 8, 7, 5, 4, 3, 2]	[2, 3, 1]
22	A	t	[]	[]	[]
\.


--
-- Data for Name: rooms_roomtype_related_items; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.rooms_roomtype_related_items (id, roomtype_id, item_id) FROM stdin;
1	3	1
39	3	3
40	3	4
41	3	5
43	7	4
44	7	5
49	6	8
50	6	7
51	4	1
52	4	3
55	4	4
56	4	5
59	1	14
60	1	15
61	6	16
62	6	17
63	6	18
64	6	20
65	6	21
69	5	20
70	5	21
72	6	30
73	6	32
74	6	31
75	2	20
76	2	21
85	1	20
86	1	21
98	6	37
99	3	7
100	5	45
101	5	46
102	5	47
103	5	48
104	5	49
105	5	50
106	5	51
107	5	52
108	5	53
109	5	54
110	4	37
111	4	45
112	4	46
113	4	47
114	4	48
115	4	49
116	4	50
117	4	51
118	4	52
119	4	53
120	4	54
121	5	3
122	5	37
123	5	39
124	5	40
125	5	7
126	5	17
127	5	18
128	5	24
129	2	4
130	2	37
131	2	47
132	2	49
133	2	50
134	2	51
135	2	52
136	2	53
137	2	54
138	7	37
139	7	45
140	7	46
141	7	47
142	7	48
143	7	49
144	7	50
145	7	51
146	7	52
147	7	53
148	7	54
149	7	21
150	7	20
151	1	4
152	1	37
153	1	5
154	1	47
155	1	48
156	1	49
157	1	50
158	1	51
159	1	52
160	1	53
161	1	54
162	3	37
163	3	45
164	3	46
165	3	47
166	3	48
167	3	49
168	3	50
169	3	51
170	3	52
171	3	53
172	3	54
173	3	21
174	3	20
175	5	4
176	5	5
177	4	20
178	4	21
179	6	3
180	6	4
181	6	45
182	6	46
183	6	47
184	6	48
185	6	49
186	6	50
187	6	51
188	6	52
189	6	53
190	6	54
191	2	2
192	2	55
193	1	56
194	1	2
195	2	57
196	1	57
197	1	16
198	2	16
199	6	39
200	5	16
201	4	16
202	4	39
203	7	16
204	7	39
205	3	16
206	3	39
208	1	60
209	1	61
210	5	60
211	5	61
212	4	60
213	4	61
214	2	60
215	2	61
216	7	60
217	7	61
218	3	60
219	3	61
220	6	60
221	6	61
222	5	62
223	5	63
224	2	62
225	2	63
226	2	24
227	2	25
228	2	23
229	1	65
230	1	66
231	1	23
232	1	24
233	1	25
234	1	27
235	1	28
236	2	65
237	2	27
238	5	32
239	5	23
240	5	31
242	7	24
243	7	23
244	9	24
245	9	23
246	4	24
247	4	23
248	6	24
249	6	23
251	1	8
252	1	68
253	1	3
254	1	7
273	3	75
274	3	76
275	3	77
276	10	3
277	10	7
278	10	40
279	10	75
280	10	76
281	10	77
282	10	78
283	10	44
284	10	17
285	10	18
286	2	79
287	1	84
288	1	85
289	1	87
290	2	84
291	2	85
292	2	87
293	10	84
294	10	85
295	10	87
296	6	84
297	6	85
298	6	87
316	22	78
326	22	80
327	22	87
328	22	82
329	22	9
330	22	10
331	22	3
332	22	85
\.


--
-- Data for Name: rooms_roomtype_room_properties; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.rooms_roomtype_room_properties (id, roomtype_id, roomproperty_id) FROM stdin;
4	2	1
5	2	2
6	2	3
7	3	1
8	3	2
9	3	3
10	4	1
11	4	2
12	4	3
13	5	1
14	5	2
15	5	3
16	6	1
17	6	2
18	6	3
25	7	5
26	7	6
27	7	7
31	7	8
32	7	9
33	9	1
34	9	2
35	9	3
37	10	1
38	10	2
39	10	3
40	10	7
57	5	7
89	1	1
90	1	2
91	1	3
\.


--
-- Data for Name: rooms_roomtypeformula; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.rooms_roomtypeformula (id, name, formula, room_type_id, is_active) FROM stdin;
5	牆身面積	"W"*"H"*2+"L"*"H"*2	3	t
4	地板面積	"W"*"L"	3	t
2	牆身面積	"W"*"H"*2+"L"*"H"*2	1	t
7	總地台面積	sum("CP.AREA")	7	t
8	總牆身面積	sum("CW.AREA")	7	t
9	總窗台面積	sum("CWS.AREA")	7	t
1	地台面積	"L"*"W"	1	t
10	地台面積	"L"*"W"	5	t
11	牆身面積	"W"*"H"*2+"L"*"H"*2	5	t
12	地台面積	"L"*"W"	6	t
13	牆身面積	"W"*"H"*2+"L"*"H"*2	6	t
14	地台面積	"L"*"W"	4	t
15	牆身面積	"W"*"H"*2+"L"*"H"*2	4	t
16	地台面積	"L"*"W"	2	t
17	牆身面積	"W"*"H"*2+"L"*"H"*2	2	t
\.


--
-- Data for Name: subscription_plans_companysubscribedplan; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.subscription_plans_companysubscribedplan (id, start_date, next_billing_date, company_id, plan_id) FROM stdin;
3	2020-10-14	\N	2	1
\.


--
-- Data for Name: subscription_plans_subscriptionplan; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.subscription_plans_subscriptionplan (id, plan_name, display_price, project_quota, function_permission, description, is_active, visible, bottom_bg_color, top_bg_color) FROM stdin;
1	Free Plan	0.00	1	{}	- 1 project	t	f	#FFFFFF	#FFFFFF
2	Standard Plan	50.00	3	{}	- 3 projects	t	t	#1A61C9	#0F4DA8
3	Advanced Plan	65.00	6	{}	- 6 projects	t	t	#0EA9D2	#0F88A8
4	Professional Plan	88.00	\N	{}	- Unlimited projects	t	t	#5A6ED4	#7361C9
\.


--
-- Data for Name: tasks_task; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tasks_task (id, title, status, priority, due_date, created_by_id, created_on, company_id) FROM stdin;
\.


--
-- Data for Name: tasks_task_assigned_to; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tasks_task_assigned_to (id, task_id, user_id) FROM stdin;
\.


--
-- Data for Name: tasks_task_contacts; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tasks_task_contacts (id, task_id, contact_id) FROM stdin;
\.


--
-- Data for Name: tasks_task_teams; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tasks_task_teams (id, task_id, teams_id) FROM stdin;
\.


--
-- Data for Name: teams_teams; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.teams_teams (id, name, description, created_by_id, created_on) FROM stdin;
\.


--
-- Data for Name: teams_teams_users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.teams_teams_users (id, teams_id, user_id) FROM stdin;
\.


--
-- Data for Name: thumbnail_kvstore; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.thumbnail_kvstore (key, value) FROM stdin;
sorl-thumbnail||image||beabac3628a9252de4f9d7528ba9072d	{"name": "companies/1/logos/icon.png", "storage": "django.core.files.storage.FileSystemStorage", "size": [406, 144]}
sorl-thumbnail||image||22207dab3f77b3290fcefb64ff7ab36c	{"name": "cache/9c/cc/9ccc0cbc3c1b6a35b1accab9afae2167.jpg", "storage": "django.core.files.storage.FileSystemStorage", "size": [125, 44]}
sorl-thumbnail||thumbnails||beabac3628a9252de4f9d7528ba9072d	["22207dab3f77b3290fcefb64ff7ab36c"]
sorl-thumbnail||image||f5fd119d02c36bb8242224ceb8f622af	{"name": "companies/None/signs/3b1ec38c-93c.jpg", "storage": "django.core.files.storage.FileSystemStorage", "size": [480, 480]}
sorl-thumbnail||image||1332121122ad947e49f6f6f0fa0d7b57	{"name": "cache/e1/cd/e1cd7efc31fd8941d4b7dac71cd67699.jpg", "storage": "django.core.files.storage.FileSystemStorage", "size": [125, 125]}
sorl-thumbnail||image||4d63c651578b78b63258b4987c613dbe	{"name": "companies/2/logos/f307271e-b15.jpg", "storage": "django.core.files.storage.FileSystemStorage", "size": [480, 480]}
sorl-thumbnail||image||d16b6b0e1d707ae7419c4b3cb82b22b6	{"name": "cache/92/fd/92fdd76aa569b8d55e1277667522e426.jpg", "storage": "django.core.files.storage.FileSystemStorage", "size": [125, 125]}
sorl-thumbnail||thumbnails||4d63c651578b78b63258b4987c613dbe	["d16b6b0e1d707ae7419c4b3cb82b22b6"]
sorl-thumbnail||image||814fdcb2004a4f5d19c5480427dffb27	{"name": "cache/e1/ab/e1ab1c3d99331172d21045fac514bc53.jpg", "storage": "django.core.files.storage.FileSystemStorage", "size": [150, 150]}
sorl-thumbnail||image||ca412e7312a9b7fc7238f727e56cdfdb	{"name": "cache/94/fd/94fdaa464f902633b9e012275610819f.jpg", "storage": "django.core.files.storage.FileSystemStorage", "size": [125, 125]}
sorl-thumbnail||thumbnails||f5fd119d02c36bb8242224ceb8f622af	["814fdcb2004a4f5d19c5480427dffb27", "ca412e7312a9b7fc7238f727e56cdfdb", "1332121122ad947e49f6f6f0fa0d7b57"]
sorl-thumbnail||image||c7159bc62f89b9356d65ba9de253197e	{"name": "companies/1/signs/quill-signature-logo-design-inspiration_57043-204.jpg", "storage": "django.core.files.storage.FileSystemStorage", "size": [626, 375]}
sorl-thumbnail||image||96efd3db1b3a94d18d01cb49e82b7197	{"name": "cache/be/7e/be7e7f130762c19b204f43220343ddf8.jpg", "storage": "django.core.files.storage.FileSystemStorage", "size": [125, 75]}
sorl-thumbnail||image||c8fe1a2f86ea60b94ddce9e917877c40	{"name": "companies/1/logos/f307271e-b15.jpg", "storage": "django.core.files.storage.FileSystemStorage", "size": [480, 480]}
sorl-thumbnail||image||0c007d490a7c2b2742111f6411817990	{"name": "cache/e7/5b/e75bbfe57190171f95a8088740a153ca.jpg", "storage": "django.core.files.storage.FileSystemStorage", "size": [125, 125]}
sorl-thumbnail||thumbnails||c8fe1a2f86ea60b94ddce9e917877c40	["0c007d490a7c2b2742111f6411817990"]
sorl-thumbnail||image||de418fea9aab037811c3172152093c42	{"name": "cache/17/57/1757795773548821103455daf5a24935.jpg", "storage": "django.core.files.storage.FileSystemStorage", "size": [125, 75]}
sorl-thumbnail||thumbnails||c7159bc62f89b9356d65ba9de253197e	["96efd3db1b3a94d18d01cb49e82b7197", "de418fea9aab037811c3172152093c42"]
sorl-thumbnail||image||c2848d24e92fa11fc425de1eaafa05c4	{"name": "companies/8/logos/b1af3879-db4.jpg", "storage": "django.core.files.storage.FileSystemStorage", "size": [480, 480]}
sorl-thumbnail||image||9fe71992f6ac6518523cc3bf3219daf4	{"name": "cache/45/3c/453ce691510fd5747da0d0d2dbcf53bb.jpg", "storage": "django.core.files.storage.FileSystemStorage", "size": [125, 125]}
sorl-thumbnail||thumbnails||c2848d24e92fa11fc425de1eaafa05c4	["9fe71992f6ac6518523cc3bf3219daf4"]
sorl-thumbnail||image||ecbecab6e68b7386dafb6bb9091ca545	{"name": "companies/9/signs/42f76971-9b6.jpg", "storage": "django.core.files.storage.FileSystemStorage", "size": [480, 480]}
sorl-thumbnail||image||6e71e52835decd7d39912b64897162c0	{"name": "cache/04/6a/046a1e9f8b4a287b15613f7ead461d46.jpg", "storage": "django.core.files.storage.FileSystemStorage", "size": [125, 125]}
sorl-thumbnail||image||9de13aa606cf2bf633917ccf0a0f8270	{"name": "companies/9/logos/bb321fb3-2c5.jpg", "storage": "django.core.files.storage.FileSystemStorage", "size": [480, 480]}
sorl-thumbnail||image||5411e1295c917d4777a0be5c4fc44fd9	{"name": "cache/ef/88/ef88930b787340b43c7f419e6e8bf4cc.jpg", "storage": "django.core.files.storage.FileSystemStorage", "size": [125, 125]}
sorl-thumbnail||thumbnails||9de13aa606cf2bf633917ccf0a0f8270	["5411e1295c917d4777a0be5c4fc44fd9"]
sorl-thumbnail||image||9903d3d406c37d1a183f782a2415c0ee	{"name": "cache/15/7e/157ef9f961ba8d5e739a34a0a51d89c0.jpg", "storage": "django.core.files.storage.FileSystemStorage", "size": [125, 125]}
sorl-thumbnail||thumbnails||ecbecab6e68b7386dafb6bb9091ca545	["9903d3d406c37d1a183f782a2415c0ee", "6e71e52835decd7d39912b64897162c0"]
sorl-thumbnail||image||ad05f4e3629a93892066f43aa8368d96	{"name": "companies/15/signs/75f1ec54-967.jpg", "storage": "django.core.files.storage.FileSystemStorage", "size": [4032, 3024]}
sorl-thumbnail||image||2575e9c4a5a804103cff7c5d9dd9963f	{"name": "cache/09/16/091694100560a69a8076744d81291f6c.jpg", "storage": "django.core.files.storage.FileSystemStorage", "size": [70, 94]}
sorl-thumbnail||thumbnails||ad05f4e3629a93892066f43aa8368d96	["2575e9c4a5a804103cff7c5d9dd9963f"]
sorl-thumbnail||image||e3f8780081f5023fea9c3096e499021c	{"name": "companies/15/logos/ee4aacb1-f24.jpg", "storage": "django.core.files.storage.FileSystemStorage", "size": [4032, 3024]}
sorl-thumbnail||image||d3a014a5bff1e06f93bda4bb4ed3e252	{"name": "cache/bd/93/bd93011f60a0a1503506a614401187af.jpg", "storage": "django.core.files.storage.FileSystemStorage", "size": [94, 125]}
sorl-thumbnail||thumbnails||e3f8780081f5023fea9c3096e499021c	["d3a014a5bff1e06f93bda4bb4ed3e252"]
sorl-thumbnail||image||799171c305af1adc724e897bc7bbf453	{"name": "companies/15/signs/d120be13-f33.jpg", "storage": "django.core.files.storage.FileSystemStorage", "size": [960, 1280]}
sorl-thumbnail||image||0114b9cda74979ef9f1b9580c607be3b	{"name": "cache/fe/a5/fea50feef515fdc6176b72663efae876.jpg", "storage": "django.core.files.storage.FileSystemStorage", "size": [125, 167]}
sorl-thumbnail||image||e2805f082ef4e6df806cc116cc7068a4	{"name": "cache/a7/79/a779ca1cfa1dcf3856d4b2d85cec5545.jpg", "storage": "django.core.files.storage.FileSystemStorage", "size": [94, 125]}
sorl-thumbnail||thumbnails||799171c305af1adc724e897bc7bbf453	["0114b9cda74979ef9f1b9580c607be3b", "e2805f082ef4e6df806cc116cc7068a4"]
sorl-thumbnail||image||45a5676eee1465ac0f55109a1c4b7e1d	{"name": "companies/15/logos/35bbc78a-c0e.jpg", "storage": "django.core.files.storage.FileSystemStorage", "size": [960, 1280]}
sorl-thumbnail||image||0a72e2c66e9f73623e86fde12038454a	{"name": "cache/44/f4/44f463f97bd82ae252e456ee3e981047.jpg", "storage": "django.core.files.storage.FileSystemStorage", "size": [94, 125]}
sorl-thumbnail||thumbnails||45a5676eee1465ac0f55109a1c4b7e1d	["0a72e2c66e9f73623e86fde12038454a"]
sorl-thumbnail||image||82e47fa37873678e3de057ea557faad8	{"name": "companies/19/logos/07cb24ad-6f6.jpg", "storage": "django.core.files.storage.FileSystemStorage", "size": [960, 1280]}
sorl-thumbnail||image||a1d5b91244f22c597c514800794f4a25	{"name": "cache/93/b8/93b87891fc075c2b39f6a6d667a7f84c.jpg", "storage": "django.core.files.storage.FileSystemStorage", "size": [94, 125]}
sorl-thumbnail||thumbnails||82e47fa37873678e3de057ea557faad8	["a1d5b91244f22c597c514800794f4a25"]
sorl-thumbnail||image||1309f2bd5bbf272d4ee4a0168174afba	{"name": "companies/11/logos/820f6dae-549.png", "storage": "django.core.files.storage.FileSystemStorage", "size": [1440, 2560]}
sorl-thumbnail||image||1f5a676edd54f43132979429e1c8f1c9	{"name": "cache/96/02/9602d93bc43a04aa424ab29e7af955a7.jpg", "storage": "django.core.files.storage.FileSystemStorage", "size": [70, 125]}
sorl-thumbnail||thumbnails||1309f2bd5bbf272d4ee4a0168174afba	["1f5a676edd54f43132979429e1c8f1c9"]
sorl-thumbnail||image||15308c420841a8bc6c5f9c5ce619af72	{"name": "companies/15/logo", "storage": "django.core.files.storage.FileSystemStorage", "size": [184, 60]}
sorl-thumbnail||image||7f4c3f2777471ce10c8e9f4467ce0126	{"name": "cache/8f/28/8f28d861b078cd0894539e3cda9bb2ea.jpg", "storage": "django.core.files.storage.FileSystemStorage", "size": [125, 41]}
sorl-thumbnail||thumbnails||15308c420841a8bc6c5f9c5ce619af72	["7f4c3f2777471ce10c8e9f4467ce0126"]
sorl-thumbnail||image||ce21ef3564f852179ef17021b553e591	{"name": "cache/c7/ed/c7eda549580a77cc74bf93784178deee.jpg", "storage": "django.core.files.storage.FileSystemStorage", "size": [125, 41]}
sorl-thumbnail||thumbnails||7f4c3f2777471ce10c8e9f4467ce0126	["ce21ef3564f852179ef17021b553e591"]
sorl-thumbnail||image||2fdbebb32561c82ff698ba05ac4b1cb9	{"name": "companies/15/86288a2a-ae7.png", "storage": "django.core.files.storage.FileSystemStorage", "size": [184, 60]}
sorl-thumbnail||image||f253a25daebe6483b75a613e1580f2fa	{"name": "cache/3d/46/3d46f6b989c5d946c39db0ebe0453479.jpg", "storage": "django.core.files.storage.FileSystemStorage", "size": [125, 41]}
sorl-thumbnail||image||60f242173fd7fa005e108ffa7c0e4655	{"name": "cache/ab/db/abdb418650af005a3b95a284bae669b9.png", "storage": "django.core.files.storage.FileSystemStorage", "size": [125, 41]}
sorl-thumbnail||thumbnails||2fdbebb32561c82ff698ba05ac4b1cb9	["60f242173fd7fa005e108ffa7c0e4655", "f253a25daebe6483b75a613e1580f2fa"]
sorl-thumbnail||image||5ed5a86b09f3cb55a9f04c6d874f905e	{"name": "companies/15/da1cfdd8-22f.png", "storage": "django.core.files.storage.FileSystemStorage", "size": [184, 60]}
sorl-thumbnail||image||7264382b4d8a8db7813513335956cf94	{"name": "cache/55/fc/55fc4a9ce530adc005fc9b6c1e0aa639.jpg", "storage": "django.core.files.storage.FileSystemStorage", "size": [125, 41]}
sorl-thumbnail||image||6378f706507adec73e0571b65e13b62c	{"name": "cache/51/59/5159487760b07705fbca85f86978b835.png", "storage": "django.core.files.storage.FileSystemStorage", "size": [125, 41]}
sorl-thumbnail||thumbnails||e6d4ff19aa9706edb1c949a7e53f0488	["ced89a22f43b31058c54ecb4306deee8", "09ee0bdf5ffd7b472654f7262a8f8c81"]
sorl-thumbnail||image||4e037e9a7a372983d93b8f42d3f8d57e	{"name": "cache/ae/a6/aea60f91c326686dd16ed6521499cf54.png", "storage": "django.core.files.storage.FileSystemStorage", "size": [125, 41]}
sorl-thumbnail||thumbnails||5ed5a86b09f3cb55a9f04c6d874f905e	["6378f706507adec73e0571b65e13b62c", "4e037e9a7a372983d93b8f42d3f8d57e", "7264382b4d8a8db7813513335956cf94"]
sorl-thumbnail||image||b65880af05289598d3f92ce3743bd82d	{"name": "companies/11/09380789-c29.jpg", "storage": "django.core.files.storage.FileSystemStorage", "size": [4032, 3024]}
sorl-thumbnail||image||fad4df01ae88e07551c0c5830cf30935	{"name": "cache/be/cb/becb8bb5bb009908a269642cdefc30dd.png", "storage": "django.core.files.storage.FileSystemStorage", "size": [70, 94]}
sorl-thumbnail||image||e88bc8b02b489a7882c12d39c13e2b21	{"name": "companies/11/c311d41b-1c8.jpg", "storage": "django.core.files.storage.FileSystemStorage", "size": [4032, 3024]}
sorl-thumbnail||image||e59e0de5d5aea9ad0e8731d0cbe92123	{"name": "cache/26/1b/261b740678a278069a62b80a0f99cf08.png", "storage": "django.core.files.storage.FileSystemStorage", "size": [94, 125]}
sorl-thumbnail||thumbnails||e88bc8b02b489a7882c12d39c13e2b21	["e59e0de5d5aea9ad0e8731d0cbe92123"]
sorl-thumbnail||image||775c96dc9d96dea6ab2bbd97d9b65861	{"name": "cache/62/34/62349226cf269a267638fcd099d7082d.png", "storage": "django.core.files.storage.FileSystemStorage", "size": [94, 125]}
sorl-thumbnail||thumbnails||b65880af05289598d3f92ce3743bd82d	["fad4df01ae88e07551c0c5830cf30935", "775c96dc9d96dea6ab2bbd97d9b65861"]
sorl-thumbnail||image||e6d4ff19aa9706edb1c949a7e53f0488	{"name": "companies/20/783a80cf-8c5.jpg", "storage": "django.core.files.storage.FileSystemStorage", "size": [381, 384]}
sorl-thumbnail||image||ced89a22f43b31058c54ecb4306deee8	{"name": "cache/82/d3/82d3b6d1afdbe7be21154bf45508e08b.png", "storage": "django.core.files.storage.FileSystemStorage", "size": [125, 126]}
sorl-thumbnail||image||7334793a44f681ded268e83030bd4334	{"name": "companies/20/cf01a3a0-e1b.jpg", "storage": "django.core.files.storage.FileSystemStorage", "size": [600, 689]}
sorl-thumbnail||image||a1ea4e3deca30ea734feab2a8d94d022	{"name": "cache/c3/51/c3516f2cdec33641915a57447d73d72a.png", "storage": "django.core.files.storage.FileSystemStorage", "size": [109, 125]}
sorl-thumbnail||thumbnails||7334793a44f681ded268e83030bd4334	["a1ea4e3deca30ea734feab2a8d94d022"]
sorl-thumbnail||image||09ee0bdf5ffd7b472654f7262a8f8c81	{"name": "cache/0b/58/0b589f18068681c7931bf2dd73acc1dc.png", "storage": "django.core.files.storage.FileSystemStorage", "size": [124, 125]}
sorl-thumbnail||image||5e54bdf78bd6a5b52da0f6288456b69c	{"name": "companies/35/fe6049dd-5f7.jpg", "storage": "django.core.files.storage.FileSystemStorage", "size": [1439, 1443]}
sorl-thumbnail||image||16613952c73520aa471acae90518409a	{"name": "cache/1d/ae/1dae4028fefc7097ee16d6c80fb6ec44.png", "storage": "django.core.files.storage.FileSystemStorage", "size": [125, 125]}
sorl-thumbnail||image||595d8bf127af28c924f616a57da71b27	{"name": "companies/35/640a004d-593.jpg", "storage": "django.core.files.storage.FileSystemStorage", "size": [1440, 3040]}
sorl-thumbnail||image||14f3185a5cdf73a7211bd54f2fb33a92	{"name": "cache/8d/b3/8db310230a5251e81414dd4a1bd5989d.png", "storage": "django.core.files.storage.FileSystemStorage", "size": [59, 125]}
sorl-thumbnail||thumbnails||595d8bf127af28c924f616a57da71b27	["6402aec1fad7bd4b91e45840a8b12446", "14f3185a5cdf73a7211bd54f2fb33a92"]
sorl-thumbnail||image||08a80af2669efb6ed19ab53e40d6f064	{"name": "cache/af/a9/afa9cb69125899a478827d0f6cf3990c.png", "storage": "django.core.files.storage.FileSystemStorage", "size": [125, 125]}
sorl-thumbnail||thumbnails||5e54bdf78bd6a5b52da0f6288456b69c	["08a80af2669efb6ed19ab53e40d6f064", "16613952c73520aa471acae90518409a"]
sorl-thumbnail||image||f95ca58953f73864c64d641bacd54216	{"name": "companies/38/8c297df4-6b1.jpg", "storage": "django.core.files.storage.FileSystemStorage", "size": [960, 1280]}
sorl-thumbnail||image||4a5ab5fc1f17756aa44129ef9f70c386	{"name": "cache/31/0d/310d287faeb993ca3b26f417210a81e1.jpg", "storage": "django.core.files.storage.FileSystemStorage", "size": [94, 125]}
sorl-thumbnail||thumbnails||f95ca58953f73864c64d641bacd54216	["4a5ab5fc1f17756aa44129ef9f70c386"]
sorl-thumbnail||image||74b313e9c5684274e2e634fc10a6dcd4	{"name": "companies/36/730616ae-af0.jpg", "storage": "django.core.files.storage.FileSystemStorage", "size": [4032, 1908]}
sorl-thumbnail||image||97fdbcfc9fda124166681127dd74bdd4	{"name": "cache/ad/ad/adad630243faf4d3d1a811f7264ee490.jpg", "storage": "django.core.files.storage.FileSystemStorage", "size": [59, 125]}
sorl-thumbnail||thumbnails||74b313e9c5684274e2e634fc10a6dcd4	["97fdbcfc9fda124166681127dd74bdd4"]
sorl-thumbnail||image||133f8178fac635f7ab230ee50e9b6ba0	{"name": "companies/32/695b16cd-f43.jpg", "storage": "django.core.files.storage.FileSystemStorage", "size": [960, 1280]}
sorl-thumbnail||image||9bb661985e0bcb09e91828b82eaf8fd7	{"name": "cache/c2/f5/c2f5d0587e2028ef2b719ffe4e3e5f0c.jpg", "storage": "django.core.files.storage.FileSystemStorage", "size": [94, 125]}
sorl-thumbnail||thumbnails||133f8178fac635f7ab230ee50e9b6ba0	["9bb661985e0bcb09e91828b82eaf8fd7"]
sorl-thumbnail||image||f0afb6a75f593841b17ac169e3ffd99b	{"name": "companies/26/9598b7fa-23c.jpg", "storage": "django.core.files.storage.FileSystemStorage", "size": [960, 1280]}
sorl-thumbnail||image||eb2fd71e050b3b5022a480895c115ddb	{"name": "cache/74/33/74337e2da90a02c380794326328f404c.jpg", "storage": "django.core.files.storage.FileSystemStorage", "size": [94, 125]}
sorl-thumbnail||thumbnails||f0afb6a75f593841b17ac169e3ffd99b	["eb2fd71e050b3b5022a480895c115ddb"]
sorl-thumbnail||image||6402aec1fad7bd4b91e45840a8b12446	{"name": "cache/59/23/5923c134bcbc12e756e686588011d38d.jpg", "storage": "django.core.files.storage.FileSystemStorage", "size": [59, 125]}
sorl-thumbnail||image||7b35b522795ccd30667310b8131df3c5	{"name": "companies/15/89d06ead-fb4.jpg", "storage": "django.core.files.storage.FileSystemStorage", "size": [1080, 1920]}
sorl-thumbnail||image||3bd2b0b2ee440fb62b782f280922f7d1	{"name": "cache/5d/36/5d36b24d2cf2f682e023c212b15e6dec.png", "storage": "django.core.files.storage.FileSystemStorage", "size": [125, 222]}
sorl-thumbnail||image||84b9ae53c6bd1b9b64b865eba1a5d330	{"name": "cache/e3/af/e3afb0e92d95c5615939dbf2615e4521.png", "storage": "django.core.files.storage.FileSystemStorage", "size": [70, 125]}
sorl-thumbnail||thumbnails||7b35b522795ccd30667310b8131df3c5	["3bd2b0b2ee440fb62b782f280922f7d1", "84b9ae53c6bd1b9b64b865eba1a5d330"]
sorl-thumbnail||image||bb96b95925511242c9eb4db2c3b92ec4	{"name": "companies/15/630ed61b-7b7.jpg", "storage": "django.core.files.storage.FileSystemStorage", "size": [1440, 1920]}
sorl-thumbnail||image||6912e287fc5e5b3757dc0a9fdf74504e	{"name": "cache/63/e9/63e9eeedaf450ae4a5bca2d8e9c632d1.png", "storage": "django.core.files.storage.FileSystemStorage", "size": [125, 167]}
sorl-thumbnail||thumbnails||bb96b95925511242c9eb4db2c3b92ec4	["6912e287fc5e5b3757dc0a9fdf74504e"]
sorl-thumbnail||image||0c4bfe0bb41c3b59671e13dd15861fea	{"name": "companies/15/ae7afd5b-5b3.jpg", "storage": "django.core.files.storage.FileSystemStorage", "size": [1440, 1920]}
sorl-thumbnail||image||cf95242c41ada169a601e3474828b6db	{"name": "cache/90/41/90416f43a8f23852c63040b76debde8b.png", "storage": "django.core.files.storage.FileSystemStorage", "size": [94, 125]}
sorl-thumbnail||thumbnails||0c4bfe0bb41c3b59671e13dd15861fea	["cf95242c41ada169a601e3474828b6db"]
sorl-thumbnail||image||394e24ba32de4127089ef91829992c64	{"name": "companies/15/bd7d6c3c-140.jpg", "storage": "django.core.files.storage.FileSystemStorage", "size": [1440, 1920]}
sorl-thumbnail||image||efc458a6f7928548c5cc73f5753e2f46	{"name": "cache/51/94/51949cf62155646636dd09c5d78de9cf.png", "storage": "django.core.files.storage.FileSystemStorage", "size": [94, 125]}
sorl-thumbnail||image||3bb1d8d0c5d09ffe06055ccb26a442ca	{"name": "companies/15/4315eba5-138.jpg", "storage": "django.core.files.storage.FileSystemStorage", "size": [1440, 1920]}
sorl-thumbnail||image||047221ad4618fec21af9b95dc7c7d6b4	{"name": "cache/6b/d6/6bd6c281c7bdf1fab36834d049d90818.png", "storage": "django.core.files.storage.FileSystemStorage", "size": [94, 125]}
sorl-thumbnail||thumbnails||3bb1d8d0c5d09ffe06055ccb26a442ca	["047221ad4618fec21af9b95dc7c7d6b4"]
sorl-thumbnail||image||be8f89181d7963cabe368bc08d92b3b6	{"name": "cache/5c/2b/5c2bff0a2b3ce6c4843615a10eb331ce.png", "storage": "django.core.files.storage.FileSystemStorage", "size": [125, 167]}
sorl-thumbnail||thumbnails||394e24ba32de4127089ef91829992c64	["be8f89181d7963cabe368bc08d92b3b6", "efc458a6f7928548c5cc73f5753e2f46"]
\.


--
-- Data for Name: token_blacklist_blacklistedtoken; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.token_blacklist_blacklistedtoken (id, blacklisted_at, token_id) FROM stdin;
587	2021-02-02 09:28:12.88213+00	911
590	2021-02-09 09:48:12.136546+00	921
594	2021-02-11 06:25:21.374335+00	928
598	2021-02-15 06:09:03.697514+00	936
602	2021-02-15 07:13:32.967391+00	941
606	2021-02-15 08:04:17.352632+00	952
610	2021-02-15 08:24:06.876999+00	955
614	2021-02-15 09:26:29.426025+00	962
618	2021-02-16 03:24:54.497853+00	974
622	2021-02-16 04:16:27.088097+00	978
626	2021-02-20 08:46:19.518178+00	982
630	2021-02-22 08:24:39.013397+00	990
634	2021-02-23 06:38:46.840319+00	996
638	2021-02-24 06:11:29.498866+00	912
639	2021-02-24 06:11:29.501356+00	920
640	2021-02-24 06:11:29.504996+00	913
641	2021-02-24 06:11:29.508234+00	914
642	2021-02-24 06:11:29.511848+00	915
643	2021-02-24 06:11:29.514777+00	924
644	2021-02-24 06:11:29.517076+00	925
645	2021-02-24 06:11:29.519901+00	926
646	2021-02-24 06:11:29.523604+00	930
647	2021-02-24 06:11:29.526684+00	931
648	2021-02-24 06:11:29.529477+00	999
649	2021-02-24 06:11:29.531563+00	932
650	2021-02-24 06:11:29.533925+00	933
651	2021-02-24 06:11:29.53606+00	967
652	2021-02-24 06:11:29.538108+00	1001
653	2021-02-24 06:11:29.54145+00	968
654	2021-02-24 06:11:29.54366+00	1002
655	2021-02-24 06:11:29.547113+00	937
656	2021-02-24 06:11:29.552732+00	979
657	2021-02-24 06:11:29.554868+00	980
658	2021-02-24 06:11:29.557294+00	981
659	2021-02-24 06:11:29.560205+00	893
660	2021-02-24 06:11:29.563662+00	902
661	2021-02-24 06:11:29.565827+00	904
662	2021-02-24 06:11:29.569363+00	910
663	2021-02-24 06:11:29.571549+00	987
664	2021-02-24 08:23:34.785996+00	1004
668	2021-02-24 08:47:33.582341+00	1003
669	2021-02-24 08:47:33.588655+00	1008
673	2021-02-25 07:50:39.107453+00	1000
676	2021-03-04 07:24:24.328015+00	1016
588	2021-02-02 10:21:17.573974+00	908
591	2021-02-09 10:06:43.712505+00	923
595	2021-02-11 09:55:20.699615+00	929
599	2021-02-15 06:09:08.087375+00	938
603	2021-02-15 07:24:16.17668+00	943
607	2021-02-15 08:05:53.563603+00	953
611	2021-02-15 08:32:05.639567+00	958
615	2021-02-15 09:26:45.143395+00	963
619	2021-02-16 03:58:28.955611+00	964
623	2021-02-16 05:10:44.94146+00	972
627	2021-02-20 08:48:38.333164+00	975
665	2021-02-24 08:24:43.022752+00	1005
635	2021-02-23 07:17:46.903777+00	997
670	2021-02-24 08:51:08.495521+00	1009
674	2021-02-25 10:37:54.128573+00	1011
677	2021-03-05 02:32:34.053855+00	1022
589	2021-02-02 12:34:57.452781+00	909
666	2021-02-24 08:29:21.180494+00	1006
596	2021-02-13 03:48:17.294482+00	934
600	2021-02-15 07:00:19.77512+00	939
604	2021-02-15 07:35:26.512699+00	944
608	2021-02-15 08:10:18.594997+00	954
612	2021-02-15 08:55:22.860536+00	957
616	2021-02-15 16:27:56.438606+00	965
620	2021-02-16 03:59:07.657174+00	976
624	2021-02-18 08:54:54.089001+00	983
671	2021-02-24 10:36:46.283813+00	1010
632	2021-02-22 08:36:53.289622+00	993
636	2021-02-23 08:03:56.68383+00	991
675	2021-02-26 12:51:04.558108+00	1012
593	2021-02-11 05:10:12.029035+00	922
597	2021-02-14 05:34:59.584477+00	935
601	2021-02-15 07:03:28.978205+00	940
605	2021-02-15 07:54:18.530251+00	942
609	2021-02-15 08:20:00.832671+00	956
613	2021-02-15 09:14:04.816986+00	959
617	2021-02-16 03:14:52.476616+00	973
621	2021-02-16 04:16:12.864759+00	977
625	2021-02-19 08:55:43.940414+00	984
629	2021-02-22 03:54:07.146999+00	988
633	2021-02-23 06:32:30.157457+00	994
637	2021-02-24 02:43:34.004248+00	995
667	2021-02-24 08:30:12.294044+00	1007
672	2021-02-25 04:22:09.064482+00	998
579	2021-01-28 15:51:41.948429+00	895
581	2021-01-28 16:02:45.811231+00	897
582	2021-01-28 16:42:34.997197+00	896
583	2021-01-29 12:34:19.817786+00	894
584	2021-01-30 07:11:03.74062+00	899
585	2021-01-30 14:56:02.826762+00	901
586	2021-01-30 14:56:09.658464+00	905
\.


--
-- Data for Name: token_blacklist_outstandingtoken; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.token_blacklist_outstandingtoken (id, token, created_at, expires_at, user_id, jti) FROM stdin;
911	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxMjY3NDE3MiwianRpIjoiZTVjZWYyZTg4YTZlNDgyODg3YzllNTliMTNiNWQ3ODIiLCJ1c2VyX2lkIjoyNH0.hOShuoIoSL6z6ONwlz7GxgeqBazvpqO_IQjE3dCniIc	\N	2021-02-07 05:02:52+00	\N	e5cef2e88a6e482887c9e59b13b5d782
912	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxMjg2Mjg5MiwianRpIjoiMDMxN2EzNTk5MTBjNDU0OTk3ZDA1ZjA2N2UzNzczYmUiLCJ1c2VyX2lkIjoyNH0.z_U-dwmdBN9XWrJEsAP247KC7RFnNrCYZ-IKxgSJ9R4	2021-02-02 09:28:12.850845+00	2021-02-09 09:28:12+00	24	0317a359910c454997d05f067e3773be
920	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxMzQ0MTI5NCwianRpIjoiZGNhMzYxMzg2ODI0NDkwNjhlMjJlZjM3MTVjNzZlMTQiLCJ1c2VyX2lkIjoyNH0.o74cyOS_2NMRKRz2BzzI18KiJ6nFkPj48JOVFhXgHS4	2021-02-09 02:08:14.519707+00	2021-02-16 02:08:14+00	24	dca36138682449068e22ef3715c76e14
954	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxMzk4MTM1MywianRpIjoiNTAyODRjOTg4MDk2NGJhNWE2ZmQxZWJlZjExYmJjNzEiLCJ1c2VyX2lkIjoyNH0.YJz8abdlVIsrYhBTUDh0BgVOCSKeXaa9Yt_ABUJhXx0	2021-02-15 08:09:13.302021+00	2021-02-22 08:09:13+00	24	50284c9880964ba5a6fd1ebef11bbc71
988	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxNDQxNTcxOCwianRpIjoiZmQxY2QzNjY4Zjg4NGJiOGIxOWQ5NDhkMWNmOWZiYWEiLCJ1c2VyX2lkIjoyNH0.S_7flDilaEKlhAaUJ_2QtMztGL_0cpXwNsz1nddgy4s	2021-02-20 08:48:38.323999+00	2021-02-27 08:48:38+00	24	fd1cd3668f884bb8b19d948d1cf9fbaa
1021	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxNTM0NDAxMSwianRpIjoiYzkxMjIzNmQ1N2JmNGJiNThkOGQ5NDk5M2NiYTJkYzciLCJ1c2VyX2lkIjoyNH0.qNxckHQa2qQ44_422-dgoaXj01BY487X9tysAucjn5s	2021-03-03 02:40:11.987736+00	2021-03-10 02:40:11+00	24	c912236d57bf4bb58d8d94993cba2dc7
913	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxMjg2MzA2NSwianRpIjoiYmY4MzAxNWM1MmI3NDQyNDhkMWUwNDRhZmVmMmRmMzMiLCJ1c2VyX2lkIjoyNH0.WMgYFB5jbC_Q_rkjuj5EBrVa1cIShsHMdBQPOsVy5eM	2021-02-02 09:31:05.834995+00	2021-02-09 09:31:05+00	24	bf83015c52b744248d1e044afef2df33
921	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxMzQ2MDEzNSwianRpIjoiNDc0ZjgyN2Q2OTJhNDIzNTllMzUzMzQ2ZjhlYTNmMzgiLCJ1c2VyX2lkIjoyNH0.eaPlz1TlbqHzVIaNoECFuR-rxx7BdgWtFMF2dCVtskQ	2021-02-09 07:22:15.336535+00	2021-02-16 07:22:15+00	24	474f827d692a42359e353346f8ea3f38
955	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxMzk4MTQyNywianRpIjoiODliMzMxYTUxMGQxNDJkYThlMDg4MzFmYzYxMzc4ZGEiLCJ1c2VyX2lkIjo2N30.0hCLrfrCNfNMNrssCaHjhXKpRsGmvRcHwYXEeORYGiI	2021-02-15 08:10:27.064369+00	2021-02-22 08:10:27+00	67	89b331a510d142da8e08831fc61378da
1022	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxNTQyOTcyMywianRpIjoiZTRkMGZlZDU5MGY5NDk2YTk4MDhkMTlhNzA5ZWJkMmIiLCJ1c2VyX2lkIjoyNH0.gjUFVrxcjfbzJ4hsIhmkBbSHUV0Kq9p0sgaQEtM5Lic	2021-03-04 02:28:43.916053+00	2021-03-11 02:28:43+00	24	e4d0fed590f9496a9808d19a709ebd2b
914	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxMjg2NjA3NywianRpIjoiM2Q5Y2RkOWQzOTMzNDk0NDhlODY3MzA5NGEzYzhjOTIiLCJ1c2VyX2lkIjoyNH0.Tqa3WdUGgG0gai3FN4tXwkPyP69I59Lc-uCoWdFATVQ	2021-02-02 10:21:17.563988+00	2021-02-09 10:21:17+00	24	3d9cdd9d393349448e8673094a3c8c92
922	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxMzQ2MDMxOCwianRpIjoiMDc0ZWIwYmU2MzQxNGQ4M2JhMzM3Y2Q5YjdmOTI1NTUiLCJ1c2VyX2lkIjoyNH0.qR1YGxhRtiqX_oz1dJBenvQScvfMeA_X9pIIvIQdQxM	2021-02-09 07:25:18.176414+00	2021-02-16 07:25:18+00	24	074eb0be63414d83ba337cd9b7f92555
956	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxMzk4MTQzOCwianRpIjoiNGQ1MjMzNTQxNThkNDIwOGE5MzM1YmZjNDEzNDVhMWUiLCJ1c2VyX2lkIjoyNH0.EEpEtcZtVyyD0Ad9eiSZPdDblrE87NoCF8iz5_dmRio	2021-02-15 08:10:38.677139+00	2021-02-22 08:10:38+00	24	4d523354158d4208a9335bfc41345a1e
990	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxNDU2MzA2NSwianRpIjoiOTQzMzc2NzkzODc3NGRmOWI0N2EzMzM5M2Q1MjU5MDMiLCJ1c2VyX2lkIjoyM30.4b3lqnQ_bE8VgP6tvtgRvN5t_pM5Njg2my-weGBUpNU	2021-02-22 01:44:25.266591+00	2021-03-01 01:44:25+00	23	9433767938774df9b47a33393d525903
1023	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxNTQ0NzQ2NCwianRpIjoiMWU4NDU4ZWJkNDg5NDhiYmIxOGY0MjE5MWY0MzY3YjciLCJ1c2VyX2lkIjoyNH0.d71Rtdls4r-G17TrbEdG3cIGyAeqxPjIMAaPEPabn2o	2021-03-04 07:24:24.310838+00	2021-03-11 07:24:24+00	24	1e8458ebd48948bbb18f42191f4367b7
915	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxMjg3NDA5NywianRpIjoiMTkxNDUxZDczZDg5NGY3OWI2NWFhYWU1MTVkYzUwZGUiLCJ1c2VyX2lkIjoyNH0.LT6nbbZGxkPQBgqr-0cPOI51441ypgDZ4VcXDeoB-7Q	2021-02-02 12:34:57.445515+00	2021-02-09 12:34:57+00	24	191451d73d894f79b65aaae515dc50de
923	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxMzQ2ODkwMiwianRpIjoiYzAyOGU5NzljOGEwNGUyMThiYTQ5NGYzZDYyYmIxYTYiLCJ1c2VyX2lkIjo1OX0.6OC349LqtHKAKpxdtAWQrrHM5BoxENQRlEeWJIuzgo0	2021-02-09 09:48:22.366816+00	2021-02-16 09:48:22+00	59	c028e979c8a04e218ba494f3d62bb1a6
957	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxMzk4MjAxMSwianRpIjoiNmM1MGY5MTEyYjM2NDdmYWJjNWQwZTc4NDk4ZDdlZTQiLCJ1c2VyX2lkIjo2N30.xPSVvMy6pEwJbpc303jmCCSJFlpICujpjzyJV20bp4E	2021-02-15 08:20:11.233829+00	2021-02-22 08:20:11+00	67	6c50f9112b3647fabc5d0e78498d7ee4
991	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxNDU3MDg0NywianRpIjoiM2RmZjE5YjZkYzljNDAzZWI3YTg2MmI5MzVmZmU0MDYiLCJ1c2VyX2lkIjoyNH0.FRaZ3n-xWdm2SXs-hkGHFCClSGfSbTlwLAlMaAVII-Q	2021-02-22 03:54:07.139708+00	2021-03-01 03:54:07+00	24	3dff19b6dc9c403eb7a862b935ffe406
1024	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxNTQ1NTg2NCwianRpIjoiY2M1ZGNkNzhhZTNhNDdlYzkyMDE1OWM3YzYxYjliOWQiLCJ1c2VyX2lkIjoyOH0.VnbJECoPicHLCYfV9jzLcnkdBdwTmoY36TXLQ9JW_og	2021-03-04 09:44:24.46128+00	2021-03-11 09:44:24+00	28	cc5dcd78ae3a47ec920159c7c61b9b9d
916	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxMjkxODUxNCwianRpIjoiYzY3NjhmYTRhYmI5NDVlMDk5OGI2MTUwMzkzMjNkZjgiLCJ1c2VyX2lkIjoyM30.bvrI1OOVV5kllDTdeKvD03CWbH6z7uG74OKVTojo2ho	2021-02-03 00:55:14.674242+00	2021-02-10 00:55:14+00	23	c6768fa4abb945e0998b615039323df8
924	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxMzQ3MDAxNCwianRpIjoiYjNiMTFiMGY3OGQzNDg4ZGE1MDk3OGZhOGRhZmM5ZWUiLCJ1c2VyX2lkIjoyNH0.Mm7BnTknscWKfAxI3zfM9Wxy2dqtd4D2QkhWP9a9DXM	2021-02-09 10:06:54.112912+00	2021-02-16 10:06:54+00	24	b3b11b0f78d3488da50978fa8dafc9ee
958	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxMzk4MjI1NSwianRpIjoiYmY3MTMzN2FhZGY1NGY2Zjg0MzdjMmJiODRlODExMjkiLCJ1c2VyX2lkIjo2N30.7wobrwR6LgzRRFH9R6Pg5ESqlnvPpxGk01ZyIR41AWw	2021-02-15 08:24:15.063339+00	2021-02-22 08:24:15+00	67	bf71337aadf54f6f8437c2bb84e81129
1025	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxNTQ1ODc4NCwianRpIjoiMzU0NjJlY2U4MmZmNDQ0Yjk5NjFiMzkwMWQ5YzAxMDAiLCJ1c2VyX2lkIjoyNH0.ZKtViEQZhdIBCgpLGXV7U1vT_-OKVIMY9lhfXfoNgw0	2021-03-04 10:33:04.333664+00	2021-03-11 10:33:04+00	24	35462ece82ff444b9961b3901d9c0100
917	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxMjkyNjQxMywianRpIjoiNjc2Yjk3ODdjYjIyNGFmMDgwYTNhOWRhMGI5YjVjOTAiLCJ1c2VyX2lkIjoyM30.yjrfnAz6394CCS5ky5g5FG5cWh4EDceX5EsrqqgTD14	2021-02-03 03:06:53.654966+00	2021-02-10 03:06:53+00	23	676b9787cb224af080a3a9da0b9b5c90
925	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxMzQ3MDg0OSwianRpIjoiYWJhNTkzODg2Y2JhNDRhYWFlMzQ3ZjRjMDA2NjY2NTciLCJ1c2VyX2lkIjoyNH0.Da1cQoEm9dVMvWRj45OXRxJgZbN2NjOVIw2xUcEg8Pg	2021-02-09 10:20:49.046438+00	2021-02-16 10:20:49+00	24	aba593886cba44aaae347f4c00666657
959	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxMzk4MjczNCwianRpIjoiNzAwMzUyZGIwZGMyNDRhM2JjOGRjZDY3MTNhMmE2MzQiLCJ1c2VyX2lkIjoyNH0.ouAxDt8jY3ADjyTL1RXlegipwO6M_N48ZkKB879UEZw	2021-02-15 08:32:14.575694+00	2021-02-22 08:32:14+00	24	700352db0dc244a3bc8dcd6713a2a634
993	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxNDU4NzEyOCwianRpIjoiYzBmMjU1M2YzNTEyNDZkZWEyYjZiZWJhZjVlMjc4ZDEiLCJ1c2VyX2lkIjoyM30.X_ak4SIznQ1ZMOHwJIOmJxloVoqLVrYBtvgKB4yJT8I	2021-02-22 08:25:28.185907+00	2021-03-01 08:25:28+00	23	c0f2553f351246dea2b6bebaf5e278d1
1026	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxNTQ1OTU0NCwianRpIjoiZWVmYThlNTU2YTQ1NDhiY2JiODY2NTRhZTcxN2Y1NTEiLCJ1c2VyX2lkIjo0M30.LDkkoy47-RWvHVqOAlngAjLG1JGVzZNqLQxZ4vPPv7A	2021-03-04 10:45:44.332104+00	2021-03-11 10:45:44+00	43	eefa8e556a4548bcbb86654ae717f551
918	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxMjk0OTAwMywianRpIjoiZjZlM2FjMzZjNjIwNGJmZDhjMGJmYmYyMDMzNGNkNTMiLCJ1c2VyX2lkIjoyM30.l5K3o3fkYuMwaJOLKpK8OhuYtL9MEEqC9smXbOGbzF4	2021-02-03 09:23:23.511455+00	2021-02-10 09:23:23+00	23	f6e3ac36c6204bfd8c0bfbf20334cd53
926	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxMzUzMDQ3MywianRpIjoiZjI3MTQzM2Q1Nzk0NDE2Y2E4MGRiN2UwZWQ4ODdjOWQiLCJ1c2VyX2lkIjoyNH0.eBikIAUCn2tzHWqTwqWeXMQztCWhenB2hjad1VGoqQ8	2021-02-10 02:54:33.863993+00	2021-02-17 02:54:33+00	24	f271433d5794416ca80db7e0ed887c9d
994	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxNDU4NzgzMSwianRpIjoiYjMwYjljMDE3ZjQ3NDk3YjkzYWU0MmVmNGRlYTk1MWMiLCJ1c2VyX2lkIjoyM30.vapUPKEmA7KaPD5pKvcSoDrDNCOXriy1jp-wud-SpU4	2021-02-22 08:37:11.651639+00	2021-03-01 08:37:11+00	23	b30b9c017f47497b93ae42ef4dea951c
1027	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxNTUxNjM1NCwianRpIjoiN2E1OTZhYjAwODJiNGJmZmJiZjk3NGFkYTcwOTIzNzAiLCJ1c2VyX2lkIjoyNH0.uoXNb25z4dwY04P2QHLSugSpbsrdsYujVZfhLy-GyNI	2021-03-05 02:32:34.043085+00	2021-03-12 02:32:34+00	24	7a596ab0082b4bffbbf974ada7092370
919	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxMzAxNjEzNSwianRpIjoiZTM4MzRiOGM5OWQyNDU0NTlmNjFkM2JhOGEyNTg0MTciLCJ1c2VyX2lkIjoyM30.jNy-ZczQAsy6ZSKeE__79VpP0ggCJKVPUk8HG91_Oa0	2021-02-04 04:02:15.760075+00	2021-02-11 04:02:15+00	23	e3834b8c99d245459f61d3ba8a258417
995	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxNDYwMDE1NiwianRpIjoiMzYyM2MyYzAzMDE0NDU2ZWI4ZDI2YmJhMmMxOTY2NTkiLCJ1c2VyX2lkIjoyOH0.bv4TIGMD5H-E5Og2WPrN80zYgegtwUB0fDEpZEEeho0	2021-02-22 12:02:36.444013+00	2021-03-01 12:02:36+00	28	3623c2c03014456eb8d26bba2c196659
928	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxMzUzOTc0MywianRpIjoiNWVjMWE4MzAwMmY1NDhmMmExNmU0YzAwMWM3MTkwZGIiLCJ1c2VyX2lkIjoyNH0.cmgERihG_fs0LVLZbXETvIUY-CGA6Oe6C0EoaIg_z5Y	2021-02-10 05:29:03.969698+00	2021-02-17 05:29:03+00	24	5ec1a83002f548f2a16e4c001c7190db
962	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxMzk4NTk3NSwianRpIjoiNTE3NmY0NmM0YTUyNGQ4ZWE3MDY1NmQ1NzQ4ZmE3NTMiLCJ1c2VyX2lkIjo2N30.nMnYXOBQ63S83sE8zX9-uqJ4wLxI6CXiu-wsJ5BfG8E	2021-02-15 09:26:15.741031+00	2021-02-22 09:26:15+00	67	5176f46c4a524d8ea70656d5748fa753
996	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxNDY2Njc4NywianRpIjoiNDE2YTgyYjYzMmZlNDVlYzlkYzU5MzNmYzk4YTAzOGEiLCJ1c2VyX2lkIjoyM30.o7hCE_vr65RZW6PiXC4jajcQKzRXxwGLKP_kxudtkiU	2021-02-23 06:33:07.926965+00	2021-03-02 06:33:07+00	23	416a82b632fe45ec9dc5933fc98a038a
929	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxMzU0OTY5MywianRpIjoiZjVkZDMxZTNmNjFhNDA0ZDhhODNiZDM3OGJiOGY2OWUiLCJ1c2VyX2lkIjoyNH0.yBGy9fXBXHP8345HzVQTXfiZ_73yPOzyeoyeGJwsF2Y	2021-02-10 08:14:53.872509+00	2021-02-17 08:14:53+00	24	f5dd31e3f61a404d8a83bd378bb8f69e
963	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxMzk4NjAwMCwianRpIjoiNDEwYjVhNmQ4NmU1NDUzMmIwYzc3Y2ExN2E0MTMwNWQiLCJ1c2VyX2lkIjo3MH0.NRweAqTGYOOIqHpgRhww47MC9-tVEA0qS0RShI3f6yk	2021-02-15 09:26:40.486842+00	2021-02-22 09:26:40+00	70	410b5a6d86e54532b0c77ca17a41305d
997	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxNDY2NzE0OCwianRpIjoiYmEzYmEwZTlhMDY4NDhkMjllOWE2YmY2ODlkNzhlYjMiLCJ1c2VyX2lkIjo3NX0.YvxPHYixB6DOiT9BGmW8A-bOPkiEDPNu-fO9YthpWc4	2021-02-23 06:39:08.279731+00	2021-03-02 06:39:08+00	75	ba3ba0e9a06848d29e9a6bf689d78eb3
930	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxMzU1NDk1MiwianRpIjoiOTBjYTZiZDkwYTMxNGY2N2EyZjA3MmI3NWFlN2JkOTQiLCJ1c2VyX2lkIjoyNH0.6qUiqioToUK0RsFYCvQLKMZ70CAV82vhUl3BxvLzZW8	2021-02-10 09:42:32.165433+00	2021-02-17 09:42:32+00	24	90ca6bd90a314f67a2f072b75ae7bd94
964	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxMzk4NzUwNCwianRpIjoiYjA2ZDRlN2Y0OGQ4NDFiNGI3ZjRmZTZmYjIyZDhlMmIiLCJ1c2VyX2lkIjoyNH0.2Er99RpD8p3jWeT4m_sxUsBCDsu903q2cWuJfTv5vXk	2021-02-15 09:51:44.044836+00	2021-02-22 09:51:44+00	24	b06d4e7f48d841b4b7f4fe6fb22d8e2b
998	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxNDY2OTQ3NiwianRpIjoiOTgyNDUxYzA0NTg1NDk3ODg5MzIyODI0NjZiMjAzZmQiLCJ1c2VyX2lkIjoyM30.xKcyz7T58WSuI0w6-cBWZn5p93HQeHGV-Y5B4lGZ314	2021-02-23 07:17:56.871917+00	2021-03-02 07:17:56+00	23	982451c0458549788932282466b203fd
931	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxMzYxNjkwOCwianRpIjoiZDNmMzIxMDE5MzIyNGU1NGE4NTI5ZGM1N2E0NTVjY2YiLCJ1c2VyX2lkIjoyNH0.SE6w8VD_ZbKOL78-ksMm4AKp3O9tmNYevxNKZJBB2qE	2021-02-11 02:55:08.960338+00	2021-02-18 02:55:08+00	24	d3f3210193224e54a8529dc57a455ccf
965	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxMzk4NzYyMiwianRpIjoiOTRlOTJlYjNlYjQxNDJhZGEzMTY3YTEwY2FlMjUyNjMiLCJ1c2VyX2lkIjoyNH0.t8LBsUH-UIDdZ4ALMEaluYg4URBLWXqu9xF1V5mj9Hk	2021-02-15 09:53:42.199752+00	2021-02-22 09:53:42+00	24	94e92eb3eb4142ada3167a10cae25263
999	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxNDY3MjIzNiwianRpIjoiNTI4NTg5NjM1ZWIwNDg5Yzg2YzEwYzQ3N2RmZDZkYzgiLCJ1c2VyX2lkIjoyNH0.hpDt8GkPHRccH_WU0Gt1CQKn7KHmvGvzF8IZxrtYo-Q	2021-02-23 08:03:56.676614+00	2021-03-02 08:03:56+00	24	528589635eb0489c86c10c477dfd6dc8
932	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxMzYyNTAxMiwianRpIjoiNGIwYmRhZjU5ZDRhNDRjY2I5ZTliODA0ZTdkODRkYWYiLCJ1c2VyX2lkIjoyNH0.fe_EmSgE2iQObDcOGQxFmOU_CLAtlJPQzDPRsNX7IXs	2021-02-11 05:10:12.013009+00	2021-02-18 05:10:12+00	24	4b0bdaf59d4a44ccb9e9b804e7d84daf
966	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxMzk5MTQyOCwianRpIjoiZjExMjhhZjFlMDU2NDEzYzhiNGM2MjVmNTZlMmUwNDIiLCJ1c2VyX2lkIjoyOH0.OZf1GT0cG-SqFZ_GNTDrPE0NttrJWdGWTwZWpTGZMeE	2021-02-15 10:57:08.89718+00	2021-02-22 10:57:08+00	28	f1128af1e056413c8b4c625f56e2e042
1000	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxNDczOTQxMywianRpIjoiNDIxYzBmMDAwOTY5NDgxOGE0MTc5NDZmNDMzZDAwMWEiLCJ1c2VyX2lkIjoyOH0.BqFWrU2-U64MYhlWsH5iMTfYW4s_mx-Au0kof5Lqve0	2021-02-24 02:43:33.996715+00	2021-03-03 02:43:33+00	28	421c0f0009694818a417946f433d001a
933	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxMzYyOTUyMSwianRpIjoiNzY5NzFhYTNhYzE1NDlhZWFkNjdiNGViMGNkMWI1ZWEiLCJ1c2VyX2lkIjoyNH0.P1QffetgKaNNJ7b_wNwNJC8XTSr-pj8RlujqysMeBfc	2021-02-11 06:25:21.366832+00	2021-02-18 06:25:21+00	24	76971aa3ac1549aead67b4eb0cd1b5ea
967	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxMzk5Nzg5MywianRpIjoiODBhZWM5ZjEwYzJjNDg3YzhmZWI5OGU4YWMxM2I1NmMiLCJ1c2VyX2lkIjoyNH0.hIsM5p_6MTDO01SEaEvcprDkP_l2jkXQM16Xz8hd7lk	2021-02-15 12:44:53.260227+00	2021-02-22 12:44:53+00	24	80aec9f10c2c487c8feb98e8ac13b56c
1001	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxNDc0NTEwNywianRpIjoiMDA2YjU2ZTUzODA3NGExNGEwNDE0MjgwZmY3NDViNDciLCJ1c2VyX2lkIjoyNH0.Ym1_1twj_sU1DfT0cuYLtONHis2ejg9qyV2e3Q3VxOY	2021-02-24 04:18:27.584352+00	2021-03-03 04:18:27+00	24	006b56e538074a14a0414280ff745b47
934	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxMzY0MjEyMCwianRpIjoiYzQwMTZiODY2YTBiNDUxMGIyYThkZjE2NmFhMDgwMmEiLCJ1c2VyX2lkIjoyNH0.pla7ibyeORaCv6rnKxz2BgsO97Zx_BKxLmgvuJe1NC0	2021-02-11 09:55:20.68848+00	2021-02-18 09:55:20+00	24	c4016b866a0b4510b2a8df166aa0802a
968	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxNDAxMTMwNywianRpIjoiNmVjOGM4YmViNzI3NDBjNDk0MjgyNTA5YjVmNDc2YTkiLCJ1c2VyX2lkIjoyNH0.3F6ecwQ8ma35Iva76dxiySiuc6ndBTmPNZXQg5cLZWM	2021-02-15 16:28:27.445926+00	2021-02-22 16:28:27+00	24	6ec8c8beb72740c494282509b5f476a9
1002	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxNDc0NjQxMSwianRpIjoiZTNmOTRmMjE4MjJlNDEyYjg4MThjZjAyZjZhNTQ2NTMiLCJ1c2VyX2lkIjoyNH0.R80J34nvnyRUfb0D03WjDFD94ZkA7XZt7G28VlTIz3I	2021-02-24 04:40:11.355783+00	2021-03-03 04:40:11+00	24	e3f94f21822e412b8818cf02f6a54653
935	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxMzc5Mjg5NywianRpIjoiY2YzYmUyZWRjYWZlNDI1NzgzNzZlNmJkODY3NjQwNWYiLCJ1c2VyX2lkIjoyNH0.CQKP0WvdpNMXI9CgKRbpW8twNYEQNnBOEt2BEKMCH-g	2021-02-13 03:48:17.286138+00	2021-02-20 03:48:17+00	24	cf3be2edcafe42578376e6bd8676405f
969	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxNDAxNjAyOCwianRpIjoiMWM1MDgyNDIyYjUwNDNmMzg1ZDFkY2RjMTEzMTc5OTAiLCJ1c2VyX2lkIjo0M30.xD8Nv5HUIicRSwaFL-ctgOU6v8vMPsAfGCW4oSszGDI	2021-02-15 17:47:08.637658+00	2021-02-22 17:47:08+00	43	1c5082422b5043f385d1dcdc11317990
1003	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxNDc1MjA4MywianRpIjoiYTk0MTExNmQ3YjY0NDJmNGIyZTJiYjU2NWQ5MTgxMmEiLCJ1c2VyX2lkIjoyNH0.uH6erf0s9PyIwkUKBhX2HOtTubdrbvO8mGsNOWjEkQ8	2021-02-24 06:14:43.406915+00	2021-03-03 06:14:43+00	24	a941116d7b6442f4b2e2bb565d91812a
936	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxMzg4NTY5OSwianRpIjoiYWY5ZjE1NGQzN2NjNDZlMDk2YTJkNjBjMWQxNGUxNzQiLCJ1c2VyX2lkIjoyNH0.KroFGrgjAiQa-PR9X45wRtuIR5fvKkLO4aWtZEuMl_Q	2021-02-14 05:34:59.576494+00	2021-02-21 05:34:59+00	24	af9f154d37cc46e096a2d60c1d14e174
970	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxNDA0NjM3NSwianRpIjoiYmUyOTM5Y2E3M2Y2NDM4ZmFmMzM3MDk3YzUwZDIyOWEiLCJ1c2VyX2lkIjoyOH0.tez49zPzOOxtTAojO24aJaGcXGX3e5uZzv2_ogNTKgE	2021-02-16 02:12:55.364159+00	2021-02-23 02:12:55+00	28	be2939ca73f6438faf337097c50d229a
1004	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxNDc1OTU2NSwianRpIjoiZmVlZjJiOGM5MjM5NDQ2ZGEwZDcyZWE0ODA5MGZlZGYiLCJ1c2VyX2lkIjoyNH0.brWe80xk7E7oi0E_9fS40ZxthIQalUd-IhNkuvd-pCU	2021-02-24 08:19:25.99258+00	2021-03-03 08:19:25+00	24	feef2b8c9239446da0d72ea48090fedf
937	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxMzkwMjE5NiwianRpIjoiOTBmNDNhNDJjNjVmNGMxMjg4OGY5NjhiNmE0ZmRhODAiLCJ1c2VyX2lkIjoyNH0.DDWTqLGnuiBugCNRkBSr--UFQGRXtWC6OErGJv8YjzM	2021-02-14 10:09:56.13209+00	2021-02-21 10:09:56+00	24	90f43a42c65f4c12888f968b6a4fda80
971	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxNDA0NjUzMywianRpIjoiOWVkMTQ1MGFkYjdkNDMxZjg4Nzc0MzA3OWZiZGEyNDciLCJ1c2VyX2lkIjo0M30.iMynedx2jE-0xq8BJuE8OIHmok69cryNhIJgMQipTpA	2021-02-16 02:15:33.597163+00	2021-02-23 02:15:33+00	43	9ed1450adb7d431f887743079fbda247
1005	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxNDc1OTgyNCwianRpIjoiZTAwZjMxMWFjNzY1NDA4OGI4Yjg4MjA0MWM4ZWE2NTIiLCJ1c2VyX2lkIjo3MH0.crzP7Hd2XDbP9bevU3XePHUw9xB0ewwu0ir6mpYqoF0	2021-02-24 08:23:44.799498+00	2021-03-03 08:23:44+00	70	e00f311ac7654088b8b882041c8ea652
938	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxMzk3NDE0MywianRpIjoiM2E1ODk0NTkxM2YyNDQzMThjNzkzMzEyYzg0YzJmMTMiLCJ1c2VyX2lkIjoyNH0.9rs9OBFjlY287fO0BGO5PzZyH32zSYIoRy9j0iLxONk	2021-02-15 06:09:03.674911+00	2021-02-22 06:09:03+00	24	3a58945913f244318c793312c84c2f13
972	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxNDA0NzE3MywianRpIjoiY2RhMDMyNGE0ZmZhNGY2MGE2MDg3YTAwYmFlNWI3ODQiLCJ1c2VyX2lkIjo0M30.kVLqTpBsVfNdu33QxiT8LQAW82BLERDSwCOySUquw6o	2021-02-16 02:26:13.768312+00	2021-02-23 02:26:13+00	43	cda0324a4ffa4f60a6087a00bae5b784
1006	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxNDc1OTkxMywianRpIjoiODExNDcyZjMwMTk3NDFhNmJjMDkzZDI0ZmZjYTgwZTAiLCJ1c2VyX2lkIjo3MH0.4u2HlzmSXy5gJlea-r1Akvr-jPO8u8t9DFq0XeWoQtc	2021-02-24 08:25:13.994437+00	2021-03-03 08:25:13+00	70	811472f3019741a6bc093d24ffca80e0
939	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxMzk3NDE1OCwianRpIjoiZDc2NTQ0NGI4MDNlNGY0OGI2NjhlMzRhZGNlNjFiZjciLCJ1c2VyX2lkIjo2N30.88Zs4i1Gge34t3mvFsXjkzzd2-E1BlG-Op0MYF_kS58	2021-02-15 06:09:18.465758+00	2021-02-22 06:09:18+00	67	d765444b803e4f48b668e34adce61bf7
973	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxNDA0ODA0NiwianRpIjoiMzhlM2I5ZmMzYzBhNDA4OGE5NGY1YjMwMzFmMzY2NjYiLCJ1c2VyX2lkIjo0M30.DRrWoe8JcY-XXTG_RgQijZ_BmnAjzz40tS-E6kFDINo	2021-02-16 02:40:46.088671+00	2021-02-23 02:40:46+00	43	38e3b9fc3c0a4088a94f5b3031f36666
1007	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxNDc2MDE3MSwianRpIjoiOWM5YWZjYTk2ZGY1NGMzODg5N2IxNDk3MDQ4Y2MxNWQiLCJ1c2VyX2lkIjo3Nn0.d-9rzSivh8AmyugHDL771AyamjXVbs_yH6RTt9sYi6I	2021-02-24 08:29:31.539501+00	2021-03-03 08:29:31+00	76	9c9afca96df54c38897b1497048cc15d
940	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxMzk3NzIyOSwianRpIjoiODU0MDIzYzA1ZjM0NDI4NGE3ZWU1NTUxNTRjNGViOTQiLCJ1c2VyX2lkIjo2N30.5BJ3dTCjk9kUZa7ck2ut5bMn0eoxXNKXHjmLxJtJito	2021-02-15 07:00:29.472415+00	2021-02-22 07:00:29+00	67	854023c05f344284a7ee555154c4eb94
974	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxNDA1MDEwMSwianRpIjoiYTllYmEyMTI4NmJiNGY4M2I0OWY4OTg5YThjNDViMDciLCJ1c2VyX2lkIjoyNH0.msB69D9ewzYZ0ckCd1aoeeSib6GVKnFZCFSEIlm4Xfw	2021-02-16 03:15:01.3798+00	2021-02-23 03:15:01+00	24	a9eba21286bb4f83b49f8989a8c45b07
1008	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxNDc2MDIyMiwianRpIjoiNjQ3MjE3MDkwNTEzNGNjZjljZDRkMWUzMDZiN2JhMmEiLCJ1c2VyX2lkIjoyNH0.bvTJ59RsUK5cTyeQXTmNbemGOEyOD0H5GSktMdWmS0M	2021-02-24 08:30:22.041358+00	2021-03-03 08:30:22+00	24	6472170905134ccf9cd4d1e306b7ba2a
941	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxMzk3NzQxOCwianRpIjoiNmEzYzhmMDEzNzhhNGUwOWE0MjE0M2Y1YmEwYzMzN2IiLCJ1c2VyX2lkIjoyNH0.tNdYCfd83A7-hfHWuiWnyU74YhjCjKJFngAYYTfPLyA	2021-02-15 07:03:38.046209+00	2021-02-22 07:03:38+00	24	6a3c8f01378a4e09a42143f5ba0c337b
975	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxNDA1MDk5MSwianRpIjoiODM1MDkwZTI2MmUwNDlkMGJmNWU4YzY5MmY3M2YwMzUiLCJ1c2VyX2lkIjoyNH0._G6WSDd6utGJGxZBAZD9tvvbr3NHUbD9nBBytI7HdPQ	2021-02-16 03:29:51.481958+00	2021-02-23 03:29:51+00	24	835090e262e049d0bf5e8c692f73f035
1009	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxNDc2MTQ0NCwianRpIjoiYjVlYzZmZTFkODYzNGE0MjgyZTgwMmM4MjA5MDEwNTkiLCJ1c2VyX2lkIjoyNH0.bfmLE_ZflpiWIt1ywRzxDivONC2qgY00uxL-z69aeng	2021-02-24 08:50:44.952408+00	2021-03-03 08:50:44+00	24	b5ec6fe1d8634a4282e802c820901059
942	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxMzk3NzcwOSwianRpIjoiNWU3ZWY2MmE4YjkwNDJhZDg3ODBkYjNlZWViZTI0ODMiLCJ1c2VyX2lkIjoyNH0.s2Y43onGOY6CdIqNhPUw3ZZsfuyuN5kZxHDDRPY1POU	2021-02-15 07:08:29.201194+00	2021-02-22 07:08:29+00	24	5e7ef62a8b9042ad8780db3eeebe2483
976	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxNDA1MjcyMiwianRpIjoiYzg4NGY0Y2Q3NzIxNGMxMDg1MWMwZjUwZDMwOGM4MWYiLCJ1c2VyX2lkIjo3MX0.2U5EN3SUgaKCej3b0WetqOTcy28D2NiIuINUaDRE0yI	2021-02-16 03:58:42.324724+00	2021-02-23 03:58:42+00	71	c884f4cd77214c10851c0f50d308c81f
1010	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxNDc2MjU2NiwianRpIjoiOGVmNTE0MmUzOTBlNDEyYTlmYzQ0YWFjMmI3NjA4NWQiLCJ1c2VyX2lkIjoyNH0.EwTdTPQloQ6X_4Rq-x49BCL3JEmk9yNK3sA62whfngc	2021-02-24 09:09:26.211874+00	2021-03-03 09:09:26+00	24	8ef5142e390e412a9fc44aac2b76085d
943	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxMzk3ODAyNCwianRpIjoiMDc1NTI4YThmZDMwNDdlOWEzYjljOWYyZDc2OTMxNDEiLCJ1c2VyX2lkIjo2N30.uasC1D5PWpEBUlyF9rk493qynJS1A-LPtIOUzcdD02c	2021-02-15 07:13:44.192487+00	2021-02-22 07:13:44+00	67	075528a8fd3047e9a3b9c9f2d7693141
977	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxNDA1Mjc3NiwianRpIjoiNzNhOTY3ODhkOTBmNDA4Yjk3MjM4OTU0ZTkxNzNlNjAiLCJ1c2VyX2lkIjo0M30.oWgT8yg8d6mo6vM0yp0p4JBIwB4ejDuDtig9rTsnXgY	2021-02-16 03:59:36.824375+00	2021-02-23 03:59:36+00	43	73a96788d90f408b97238954e9173e60
1011	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxNDc2Nzg0NSwianRpIjoiMDg2ZjExMGJiMWVlNGZlZDhhMDVmNjVmMDAyNTI5YzgiLCJ1c2VyX2lkIjoyNH0.RywKj5B_X5SdXOX7oTO19K_r42f_wXIlEWqKzrxRj2g	2021-02-24 10:37:25.051176+00	2021-03-03 10:37:25+00	24	086f110bb1ee4fed8a05f65f002529c8
944	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxMzk3ODY2NiwianRpIjoiYTMzNjQ3MDAwNTNhNDJiYzkzNjc0NjkyZjUxMDA5ZjEiLCJ1c2VyX2lkIjo2N30.1yeiC3x6l6it5CYf9PMHWSMOTM6YYwU8Vtt7yN7nqL8	2021-02-15 07:24:26.078585+00	2021-02-22 07:24:26+00	67	a3364700053a42bc93674692f51009f1
978	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxNDA1Mzc4MywianRpIjoiMGZlMmFlMDllNzdkNDE3YzlhN2E4ZWMyZTRjNjUyZDgiLCJ1c2VyX2lkIjo3MX0.WodMXPX0fLR8MD7_0yZ2s6Nt0biOMpFGB4c_kNmlZgU	2021-02-16 04:16:23.40226+00	2021-02-23 04:16:23+00	71	0fe2ae09e77d417c9a7a8ec2e4c652d8
1012	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxNDgzMTcyOSwianRpIjoiYzM2YmY5NDIzNDFhNGE3MDgxNjdhMDAwNGE3YmFlMmIiLCJ1c2VyX2lkIjoyM30.v7CGDIqhiKoHDPzfUrzOK9lxQwltFBJbk7qSgPHU9zM	2021-02-25 04:22:09.056822+00	2021-03-04 04:22:09+00	23	c36bf942341a4a708167a0004a7bae2b
945	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxMzk3OTMzNiwianRpIjoiN2E4NGQzYTlmODUxNGIzY2E1Yzc2NDE1N2JmOTY5YWEiLCJ1c2VyX2lkIjo2N30.xYwoa7xS9Z64LTP535V6wPqUR3AEfzZJbFkq8Zk0C48	2021-02-15 07:35:36.581057+00	2021-02-22 07:35:36+00	67	7a84d3a9f8514b3ca5c764157bf969aa
979	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxNDA1MzgwMiwianRpIjoiMDQ2M2I3OTUxYzQyNDg1ZmI2MzY3MjZhMjg5MzM5NWEiLCJ1c2VyX2lkIjoyNH0.Nf8U_FLfopzpV8gvepcJSW2jIOZtQhle1A9i__olDMY	2021-02-16 04:16:42.380387+00	2021-02-23 04:16:42+00	24	0463b7951c42485fb636726a2893395a
1013	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxNDgzMzI4MSwianRpIjoiM2EyOWU4YzE5YTA0NDRiZjk5MDdhMzEwYmI1ZjViMDEiLCJ1c2VyX2lkIjoyNH0.QwktJR_p3xmRWKmGo-mlXyVzECFgpfcbhg4o1qUpwF8	2021-02-25 04:48:01.219337+00	2021-03-04 04:48:01+00	24	3a29e8c19a0444bf9907a310bb5f5b01
946	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxMzk3OTQ4NCwianRpIjoiYTg4NGJiYmM5NDlkNGM3YmI0ZTdmYWY1YWZiYmEzZGUiLCJ1c2VyX2lkIjo2N30.-kzdxQmsIggras42dXuvpL7TmdpG5nLUswYJlg11GXs	2021-02-15 07:38:04.432196+00	2021-02-22 07:38:04+00	67	a884bbbc949d4c7bb4e7faf5afbba3de
980	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxNDA1NzM0OCwianRpIjoiNThmZWJlNzczNDc2NDFiNzg5MDM3Y2RlZmY4OTIxMzgiLCJ1c2VyX2lkIjoyNH0.OIU_RW41VokyoE0A_7znQf6J9pichHZPZ61cD0Gb7Dw	2021-02-16 05:15:48.908563+00	2021-02-23 05:15:48+00	24	58febe77347641b789037cdeff892138
1014	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxNDg0NDIzOSwianRpIjoiODEyZjNjYWIyOTk3NGE4MzlhOGIwNTE5ZTNkNmU2ZjciLCJ1c2VyX2lkIjoyOH0.4rCGGIBRpQIFUBC0ThAD8VxN-h60PJAh6FvfktfinD4	2021-02-25 07:50:39.100048+00	2021-03-04 07:50:39+00	28	812f3cab29974a839a8b0519e3d6e6f7
947	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxMzk3OTQ5OSwianRpIjoiNGM5NzFhNTNlY2YyNDIwY2I3ZDljYjIxNDM1NGFjMjAiLCJ1c2VyX2lkIjo2N30.yx164RfrjFuNnJfT80CgqwBwTZp50xCdS4Eudwjua6U	2021-02-15 07:38:19.437896+00	2021-02-22 07:38:19+00	67	4c971a53ecf2420cb7d9cb214354ac20
981	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxNDA1OTMwMywianRpIjoiNTRjZGRhYTk1MmQwNDBlNjgxZDgzODNkNDZkZjMwNjkiLCJ1c2VyX2lkIjoyNH0.hRAeR6ywoK4qDpmRhlhFQKelrJ2c-Py1cy5umRMCbwE	2021-02-16 05:48:23.840971+00	2021-02-23 05:48:23+00	24	54cddaa952d040e681d8383d46df3069
1015	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxNDg1NDI3NCwianRpIjoiMmVhNGFjNTFhNDZjNDFiZWE0NmEwN2I1ZGNjNTdhMmEiLCJ1c2VyX2lkIjoyNH0.CGLbrzZVmzGdZ7f1njjCHw2l3XQboRgLoaRkSXXR9sk	2021-02-25 10:37:54.111348+00	2021-03-04 10:37:54+00	24	2ea4ac51a46c41bea46a07b5dcc57a2a
948	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxMzk4MDQ4MCwianRpIjoiYTI5ODczMTZlNDA5NGRhNTgyZTZiMWMwYjljZWQ0OGMiLCJ1c2VyX2lkIjo2N30.y-fZZ6LBk1eCLIDZTlar2Do5c_IUPoVQiVRf4vxAto0	2021-02-15 07:54:40.954867+00	2021-02-22 07:54:40+00	67	a2987316e4094da582e6b1c0b9ced48c
982	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxNDA3MzQ1MiwianRpIjoiYzI5OGUxNmM2YjdlNGUxYmI2OTc3Y2JkYjA2ZjAyNTEiLCJ1c2VyX2lkIjoyNH0.0OiJFSmce3L7R0kglt8hBFiqj2HuhyfZVb8mpBlMfjw	2021-02-16 09:44:12.668718+00	2021-02-23 09:44:12+00	24	c298e16c6b7e4e1bb6977cbdb06f0251
1016	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxNDg2MzM3MSwianRpIjoiNGI4NmIxNDNlYmM1NGM1M2E4ZjIzNzQ3NzU1OGM2OWYiLCJ1c2VyX2lkIjoyNH0.tkjllMnabqPCx4XMw29MN0Iu6hIpwQnuxKtauOJXzjs	2021-02-25 13:09:31.940927+00	2021-03-04 13:09:31+00	24	4b86b143ebc54c53a8f237477558c69f
949	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxMzk4MDY0OSwianRpIjoiZTZlMDVmMWQ0OTQxNDNiZmJmYjlmZDNmZTU5MDRiNDQiLCJ1c2VyX2lkIjo2N30.ksQWCehpOlP_yWPqlGR_hRIaQBSxu2yEGK2bx9RF0O8	2021-02-15 07:57:29.767314+00	2021-02-22 07:57:29+00	67	e6e05f1d494143bfbfb9fd3fe5904b44
983	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxNDE1Njg3NiwianRpIjoiODRmMGVlYTNjMmI3NGUwMWIxZjM2ZDAwYmIwYWE2ODYiLCJ1c2VyX2lkIjoyM30.Po9QxTU93sECeL2rSFJFVkbZAiUlRVXvdp8p_A1A2Ss	2021-02-17 08:54:36.075714+00	2021-02-24 08:54:36+00	23	84f0eea3c2b74e01b1f36d00bb0aa686
1017	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxNDkyMDk2NywianRpIjoiZjhlZDdmOGQyMDY4NDlmZTllMzMwMTg1YjUxMGFmYjQiLCJ1c2VyX2lkIjoyNH0.OSX6qp8hoZ9-vj7hCaUhb8RB3YNo30ESh5DjWN6nY_k	2021-02-26 05:09:27.676537+00	2021-03-05 05:09:27+00	24	f8ed7f8d206849fe9e330185b510afb4
950	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxMzk4MDcxOCwianRpIjoiNTIyMzJkMGZkY2RmNDNlOGE3ZTY1MjIyMGIzZDllZGIiLCJ1c2VyX2lkIjo2N30.cEIy6XIwD57QmPPhOJ4tZJH4rIrlXLdfZSxcxIXFnEE	2021-02-15 07:58:38.386161+00	2021-02-22 07:58:38+00	67	52232d0fdcdf43e8a7e652220b3d9edb
984	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxNDI0MzI5NCwianRpIjoiODkyNjE1YjdjMGVjNGY2Y2FjZTRkNDJkODg1MmJiNWQiLCJ1c2VyX2lkIjoyM30.0Q9dF1R62lVbSdFHudpjR6fLx-J3R4DQOj4vqUEgUmA	2021-02-18 08:54:54.081318+00	2021-02-25 08:54:54+00	23	892615b7c0ec4f6cace4d42d8852bb5d
1018	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxNDk0ODY2NCwianRpIjoiOTdmOWM2OWJiNWEyNGUwMzkwYjkxMmU3NjU5MjRjMGEiLCJ1c2VyX2lkIjoyM30.yqTd6vVbEhNd2loPGJ6cEWn-mWGsPNG66Cb-c8e2iiA	2021-02-26 12:51:04.550649+00	2021-03-05 12:51:04+00	23	97f9c69bb5a24e0390b912e765924c0a
951	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxMzk4MDc4OCwianRpIjoiMjA5MDNmNzA3ODJmNGU5NTljNTA3OWUyZWQzY2ZmNjQiLCJ1c2VyX2lkIjo2N30.ACP8gk6GpaQXi-J8ag-utuGSKk0_6x7K0BbD-CudfBY	2021-02-15 07:59:48.56934+00	2021-02-22 07:59:48+00	67	20903f70782f4e959c5079e2ed3cff64
985	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxNDI3NzEzOCwianRpIjoiNTBjYWVhYmI2MDAxNGE4ZTgwYzA2NzUyMDk5YjA3YzMiLCJ1c2VyX2lkIjoyM30.nxU7PjX1R_DL-yzUdDPIiHcrW2-2vkXaFWUJKPhIUYA	2021-02-18 18:18:58.662736+00	2021-02-25 18:18:58+00	23	50caeabb60014a8e80c06752099b07c3
1019	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxNTI1NzY1NSwianRpIjoiYWQ1YTM1NTE5ZDVjNGIyYzgwMTg3MWUzODRkNmE3NWEiLCJ1c2VyX2lkIjoyNH0.gY707Tcswj99svXECDXQVX35RL45upJoni0mhRIicHI	2021-03-02 02:40:55.428556+00	2021-03-09 02:40:55+00	24	ad5a35519d5c4b2c801871e384d6a75a
952	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxMzk4MTA1NSwianRpIjoiZTk3OTkxNjczODZhNGFmZThhMTg5NmFiNDY1ZTEzODEiLCJ1c2VyX2lkIjo2N30.iNgsnnAS7i2SizBs8g_Zc-upErS3GdvgKEteq7pFmJk	2021-02-15 08:04:15.837565+00	2021-02-22 08:04:15+00	67	e9799167386a4afe8a1896ab465e1381
986	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxNDMyOTc0MywianRpIjoiMmRkZGU2OTg1MjFhNDcyOWJlODYzOGZiOGYwOWY5Y2EiLCJ1c2VyX2lkIjoyM30.Z2z7xMcVT764bQ6HkEAauleOEOq0E-1CDlgPfQTv5uk	2021-02-19 08:55:43.93046+00	2021-02-26 08:55:43+00	23	2ddde698521a4729be8638fb8f09f9ca
1020	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxNTI1ODU4OCwianRpIjoiNTlkMWE4NWI5ZGU1NGFlNTgyMmY0ZmRlOGZhNTI2MjEiLCJ1c2VyX2lkIjoyNH0.LyJ7pVPpAnUr3b8JpRjtBAL1gUYTcVSwsGH2c50i2y8	2021-03-02 02:56:28.876994+00	2021-03-09 02:56:28+00	24	59d1a85b9de54ae5822f4fde8fa52621
892	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxMjM3MDE5MywianRpIjoiOGMyNGNmY2QxZDczNGNlNGEwMzJmYjZhYmQ0NzlkMTMiLCJ1c2VyX2lkIjoyM30.Dhtbx5QcjGVbLgUFYUJSmtJmZcvyKCIBXLpxOP38gG0	2021-01-27 16:36:33.666529+00	2021-02-03 16:36:33+00	23	8c24cfcd1d734ce4a032fb6abd479d13
893	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxMjQxMjM3NSwianRpIjoiYTM5MmY3YjNlNGMyNGQ4Nzk4ZmVlMGZiZjA5ZTRiNTYiLCJ1c2VyX2lkIjoyNH0.iZ7vLuzx7oFm0pwvb2zQ7g8doP9UOwGrtZzDhvp0QZg	2021-01-28 04:19:35.752742+00	2021-02-04 04:19:35+00	24	a392f7b3e4c24d8798fee0fbf09e4b56
894	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxMjQzMDA2NCwianRpIjoiYWQwMzE4YjgxMGU4NGUyMDg3ZDNkNzg0ZjNiNjM3ZDYiLCJ1c2VyX2lkIjoyNH0.eGKj5YR5wtcMGnPJgedvcOnI5nnfZSNmxNR9RB4aeUM	2021-01-28 09:14:24.350723+00	2021-02-04 09:14:24+00	24	ad0318b810e84e2087d3d784f3b637d6
895	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxMjQ1MzgzMywianRpIjoiNWYwYWY3NzVkZmVjNGNkN2JhYWY2MWQzYzFkY2VlNTMiLCJ1c2VyX2lkIjoyM30.xWe6_LcvTo4ptiFz_pfCqJCNU7wcbXQbArCxkvMr7iE	2021-01-28 15:50:33.144483+00	2021-02-04 15:50:33+00	23	5f0af775dfec4cd7baaf61d3c1dcee53
896	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxMjQ1MzkxMywianRpIjoiYzUzMGM5MzMwZDM3NGY1NThjZDUwMzEwZDFmZjdhMzYiLCJ1c2VyX2lkIjoyM30.0i5w-BvRvdUFgeDcJLQae9T2PK-sg7M8lEwBXqfzxak	2021-01-28 15:51:53.169655+00	2021-02-04 15:51:53+00	23	c530c9330d374f558cd50310d1ff7a36
897	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxMjQ1NDU1MSwianRpIjoiYzJkYzY0Njg4NjAwNDE1NTgxNjkwYzcwYjc4MDA3NjYiLCJ1c2VyX2lkIjoyOH0.zYnvneRKMj8eDjqrH8kFPqeowXU7ykoTGvKslwNMD34	2021-01-28 16:02:31.703188+00	2021-02-04 16:02:31+00	28	c2dc64688600415581690c70b7800766
898	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxMjQ1NDU1OCwianRpIjoiNjZlOTIwZmIyN2UyNGY5YThhYzhhMDQwMWI1NmZhMGMiLCJ1c2VyX2lkIjoyM30.Y-A9HjbI5-_qiwoh1onhu4u56T2nKHFHOD1Kw6VedOw	2021-01-28 16:02:38.448807+00	2021-02-04 16:02:38+00	23	66e920fb27e24f9a8ac8a0401b56fa0c
899	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxMjQ1NDU4OCwianRpIjoiYTZjNDRiMWI5ZTk5NDAyNDg2Y2FmZGE1NTlkZGUwZWUiLCJ1c2VyX2lkIjoyNH0.obQgOOQPGInMWwzWhqnoMXP1zzPcLWC9ZKhWXu-pExs	2021-01-28 16:03:08.359685+00	2021-02-04 16:03:08+00	24	a6c44b1b9e99402486cafda559dde0ee
900	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxMjQ1NzAwMywianRpIjoiNzA4MDc5ZjNhMjkxNDIzZmE2YWZjN2EwMTNmODYwNjAiLCJ1c2VyX2lkIjoyM30.9qIvMst_YNxjGE3hzedoHLHe3ydEkyZfn9qotZHO9n4	2021-01-28 16:43:23.175007+00	2021-02-04 16:43:23+00	23	708079f3a291423fa6afc7a013f86060
901	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxMjUwOTg2MiwianRpIjoiNzBkMTc5MDU1YTFjNDcyZWFmOTU4NjUzOTFhMWUxN2IiLCJ1c2VyX2lkIjoyM30.QrGseThKwXjdgcZY849dAjfcKfaCZ7J9dQDVBhoyyL0	2021-01-29 07:24:22.372314+00	2021-02-05 07:24:22+00	23	70d179055a1c472eaf95865391a1e17b
902	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxMjUyODQ1OSwianRpIjoiOTdkZDhkMmIxNTcwNDcxNGIxYTE2Mzg2NzAwZTU1MDAiLCJ1c2VyX2lkIjoyNH0.BpK-9TNykvMc9i-NZFOoFI3M4YkhnVLa8tfc2NH-kc8	2021-01-29 12:34:19.81088+00	2021-02-05 12:34:19+00	24	97dd8d2b15704714b1a16386700e5500
903	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxMjUyOTM5OCwianRpIjoiNmYwMjJlZDM0ZGM5NDE1ODgxYzg1YWVhODkyOTFmYzgiLCJ1c2VyX2lkIjoyM30.2VcSvHbug63i_tzJMi8YCCFT_aJO5Lv-baSZUFKSN6o	2021-01-29 12:49:58.293608+00	2021-02-05 12:49:58+00	23	6f022ed34dc9415881c85aea89291fc8
904	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxMjU5NTQ2MywianRpIjoiMDZkZjU5NTJiOGVjNGFiM2EwNjIzZjM3ODg1ZWYyZjEiLCJ1c2VyX2lkIjoyNH0.UGT-OMzdsrTfw20O77pk8tmEUvMn92OOTIVSXKPZdVs	2021-01-30 07:11:03.733167+00	2021-02-06 07:11:03+00	24	06df5952b8ec4ab3a0623f37885ef2f1
905	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxMjYyMzM2MiwianRpIjoiODQ0ZDdlMzdhZWE4NDNjYmI4OWExNDk4MjY1OTIyZGEiLCJ1c2VyX2lkIjoyM30.-1LUBfbbVNqP-5RlB7yeYhXDfgVCOwaL1SghUtTsII8	2021-01-30 14:56:02.819397+00	2021-02-06 14:56:02+00	23	844d7e37aea843cbb89a1498265922da
906	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxMjYyMzM4MSwianRpIjoiMDQxZDc0ZDVlZWE4NDZjOTk3Y2E2ZTkxMjljNTNhZjkiLCJ1c2VyX2lkIjoyM30.lb6m8s9TmEotfYbCXEBixnm4tmseAeIkIN-GKWXXyx4	2021-01-30 14:56:21.493481+00	2021-02-06 14:56:21+00	23	041d74d5eea846c997ca6e9129c53af9
907	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxMjYyMzU4NywianRpIjoiNzkxMjUyNzY0N2EyNGUzYmE3MjA1MTc0NTMzNzVhNzUiLCJ1c2VyX2lkIjoyM30.1xrwKUJ9LBRAYujadbTU-7sAXloO13Y8rrCX2cBs2b4	2021-01-30 14:59:47.543467+00	2021-02-06 14:59:47+00	23	7912527647a24e3ba720517453375a75
908	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxMjc3ODY0MywianRpIjoiYTBlN2UzNDQxNzQxNGFmMWEyMjhmZjIzMzI5OWEyMWUiLCJ1c2VyX2lkIjoyNH0.q6-yCEKYNH0xlfPAYdIXcPh6YXCVrQUHqKVPbcDN50w	2021-02-01 10:04:03.25656+00	2021-02-08 10:04:03+00	24	a0e7e34417414af1a228ff233299a21e
909	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxMjc3OTI4NiwianRpIjoiYjRiOWU5ZGY1NjU5NDE4Njg1NTk1MTNmY2Y2NTc0NjgiLCJ1c2VyX2lkIjoyNH0.P0trjwWPWaadphgNaVvgRLE5PiieisUVX1R4lOYuOLg	2021-02-01 10:14:46.638585+00	2021-02-08 10:14:46+00	24	b4b9e9df565941868559513fcf657468
910	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxMjg0ODYwOSwianRpIjoiOGIyM2FlZjc3ZjM2NDc5ZGIwODk2YThmODlmMDk0NmIiLCJ1c2VyX2lkIjoyNH0.9wxctJBHtvg0p8zpRidpM7IdDAd4o36ejKGK3Prqj4A	2021-02-02 05:30:09.935268+00	2021-02-09 05:30:09+00	24	8b23aef77f36479db0896a8f89f0946b
953	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxMzk4MTA2NywianRpIjoiYjM2YmFhN2NjMDlkNDRhN2FmMmZhNDEzNThhNmNjNGMiLCJ1c2VyX2lkIjo2N30.oaB6aVAHik-rKF7573DN_LiWk3trOtFwqdB92MJDo2s	2021-02-15 08:04:27.683311+00	2021-02-22 08:04:27+00	67	b36baa7cc09d44a7af2fa41358a6cc4c
987	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxNDQxNTU3OSwianRpIjoiOWFkMmFjMWU2MjNkNDZhYWFjMTcxYjA2M2EwNGE2ODgiLCJ1c2VyX2lkIjoyNH0.KiGR-NYwyTb3Eunc85YxlhPwLM6SsbPekSPP_gly_3M	2021-02-20 08:46:19.506804+00	2021-02-27 08:46:19+00	24	9ad2ac1e623d46aaac171b063a04a688
\.


--
-- Name: accounts_account_assigned_to_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.accounts_account_assigned_to_id_seq', 1, false);


--
-- Name: accounts_account_contacts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.accounts_account_contacts_id_seq', 1, false);


--
-- Name: accounts_account_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.accounts_account_id_seq', 1, false);


--
-- Name: accounts_account_tags_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.accounts_account_tags_id_seq', 1, false);


--
-- Name: accounts_account_teams_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.accounts_account_teams_id_seq', 1, false);


--
-- Name: accounts_email_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.accounts_email_id_seq', 1, false);


--
-- Name: accounts_email_recipients_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.accounts_email_recipients_id_seq', 1, false);


--
-- Name: accounts_emaillog_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.accounts_emaillog_id_seq', 1, false);


--
-- Name: accounts_tags_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.accounts_tags_id_seq', 1, false);


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 478, true);


--
-- Name: cases_case_assigned_to_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.cases_case_assigned_to_id_seq', 1, false);


--
-- Name: cases_case_contacts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.cases_case_contacts_id_seq', 1, false);


--
-- Name: cases_case_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.cases_case_id_seq', 1, false);


--
-- Name: cases_case_teams_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.cases_case_teams_id_seq', 1, false);


--
-- Name: common_address_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.common_address_id_seq', 1, false);


--
-- Name: common_apisettings_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.common_apisettings_id_seq', 1, false);


--
-- Name: common_apisettings_lead_assigned_to_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.common_apisettings_lead_assigned_to_id_seq', 1, false);


--
-- Name: common_apisettings_tags_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.common_apisettings_tags_id_seq', 1, false);


--
-- Name: common_attachments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.common_attachments_id_seq', 1, true);


--
-- Name: common_comment_files_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.common_comment_files_id_seq', 1, false);


--
-- Name: common_comment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.common_comment_id_seq', 8, true);


--
-- Name: common_document_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.common_document_id_seq', 1, false);


--
-- Name: common_document_shared_to_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.common_document_shared_to_id_seq', 1, false);


--
-- Name: common_document_teams_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.common_document_teams_id_seq', 1, false);


--
-- Name: common_google_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.common_google_id_seq', 1, false);


--
-- Name: common_profile_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.common_profile_id_seq', 1, false);


--
-- Name: common_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.common_user_groups_id_seq', 1, false);


--
-- Name: common_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.common_user_id_seq', 77, true);


--
-- Name: common_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.common_user_user_permissions_id_seq', 1, false);


--
-- Name: companies_chargingstages_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.companies_chargingstages_id_seq', 25, true);


--
-- Name: companies_company_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.companies_company_id_seq', 64, true);


--
-- Name: companies_company_tags_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.companies_company_tags_id_seq', 1, false);


--
-- Name: companies_documentformat_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.companies_documentformat_id_seq', 27, true);


--
-- Name: companies_documentheaderinformation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.companies_documentheaderinformation_id_seq', 25, true);


--
-- Name: companies_email_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.companies_email_id_seq', 1, false);


--
-- Name: companies_email_recipients_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.companies_email_recipients_id_seq', 1, false);


--
-- Name: companies_emaillog_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.companies_emaillog_id_seq', 1, false);


--
-- Name: companies_invoicegeneralremark_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.companies_invoicegeneralremark_id_seq', 35, true);


--
-- Name: companies_quotationgeneralremark_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.companies_quotationgeneralremark_id_seq', 63, true);


--
-- Name: companies_receiptgeneralremark_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.companies_receiptgeneralremark_id_seq', 21, true);


--
-- Name: companies_tags_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.companies_tags_id_seq', 1, false);


--
-- Name: contacts_contact_assigned_to_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.contacts_contact_assigned_to_id_seq', 1, false);


--
-- Name: contacts_contact_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.contacts_contact_id_seq', 1, false);


--
-- Name: contacts_contact_teams_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.contacts_contact_teams_id_seq', 1, false);


--
-- Name: customers_customer_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.customers_customer_id_seq', 122, true);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 453, true);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 167, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 402, true);


--
-- Name: emails_email_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.emails_email_id_seq', 1, false);


--
-- Name: events_event_assigned_to_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.events_event_assigned_to_id_seq', 1, false);


--
-- Name: events_event_contacts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.events_event_contacts_id_seq', 1, false);


--
-- Name: events_event_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.events_event_id_seq', 1, false);


--
-- Name: events_event_teams_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.events_event_teams_id_seq', 1, false);


--
-- Name: function_items_functionitem_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.function_items_functionitem_id_seq', 1, false);


--
-- Name: function_items_functionitemhistory_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.function_items_functionitemhistory_id_seq', 1, false);


--
-- Name: function_items_subfunctionitem_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.function_items_subfunctionitem_id_seq', 1, false);


--
-- Name: function_items_subfunctionitemhistory_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.function_items_subfunctionitemhistory_id_seq', 1, false);


--
-- Name: invoices_invoice_assigned_to_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.invoices_invoice_assigned_to_id_seq', 1, false);


--
-- Name: invoices_invoice_companies_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.invoices_invoice_companies_id_seq', 1, false);


--
-- Name: invoices_invoice_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.invoices_invoice_id_seq', 1, false);


--
-- Name: invoices_invoice_teams_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.invoices_invoice_teams_id_seq', 1, false);


--
-- Name: invoices_invoicehistory_assigned_to_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.invoices_invoicehistory_assigned_to_id_seq', 1, false);


--
-- Name: invoices_invoicehistory_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.invoices_invoicehistory_id_seq', 1, false);


--
-- Name: leads_lead_assigned_to_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.leads_lead_assigned_to_id_seq', 1, false);


--
-- Name: leads_lead_contacts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.leads_lead_contacts_id_seq', 1, false);


--
-- Name: leads_lead_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.leads_lead_id_seq', 1, false);


--
-- Name: leads_lead_teams_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.leads_lead_teams_id_seq', 1, false);


--
-- Name: marketing_blockeddomain_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.marketing_blockeddomain_id_seq', 1, false);


--
-- Name: marketing_blockedemail_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.marketing_blockedemail_id_seq', 1, false);


--
-- Name: marketing_campaign_contact_lists_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.marketing_campaign_contact_lists_id_seq', 1, false);


--
-- Name: marketing_campaign_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.marketing_campaign_id_seq', 1, false);


--
-- Name: marketing_campaign_tags_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.marketing_campaign_tags_id_seq', 1, false);


--
-- Name: marketing_campaigncompleted_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.marketing_campaigncompleted_id_seq', 1, false);


--
-- Name: marketing_campaignlinkclick_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.marketing_campaignlinkclick_id_seq', 1, false);


--
-- Name: marketing_campaignlog_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.marketing_campaignlog_id_seq', 1, false);


--
-- Name: marketing_campaignopen_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.marketing_campaignopen_id_seq', 1, false);


--
-- Name: marketing_contact_contact_list_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.marketing_contact_contact_list_id_seq', 1, false);


--
-- Name: marketing_contact_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.marketing_contact_id_seq', 1, false);


--
-- Name: marketing_contactemailcampaign_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.marketing_contactemailcampaign_id_seq', 1, false);


--
-- Name: marketing_contactlist_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.marketing_contactlist_id_seq', 1, false);


--
-- Name: marketing_contactlist_tags_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.marketing_contactlist_tags_id_seq', 1, false);


--
-- Name: marketing_contactlist_visible_to_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.marketing_contactlist_visible_to_id_seq', 1, false);


--
-- Name: marketing_contactunsubscribedcampaign_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.marketing_contactunsubscribedcampaign_id_seq', 1, false);


--
-- Name: marketing_duplicatecontacts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.marketing_duplicatecontacts_id_seq', 1, false);


--
-- Name: marketing_emailtemplate_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.marketing_emailtemplate_id_seq', 1, false);


--
-- Name: marketing_failedcontact_contact_list_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.marketing_failedcontact_contact_list_id_seq', 1, false);


--
-- Name: marketing_failedcontact_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.marketing_failedcontact_id_seq', 1, false);


--
-- Name: marketing_link_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.marketing_link_id_seq', 1, false);


--
-- Name: marketing_tag_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.marketing_tag_id_seq', 1, false);


--
-- Name: opportunity_opportunity_assigned_to_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.opportunity_opportunity_assigned_to_id_seq', 1, false);


--
-- Name: opportunity_opportunity_contacts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.opportunity_opportunity_contacts_id_seq', 1, false);


--
-- Name: opportunity_opportunity_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.opportunity_opportunity_id_seq', 1, false);


--
-- Name: opportunity_opportunity_tags_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.opportunity_opportunity_tags_id_seq', 1, false);


--
-- Name: opportunity_opportunity_teams_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.opportunity_opportunity_teams_id_seq', 1, false);


--
-- Name: planner_event_assigned_to_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.planner_event_assigned_to_id_seq', 1, false);


--
-- Name: planner_event_attendees_contacts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.planner_event_attendees_contacts_id_seq', 1, false);


--
-- Name: planner_event_attendees_leads_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.planner_event_attendees_leads_id_seq', 1, false);


--
-- Name: planner_event_attendees_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.planner_event_attendees_user_id_seq', 1, false);


--
-- Name: planner_event_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.planner_event_id_seq', 1, false);


--
-- Name: planner_event_reminders_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.planner_event_reminders_id_seq', 1, false);


--
-- Name: planner_reminder_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.planner_reminder_id_seq', 1, false);


--
-- Name: project_expenses_expendtype_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.project_expenses_expendtype_id_seq', 13, true);


--
-- Name: project_expenses_projectexpend_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.project_expenses_projectexpend_id_seq', 61, true);


--
-- Name: project_items_item_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.project_items_item_id_seq', 94, true);


--
-- Name: project_items_item_item_properties_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.project_items_item_item_properties_id_seq', 96, true);


--
-- Name: project_items_itemformula_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.project_items_itemformula_id_seq', 5, true);


--
-- Name: project_items_itemproperty_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.project_items_itemproperty_id_seq', 12, true);


--
-- Name: project_items_itemtype_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.project_items_itemtype_id_seq', 14, true);


--
-- Name: project_items_itemtypematerial_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.project_items_itemtypematerial_id_seq', 9, true);


--
-- Name: project_misc_misc_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.project_misc_misc_id_seq', 11, true);


--
-- Name: project_misc_projectmisc_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.project_misc_projectmisc_id_seq', 210, true);


--
-- Name: project_timetable_projectmilestone_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.project_timetable_projectmilestone_id_seq', 125, true);


--
-- Name: project_timetable_projectwork_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.project_timetable_projectwork_id_seq', 102, true);


--
-- Name: projects_companyprojectcomparison_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.projects_companyprojectcomparison_id_seq', 4, true);


--
-- Name: projects_companyprojectcomparison_projects_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.projects_companyprojectcomparison_projects_id_seq', 81, true);


--
-- Name: projects_project_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.projects_project_id_seq', 180, true);


--
-- Name: projects_projecthistory_assigned_to_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.projects_projecthistory_assigned_to_id_seq', 1, false);


--
-- Name: projects_projecthistory_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.projects_projecthistory_id_seq', 1, false);


--
-- Name: projects_projectimage_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.projects_projectimage_id_seq', 454, true);


--
-- Name: projects_projectimageset_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.projects_projectimageset_id_seq', 172, true);


--
-- Name: projects_projectimageset_imgs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.projects_projectimageset_imgs_id_seq', 475, true);


--
-- Name: projects_projectinvoice_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.projects_projectinvoice_id_seq', 37, true);


--
-- Name: projects_projectreceipt_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.projects_projectreceipt_id_seq', 19, true);


--
-- Name: quotations_quotation_assigned_to_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.quotations_quotation_assigned_to_id_seq', 1, false);


--
-- Name: quotations_quotation_companies_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.quotations_quotation_companies_id_seq', 1, false);


--
-- Name: quotations_quotation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.quotations_quotation_id_seq', 1, false);


--
-- Name: quotations_quotation_teams_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.quotations_quotation_teams_id_seq', 1, false);


--
-- Name: quotations_quotationhistory_assigned_to_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.quotations_quotationhistory_assigned_to_id_seq', 1, false);


--
-- Name: quotations_quotationhistory_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.quotations_quotationhistory_id_seq', 1, false);


--
-- Name: rooms_room_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.rooms_room_id_seq', 296, true);


--
-- Name: rooms_roomitem_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.rooms_roomitem_id_seq', 604, true);


--
-- Name: rooms_roomproperty_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.rooms_roomproperty_id_seq', 19, true);


--
-- Name: rooms_roomtype_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.rooms_roomtype_id_seq', 22, true);


--
-- Name: rooms_roomtype_related_items_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.rooms_roomtype_related_items_id_seq', 332, true);


--
-- Name: rooms_roomtype_room_properties_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.rooms_roomtype_room_properties_id_seq', 100, true);


--
-- Name: rooms_roomtypeformula_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.rooms_roomtypeformula_id_seq', 17, true);


--
-- Name: subscription_plans_companysubscribedplan_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.subscription_plans_companysubscribedplan_id_seq', 3, true);


--
-- Name: subscription_plans_subscriptionplan_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.subscription_plans_subscriptionplan_id_seq', 4, true);


--
-- Name: tasks_task_assigned_to_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tasks_task_assigned_to_id_seq', 1, false);


--
-- Name: tasks_task_contacts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tasks_task_contacts_id_seq', 1, false);


--
-- Name: tasks_task_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tasks_task_id_seq', 1, false);


--
-- Name: tasks_task_teams_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tasks_task_teams_id_seq', 1, false);


--
-- Name: teams_teams_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.teams_teams_id_seq', 1, false);


--
-- Name: teams_teams_users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.teams_teams_users_id_seq', 1, false);


--
-- Name: token_blacklist_blacklistedtoken_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.token_blacklist_blacklistedtoken_id_seq', 677, true);


--
-- Name: token_blacklist_outstandingtoken_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.token_blacklist_outstandingtoken_id_seq', 1027, true);


--
-- Name: accounts_account_assigned_to accounts_account_assigned_to_account_id_user_id_44dc1cab_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_account_assigned_to
    ADD CONSTRAINT accounts_account_assigned_to_account_id_user_id_44dc1cab_uniq UNIQUE (account_id, user_id);


--
-- Name: accounts_account_assigned_to accounts_account_assigned_to_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_account_assigned_to
    ADD CONSTRAINT accounts_account_assigned_to_pkey PRIMARY KEY (id);


--
-- Name: accounts_account_contacts accounts_account_contacts_account_id_contact_id_63ccfc8f_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_account_contacts
    ADD CONSTRAINT accounts_account_contacts_account_id_contact_id_63ccfc8f_uniq UNIQUE (account_id, contact_id);


--
-- Name: accounts_account_contacts accounts_account_contacts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_account_contacts
    ADD CONSTRAINT accounts_account_contacts_pkey PRIMARY KEY (id);


--
-- Name: accounts_account accounts_account_name_1d0ba595_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_account
    ADD CONSTRAINT accounts_account_name_1d0ba595_uniq UNIQUE (name);


--
-- Name: accounts_account accounts_account_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_account
    ADD CONSTRAINT accounts_account_pkey PRIMARY KEY (id);


--
-- Name: accounts_account_tags accounts_account_tags_account_id_tags_id_5920940e_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_account_tags
    ADD CONSTRAINT accounts_account_tags_account_id_tags_id_5920940e_uniq UNIQUE (account_id, tags_id);


--
-- Name: accounts_account_tags accounts_account_tags_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_account_tags
    ADD CONSTRAINT accounts_account_tags_pkey PRIMARY KEY (id);


--
-- Name: accounts_account_teams accounts_account_teams_account_id_teams_id_63eb02cd_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_account_teams
    ADD CONSTRAINT accounts_account_teams_account_id_teams_id_63eb02cd_uniq UNIQUE (account_id, teams_id);


--
-- Name: accounts_account_teams accounts_account_teams_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_account_teams
    ADD CONSTRAINT accounts_account_teams_pkey PRIMARY KEY (id);


--
-- Name: accounts_email accounts_email_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_email
    ADD CONSTRAINT accounts_email_pkey PRIMARY KEY (id);


--
-- Name: accounts_email_recipients accounts_email_recipients_email_id_contact_id_39ddf0f8_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_email_recipients
    ADD CONSTRAINT accounts_email_recipients_email_id_contact_id_39ddf0f8_uniq UNIQUE (email_id, contact_id);


--
-- Name: accounts_email_recipients accounts_email_recipients_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_email_recipients
    ADD CONSTRAINT accounts_email_recipients_pkey PRIMARY KEY (id);


--
-- Name: accounts_emaillog accounts_emaillog_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_emaillog
    ADD CONSTRAINT accounts_emaillog_pkey PRIMARY KEY (id);


--
-- Name: accounts_tags accounts_tags_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_tags
    ADD CONSTRAINT accounts_tags_pkey PRIMARY KEY (id);


--
-- Name: accounts_tags accounts_tags_slug_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_tags
    ADD CONSTRAINT accounts_tags_slug_key UNIQUE (slug);


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: cases_case_assigned_to cases_case_assigned_to_case_id_user_id_d3edec98_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cases_case_assigned_to
    ADD CONSTRAINT cases_case_assigned_to_case_id_user_id_d3edec98_uniq UNIQUE (case_id, user_id);


--
-- Name: cases_case_assigned_to cases_case_assigned_to_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cases_case_assigned_to
    ADD CONSTRAINT cases_case_assigned_to_pkey PRIMARY KEY (id);


--
-- Name: cases_case_contacts cases_case_contacts_case_id_contact_id_79772048_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cases_case_contacts
    ADD CONSTRAINT cases_case_contacts_case_id_contact_id_79772048_uniq UNIQUE (case_id, contact_id);


--
-- Name: cases_case_contacts cases_case_contacts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cases_case_contacts
    ADD CONSTRAINT cases_case_contacts_pkey PRIMARY KEY (id);


--
-- Name: cases_case cases_case_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cases_case
    ADD CONSTRAINT cases_case_pkey PRIMARY KEY (id);


--
-- Name: cases_case_teams cases_case_teams_case_id_teams_id_975db1af_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cases_case_teams
    ADD CONSTRAINT cases_case_teams_case_id_teams_id_975db1af_uniq UNIQUE (case_id, teams_id);


--
-- Name: cases_case_teams cases_case_teams_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cases_case_teams
    ADD CONSTRAINT cases_case_teams_pkey PRIMARY KEY (id);


--
-- Name: common_address common_address_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.common_address
    ADD CONSTRAINT common_address_pkey PRIMARY KEY (id);


--
-- Name: common_apisettings_lead_assigned_to common_apisettings_lead__apisettings_id_user_id_31b7a12b_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.common_apisettings_lead_assigned_to
    ADD CONSTRAINT common_apisettings_lead__apisettings_id_user_id_31b7a12b_uniq UNIQUE (apisettings_id, user_id);


--
-- Name: common_apisettings_lead_assigned_to common_apisettings_lead_assigned_to_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.common_apisettings_lead_assigned_to
    ADD CONSTRAINT common_apisettings_lead_assigned_to_pkey PRIMARY KEY (id);


--
-- Name: common_apisettings common_apisettings_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.common_apisettings
    ADD CONSTRAINT common_apisettings_pkey PRIMARY KEY (id);


--
-- Name: common_apisettings_tags common_apisettings_tags_apisettings_id_tags_id_74019ad7_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.common_apisettings_tags
    ADD CONSTRAINT common_apisettings_tags_apisettings_id_tags_id_74019ad7_uniq UNIQUE (apisettings_id, tags_id);


--
-- Name: common_apisettings_tags common_apisettings_tags_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.common_apisettings_tags
    ADD CONSTRAINT common_apisettings_tags_pkey PRIMARY KEY (id);


--
-- Name: common_attachments common_attachments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.common_attachments
    ADD CONSTRAINT common_attachments_pkey PRIMARY KEY (id);


--
-- Name: common_comment_files common_comment_files_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.common_comment_files
    ADD CONSTRAINT common_comment_files_pkey PRIMARY KEY (id);


--
-- Name: common_comment common_comment_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.common_comment
    ADD CONSTRAINT common_comment_pkey PRIMARY KEY (id);


--
-- Name: common_document common_document_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.common_document
    ADD CONSTRAINT common_document_pkey PRIMARY KEY (id);


--
-- Name: common_document_shared_to common_document_shared_to_document_id_user_id_270c028b_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.common_document_shared_to
    ADD CONSTRAINT common_document_shared_to_document_id_user_id_270c028b_uniq UNIQUE (document_id, user_id);


--
-- Name: common_document_shared_to common_document_shared_to_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.common_document_shared_to
    ADD CONSTRAINT common_document_shared_to_pkey PRIMARY KEY (id);


--
-- Name: common_document_teams common_document_teams_document_id_teams_id_1a1b5d77_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.common_document_teams
    ADD CONSTRAINT common_document_teams_document_id_teams_id_1a1b5d77_uniq UNIQUE (document_id, teams_id);


--
-- Name: common_document_teams common_document_teams_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.common_document_teams
    ADD CONSTRAINT common_document_teams_pkey PRIMARY KEY (id);


--
-- Name: common_google common_google_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.common_google
    ADD CONSTRAINT common_google_pkey PRIMARY KEY (id);


--
-- Name: common_profile common_profile_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.common_profile
    ADD CONSTRAINT common_profile_pkey PRIMARY KEY (id);


--
-- Name: common_profile common_profile_user_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.common_profile
    ADD CONSTRAINT common_profile_user_id_key UNIQUE (user_id);


--
-- Name: common_user_groups common_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.common_user_groups
    ADD CONSTRAINT common_user_groups_pkey PRIMARY KEY (id);


--
-- Name: common_user_groups common_user_groups_user_id_group_id_ba201ca9_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.common_user_groups
    ADD CONSTRAINT common_user_groups_user_id_group_id_ba201ca9_uniq UNIQUE (user_id, group_id);


--
-- Name: common_user common_user_phone_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.common_user
    ADD CONSTRAINT common_user_phone_key UNIQUE (phone);


--
-- Name: common_user common_user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.common_user
    ADD CONSTRAINT common_user_pkey PRIMARY KEY (id);


--
-- Name: common_user_user_permissions common_user_user_permiss_user_id_permission_id_5694f4c4_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.common_user_user_permissions
    ADD CONSTRAINT common_user_user_permiss_user_id_permission_id_5694f4c4_uniq UNIQUE (user_id, permission_id);


--
-- Name: common_user_user_permissions common_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.common_user_user_permissions
    ADD CONSTRAINT common_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: common_user common_user_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.common_user
    ADD CONSTRAINT common_user_username_key UNIQUE (username);


--
-- Name: companies_chargingstages companies_chargingstages_company_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.companies_chargingstages
    ADD CONSTRAINT companies_chargingstages_company_id_key UNIQUE (company_id);


--
-- Name: companies_chargingstages companies_chargingstages_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.companies_chargingstages
    ADD CONSTRAINT companies_chargingstages_pkey PRIMARY KEY (id);


--
-- Name: companies_company companies_company_owner_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.companies_company
    ADD CONSTRAINT companies_company_owner_id_key UNIQUE (owner_id);


--
-- Name: companies_company companies_company_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.companies_company
    ADD CONSTRAINT companies_company_pkey PRIMARY KEY (id);


--
-- Name: companies_company_tags companies_company_tags_company_id_tags_id_952c43d3_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.companies_company_tags
    ADD CONSTRAINT companies_company_tags_company_id_tags_id_952c43d3_uniq UNIQUE (company_id, tags_id);


--
-- Name: companies_company_tags companies_company_tags_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.companies_company_tags
    ADD CONSTRAINT companies_company_tags_pkey PRIMARY KEY (id);


--
-- Name: companies_documentformat companies_documentformat_company_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.companies_documentformat
    ADD CONSTRAINT companies_documentformat_company_id_key UNIQUE (company_id);


--
-- Name: companies_documentformat companies_documentformat_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.companies_documentformat
    ADD CONSTRAINT companies_documentformat_pkey PRIMARY KEY (id);


--
-- Name: companies_documentheaderinformation companies_documentheaderinformation_company_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.companies_documentheaderinformation
    ADD CONSTRAINT companies_documentheaderinformation_company_id_key UNIQUE (company_id);


--
-- Name: companies_documentheaderinformation companies_documentheaderinformation_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.companies_documentheaderinformation
    ADD CONSTRAINT companies_documentheaderinformation_pkey PRIMARY KEY (id);


--
-- Name: companies_email companies_email_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.companies_email
    ADD CONSTRAINT companies_email_pkey PRIMARY KEY (id);


--
-- Name: companies_email_recipients companies_email_recipients_email_id_contact_id_e3ac1a0d_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.companies_email_recipients
    ADD CONSTRAINT companies_email_recipients_email_id_contact_id_e3ac1a0d_uniq UNIQUE (email_id, contact_id);


--
-- Name: companies_email_recipients companies_email_recipients_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.companies_email_recipients
    ADD CONSTRAINT companies_email_recipients_pkey PRIMARY KEY (id);


--
-- Name: companies_emaillog companies_emaillog_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.companies_emaillog
    ADD CONSTRAINT companies_emaillog_pkey PRIMARY KEY (id);


--
-- Name: companies_invoicegeneralremark companies_invoicegeneralremark_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.companies_invoicegeneralremark
    ADD CONSTRAINT companies_invoicegeneralremark_pkey PRIMARY KEY (id);


--
-- Name: companies_quotationgeneralremark companies_quotationgeneralremark_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.companies_quotationgeneralremark
    ADD CONSTRAINT companies_quotationgeneralremark_pkey PRIMARY KEY (id);


--
-- Name: companies_receiptgeneralremark companies_receiptgeneralremark_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.companies_receiptgeneralremark
    ADD CONSTRAINT companies_receiptgeneralremark_pkey PRIMARY KEY (id);


--
-- Name: companies_tags companies_tags_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.companies_tags
    ADD CONSTRAINT companies_tags_pkey PRIMARY KEY (id);


--
-- Name: companies_tags companies_tags_slug_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.companies_tags
    ADD CONSTRAINT companies_tags_slug_key UNIQUE (slug);


--
-- Name: contacts_contact_assigned_to contacts_contact_assigned_to_contact_id_user_id_145bff71_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contacts_contact_assigned_to
    ADD CONSTRAINT contacts_contact_assigned_to_contact_id_user_id_145bff71_uniq UNIQUE (contact_id, user_id);


--
-- Name: contacts_contact_assigned_to contacts_contact_assigned_to_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contacts_contact_assigned_to
    ADD CONSTRAINT contacts_contact_assigned_to_pkey PRIMARY KEY (id);


--
-- Name: contacts_contact contacts_contact_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contacts_contact
    ADD CONSTRAINT contacts_contact_email_key UNIQUE (email);


--
-- Name: contacts_contact contacts_contact_phone_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contacts_contact
    ADD CONSTRAINT contacts_contact_phone_key UNIQUE (phone);


--
-- Name: contacts_contact contacts_contact_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contacts_contact
    ADD CONSTRAINT contacts_contact_pkey PRIMARY KEY (id);


--
-- Name: contacts_contact_teams contacts_contact_teams_contact_id_teams_id_70cea3c6_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contacts_contact_teams
    ADD CONSTRAINT contacts_contact_teams_contact_id_teams_id_70cea3c6_uniq UNIQUE (contact_id, teams_id);


--
-- Name: contacts_contact_teams contacts_contact_teams_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contacts_contact_teams
    ADD CONSTRAINT contacts_contact_teams_pkey PRIMARY KEY (id);


--
-- Name: customers_customer customers_customer_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.customers_customer
    ADD CONSTRAINT customers_customer_pkey PRIMARY KEY (id);


--
-- Name: customers_customer customers_customer_project_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.customers_customer
    ADD CONSTRAINT customers_customer_project_id_key UNIQUE (project_id);


--
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: emails_email emails_email_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.emails_email
    ADD CONSTRAINT emails_email_pkey PRIMARY KEY (id);


--
-- Name: events_event_assigned_to events_event_assigned_to_event_id_user_id_8d2e75e1_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.events_event_assigned_to
    ADD CONSTRAINT events_event_assigned_to_event_id_user_id_8d2e75e1_uniq UNIQUE (event_id, user_id);


--
-- Name: events_event_assigned_to events_event_assigned_to_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.events_event_assigned_to
    ADD CONSTRAINT events_event_assigned_to_pkey PRIMARY KEY (id);


--
-- Name: events_event_contacts events_event_contacts_event_id_contact_id_a262e2d5_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.events_event_contacts
    ADD CONSTRAINT events_event_contacts_event_id_contact_id_a262e2d5_uniq UNIQUE (event_id, contact_id);


--
-- Name: events_event_contacts events_event_contacts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.events_event_contacts
    ADD CONSTRAINT events_event_contacts_pkey PRIMARY KEY (id);


--
-- Name: events_event events_event_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.events_event
    ADD CONSTRAINT events_event_pkey PRIMARY KEY (id);


--
-- Name: events_event_teams events_event_teams_event_id_teams_id_8c426c0e_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.events_event_teams
    ADD CONSTRAINT events_event_teams_event_id_teams_id_8c426c0e_uniq UNIQUE (event_id, teams_id);


--
-- Name: events_event_teams events_event_teams_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.events_event_teams
    ADD CONSTRAINT events_event_teams_pkey PRIMARY KEY (id);


--
-- Name: function_items_functionitem function_items_functionitem_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.function_items_functionitem
    ADD CONSTRAINT function_items_functionitem_pkey PRIMARY KEY (id);


--
-- Name: function_items_functionitemhistory function_items_functionitemhistory_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.function_items_functionitemhistory
    ADD CONSTRAINT function_items_functionitemhistory_pkey PRIMARY KEY (id);


--
-- Name: function_items_subfunctionitem function_items_subfunctionitem_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.function_items_subfunctionitem
    ADD CONSTRAINT function_items_subfunctionitem_pkey PRIMARY KEY (id);


--
-- Name: function_items_subfunctionitemhistory function_items_subfunctionitemhistory_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.function_items_subfunctionitemhistory
    ADD CONSTRAINT function_items_subfunctionitemhistory_pkey PRIMARY KEY (id);


--
-- Name: invoices_invoice_assigned_to invoices_invoice_assigned_to_invoice_id_user_id_dd2062db_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.invoices_invoice_assigned_to
    ADD CONSTRAINT invoices_invoice_assigned_to_invoice_id_user_id_dd2062db_uniq UNIQUE (invoice_id, user_id);


--
-- Name: invoices_invoice_assigned_to invoices_invoice_assigned_to_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.invoices_invoice_assigned_to
    ADD CONSTRAINT invoices_invoice_assigned_to_pkey PRIMARY KEY (id);


--
-- Name: invoices_invoice_companies invoices_invoice_companies_invoice_id_company_id_725dfb9b_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.invoices_invoice_companies
    ADD CONSTRAINT invoices_invoice_companies_invoice_id_company_id_725dfb9b_uniq UNIQUE (invoice_id, company_id);


--
-- Name: invoices_invoice_companies invoices_invoice_companies_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.invoices_invoice_companies
    ADD CONSTRAINT invoices_invoice_companies_pkey PRIMARY KEY (id);


--
-- Name: invoices_invoice invoices_invoice_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.invoices_invoice
    ADD CONSTRAINT invoices_invoice_pkey PRIMARY KEY (id);


--
-- Name: invoices_invoice_teams invoices_invoice_teams_invoice_id_teams_id_82e5289d_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.invoices_invoice_teams
    ADD CONSTRAINT invoices_invoice_teams_invoice_id_teams_id_82e5289d_uniq UNIQUE (invoice_id, teams_id);


--
-- Name: invoices_invoice_teams invoices_invoice_teams_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.invoices_invoice_teams
    ADD CONSTRAINT invoices_invoice_teams_pkey PRIMARY KEY (id);


--
-- Name: invoices_invoicehistory_assigned_to invoices_invoicehistory__invoicehistory_id_user_i_1b9adc64_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.invoices_invoicehistory_assigned_to
    ADD CONSTRAINT invoices_invoicehistory__invoicehistory_id_user_i_1b9adc64_uniq UNIQUE (invoicehistory_id, user_id);


--
-- Name: invoices_invoicehistory_assigned_to invoices_invoicehistory_assigned_to_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.invoices_invoicehistory_assigned_to
    ADD CONSTRAINT invoices_invoicehistory_assigned_to_pkey PRIMARY KEY (id);


--
-- Name: invoices_invoicehistory invoices_invoicehistory_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.invoices_invoicehistory
    ADD CONSTRAINT invoices_invoicehistory_pkey PRIMARY KEY (id);


--
-- Name: leads_lead_assigned_to leads_lead_assigned_to_lead_id_user_id_96e37802_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.leads_lead_assigned_to
    ADD CONSTRAINT leads_lead_assigned_to_lead_id_user_id_96e37802_uniq UNIQUE (lead_id, user_id);


--
-- Name: leads_lead_assigned_to leads_lead_assigned_to_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.leads_lead_assigned_to
    ADD CONSTRAINT leads_lead_assigned_to_pkey PRIMARY KEY (id);


--
-- Name: leads_lead_contacts leads_lead_contacts_lead_id_contact_id_9282b1c1_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.leads_lead_contacts
    ADD CONSTRAINT leads_lead_contacts_lead_id_contact_id_9282b1c1_uniq UNIQUE (lead_id, contact_id);


--
-- Name: leads_lead_contacts leads_lead_contacts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.leads_lead_contacts
    ADD CONSTRAINT leads_lead_contacts_pkey PRIMARY KEY (id);


--
-- Name: leads_lead leads_lead_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.leads_lead
    ADD CONSTRAINT leads_lead_pkey PRIMARY KEY (id);


--
-- Name: leads_lead_teams leads_lead_teams_lead_id_teams_id_e2392e4d_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.leads_lead_teams
    ADD CONSTRAINT leads_lead_teams_lead_id_teams_id_e2392e4d_uniq UNIQUE (lead_id, teams_id);


--
-- Name: leads_lead_teams leads_lead_teams_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.leads_lead_teams
    ADD CONSTRAINT leads_lead_teams_pkey PRIMARY KEY (id);


--
-- Name: marketing_blockeddomain marketing_blockeddomain_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_blockeddomain
    ADD CONSTRAINT marketing_blockeddomain_pkey PRIMARY KEY (id);


--
-- Name: marketing_blockedemail marketing_blockedemail_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_blockedemail
    ADD CONSTRAINT marketing_blockedemail_pkey PRIMARY KEY (id);


--
-- Name: marketing_campaign_contact_lists marketing_campaign_conta_campaign_id_contactlist__020d6f66_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_campaign_contact_lists
    ADD CONSTRAINT marketing_campaign_conta_campaign_id_contactlist__020d6f66_uniq UNIQUE (campaign_id, contactlist_id);


--
-- Name: marketing_campaign_contact_lists marketing_campaign_contact_lists_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_campaign_contact_lists
    ADD CONSTRAINT marketing_campaign_contact_lists_pkey PRIMARY KEY (id);


--
-- Name: marketing_campaign marketing_campaign_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_campaign
    ADD CONSTRAINT marketing_campaign_pkey PRIMARY KEY (id);


--
-- Name: marketing_campaign_tags marketing_campaign_tags_campaign_id_tag_id_83900b94_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_campaign_tags
    ADD CONSTRAINT marketing_campaign_tags_campaign_id_tag_id_83900b94_uniq UNIQUE (campaign_id, tag_id);


--
-- Name: marketing_campaign_tags marketing_campaign_tags_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_campaign_tags
    ADD CONSTRAINT marketing_campaign_tags_pkey PRIMARY KEY (id);


--
-- Name: marketing_campaigncompleted marketing_campaigncompleted_campaign_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_campaigncompleted
    ADD CONSTRAINT marketing_campaigncompleted_campaign_id_key UNIQUE (campaign_id);


--
-- Name: marketing_campaigncompleted marketing_campaigncompleted_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_campaigncompleted
    ADD CONSTRAINT marketing_campaigncompleted_pkey PRIMARY KEY (id);


--
-- Name: marketing_campaignlinkclick marketing_campaignlinkclick_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_campaignlinkclick
    ADD CONSTRAINT marketing_campaignlinkclick_pkey PRIMARY KEY (id);


--
-- Name: marketing_campaignlog marketing_campaignlog_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_campaignlog
    ADD CONSTRAINT marketing_campaignlog_pkey PRIMARY KEY (id);


--
-- Name: marketing_campaignopen marketing_campaignopen_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_campaignopen
    ADD CONSTRAINT marketing_campaignopen_pkey PRIMARY KEY (id);


--
-- Name: marketing_contact_contact_list marketing_contact_contac_contact_id_contactlist_i_a64027db_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_contact_contact_list
    ADD CONSTRAINT marketing_contact_contac_contact_id_contactlist_i_a64027db_uniq UNIQUE (contact_id, contactlist_id);


--
-- Name: marketing_contact_contact_list marketing_contact_contact_list_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_contact_contact_list
    ADD CONSTRAINT marketing_contact_contact_list_pkey PRIMARY KEY (id);


--
-- Name: marketing_contact marketing_contact_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_contact
    ADD CONSTRAINT marketing_contact_pkey PRIMARY KEY (id);


--
-- Name: marketing_contactemailcampaign marketing_contactemailcampaign_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_contactemailcampaign
    ADD CONSTRAINT marketing_contactemailcampaign_pkey PRIMARY KEY (id);


--
-- Name: marketing_contactlist marketing_contactlist_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_contactlist
    ADD CONSTRAINT marketing_contactlist_pkey PRIMARY KEY (id);


--
-- Name: marketing_contactlist_tags marketing_contactlist_tags_contactlist_id_tag_id_a157ecf0_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_contactlist_tags
    ADD CONSTRAINT marketing_contactlist_tags_contactlist_id_tag_id_a157ecf0_uniq UNIQUE (contactlist_id, tag_id);


--
-- Name: marketing_contactlist_tags marketing_contactlist_tags_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_contactlist_tags
    ADD CONSTRAINT marketing_contactlist_tags_pkey PRIMARY KEY (id);


--
-- Name: marketing_contactlist_visible_to marketing_contactlist_vi_contactlist_id_user_id_4ab3b57e_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_contactlist_visible_to
    ADD CONSTRAINT marketing_contactlist_vi_contactlist_id_user_id_4ab3b57e_uniq UNIQUE (contactlist_id, user_id);


--
-- Name: marketing_contactlist_visible_to marketing_contactlist_visible_to_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_contactlist_visible_to
    ADD CONSTRAINT marketing_contactlist_visible_to_pkey PRIMARY KEY (id);


--
-- Name: marketing_contactunsubscribedcampaign marketing_contactunsubscribedcampaign_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_contactunsubscribedcampaign
    ADD CONSTRAINT marketing_contactunsubscribedcampaign_pkey PRIMARY KEY (id);


--
-- Name: marketing_duplicatecontacts marketing_duplicatecontacts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_duplicatecontacts
    ADD CONSTRAINT marketing_duplicatecontacts_pkey PRIMARY KEY (id);


--
-- Name: marketing_emailtemplate marketing_emailtemplate_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_emailtemplate
    ADD CONSTRAINT marketing_emailtemplate_pkey PRIMARY KEY (id);


--
-- Name: marketing_failedcontact_contact_list marketing_failedcontact__failedcontact_id_contact_d1cdb0d5_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_failedcontact_contact_list
    ADD CONSTRAINT marketing_failedcontact__failedcontact_id_contact_d1cdb0d5_uniq UNIQUE (failedcontact_id, contactlist_id);


--
-- Name: marketing_failedcontact_contact_list marketing_failedcontact_contact_list_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_failedcontact_contact_list
    ADD CONSTRAINT marketing_failedcontact_contact_list_pkey PRIMARY KEY (id);


--
-- Name: marketing_failedcontact marketing_failedcontact_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_failedcontact
    ADD CONSTRAINT marketing_failedcontact_pkey PRIMARY KEY (id);


--
-- Name: marketing_link marketing_link_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_link
    ADD CONSTRAINT marketing_link_pkey PRIMARY KEY (id);


--
-- Name: marketing_tag marketing_tag_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_tag
    ADD CONSTRAINT marketing_tag_pkey PRIMARY KEY (id);


--
-- Name: opportunity_opportunity_contacts opportunity_opportunity__opportunity_id_contact_i_0184536a_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.opportunity_opportunity_contacts
    ADD CONSTRAINT opportunity_opportunity__opportunity_id_contact_i_0184536a_uniq UNIQUE (opportunity_id, contact_id);


--
-- Name: opportunity_opportunity_tags opportunity_opportunity__opportunity_id_tags_id_c03dc1e3_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.opportunity_opportunity_tags
    ADD CONSTRAINT opportunity_opportunity__opportunity_id_tags_id_c03dc1e3_uniq UNIQUE (opportunity_id, tags_id);


--
-- Name: opportunity_opportunity_teams opportunity_opportunity__opportunity_id_teams_id_5963d744_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.opportunity_opportunity_teams
    ADD CONSTRAINT opportunity_opportunity__opportunity_id_teams_id_5963d744_uniq UNIQUE (opportunity_id, teams_id);


--
-- Name: opportunity_opportunity_assigned_to opportunity_opportunity__opportunity_id_user_id_b1055494_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.opportunity_opportunity_assigned_to
    ADD CONSTRAINT opportunity_opportunity__opportunity_id_user_id_b1055494_uniq UNIQUE (opportunity_id, user_id);


--
-- Name: opportunity_opportunity_assigned_to opportunity_opportunity_assigned_to_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.opportunity_opportunity_assigned_to
    ADD CONSTRAINT opportunity_opportunity_assigned_to_pkey PRIMARY KEY (id);


--
-- Name: opportunity_opportunity_contacts opportunity_opportunity_contacts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.opportunity_opportunity_contacts
    ADD CONSTRAINT opportunity_opportunity_contacts_pkey PRIMARY KEY (id);


--
-- Name: opportunity_opportunity opportunity_opportunity_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.opportunity_opportunity
    ADD CONSTRAINT opportunity_opportunity_pkey PRIMARY KEY (id);


--
-- Name: opportunity_opportunity_tags opportunity_opportunity_tags_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.opportunity_opportunity_tags
    ADD CONSTRAINT opportunity_opportunity_tags_pkey PRIMARY KEY (id);


--
-- Name: opportunity_opportunity_teams opportunity_opportunity_teams_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.opportunity_opportunity_teams
    ADD CONSTRAINT opportunity_opportunity_teams_pkey PRIMARY KEY (id);


--
-- Name: planner_event_assigned_to planner_event_assigned_to_event_id_user_id_a9857a09_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.planner_event_assigned_to
    ADD CONSTRAINT planner_event_assigned_to_event_id_user_id_a9857a09_uniq UNIQUE (event_id, user_id);


--
-- Name: planner_event_assigned_to planner_event_assigned_to_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.planner_event_assigned_to
    ADD CONSTRAINT planner_event_assigned_to_pkey PRIMARY KEY (id);


--
-- Name: planner_event_attendees_contacts planner_event_attendees__event_id_contact_id_a1abf61b_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.planner_event_attendees_contacts
    ADD CONSTRAINT planner_event_attendees__event_id_contact_id_a1abf61b_uniq UNIQUE (event_id, contact_id);


--
-- Name: planner_event_attendees_contacts planner_event_attendees_contacts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.planner_event_attendees_contacts
    ADD CONSTRAINT planner_event_attendees_contacts_pkey PRIMARY KEY (id);


--
-- Name: planner_event_attendees_leads planner_event_attendees_leads_event_id_lead_id_2f4d367c_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.planner_event_attendees_leads
    ADD CONSTRAINT planner_event_attendees_leads_event_id_lead_id_2f4d367c_uniq UNIQUE (event_id, lead_id);


--
-- Name: planner_event_attendees_leads planner_event_attendees_leads_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.planner_event_attendees_leads
    ADD CONSTRAINT planner_event_attendees_leads_pkey PRIMARY KEY (id);


--
-- Name: planner_event_attendees_user planner_event_attendees_user_event_id_user_id_89db87fa_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.planner_event_attendees_user
    ADD CONSTRAINT planner_event_attendees_user_event_id_user_id_89db87fa_uniq UNIQUE (event_id, user_id);


--
-- Name: planner_event_attendees_user planner_event_attendees_user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.planner_event_attendees_user
    ADD CONSTRAINT planner_event_attendees_user_pkey PRIMARY KEY (id);


--
-- Name: planner_event planner_event_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.planner_event
    ADD CONSTRAINT planner_event_pkey PRIMARY KEY (id);


--
-- Name: planner_event_reminders planner_event_reminders_event_id_reminder_id_ee1ba293_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.planner_event_reminders
    ADD CONSTRAINT planner_event_reminders_event_id_reminder_id_ee1ba293_uniq UNIQUE (event_id, reminder_id);


--
-- Name: planner_event_reminders planner_event_reminders_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.planner_event_reminders
    ADD CONSTRAINT planner_event_reminders_pkey PRIMARY KEY (id);


--
-- Name: planner_reminder planner_reminder_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.planner_reminder
    ADD CONSTRAINT planner_reminder_pkey PRIMARY KEY (id);


--
-- Name: project_expenses_expensetype project_expenses_expendtype_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.project_expenses_expensetype
    ADD CONSTRAINT project_expenses_expendtype_pkey PRIMARY KEY (id);


--
-- Name: project_expenses_projectexpense project_expenses_projectexpend_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.project_expenses_projectexpense
    ADD CONSTRAINT project_expenses_projectexpend_pkey PRIMARY KEY (id);


--
-- Name: project_items_item_item_properties project_items_item_item__item_id_itemproperty_id_c2d1e000_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.project_items_item_item_properties
    ADD CONSTRAINT project_items_item_item__item_id_itemproperty_id_c2d1e000_uniq UNIQUE (item_id, itemproperty_id);


--
-- Name: project_items_item_item_properties project_items_item_item_properties_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.project_items_item_item_properties
    ADD CONSTRAINT project_items_item_item_properties_pkey PRIMARY KEY (id);


--
-- Name: project_items_item project_items_item_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.project_items_item
    ADD CONSTRAINT project_items_item_pkey PRIMARY KEY (id);


--
-- Name: project_items_itemformula project_items_itemformula_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.project_items_itemformula
    ADD CONSTRAINT project_items_itemformula_pkey PRIMARY KEY (id);


--
-- Name: project_items_itemproperty project_items_itemproperty_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.project_items_itemproperty
    ADD CONSTRAINT project_items_itemproperty_pkey PRIMARY KEY (id);


--
-- Name: project_items_itemproperty project_items_itemproperty_symbol_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.project_items_itemproperty
    ADD CONSTRAINT project_items_itemproperty_symbol_key UNIQUE (symbol);


--
-- Name: project_items_itemtype project_items_itemtype_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.project_items_itemtype
    ADD CONSTRAINT project_items_itemtype_pkey PRIMARY KEY (id);


--
-- Name: project_items_itemtypematerial project_items_itemtypematerial_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.project_items_itemtypematerial
    ADD CONSTRAINT project_items_itemtypematerial_pkey PRIMARY KEY (id);


--
-- Name: project_misc_misc project_misc_misc_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.project_misc_misc
    ADD CONSTRAINT project_misc_misc_pkey PRIMARY KEY (id);


--
-- Name: project_misc_projectmisc project_misc_projectmisc_misc_id_project_id_fa29bd21_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.project_misc_projectmisc
    ADD CONSTRAINT project_misc_projectmisc_misc_id_project_id_fa29bd21_uniq UNIQUE (misc_id, project_id);


--
-- Name: project_misc_projectmisc project_misc_projectmisc_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.project_misc_projectmisc
    ADD CONSTRAINT project_misc_projectmisc_pkey PRIMARY KEY (id);


--
-- Name: project_timetable_projectmilestone project_timetable_projectmilestone_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.project_timetable_projectmilestone
    ADD CONSTRAINT project_timetable_projectmilestone_pkey PRIMARY KEY (id);


--
-- Name: project_timetable_projectwork project_timetable_projectwork_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.project_timetable_projectwork
    ADD CONSTRAINT project_timetable_projectwork_pkey PRIMARY KEY (id);


--
-- Name: projects_companyprojectcomparison_projects projects_companyprojectc_companyprojectcomparison_deb6bd54_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects_companyprojectcomparison_projects
    ADD CONSTRAINT projects_companyprojectc_companyprojectcomparison_deb6bd54_uniq UNIQUE (companyprojectcomparison_id, project_id);


--
-- Name: projects_companyprojectcomparison projects_companyprojectcomparison_company_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects_companyprojectcomparison
    ADD CONSTRAINT projects_companyprojectcomparison_company_id_key UNIQUE (company_id);


--
-- Name: projects_companyprojectcomparison projects_companyprojectcomparison_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects_companyprojectcomparison
    ADD CONSTRAINT projects_companyprojectcomparison_pkey PRIMARY KEY (id);


--
-- Name: projects_companyprojectcomparison_projects projects_companyprojectcomparison_projects_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects_companyprojectcomparison_projects
    ADD CONSTRAINT projects_companyprojectcomparison_projects_pkey PRIMARY KEY (id);


--
-- Name: projects_project projects_project_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects_project
    ADD CONSTRAINT projects_project_pkey PRIMARY KEY (id);


--
-- Name: projects_projecthistory_assigned_to projects_projecthistory__projecthistory_id_user_i_69c9feb7_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects_projecthistory_assigned_to
    ADD CONSTRAINT projects_projecthistory__projecthistory_id_user_i_69c9feb7_uniq UNIQUE (projecthistory_id, user_id);


--
-- Name: projects_projecthistory_assigned_to projects_projecthistory_assigned_to_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects_projecthistory_assigned_to
    ADD CONSTRAINT projects_projecthistory_assigned_to_pkey PRIMARY KEY (id);


--
-- Name: projects_projecthistory projects_projecthistory_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects_projecthistory
    ADD CONSTRAINT projects_projecthistory_pkey PRIMARY KEY (id);


--
-- Name: projects_projectimage projects_projectimage_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects_projectimage
    ADD CONSTRAINT projects_projectimage_pkey PRIMARY KEY (id);


--
-- Name: projects_projectimageset_imgs projects_projectimageset_imgs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects_projectimageset_imgs
    ADD CONSTRAINT projects_projectimageset_imgs_pkey PRIMARY KEY (id);


--
-- Name: projects_projectimageset projects_projectimageset_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects_projectimageset
    ADD CONSTRAINT projects_projectimageset_pkey PRIMARY KEY (id);


--
-- Name: projects_projectimageset projects_projectimageset_project_milestone_id_d548a3e0_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects_projectimageset
    ADD CONSTRAINT projects_projectimageset_project_milestone_id_d548a3e0_uniq UNIQUE (project_milestone_id);


--
-- Name: projects_projectimageset_imgs projects_projectimageset_projectimageset_id_proje_05e5d74c_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects_projectimageset_imgs
    ADD CONSTRAINT projects_projectimageset_projectimageset_id_proje_05e5d74c_uniq UNIQUE (projectimageset_id, projectimage_id);


--
-- Name: projects_projectinvoice projects_projectinvoice_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects_projectinvoice
    ADD CONSTRAINT projects_projectinvoice_pkey PRIMARY KEY (id);


--
-- Name: projects_projectinvoice projects_projectinvoice_project_id_invoice_id_8d2f17b6_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects_projectinvoice
    ADD CONSTRAINT projects_projectinvoice_project_id_invoice_id_8d2f17b6_uniq UNIQUE (project_id, invoice_id);


--
-- Name: projects_projectreceipt projects_projectreceipt_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects_projectreceipt
    ADD CONSTRAINT projects_projectreceipt_pkey PRIMARY KEY (id);


--
-- Name: projects_projectreceipt projects_projectreceipt_project_id_receipt_id_e79382d8_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects_projectreceipt
    ADD CONSTRAINT projects_projectreceipt_project_id_receipt_id_e79382d8_uniq UNIQUE (project_id, receipt_id);


--
-- Name: quotations_quotation_assigned_to quotations_quotation_ass_quotation_id_user_id_0b5a471b_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.quotations_quotation_assigned_to
    ADD CONSTRAINT quotations_quotation_ass_quotation_id_user_id_0b5a471b_uniq UNIQUE (quotation_id, user_id);


--
-- Name: quotations_quotation_assigned_to quotations_quotation_assigned_to_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.quotations_quotation_assigned_to
    ADD CONSTRAINT quotations_quotation_assigned_to_pkey PRIMARY KEY (id);


--
-- Name: quotations_quotation_companies quotations_quotation_com_quotation_id_company_id_cf6d3478_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.quotations_quotation_companies
    ADD CONSTRAINT quotations_quotation_com_quotation_id_company_id_cf6d3478_uniq UNIQUE (quotation_id, company_id);


--
-- Name: quotations_quotation_companies quotations_quotation_companies_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.quotations_quotation_companies
    ADD CONSTRAINT quotations_quotation_companies_pkey PRIMARY KEY (id);


--
-- Name: quotations_quotation quotations_quotation_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.quotations_quotation
    ADD CONSTRAINT quotations_quotation_pkey PRIMARY KEY (id);


--
-- Name: quotations_quotation_teams quotations_quotation_teams_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.quotations_quotation_teams
    ADD CONSTRAINT quotations_quotation_teams_pkey PRIMARY KEY (id);


--
-- Name: quotations_quotation_teams quotations_quotation_teams_quotation_id_teams_id_68eccdac_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.quotations_quotation_teams
    ADD CONSTRAINT quotations_quotation_teams_quotation_id_teams_id_68eccdac_uniq UNIQUE (quotation_id, teams_id);


--
-- Name: quotations_quotationhistory_assigned_to quotations_quotationhist_quotationhistory_id_user_e478bf4f_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.quotations_quotationhistory_assigned_to
    ADD CONSTRAINT quotations_quotationhist_quotationhistory_id_user_e478bf4f_uniq UNIQUE (quotationhistory_id, user_id);


--
-- Name: quotations_quotationhistory_assigned_to quotations_quotationhistory_assigned_to_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.quotations_quotationhistory_assigned_to
    ADD CONSTRAINT quotations_quotationhistory_assigned_to_pkey PRIMARY KEY (id);


--
-- Name: quotations_quotationhistory quotations_quotationhistory_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.quotations_quotationhistory
    ADD CONSTRAINT quotations_quotationhistory_pkey PRIMARY KEY (id);


--
-- Name: rooms_room rooms_room_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rooms_room
    ADD CONSTRAINT rooms_room_pkey PRIMARY KEY (id);


--
-- Name: rooms_roomitem rooms_roomitem_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rooms_roomitem
    ADD CONSTRAINT rooms_roomitem_pkey PRIMARY KEY (id);


--
-- Name: rooms_roomproperty rooms_roomproperty_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rooms_roomproperty
    ADD CONSTRAINT rooms_roomproperty_pkey PRIMARY KEY (id);


--
-- Name: rooms_roomproperty rooms_roomproperty_symbol_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rooms_roomproperty
    ADD CONSTRAINT rooms_roomproperty_symbol_key UNIQUE (symbol);


--
-- Name: rooms_roomtype rooms_roomtype_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rooms_roomtype
    ADD CONSTRAINT rooms_roomtype_pkey PRIMARY KEY (id);


--
-- Name: rooms_roomtype_related_items rooms_roomtype_related_items_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rooms_roomtype_related_items
    ADD CONSTRAINT rooms_roomtype_related_items_pkey PRIMARY KEY (id);


--
-- Name: rooms_roomtype_related_items rooms_roomtype_related_items_roomtype_id_item_id_afec5bd2_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rooms_roomtype_related_items
    ADD CONSTRAINT rooms_roomtype_related_items_roomtype_id_item_id_afec5bd2_uniq UNIQUE (roomtype_id, item_id);


--
-- Name: rooms_roomtype_room_properties rooms_roomtype_room_prop_roomtype_id_roomproperty_9e8e5fb9_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rooms_roomtype_room_properties
    ADD CONSTRAINT rooms_roomtype_room_prop_roomtype_id_roomproperty_9e8e5fb9_uniq UNIQUE (roomtype_id, roomproperty_id);


--
-- Name: rooms_roomtype_room_properties rooms_roomtype_room_properties_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rooms_roomtype_room_properties
    ADD CONSTRAINT rooms_roomtype_room_properties_pkey PRIMARY KEY (id);


--
-- Name: rooms_roomtypeformula rooms_roomtypeformula_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rooms_roomtypeformula
    ADD CONSTRAINT rooms_roomtypeformula_pkey PRIMARY KEY (id);


--
-- Name: subscription_plans_companysubscribedplan subscription_plans_companysubscribedplan_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subscription_plans_companysubscribedplan
    ADD CONSTRAINT subscription_plans_companysubscribedplan_pkey PRIMARY KEY (id);


--
-- Name: subscription_plans_subscriptionplan subscription_plans_subscriptionplan_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subscription_plans_subscriptionplan
    ADD CONSTRAINT subscription_plans_subscriptionplan_pkey PRIMARY KEY (id);


--
-- Name: tasks_task_assigned_to tasks_task_assigned_to_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tasks_task_assigned_to
    ADD CONSTRAINT tasks_task_assigned_to_pkey PRIMARY KEY (id);


--
-- Name: tasks_task_assigned_to tasks_task_assigned_to_task_id_user_id_5e8e7fa1_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tasks_task_assigned_to
    ADD CONSTRAINT tasks_task_assigned_to_task_id_user_id_5e8e7fa1_uniq UNIQUE (task_id, user_id);


--
-- Name: tasks_task_contacts tasks_task_contacts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tasks_task_contacts
    ADD CONSTRAINT tasks_task_contacts_pkey PRIMARY KEY (id);


--
-- Name: tasks_task_contacts tasks_task_contacts_task_id_contact_id_7a2e8081_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tasks_task_contacts
    ADD CONSTRAINT tasks_task_contacts_task_id_contact_id_7a2e8081_uniq UNIQUE (task_id, contact_id);


--
-- Name: tasks_task tasks_task_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tasks_task
    ADD CONSTRAINT tasks_task_pkey PRIMARY KEY (id);


--
-- Name: tasks_task_teams tasks_task_teams_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tasks_task_teams
    ADD CONSTRAINT tasks_task_teams_pkey PRIMARY KEY (id);


--
-- Name: tasks_task_teams tasks_task_teams_task_id_teams_id_b550c90f_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tasks_task_teams
    ADD CONSTRAINT tasks_task_teams_task_id_teams_id_b550c90f_uniq UNIQUE (task_id, teams_id);


--
-- Name: teams_teams teams_teams_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.teams_teams
    ADD CONSTRAINT teams_teams_pkey PRIMARY KEY (id);


--
-- Name: teams_teams_users teams_teams_users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.teams_teams_users
    ADD CONSTRAINT teams_teams_users_pkey PRIMARY KEY (id);


--
-- Name: teams_teams_users teams_teams_users_teams_id_user_id_d2c2dd7b_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.teams_teams_users
    ADD CONSTRAINT teams_teams_users_teams_id_user_id_d2c2dd7b_uniq UNIQUE (teams_id, user_id);


--
-- Name: thumbnail_kvstore thumbnail_kvstore_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.thumbnail_kvstore
    ADD CONSTRAINT thumbnail_kvstore_pkey PRIMARY KEY (key);


--
-- Name: token_blacklist_blacklistedtoken token_blacklist_blacklistedtoken_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.token_blacklist_blacklistedtoken
    ADD CONSTRAINT token_blacklist_blacklistedtoken_pkey PRIMARY KEY (id);


--
-- Name: token_blacklist_blacklistedtoken token_blacklist_blacklistedtoken_token_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.token_blacklist_blacklistedtoken
    ADD CONSTRAINT token_blacklist_blacklistedtoken_token_id_key UNIQUE (token_id);


--
-- Name: token_blacklist_outstandingtoken token_blacklist_outstandingtoken_jti_hex_d9bdf6f7_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.token_blacklist_outstandingtoken
    ADD CONSTRAINT token_blacklist_outstandingtoken_jti_hex_d9bdf6f7_uniq UNIQUE (jti);


--
-- Name: token_blacklist_outstandingtoken token_blacklist_outstandingtoken_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.token_blacklist_outstandingtoken
    ADD CONSTRAINT token_blacklist_outstandingtoken_pkey PRIMARY KEY (id);


--
-- Name: accounts_account_assigned_to_account_id_7e994f48; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX accounts_account_assigned_to_account_id_7e994f48 ON public.accounts_account_assigned_to USING btree (account_id);


--
-- Name: accounts_account_assigned_to_user_id_407e8c4d; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX accounts_account_assigned_to_user_id_407e8c4d ON public.accounts_account_assigned_to USING btree (user_id);


--
-- Name: accounts_account_contacts_account_id_dd7706b6; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX accounts_account_contacts_account_id_dd7706b6 ON public.accounts_account_contacts USING btree (account_id);


--
-- Name: accounts_account_contacts_contact_id_1ebaea8d; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX accounts_account_contacts_contact_id_1ebaea8d ON public.accounts_account_contacts USING btree (contact_id);


--
-- Name: accounts_account_created_by_id_96988f15; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX accounts_account_created_by_id_96988f15 ON public.accounts_account USING btree (created_by_id);


--
-- Name: accounts_account_leads_id_9564d6bb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX accounts_account_leads_id_9564d6bb ON public.accounts_account USING btree (lead_id);


--
-- Name: accounts_account_name_1d0ba595_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX accounts_account_name_1d0ba595_like ON public.accounts_account USING btree (name varchar_pattern_ops);


--
-- Name: accounts_account_tags_account_id_3be82424; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX accounts_account_tags_account_id_3be82424 ON public.accounts_account_tags USING btree (account_id);


--
-- Name: accounts_account_tags_tags_id_78fe9bd2; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX accounts_account_tags_tags_id_78fe9bd2 ON public.accounts_account_tags USING btree (tags_id);


--
-- Name: accounts_account_teams_account_id_7be328bb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX accounts_account_teams_account_id_7be328bb ON public.accounts_account_teams USING btree (account_id);


--
-- Name: accounts_account_teams_teams_id_f8111d1e; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX accounts_account_teams_teams_id_f8111d1e ON public.accounts_account_teams USING btree (teams_id);


--
-- Name: accounts_email_recipients_contact_id_8b4d5e07; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX accounts_email_recipients_contact_id_8b4d5e07 ON public.accounts_email_recipients USING btree (contact_id);


--
-- Name: accounts_email_recipients_email_id_a9e1dba2; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX accounts_email_recipients_email_id_a9e1dba2 ON public.accounts_email_recipients USING btree (email_id);


--
-- Name: accounts_email_sender_id_56ba2c1d; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX accounts_email_sender_id_56ba2c1d ON public.accounts_email USING btree (from_account_id);


--
-- Name: accounts_emaillog_contact_id_10e17a75; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX accounts_emaillog_contact_id_10e17a75 ON public.accounts_emaillog USING btree (contact_id);


--
-- Name: accounts_emaillog_email_id_b252a46b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX accounts_emaillog_email_id_b252a46b ON public.accounts_emaillog USING btree (email_id);


--
-- Name: accounts_tags_slug_44e35c2f_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX accounts_tags_slug_44e35c2f_like ON public.accounts_tags USING btree (slug varchar_pattern_ops);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);


--
-- Name: cases_case_assigned_to_case_id_2e4863d1; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX cases_case_assigned_to_case_id_2e4863d1 ON public.cases_case_assigned_to USING btree (case_id);


--
-- Name: cases_case_assigned_to_user_id_475b56e3; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX cases_case_assigned_to_user_id_475b56e3 ON public.cases_case_assigned_to USING btree (user_id);


--
-- Name: cases_case_company_id_0d4c7ae8; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX cases_case_company_id_0d4c7ae8 ON public.cases_case USING btree (company_id);


--
-- Name: cases_case_contacts_case_id_76980f08; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX cases_case_contacts_case_id_76980f08 ON public.cases_case_contacts USING btree (case_id);


--
-- Name: cases_case_contacts_contact_id_b13062a2; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX cases_case_contacts_contact_id_b13062a2 ON public.cases_case_contacts USING btree (contact_id);


--
-- Name: cases_case_created_by_id_91d115ec; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX cases_case_created_by_id_91d115ec ON public.cases_case USING btree (created_by_id);


--
-- Name: cases_case_teams_case_id_18a51654; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX cases_case_teams_case_id_18a51654 ON public.cases_case_teams USING btree (case_id);


--
-- Name: cases_case_teams_teams_id_48201301; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX cases_case_teams_teams_id_48201301 ON public.cases_case_teams USING btree (teams_id);


--
-- Name: common_apisettings_created_by_id_98c6c22e; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX common_apisettings_created_by_id_98c6c22e ON public.common_apisettings USING btree (created_by_id);


--
-- Name: common_apisettings_lead_assigned_to_apisettings_id_bcb9b4d4; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX common_apisettings_lead_assigned_to_apisettings_id_bcb9b4d4 ON public.common_apisettings_lead_assigned_to USING btree (apisettings_id);


--
-- Name: common_apisettings_lead_assigned_to_user_id_0e624afc; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX common_apisettings_lead_assigned_to_user_id_0e624afc ON public.common_apisettings_lead_assigned_to USING btree (user_id);


--
-- Name: common_apisettings_tags_apisettings_id_37ac3e70; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX common_apisettings_tags_apisettings_id_37ac3e70 ON public.common_apisettings_tags USING btree (apisettings_id);


--
-- Name: common_apisettings_tags_tags_id_53f647a4; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX common_apisettings_tags_tags_id_53f647a4 ON public.common_apisettings_tags USING btree (tags_id);


--
-- Name: common_attachments_account_id_3ded5aec; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX common_attachments_account_id_3ded5aec ON public.common_attachments USING btree (account_id);


--
-- Name: common_attachments_case_id_9141eaa4; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX common_attachments_case_id_9141eaa4 ON public.common_attachments USING btree (case_id);


--
-- Name: common_attachments_company_id_c7ab9ceb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX common_attachments_company_id_c7ab9ceb ON public.common_attachments USING btree (company_id);


--
-- Name: common_attachments_contact_id_f32626af; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX common_attachments_contact_id_f32626af ON public.common_attachments USING btree (contact_id);


--
-- Name: common_attachments_created_by_id_de1aec79; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX common_attachments_created_by_id_de1aec79 ON public.common_attachments USING btree (created_by_id);


--
-- Name: common_attachments_event_id_a2570824; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX common_attachments_event_id_a2570824 ON public.common_attachments USING btree (event_id);


--
-- Name: common_attachments_lead_id_408ab6f8; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX common_attachments_lead_id_408ab6f8 ON public.common_attachments USING btree (lead_id);


--
-- Name: common_attachments_opportunity_id_55c921d1; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX common_attachments_opportunity_id_55c921d1 ON public.common_attachments USING btree (opportunity_id);


--
-- Name: common_attachments_quotation_id_a25eb41c; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX common_attachments_quotation_id_a25eb41c ON public.common_attachments USING btree (quotation_id);


--
-- Name: common_attachments_task_id_a2c58513; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX common_attachments_task_id_a2c58513 ON public.common_attachments USING btree (task_id);


--
-- Name: common_comment_account_id_dfaa7135; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX common_comment_account_id_dfaa7135 ON public.common_comment USING btree (account_id);


--
-- Name: common_comment_case_id_1869f987; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX common_comment_case_id_1869f987 ON public.common_comment USING btree (case_id);


--
-- Name: common_comment_commented_by_id_d25d4735; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX common_comment_commented_by_id_d25d4735 ON public.common_comment USING btree (commented_by_id);


--
-- Name: common_comment_company_id_69591727; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX common_comment_company_id_69591727 ON public.common_comment USING btree (company_id);


--
-- Name: common_comment_contact_id_5001da5f; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX common_comment_contact_id_5001da5f ON public.common_comment USING btree (contact_id);


--
-- Name: common_comment_event_id_743a165c; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX common_comment_event_id_743a165c ON public.common_comment USING btree (event_id);


--
-- Name: common_comment_files_comment_id_4a871ebd; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX common_comment_files_comment_id_4a871ebd ON public.common_comment_files USING btree (comment_id);


--
-- Name: common_comment_lead_id_a06ba983; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX common_comment_lead_id_a06ba983 ON public.common_comment USING btree (lead_id);


--
-- Name: common_comment_opportunity_id_69135f56; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX common_comment_opportunity_id_69135f56 ON public.common_comment USING btree (opportunity_id);


--
-- Name: common_comment_quotation_id_a57d7341; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX common_comment_quotation_id_a57d7341 ON public.common_comment USING btree (quotation_id);


--
-- Name: common_comment_task_id_4d5c683f; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX common_comment_task_id_4d5c683f ON public.common_comment USING btree (task_id);


--
-- Name: common_comment_user_id_06e537fc; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX common_comment_user_id_06e537fc ON public.common_comment USING btree (user_id);


--
-- Name: common_document_created_by_id_19742726; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX common_document_created_by_id_19742726 ON public.common_document USING btree (created_by_id);


--
-- Name: common_document_shared_to_document_id_f5146fd1; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX common_document_shared_to_document_id_f5146fd1 ON public.common_document_shared_to USING btree (document_id);


--
-- Name: common_document_shared_to_user_id_09ae644f; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX common_document_shared_to_user_id_09ae644f ON public.common_document_shared_to USING btree (user_id);


--
-- Name: common_document_teams_document_id_494fb8a5; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX common_document_teams_document_id_494fb8a5 ON public.common_document_teams USING btree (document_id);


--
-- Name: common_document_teams_teams_id_17146b17; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX common_document_teams_teams_id_17146b17 ON public.common_document_teams USING btree (teams_id);


--
-- Name: common_google_email_cc75d7a4; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX common_google_email_cc75d7a4 ON public.common_google USING btree (email);


--
-- Name: common_google_email_cc75d7a4_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX common_google_email_cc75d7a4_like ON public.common_google USING btree (email varchar_pattern_ops);


--
-- Name: common_google_user_id_83499ce5; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX common_google_user_id_83499ce5 ON public.common_google USING btree (user_id);


--
-- Name: common_user_groups_group_id_27a26245; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX common_user_groups_group_id_27a26245 ON public.common_user_groups USING btree (group_id);


--
-- Name: common_user_groups_user_id_92ddbe7a; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX common_user_groups_user_id_92ddbe7a ON public.common_user_groups USING btree (user_id);


--
-- Name: common_user_phone_c2121075_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX common_user_phone_c2121075_like ON public.common_user USING btree (phone varchar_pattern_ops);


--
-- Name: common_user_user_permissions_permission_id_a6da427c; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX common_user_user_permissions_permission_id_a6da427c ON public.common_user_user_permissions USING btree (permission_id);


--
-- Name: common_user_user_permissions_user_id_56b84879; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX common_user_user_permissions_user_id_56b84879 ON public.common_user_user_permissions USING btree (user_id);


--
-- Name: common_user_username_01dcd042_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX common_user_username_01dcd042_like ON public.common_user USING btree (username varchar_pattern_ops);


--
-- Name: companies_company_created_by_id_5b37702d; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX companies_company_created_by_id_5b37702d ON public.companies_company USING btree (created_by_id);


--
-- Name: companies_company_tags_company_id_bbf3f023; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX companies_company_tags_company_id_bbf3f023 ON public.companies_company_tags USING btree (company_id);


--
-- Name: companies_company_tags_tags_id_4e1b5d55; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX companies_company_tags_tags_id_4e1b5d55 ON public.companies_company_tags USING btree (tags_id);


--
-- Name: companies_email_from_company_id_99e7e9b5; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX companies_email_from_company_id_99e7e9b5 ON public.companies_email USING btree (from_company_id);


--
-- Name: companies_email_recipients_contact_id_05992f87; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX companies_email_recipients_contact_id_05992f87 ON public.companies_email_recipients USING btree (contact_id);


--
-- Name: companies_email_recipients_email_id_34cd5058; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX companies_email_recipients_email_id_34cd5058 ON public.companies_email_recipients USING btree (email_id);


--
-- Name: companies_emaillog_contact_id_c2c70d83; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX companies_emaillog_contact_id_c2c70d83 ON public.companies_emaillog USING btree (contact_id);


--
-- Name: companies_emaillog_email_id_f1540de3; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX companies_emaillog_email_id_f1540de3 ON public.companies_emaillog USING btree (email_id);


--
-- Name: companies_invoicegeneralremark_company_id_8e90bf7d; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX companies_invoicegeneralremark_company_id_8e90bf7d ON public.companies_invoicegeneralremark USING btree (company_id);


--
-- Name: companies_quotationgeneralremark_company_id_586c34c5; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX companies_quotationgeneralremark_company_id_586c34c5 ON public.companies_quotationgeneralremark USING btree (company_id);


--
-- Name: companies_receiptgeneralremark_company_id_a6d8e6af; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX companies_receiptgeneralremark_company_id_a6d8e6af ON public.companies_receiptgeneralremark USING btree (company_id);


--
-- Name: companies_tags_slug_cdaf2751_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX companies_tags_slug_cdaf2751_like ON public.companies_tags USING btree (slug varchar_pattern_ops);


--
-- Name: contacts_contact_address_id_0dbb18a0; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX contacts_contact_address_id_0dbb18a0 ON public.contacts_contact USING btree (address_id);


--
-- Name: contacts_contact_assigned_to_contact_id_0269bc5d; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX contacts_contact_assigned_to_contact_id_0269bc5d ON public.contacts_contact_assigned_to USING btree (contact_id);


--
-- Name: contacts_contact_assigned_to_user_id_727306dd; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX contacts_contact_assigned_to_user_id_727306dd ON public.contacts_contact_assigned_to USING btree (user_id);


--
-- Name: contacts_contact_created_by_id_57537352; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX contacts_contact_created_by_id_57537352 ON public.contacts_contact USING btree (created_by_id);


--
-- Name: contacts_contact_email_b008e8f9_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX contacts_contact_email_b008e8f9_like ON public.contacts_contact USING btree (email varchar_pattern_ops);


--
-- Name: contacts_contact_phone_2a8bc2d8_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX contacts_contact_phone_2a8bc2d8_like ON public.contacts_contact USING btree (phone varchar_pattern_ops);


--
-- Name: contacts_contact_teams_contact_id_76009c86; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX contacts_contact_teams_contact_id_76009c86 ON public.contacts_contact_teams USING btree (contact_id);


--
-- Name: contacts_contact_teams_teams_id_b69a29e7; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX contacts_contact_teams_teams_id_b69a29e7 ON public.contacts_contact_teams USING btree (teams_id);


--
-- Name: customers_customer_created_by_id_e3e9e010; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX customers_customer_created_by_id_e3e9e010 ON public.customers_customer USING btree (created_by_id);


--
-- Name: django_admin_log_content_type_id_c4bce8eb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id_c564eba6; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);


--
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: events_event_assigned_to_event_id_211aebd2; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX events_event_assigned_to_event_id_211aebd2 ON public.events_event_assigned_to USING btree (event_id);


--
-- Name: events_event_assigned_to_user_id_88f9a1f0; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX events_event_assigned_to_user_id_88f9a1f0 ON public.events_event_assigned_to USING btree (user_id);


--
-- Name: events_event_contacts_contact_id_de30d576; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX events_event_contacts_contact_id_de30d576 ON public.events_event_contacts USING btree (contact_id);


--
-- Name: events_event_contacts_event_id_3da8569b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX events_event_contacts_event_id_3da8569b ON public.events_event_contacts USING btree (event_id);


--
-- Name: events_event_created_by_id_2c28ea90; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX events_event_created_by_id_2c28ea90 ON public.events_event USING btree (created_by_id);


--
-- Name: events_event_teams_event_id_ebaa210d; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX events_event_teams_event_id_ebaa210d ON public.events_event_teams USING btree (event_id);


--
-- Name: events_event_teams_teams_id_8c21a9a0; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX events_event_teams_teams_id_8c21a9a0 ON public.events_event_teams USING btree (teams_id);


--
-- Name: function_items_functionitem_approved_by_id_02875902; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX function_items_functionitem_approved_by_id_02875902 ON public.function_items_functionitem USING btree (approved_by_id);


--
-- Name: function_items_functionitem_created_by_id_5f94ff8b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX function_items_functionitem_created_by_id_5f94ff8b ON public.function_items_functionitem USING btree (created_by_id);


--
-- Name: function_items_functionitem_last_updated_by_id_6ba5a432; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX function_items_functionitem_last_updated_by_id_6ba5a432 ON public.function_items_functionitem USING btree (last_updated_by_id);


--
-- Name: function_items_functionitemhistory_function_item_id_2e6850d2; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX function_items_functionitemhistory_function_item_id_2e6850d2 ON public.function_items_functionitemhistory USING btree (function_item_id);


--
-- Name: function_items_functionitemhistory_updated_by_id_3afbe02a; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX function_items_functionitemhistory_updated_by_id_3afbe02a ON public.function_items_functionitemhistory USING btree (updated_by_id);


--
-- Name: function_items_subfunction_related_function_item_id_8f2bd2de; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX function_items_subfunction_related_function_item_id_8f2bd2de ON public.function_items_subfunctionitem USING btree (related_function_item_id);


--
-- Name: function_items_subfunction_sub_function_item_id_b176cb95; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX function_items_subfunction_sub_function_item_id_b176cb95 ON public.function_items_subfunctionitemhistory USING btree (sub_function_item_id);


--
-- Name: function_items_subfunctionitem_approved_by_id_c2f3ab62; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX function_items_subfunctionitem_approved_by_id_c2f3ab62 ON public.function_items_subfunctionitem USING btree (approved_by_id);


--
-- Name: function_items_subfunctionitem_created_by_id_a5121cb9; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX function_items_subfunctionitem_created_by_id_a5121cb9 ON public.function_items_subfunctionitem USING btree (created_by_id);


--
-- Name: function_items_subfunctionitem_last_updated_by_id_01e35040; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX function_items_subfunctionitem_last_updated_by_id_01e35040 ON public.function_items_subfunctionitem USING btree (last_updated_by_id);


--
-- Name: function_items_subfunctionitemhistory_updated_by_id_c4614a1f; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX function_items_subfunctionitemhistory_updated_by_id_c4614a1f ON public.function_items_subfunctionitemhistory USING btree (updated_by_id);


--
-- Name: invoices_invoice_assigned_to_invoice_id_8b0ff865; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX invoices_invoice_assigned_to_invoice_id_8b0ff865 ON public.invoices_invoice_assigned_to USING btree (invoice_id);


--
-- Name: invoices_invoice_assigned_to_user_id_0aa3df96; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX invoices_invoice_assigned_to_user_id_0aa3df96 ON public.invoices_invoice_assigned_to USING btree (user_id);


--
-- Name: invoices_invoice_companies_company_id_ab7d6e05; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX invoices_invoice_companies_company_id_ab7d6e05 ON public.invoices_invoice_companies USING btree (company_id);


--
-- Name: invoices_invoice_companies_invoice_id_2a580af9; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX invoices_invoice_companies_invoice_id_2a580af9 ON public.invoices_invoice_companies USING btree (invoice_id);


--
-- Name: invoices_invoice_created_by_id_9b878bcd; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX invoices_invoice_created_by_id_9b878bcd ON public.invoices_invoice USING btree (created_by_id);


--
-- Name: invoices_invoice_from_address_id_c42db748; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX invoices_invoice_from_address_id_c42db748 ON public.invoices_invoice USING btree (from_address_id);


--
-- Name: invoices_invoice_teams_invoice_id_a15c151f; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX invoices_invoice_teams_invoice_id_a15c151f ON public.invoices_invoice_teams USING btree (invoice_id);


--
-- Name: invoices_invoice_teams_teams_id_b51618e6; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX invoices_invoice_teams_teams_id_b51618e6 ON public.invoices_invoice_teams USING btree (teams_id);


--
-- Name: invoices_invoice_to_address_id_d9360206; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX invoices_invoice_to_address_id_d9360206 ON public.invoices_invoice USING btree (to_address_id);


--
-- Name: invoices_invoicehistory_assigned_to_invoicehistory_id_02417412; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX invoices_invoicehistory_assigned_to_invoicehistory_id_02417412 ON public.invoices_invoicehistory_assigned_to USING btree (invoicehistory_id);


--
-- Name: invoices_invoicehistory_assigned_to_user_id_7b1e7786; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX invoices_invoicehistory_assigned_to_user_id_7b1e7786 ON public.invoices_invoicehistory_assigned_to USING btree (user_id);


--
-- Name: invoices_invoicehistory_from_address_id_cffac1b5; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX invoices_invoicehistory_from_address_id_cffac1b5 ON public.invoices_invoicehistory USING btree (from_address_id);


--
-- Name: invoices_invoicehistory_invoice_id_05ee6eb8; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX invoices_invoicehistory_invoice_id_05ee6eb8 ON public.invoices_invoicehistory USING btree (invoice_id);


--
-- Name: invoices_invoicehistory_to_address_id_492fbb02; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX invoices_invoicehistory_to_address_id_492fbb02 ON public.invoices_invoicehistory USING btree (to_address_id);


--
-- Name: invoices_invoicehistory_updated_by_id_2ccd68d8; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX invoices_invoicehistory_updated_by_id_2ccd68d8 ON public.invoices_invoicehistory USING btree (updated_by_id);


--
-- Name: leads_lead_assigned_to_lead_id_b43e64b4; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX leads_lead_assigned_to_lead_id_b43e64b4 ON public.leads_lead_assigned_to USING btree (lead_id);


--
-- Name: leads_lead_assigned_to_user_id_e9de5cbf; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX leads_lead_assigned_to_user_id_e9de5cbf ON public.leads_lead_assigned_to USING btree (user_id);


--
-- Name: leads_lead_contacts_contact_id_643d700d; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX leads_lead_contacts_contact_id_643d700d ON public.leads_lead_contacts USING btree (contact_id);


--
-- Name: leads_lead_contacts_lead_id_e9cd308e; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX leads_lead_contacts_lead_id_e9cd308e ON public.leads_lead_contacts USING btree (lead_id);


--
-- Name: leads_lead_created_by_id_bd2e8097; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX leads_lead_created_by_id_bd2e8097 ON public.leads_lead USING btree (created_by_id);


--
-- Name: leads_lead_teams_lead_id_fb912735; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX leads_lead_teams_lead_id_fb912735 ON public.leads_lead_teams USING btree (lead_id);


--
-- Name: leads_lead_teams_teams_id_9753bcb3; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX leads_lead_teams_teams_id_9753bcb3 ON public.leads_lead_teams USING btree (teams_id);


--
-- Name: marketing_blockeddomain_created_by_id_a4cbe960; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX marketing_blockeddomain_created_by_id_a4cbe960 ON public.marketing_blockeddomain USING btree (created_by_id);


--
-- Name: marketing_blockedemail_created_by_id_7f859478; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX marketing_blockedemail_created_by_id_7f859478 ON public.marketing_blockedemail USING btree (created_by_id);


--
-- Name: marketing_campaign_contact_lists_campaign_id_47b7ad3f; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX marketing_campaign_contact_lists_campaign_id_47b7ad3f ON public.marketing_campaign_contact_lists USING btree (campaign_id);


--
-- Name: marketing_campaign_contact_lists_contactlist_id_f870c4d0; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX marketing_campaign_contact_lists_contactlist_id_f870c4d0 ON public.marketing_campaign_contact_lists USING btree (contactlist_id);


--
-- Name: marketing_campaign_created_by_id_c4d2ec89; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX marketing_campaign_created_by_id_c4d2ec89 ON public.marketing_campaign USING btree (created_by_id);


--
-- Name: marketing_campaign_email_template_id_16ed1ee5; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX marketing_campaign_email_template_id_16ed1ee5 ON public.marketing_campaign USING btree (email_template_id);


--
-- Name: marketing_campaign_tags_campaign_id_4a5b98e2; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX marketing_campaign_tags_campaign_id_4a5b98e2 ON public.marketing_campaign_tags USING btree (campaign_id);


--
-- Name: marketing_campaign_tags_tag_id_973530fe; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX marketing_campaign_tags_tag_id_973530fe ON public.marketing_campaign_tags USING btree (tag_id);


--
-- Name: marketing_campaignlinkclick_campaign_id_bad5722a; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX marketing_campaignlinkclick_campaign_id_bad5722a ON public.marketing_campaignlinkclick USING btree (campaign_id);


--
-- Name: marketing_campaignlinkclick_contact_id_a20f4980; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX marketing_campaignlinkclick_contact_id_a20f4980 ON public.marketing_campaignlinkclick USING btree (contact_id);


--
-- Name: marketing_campaignlinkclick_link_id_df848b66; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX marketing_campaignlinkclick_link_id_df848b66 ON public.marketing_campaignlinkclick USING btree (link_id);


--
-- Name: marketing_campaignlog_campaign_id_0a5d9b5a; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX marketing_campaignlog_campaign_id_0a5d9b5a ON public.marketing_campaignlog USING btree (campaign_id);


--
-- Name: marketing_campaignlog_contact_id_757a80df; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX marketing_campaignlog_contact_id_757a80df ON public.marketing_campaignlog USING btree (contact_id);


--
-- Name: marketing_campaignopen_campaign_id_18fc81d4; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX marketing_campaignopen_campaign_id_18fc81d4 ON public.marketing_campaignopen USING btree (campaign_id);


--
-- Name: marketing_campaignopen_contact_id_f1813fb0; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX marketing_campaignopen_contact_id_f1813fb0 ON public.marketing_campaignopen USING btree (contact_id);


--
-- Name: marketing_contact_contact_list_contact_id_23181bed; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX marketing_contact_contact_list_contact_id_23181bed ON public.marketing_contact_contact_list USING btree (contact_id);


--
-- Name: marketing_contact_contact_list_contactlist_id_51f313b1; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX marketing_contact_contact_list_contactlist_id_51f313b1 ON public.marketing_contact_contact_list USING btree (contactlist_id);


--
-- Name: marketing_contact_created_by_id_c5fc4040; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX marketing_contact_created_by_id_c5fc4040 ON public.marketing_contact USING btree (created_by_id);


--
-- Name: marketing_contactemailcampaign_created_by_id_49bdc16d; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX marketing_contactemailcampaign_created_by_id_49bdc16d ON public.marketing_contactemailcampaign USING btree (created_by_id);


--
-- Name: marketing_contactlist_created_by_id_ca6d9a00; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX marketing_contactlist_created_by_id_ca6d9a00 ON public.marketing_contactlist USING btree (created_by_id);


--
-- Name: marketing_contactlist_tags_contactlist_id_d5b1120c; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX marketing_contactlist_tags_contactlist_id_d5b1120c ON public.marketing_contactlist_tags USING btree (contactlist_id);


--
-- Name: marketing_contactlist_tags_tag_id_d2d98941; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX marketing_contactlist_tags_tag_id_d2d98941 ON public.marketing_contactlist_tags USING btree (tag_id);


--
-- Name: marketing_contactlist_visible_to_contactlist_id_239ee189; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX marketing_contactlist_visible_to_contactlist_id_239ee189 ON public.marketing_contactlist_visible_to USING btree (contactlist_id);


--
-- Name: marketing_contactlist_visible_to_user_id_55499a9a; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX marketing_contactlist_visible_to_user_id_55499a9a ON public.marketing_contactlist_visible_to USING btree (user_id);


--
-- Name: marketing_contactunsubscribedcampaign_campaigns_id_631325bd; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX marketing_contactunsubscribedcampaign_campaigns_id_631325bd ON public.marketing_contactunsubscribedcampaign USING btree (campaigns_id);


--
-- Name: marketing_contactunsubscribedcampaign_contacts_id_0a7bbbe4; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX marketing_contactunsubscribedcampaign_contacts_id_0a7bbbe4 ON public.marketing_contactunsubscribedcampaign USING btree (contacts_id);


--
-- Name: marketing_duplicatecontacts_contact_list_id_eb57a05e; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX marketing_duplicatecontacts_contact_list_id_eb57a05e ON public.marketing_duplicatecontacts USING btree (contact_list_id);


--
-- Name: marketing_duplicatecontacts_contacts_id_0cd30367; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX marketing_duplicatecontacts_contacts_id_0cd30367 ON public.marketing_duplicatecontacts USING btree (contacts_id);


--
-- Name: marketing_emailtemplate_created_by_id_6641e947; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX marketing_emailtemplate_created_by_id_6641e947 ON public.marketing_emailtemplate USING btree (created_by_id);


--
-- Name: marketing_failedcontact_contact_list_contactlist_id_0774af5c; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX marketing_failedcontact_contact_list_contactlist_id_0774af5c ON public.marketing_failedcontact_contact_list USING btree (contactlist_id);


--
-- Name: marketing_failedcontact_contact_list_failedcontact_id_2ec42ab1; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX marketing_failedcontact_contact_list_failedcontact_id_2ec42ab1 ON public.marketing_failedcontact_contact_list USING btree (failedcontact_id);


--
-- Name: marketing_failedcontact_created_by_id_69df0cfc; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX marketing_failedcontact_created_by_id_69df0cfc ON public.marketing_failedcontact USING btree (created_by_id);


--
-- Name: marketing_link_campaign_id_87874449; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX marketing_link_campaign_id_87874449 ON public.marketing_link USING btree (campaign_id);


--
-- Name: marketing_tag_created_by_id_e0e8f0cb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX marketing_tag_created_by_id_e0e8f0cb ON public.marketing_tag USING btree (created_by_id);


--
-- Name: opportunity_opportunity_assigned_to_opportunity_id_1c8df51a; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX opportunity_opportunity_assigned_to_opportunity_id_1c8df51a ON public.opportunity_opportunity_assigned_to USING btree (opportunity_id);


--
-- Name: opportunity_opportunity_assigned_to_user_id_ce65565d; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX opportunity_opportunity_assigned_to_user_id_ce65565d ON public.opportunity_opportunity_assigned_to USING btree (user_id);


--
-- Name: opportunity_opportunity_closed_by_id_7399917f; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX opportunity_opportunity_closed_by_id_7399917f ON public.opportunity_opportunity USING btree (closed_by_id);


--
-- Name: opportunity_opportunity_company_id_dde6fcb8; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX opportunity_opportunity_company_id_dde6fcb8 ON public.opportunity_opportunity USING btree (company_id);


--
-- Name: opportunity_opportunity_contacts_contact_id_64ee0712; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX opportunity_opportunity_contacts_contact_id_64ee0712 ON public.opportunity_opportunity_contacts USING btree (contact_id);


--
-- Name: opportunity_opportunity_contacts_opportunity_id_01fbf845; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX opportunity_opportunity_contacts_opportunity_id_01fbf845 ON public.opportunity_opportunity_contacts USING btree (opportunity_id);


--
-- Name: opportunity_opportunity_created_by_id_89d5f804; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX opportunity_opportunity_created_by_id_89d5f804 ON public.opportunity_opportunity USING btree (created_by_id);


--
-- Name: opportunity_opportunity_tags_opportunity_id_98683361; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX opportunity_opportunity_tags_opportunity_id_98683361 ON public.opportunity_opportunity_tags USING btree (opportunity_id);


--
-- Name: opportunity_opportunity_tags_tags_id_89b307a4; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX opportunity_opportunity_tags_tags_id_89b307a4 ON public.opportunity_opportunity_tags USING btree (tags_id);


--
-- Name: opportunity_opportunity_teams_opportunity_id_81eab463; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX opportunity_opportunity_teams_opportunity_id_81eab463 ON public.opportunity_opportunity_teams USING btree (opportunity_id);


--
-- Name: opportunity_opportunity_teams_teams_id_4f8d4a54; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX opportunity_opportunity_teams_teams_id_4f8d4a54 ON public.opportunity_opportunity_teams USING btree (teams_id);


--
-- Name: planner_event_assigned_to_event_id_467b0d2b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX planner_event_assigned_to_event_id_467b0d2b ON public.planner_event_assigned_to USING btree (event_id);


--
-- Name: planner_event_assigned_to_user_id_3d65f14a; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX planner_event_assigned_to_user_id_3d65f14a ON public.planner_event_assigned_to USING btree (user_id);


--
-- Name: planner_event_attendees_contacts_contact_id_2c29dbd4; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX planner_event_attendees_contacts_contact_id_2c29dbd4 ON public.planner_event_attendees_contacts USING btree (contact_id);


--
-- Name: planner_event_attendees_contacts_event_id_7a6e26bc; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX planner_event_attendees_contacts_event_id_7a6e26bc ON public.planner_event_attendees_contacts USING btree (event_id);


--
-- Name: planner_event_attendees_leads_event_id_05e9c4f9; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX planner_event_attendees_leads_event_id_05e9c4f9 ON public.planner_event_attendees_leads USING btree (event_id);


--
-- Name: planner_event_attendees_leads_lead_id_b543353a; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX planner_event_attendees_leads_lead_id_b543353a ON public.planner_event_attendees_leads USING btree (lead_id);


--
-- Name: planner_event_attendees_user_event_id_f806e2a6; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX planner_event_attendees_user_event_id_f806e2a6 ON public.planner_event_attendees_user USING btree (event_id);


--
-- Name: planner_event_attendees_user_user_id_d6b53a5e; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX planner_event_attendees_user_user_id_d6b53a5e ON public.planner_event_attendees_user USING btree (user_id);


--
-- Name: planner_event_content_type_id_e1697281; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX planner_event_content_type_id_e1697281 ON public.planner_event USING btree (content_type_id);


--
-- Name: planner_event_created_by_id_ff507edf; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX planner_event_created_by_id_ff507edf ON public.planner_event USING btree (created_by_id);


--
-- Name: planner_event_reminders_event_id_9c33650c; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX planner_event_reminders_event_id_9c33650c ON public.planner_event_reminders USING btree (event_id);


--
-- Name: planner_event_reminders_reminder_id_a980f736; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX planner_event_reminders_reminder_id_a980f736 ON public.planner_event_reminders USING btree (reminder_id);


--
-- Name: planner_event_updated_by_id_1a3b400a; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX planner_event_updated_by_id_1a3b400a ON public.planner_event USING btree (updated_by_id);


--
-- Name: project_expenses_projectexpend_project_id_bb8f9d07; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX project_expenses_projectexpend_project_id_bb8f9d07 ON public.project_expenses_projectexpense USING btree (project_id);


--
-- Name: project_expenses_projectexpense_expense_type_id_055551ef; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX project_expenses_projectexpense_expense_type_id_055551ef ON public.project_expenses_projectexpense USING btree (expense_type_id);


--
-- Name: project_items_item_item_properties_item_id_94cb7d40; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX project_items_item_item_properties_item_id_94cb7d40 ON public.project_items_item_item_properties USING btree (item_id);


--
-- Name: project_items_item_item_properties_itemproperty_id_ce36b063; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX project_items_item_item_properties_itemproperty_id_ce36b063 ON public.project_items_item_item_properties USING btree (itemproperty_id);


--
-- Name: project_items_item_item_type_id_547d8eba; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX project_items_item_item_type_id_547d8eba ON public.project_items_item USING btree (item_type_id);


--
-- Name: project_items_itemformula_item_id_c9ba87fc; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX project_items_itemformula_item_id_c9ba87fc ON public.project_items_itemformula USING btree (item_id);


--
-- Name: project_items_itemproperty_symbol_a2edada6_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX project_items_itemproperty_symbol_a2edada6_like ON public.project_items_itemproperty USING btree (symbol varchar_pattern_ops);


--
-- Name: project_items_itemtypematerial_item_type_id_e402a683; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX project_items_itemtypematerial_item_type_id_e402a683 ON public.project_items_itemtypematerial USING btree (item_type_id);


--
-- Name: project_misc_projectmisc_misc_id_64c4a54b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX project_misc_projectmisc_misc_id_64c4a54b ON public.project_misc_projectmisc USING btree (misc_id);


--
-- Name: project_misc_projectmisc_project_id_2b8485b5; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX project_misc_projectmisc_project_id_2b8485b5 ON public.project_misc_projectmisc USING btree (project_id);


--
-- Name: project_timetable_projectmilestone_project_id_319ea6aa; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX project_timetable_projectmilestone_project_id_319ea6aa ON public.project_timetable_projectmilestone USING btree (project_id);


--
-- Name: project_timetable_projectwork_project_id_7b7200d0; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX project_timetable_projectwork_project_id_7b7200d0 ON public.project_timetable_projectwork USING btree (project_id);


--
-- Name: projects_companyprojectcom_companyprojectcomparison_i_73145583; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX projects_companyprojectcom_companyprojectcomparison_i_73145583 ON public.projects_companyprojectcomparison_projects USING btree (companyprojectcomparison_id);


--
-- Name: projects_companyprojectcomparison_projects_project_id_b6cfd7c7; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX projects_companyprojectcomparison_projects_project_id_b6cfd7c7 ON public.projects_companyprojectcomparison_projects USING btree (project_id);


--
-- Name: projects_project_company_id_66b5c58b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX projects_project_company_id_66b5c58b ON public.projects_project USING btree (company_id);


--
-- Name: projects_project_created_by_id_c49d7b6d; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX projects_project_created_by_id_c49d7b6d ON public.projects_project USING btree (created_by_id);


--
-- Name: projects_projecthistory_assigned_to_projecthistory_id_d6490520; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX projects_projecthistory_assigned_to_projecthistory_id_d6490520 ON public.projects_projecthistory_assigned_to USING btree (projecthistory_id);


--
-- Name: projects_projecthistory_assigned_to_user_id_6d816790; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX projects_projecthistory_assigned_to_user_id_6d816790 ON public.projects_projecthistory_assigned_to USING btree (user_id);


--
-- Name: projects_projecthistory_from_address_id_ae28216a; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX projects_projecthistory_from_address_id_ae28216a ON public.projects_projecthistory USING btree (from_address_id);


--
-- Name: projects_projecthistory_project_id_2bbe7236; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX projects_projecthistory_project_id_2bbe7236 ON public.projects_projecthistory USING btree (project_id);


--
-- Name: projects_projecthistory_to_address_id_a3022acd; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX projects_projecthistory_to_address_id_a3022acd ON public.projects_projecthistory USING btree (to_address_id);


--
-- Name: projects_projecthistory_updated_by_id_3ca3d6b3; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX projects_projecthistory_updated_by_id_3ca3d6b3 ON public.projects_projecthistory USING btree (updated_by_id);


--
-- Name: projects_projectimage_related_project_id_d9c75c44; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX projects_projectimage_related_project_id_d9c75c44 ON public.projects_projectimage USING btree (related_project_id);


--
-- Name: projects_projectimageset_imgs_projectimage_id_b6ebbc55; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX projects_projectimageset_imgs_projectimage_id_b6ebbc55 ON public.projects_projectimageset_imgs USING btree (projectimage_id);


--
-- Name: projects_projectimageset_imgs_projectimageset_id_f87d1b7e; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX projects_projectimageset_imgs_projectimageset_id_f87d1b7e ON public.projects_projectimageset_imgs USING btree (projectimageset_id);


--
-- Name: projects_projectimageset_related_project_id_1e8f4d16; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX projects_projectimageset_related_project_id_1e8f4d16 ON public.projects_projectimageset USING btree (related_project_id);


--
-- Name: projects_projectinvoice_project_id_7ebf8b67; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX projects_projectinvoice_project_id_7ebf8b67 ON public.projects_projectinvoice USING btree (project_id);


--
-- Name: projects_projectreceipt_project_id_437bb88a; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX projects_projectreceipt_project_id_437bb88a ON public.projects_projectreceipt USING btree (project_id);


--
-- Name: quotations_quotation_approved_by_id_5c8a042e; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX quotations_quotation_approved_by_id_5c8a042e ON public.quotations_quotation USING btree (approved_by_id);


--
-- Name: quotations_quotation_assigned_to_quotation_id_47354fdf; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX quotations_quotation_assigned_to_quotation_id_47354fdf ON public.quotations_quotation_assigned_to USING btree (quotation_id);


--
-- Name: quotations_quotation_assigned_to_user_id_7af1c95f; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX quotations_quotation_assigned_to_user_id_7af1c95f ON public.quotations_quotation_assigned_to USING btree (user_id);


--
-- Name: quotations_quotation_companies_company_id_0493e81f; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX quotations_quotation_companies_company_id_0493e81f ON public.quotations_quotation_companies USING btree (company_id);


--
-- Name: quotations_quotation_companies_quotation_id_57749bb7; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX quotations_quotation_companies_quotation_id_57749bb7 ON public.quotations_quotation_companies USING btree (quotation_id);


--
-- Name: quotations_quotation_created_by_id_f86a7566; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX quotations_quotation_created_by_id_f86a7566 ON public.quotations_quotation USING btree (created_by_id);


--
-- Name: quotations_quotation_from_address_id_c5ab9397; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX quotations_quotation_from_address_id_c5ab9397 ON public.quotations_quotation USING btree (from_address_id);


--
-- Name: quotations_quotation_last_updated_by_id_0ad36aaa; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX quotations_quotation_last_updated_by_id_0ad36aaa ON public.quotations_quotation USING btree (last_updated_by_id);


--
-- Name: quotations_quotation_teams_quotation_id_40df249e; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX quotations_quotation_teams_quotation_id_40df249e ON public.quotations_quotation_teams USING btree (quotation_id);


--
-- Name: quotations_quotation_teams_teams_id_1a13ccfe; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX quotations_quotation_teams_teams_id_1a13ccfe ON public.quotations_quotation_teams USING btree (teams_id);


--
-- Name: quotations_quotation_to_address_id_5047eb68; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX quotations_quotation_to_address_id_5047eb68 ON public.quotations_quotation USING btree (to_address_id);


--
-- Name: quotations_quotationhistor_quotationhistory_id_adf697b4; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX quotations_quotationhistor_quotationhistory_id_adf697b4 ON public.quotations_quotationhistory_assigned_to USING btree (quotationhistory_id);


--
-- Name: quotations_quotationhistory_assigned_to_user_id_05a80596; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX quotations_quotationhistory_assigned_to_user_id_05a80596 ON public.quotations_quotationhistory_assigned_to USING btree (user_id);


--
-- Name: quotations_quotationhistory_from_address_id_95f05125; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX quotations_quotationhistory_from_address_id_95f05125 ON public.quotations_quotationhistory USING btree (from_address_id);


--
-- Name: quotations_quotationhistory_quotation_id_da50d945; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX quotations_quotationhistory_quotation_id_da50d945 ON public.quotations_quotationhistory USING btree (quotation_id);


--
-- Name: quotations_quotationhistory_to_address_id_e224b1e3; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX quotations_quotationhistory_to_address_id_e224b1e3 ON public.quotations_quotationhistory USING btree (to_address_id);


--
-- Name: quotations_quotationhistory_updated_by_id_d4b10b58; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX quotations_quotationhistory_updated_by_id_d4b10b58 ON public.quotations_quotationhistory USING btree (updated_by_id);


--
-- Name: rooms_room_related_project_id_520c6c88; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX rooms_room_related_project_id_520c6c88 ON public.rooms_room USING btree (related_project_id);


--
-- Name: rooms_room_type_id_90dc2bc9; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX rooms_room_type_id_90dc2bc9 ON public.rooms_room USING btree (room_type_id);


--
-- Name: rooms_roomitem_item_id_474eaabc; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX rooms_roomitem_item_id_474eaabc ON public.rooms_roomitem USING btree (item_id);


--
-- Name: rooms_roomitem_room_id_184c0f52; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX rooms_roomitem_room_id_184c0f52 ON public.rooms_roomitem USING btree (room_id);


--
-- Name: rooms_roomproperty_symbol_9301e596_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX rooms_roomproperty_symbol_9301e596_like ON public.rooms_roomproperty USING btree (symbol varchar_pattern_ops);


--
-- Name: rooms_roomtype_related_items_item_id_b808a064; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX rooms_roomtype_related_items_item_id_b808a064 ON public.rooms_roomtype_related_items USING btree (item_id);


--
-- Name: rooms_roomtype_related_items_roomtype_id_79027218; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX rooms_roomtype_related_items_roomtype_id_79027218 ON public.rooms_roomtype_related_items USING btree (roomtype_id);


--
-- Name: rooms_roomtype_room_properties_roomproperty_id_34f8a1e2; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX rooms_roomtype_room_properties_roomproperty_id_34f8a1e2 ON public.rooms_roomtype_room_properties USING btree (roomproperty_id);


--
-- Name: rooms_roomtype_room_properties_roomtype_id_e08c5f05; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX rooms_roomtype_room_properties_roomtype_id_e08c5f05 ON public.rooms_roomtype_room_properties USING btree (roomtype_id);


--
-- Name: rooms_roomtypeformula_room_type_id_69b586c5; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX rooms_roomtypeformula_room_type_id_69b586c5 ON public.rooms_roomtypeformula USING btree (room_type_id);


--
-- Name: subscription_plans_companysubscribedplan_company_id_d41fd89e; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX subscription_plans_companysubscribedplan_company_id_d41fd89e ON public.subscription_plans_companysubscribedplan USING btree (company_id);


--
-- Name: subscription_plans_companysubscribedplan_plan_id_2c228c31; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX subscription_plans_companysubscribedplan_plan_id_2c228c31 ON public.subscription_plans_companysubscribedplan USING btree (plan_id);


--
-- Name: tasks_task_assigned_to_task_id_daf1a7ac; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX tasks_task_assigned_to_task_id_daf1a7ac ON public.tasks_task_assigned_to USING btree (task_id);


--
-- Name: tasks_task_assigned_to_user_id_a003647a; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX tasks_task_assigned_to_user_id_a003647a ON public.tasks_task_assigned_to USING btree (user_id);


--
-- Name: tasks_task_company_id_f699f141; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX tasks_task_company_id_f699f141 ON public.tasks_task USING btree (company_id);


--
-- Name: tasks_task_contacts_contact_id_29ef4ac7; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX tasks_task_contacts_contact_id_29ef4ac7 ON public.tasks_task_contacts USING btree (contact_id);


--
-- Name: tasks_task_contacts_task_id_90df7d53; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX tasks_task_contacts_task_id_90df7d53 ON public.tasks_task_contacts USING btree (task_id);


--
-- Name: tasks_task_created_by_id_1345568a; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX tasks_task_created_by_id_1345568a ON public.tasks_task USING btree (created_by_id);


--
-- Name: tasks_task_teams_task_id_d1e3d547; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX tasks_task_teams_task_id_d1e3d547 ON public.tasks_task_teams USING btree (task_id);


--
-- Name: tasks_task_teams_teams_id_69d613d1; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX tasks_task_teams_teams_id_69d613d1 ON public.tasks_task_teams USING btree (teams_id);


--
-- Name: teams_teams_created_by_id_c6e9aee3; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX teams_teams_created_by_id_c6e9aee3 ON public.teams_teams USING btree (created_by_id);


--
-- Name: teams_teams_users_teams_id_14b49914; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX teams_teams_users_teams_id_14b49914 ON public.teams_teams_users USING btree (teams_id);


--
-- Name: teams_teams_users_user_id_f834347a; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX teams_teams_users_user_id_f834347a ON public.teams_teams_users USING btree (user_id);


--
-- Name: thumbnail_kvstore_key_3f850178_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX thumbnail_kvstore_key_3f850178_like ON public.thumbnail_kvstore USING btree (key varchar_pattern_ops);


--
-- Name: token_blacklist_outstandingtoken_jti_hex_d9bdf6f7_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX token_blacklist_outstandingtoken_jti_hex_d9bdf6f7_like ON public.token_blacklist_outstandingtoken USING btree (jti varchar_pattern_ops);


--
-- Name: token_blacklist_outstandingtoken_user_id_83bc629a; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX token_blacklist_outstandingtoken_user_id_83bc629a ON public.token_blacklist_outstandingtoken USING btree (user_id);


--
-- Name: accounts_account_assigned_to accounts_account_ass_account_id_7e994f48_fk_accounts_; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_account_assigned_to
    ADD CONSTRAINT accounts_account_ass_account_id_7e994f48_fk_accounts_ FOREIGN KEY (account_id) REFERENCES public.accounts_account(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: accounts_account_assigned_to accounts_account_assigned_to_user_id_407e8c4d_fk_common_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_account_assigned_to
    ADD CONSTRAINT accounts_account_assigned_to_user_id_407e8c4d_fk_common_user_id FOREIGN KEY (user_id) REFERENCES public.common_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: accounts_account_contacts accounts_account_con_account_id_dd7706b6_fk_accounts_; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_account_contacts
    ADD CONSTRAINT accounts_account_con_account_id_dd7706b6_fk_accounts_ FOREIGN KEY (account_id) REFERENCES public.accounts_account(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: accounts_account_contacts accounts_account_con_contact_id_1ebaea8d_fk_contacts_; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_account_contacts
    ADD CONSTRAINT accounts_account_con_contact_id_1ebaea8d_fk_contacts_ FOREIGN KEY (contact_id) REFERENCES public.contacts_contact(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: accounts_account accounts_account_created_by_id_96988f15_fk_common_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_account
    ADD CONSTRAINT accounts_account_created_by_id_96988f15_fk_common_user_id FOREIGN KEY (created_by_id) REFERENCES public.common_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: accounts_account accounts_account_lead_id_f33685c2_fk_leads_lead_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_account
    ADD CONSTRAINT accounts_account_lead_id_f33685c2_fk_leads_lead_id FOREIGN KEY (lead_id) REFERENCES public.leads_lead(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: accounts_account_tags accounts_account_tag_account_id_3be82424_fk_accounts_; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_account_tags
    ADD CONSTRAINT accounts_account_tag_account_id_3be82424_fk_accounts_ FOREIGN KEY (account_id) REFERENCES public.accounts_account(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: accounts_account_tags accounts_account_tags_tags_id_78fe9bd2_fk_accounts_tags_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_account_tags
    ADD CONSTRAINT accounts_account_tags_tags_id_78fe9bd2_fk_accounts_tags_id FOREIGN KEY (tags_id) REFERENCES public.accounts_tags(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: accounts_account_teams accounts_account_tea_account_id_7be328bb_fk_accounts_; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_account_teams
    ADD CONSTRAINT accounts_account_tea_account_id_7be328bb_fk_accounts_ FOREIGN KEY (account_id) REFERENCES public.accounts_account(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: accounts_account_teams accounts_account_teams_teams_id_f8111d1e_fk_teams_teams_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_account_teams
    ADD CONSTRAINT accounts_account_teams_teams_id_f8111d1e_fk_teams_teams_id FOREIGN KEY (teams_id) REFERENCES public.teams_teams(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: accounts_email accounts_email_from_account_id_86dd0e6a_fk_accounts_account_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_email
    ADD CONSTRAINT accounts_email_from_account_id_86dd0e6a_fk_accounts_account_id FOREIGN KEY (from_account_id) REFERENCES public.accounts_account(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: accounts_email_recipients accounts_email_recip_contact_id_8b4d5e07_fk_contacts_; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_email_recipients
    ADD CONSTRAINT accounts_email_recip_contact_id_8b4d5e07_fk_contacts_ FOREIGN KEY (contact_id) REFERENCES public.contacts_contact(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: accounts_email_recipients accounts_email_recip_email_id_a9e1dba2_fk_accounts_; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_email_recipients
    ADD CONSTRAINT accounts_email_recip_email_id_a9e1dba2_fk_accounts_ FOREIGN KEY (email_id) REFERENCES public.accounts_email(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: accounts_emaillog accounts_emaillog_contact_id_10e17a75_fk_contacts_contact_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_emaillog
    ADD CONSTRAINT accounts_emaillog_contact_id_10e17a75_fk_contacts_contact_id FOREIGN KEY (contact_id) REFERENCES public.contacts_contact(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: accounts_emaillog accounts_emaillog_email_id_b252a46b_fk_accounts_email_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts_emaillog
    ADD CONSTRAINT accounts_emaillog_email_id_b252a46b_fk_accounts_email_id FOREIGN KEY (email_id) REFERENCES public.accounts_email(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cases_case_assigned_to cases_case_assigned_to_case_id_2e4863d1_fk_cases_case_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cases_case_assigned_to
    ADD CONSTRAINT cases_case_assigned_to_case_id_2e4863d1_fk_cases_case_id FOREIGN KEY (case_id) REFERENCES public.cases_case(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cases_case_assigned_to cases_case_assigned_to_user_id_475b56e3_fk_common_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cases_case_assigned_to
    ADD CONSTRAINT cases_case_assigned_to_user_id_475b56e3_fk_common_user_id FOREIGN KEY (user_id) REFERENCES public.common_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cases_case cases_case_company_id_0d4c7ae8_fk_companies_company_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cases_case
    ADD CONSTRAINT cases_case_company_id_0d4c7ae8_fk_companies_company_id FOREIGN KEY (company_id) REFERENCES public.companies_company(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cases_case_contacts cases_case_contacts_case_id_76980f08_fk_cases_case_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cases_case_contacts
    ADD CONSTRAINT cases_case_contacts_case_id_76980f08_fk_cases_case_id FOREIGN KEY (case_id) REFERENCES public.cases_case(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cases_case_contacts cases_case_contacts_contact_id_b13062a2_fk_contacts_contact_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cases_case_contacts
    ADD CONSTRAINT cases_case_contacts_contact_id_b13062a2_fk_contacts_contact_id FOREIGN KEY (contact_id) REFERENCES public.contacts_contact(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cases_case cases_case_created_by_id_91d115ec_fk_common_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cases_case
    ADD CONSTRAINT cases_case_created_by_id_91d115ec_fk_common_user_id FOREIGN KEY (created_by_id) REFERENCES public.common_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cases_case_teams cases_case_teams_case_id_18a51654_fk_cases_case_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cases_case_teams
    ADD CONSTRAINT cases_case_teams_case_id_18a51654_fk_cases_case_id FOREIGN KEY (case_id) REFERENCES public.cases_case(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cases_case_teams cases_case_teams_teams_id_48201301_fk_teams_teams_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cases_case_teams
    ADD CONSTRAINT cases_case_teams_teams_id_48201301_fk_teams_teams_id FOREIGN KEY (teams_id) REFERENCES public.teams_teams(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_apisettings common_apisettings_created_by_id_98c6c22e_fk_common_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.common_apisettings
    ADD CONSTRAINT common_apisettings_created_by_id_98c6c22e_fk_common_user_id FOREIGN KEY (created_by_id) REFERENCES public.common_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_apisettings_lead_assigned_to common_apisettings_l_apisettings_id_bcb9b4d4_fk_common_ap; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.common_apisettings_lead_assigned_to
    ADD CONSTRAINT common_apisettings_l_apisettings_id_bcb9b4d4_fk_common_ap FOREIGN KEY (apisettings_id) REFERENCES public.common_apisettings(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_apisettings_lead_assigned_to common_apisettings_l_user_id_0e624afc_fk_common_us; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.common_apisettings_lead_assigned_to
    ADD CONSTRAINT common_apisettings_l_user_id_0e624afc_fk_common_us FOREIGN KEY (user_id) REFERENCES public.common_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_apisettings_tags common_apisettings_t_apisettings_id_37ac3e70_fk_common_ap; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.common_apisettings_tags
    ADD CONSTRAINT common_apisettings_t_apisettings_id_37ac3e70_fk_common_ap FOREIGN KEY (apisettings_id) REFERENCES public.common_apisettings(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_apisettings_tags common_apisettings_tags_tags_id_53f647a4_fk_companies_tags_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.common_apisettings_tags
    ADD CONSTRAINT common_apisettings_tags_tags_id_53f647a4_fk_companies_tags_id FOREIGN KEY (tags_id) REFERENCES public.companies_tags(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_attachments common_attachments_account_id_3ded5aec_fk_accounts_account_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.common_attachments
    ADD CONSTRAINT common_attachments_account_id_3ded5aec_fk_accounts_account_id FOREIGN KEY (account_id) REFERENCES public.accounts_account(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_attachments common_attachments_case_id_9141eaa4_fk_cases_case_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.common_attachments
    ADD CONSTRAINT common_attachments_case_id_9141eaa4_fk_cases_case_id FOREIGN KEY (case_id) REFERENCES public.cases_case(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_attachments common_attachments_company_id_c7ab9ceb_fk_companies_company_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.common_attachments
    ADD CONSTRAINT common_attachments_company_id_c7ab9ceb_fk_companies_company_id FOREIGN KEY (company_id) REFERENCES public.companies_company(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_attachments common_attachments_contact_id_f32626af_fk_contacts_contact_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.common_attachments
    ADD CONSTRAINT common_attachments_contact_id_f32626af_fk_contacts_contact_id FOREIGN KEY (contact_id) REFERENCES public.contacts_contact(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_attachments common_attachments_created_by_id_de1aec79_fk_common_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.common_attachments
    ADD CONSTRAINT common_attachments_created_by_id_de1aec79_fk_common_user_id FOREIGN KEY (created_by_id) REFERENCES public.common_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_attachments common_attachments_event_id_a2570824_fk_events_event_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.common_attachments
    ADD CONSTRAINT common_attachments_event_id_a2570824_fk_events_event_id FOREIGN KEY (event_id) REFERENCES public.events_event(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_attachments common_attachments_lead_id_408ab6f8_fk_leads_lead_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.common_attachments
    ADD CONSTRAINT common_attachments_lead_id_408ab6f8_fk_leads_lead_id FOREIGN KEY (lead_id) REFERENCES public.leads_lead(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_attachments common_attachments_opportunity_id_55c921d1_fk_opportuni; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.common_attachments
    ADD CONSTRAINT common_attachments_opportunity_id_55c921d1_fk_opportuni FOREIGN KEY (opportunity_id) REFERENCES public.opportunity_opportunity(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_attachments common_attachments_quotation_id_a25eb41c_fk_quotation; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.common_attachments
    ADD CONSTRAINT common_attachments_quotation_id_a25eb41c_fk_quotation FOREIGN KEY (quotation_id) REFERENCES public.quotations_quotation(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_attachments common_attachments_task_id_a2c58513_fk_tasks_task_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.common_attachments
    ADD CONSTRAINT common_attachments_task_id_a2c58513_fk_tasks_task_id FOREIGN KEY (task_id) REFERENCES public.tasks_task(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_comment common_comment_account_id_dfaa7135_fk_accounts_account_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.common_comment
    ADD CONSTRAINT common_comment_account_id_dfaa7135_fk_accounts_account_id FOREIGN KEY (account_id) REFERENCES public.accounts_account(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_comment common_comment_case_id_1869f987_fk_cases_case_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.common_comment
    ADD CONSTRAINT common_comment_case_id_1869f987_fk_cases_case_id FOREIGN KEY (case_id) REFERENCES public.cases_case(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_comment common_comment_commented_by_id_d25d4735_fk_common_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.common_comment
    ADD CONSTRAINT common_comment_commented_by_id_d25d4735_fk_common_user_id FOREIGN KEY (commented_by_id) REFERENCES public.common_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_comment common_comment_company_id_69591727_fk_companies_company_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.common_comment
    ADD CONSTRAINT common_comment_company_id_69591727_fk_companies_company_id FOREIGN KEY (company_id) REFERENCES public.companies_company(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_comment common_comment_contact_id_5001da5f_fk_contacts_contact_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.common_comment
    ADD CONSTRAINT common_comment_contact_id_5001da5f_fk_contacts_contact_id FOREIGN KEY (contact_id) REFERENCES public.contacts_contact(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_comment common_comment_event_id_743a165c_fk_events_event_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.common_comment
    ADD CONSTRAINT common_comment_event_id_743a165c_fk_events_event_id FOREIGN KEY (event_id) REFERENCES public.events_event(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_comment_files common_comment_files_comment_id_4a871ebd_fk_common_comment_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.common_comment_files
    ADD CONSTRAINT common_comment_files_comment_id_4a871ebd_fk_common_comment_id FOREIGN KEY (comment_id) REFERENCES public.common_comment(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_comment common_comment_lead_id_a06ba983_fk_leads_lead_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.common_comment
    ADD CONSTRAINT common_comment_lead_id_a06ba983_fk_leads_lead_id FOREIGN KEY (lead_id) REFERENCES public.leads_lead(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_comment common_comment_opportunity_id_69135f56_fk_opportuni; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.common_comment
    ADD CONSTRAINT common_comment_opportunity_id_69135f56_fk_opportuni FOREIGN KEY (opportunity_id) REFERENCES public.opportunity_opportunity(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_comment common_comment_quotation_id_a57d7341_fk_quotations_quotation_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.common_comment
    ADD CONSTRAINT common_comment_quotation_id_a57d7341_fk_quotations_quotation_id FOREIGN KEY (quotation_id) REFERENCES public.quotations_quotation(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_comment common_comment_task_id_4d5c683f_fk_tasks_task_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.common_comment
    ADD CONSTRAINT common_comment_task_id_4d5c683f_fk_tasks_task_id FOREIGN KEY (task_id) REFERENCES public.tasks_task(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_comment common_comment_user_id_06e537fc_fk_common_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.common_comment
    ADD CONSTRAINT common_comment_user_id_06e537fc_fk_common_user_id FOREIGN KEY (user_id) REFERENCES public.common_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_document common_document_created_by_id_19742726_fk_common_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.common_document
    ADD CONSTRAINT common_document_created_by_id_19742726_fk_common_user_id FOREIGN KEY (created_by_id) REFERENCES public.common_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_document_shared_to common_document_shar_document_id_f5146fd1_fk_common_do; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.common_document_shared_to
    ADD CONSTRAINT common_document_shar_document_id_f5146fd1_fk_common_do FOREIGN KEY (document_id) REFERENCES public.common_document(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_document_shared_to common_document_shared_to_user_id_09ae644f_fk_common_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.common_document_shared_to
    ADD CONSTRAINT common_document_shared_to_user_id_09ae644f_fk_common_user_id FOREIGN KEY (user_id) REFERENCES public.common_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_document_teams common_document_team_document_id_494fb8a5_fk_common_do; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.common_document_teams
    ADD CONSTRAINT common_document_team_document_id_494fb8a5_fk_common_do FOREIGN KEY (document_id) REFERENCES public.common_document(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_document_teams common_document_teams_teams_id_17146b17_fk_teams_teams_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.common_document_teams
    ADD CONSTRAINT common_document_teams_teams_id_17146b17_fk_teams_teams_id FOREIGN KEY (teams_id) REFERENCES public.teams_teams(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_google common_google_user_id_83499ce5_fk_common_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.common_google
    ADD CONSTRAINT common_google_user_id_83499ce5_fk_common_user_id FOREIGN KEY (user_id) REFERENCES public.common_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_profile common_profile_user_id_8573ee5c_fk_common_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.common_profile
    ADD CONSTRAINT common_profile_user_id_8573ee5c_fk_common_user_id FOREIGN KEY (user_id) REFERENCES public.common_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_user_groups common_user_groups_group_id_27a26245_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.common_user_groups
    ADD CONSTRAINT common_user_groups_group_id_27a26245_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_user_groups common_user_groups_user_id_92ddbe7a_fk_common_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.common_user_groups
    ADD CONSTRAINT common_user_groups_user_id_92ddbe7a_fk_common_user_id FOREIGN KEY (user_id) REFERENCES public.common_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_user_user_permissions common_user_user_per_permission_id_a6da427c_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.common_user_user_permissions
    ADD CONSTRAINT common_user_user_per_permission_id_a6da427c_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_user_user_permissions common_user_user_permissions_user_id_56b84879_fk_common_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.common_user_user_permissions
    ADD CONSTRAINT common_user_user_permissions_user_id_56b84879_fk_common_user_id FOREIGN KEY (user_id) REFERENCES public.common_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: companies_chargingstages companies_chargingst_company_id_06259d62_fk_companies; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.companies_chargingstages
    ADD CONSTRAINT companies_chargingst_company_id_06259d62_fk_companies FOREIGN KEY (company_id) REFERENCES public.companies_company(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: companies_company companies_company_created_by_id_5b37702d_fk_common_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.companies_company
    ADD CONSTRAINT companies_company_created_by_id_5b37702d_fk_common_user_id FOREIGN KEY (created_by_id) REFERENCES public.common_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: companies_company companies_company_owner_id_89314e2a_fk_common_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.companies_company
    ADD CONSTRAINT companies_company_owner_id_89314e2a_fk_common_user_id FOREIGN KEY (owner_id) REFERENCES public.common_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: companies_company_tags companies_company_ta_company_id_bbf3f023_fk_companies; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.companies_company_tags
    ADD CONSTRAINT companies_company_ta_company_id_bbf3f023_fk_companies FOREIGN KEY (company_id) REFERENCES public.companies_company(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: companies_company_tags companies_company_tags_tags_id_4e1b5d55_fk_companies_tags_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.companies_company_tags
    ADD CONSTRAINT companies_company_tags_tags_id_4e1b5d55_fk_companies_tags_id FOREIGN KEY (tags_id) REFERENCES public.companies_tags(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: companies_documentformat companies_documentfo_company_id_497bf3af_fk_companies; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.companies_documentformat
    ADD CONSTRAINT companies_documentfo_company_id_497bf3af_fk_companies FOREIGN KEY (company_id) REFERENCES public.companies_company(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: companies_documentheaderinformation companies_documenthe_company_id_9d6e75b7_fk_companies; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.companies_documentheaderinformation
    ADD CONSTRAINT companies_documenthe_company_id_9d6e75b7_fk_companies FOREIGN KEY (company_id) REFERENCES public.companies_company(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: companies_email companies_email_from_company_id_99e7e9b5_fk_companies; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.companies_email
    ADD CONSTRAINT companies_email_from_company_id_99e7e9b5_fk_companies FOREIGN KEY (from_company_id) REFERENCES public.companies_company(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: companies_email_recipients companies_email_reci_contact_id_05992f87_fk_contacts_; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.companies_email_recipients
    ADD CONSTRAINT companies_email_reci_contact_id_05992f87_fk_contacts_ FOREIGN KEY (contact_id) REFERENCES public.contacts_contact(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: companies_email_recipients companies_email_reci_email_id_34cd5058_fk_companies; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.companies_email_recipients
    ADD CONSTRAINT companies_email_reci_email_id_34cd5058_fk_companies FOREIGN KEY (email_id) REFERENCES public.companies_email(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: companies_emaillog companies_emaillog_contact_id_c2c70d83_fk_contacts_contact_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.companies_emaillog
    ADD CONSTRAINT companies_emaillog_contact_id_c2c70d83_fk_contacts_contact_id FOREIGN KEY (contact_id) REFERENCES public.contacts_contact(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: companies_emaillog companies_emaillog_email_id_f1540de3_fk_companies_email_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.companies_emaillog
    ADD CONSTRAINT companies_emaillog_email_id_f1540de3_fk_companies_email_id FOREIGN KEY (email_id) REFERENCES public.companies_email(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: companies_invoicegeneralremark companies_invoicegen_company_id_8e90bf7d_fk_companies; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.companies_invoicegeneralremark
    ADD CONSTRAINT companies_invoicegen_company_id_8e90bf7d_fk_companies FOREIGN KEY (company_id) REFERENCES public.companies_company(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: companies_quotationgeneralremark companies_quotationg_company_id_586c34c5_fk_companies; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.companies_quotationgeneralremark
    ADD CONSTRAINT companies_quotationg_company_id_586c34c5_fk_companies FOREIGN KEY (company_id) REFERENCES public.companies_company(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: companies_receiptgeneralremark companies_receiptgen_company_id_a6d8e6af_fk_companies; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.companies_receiptgeneralremark
    ADD CONSTRAINT companies_receiptgen_company_id_a6d8e6af_fk_companies FOREIGN KEY (company_id) REFERENCES public.companies_company(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: contacts_contact contacts_contact_address_id_0dbb18a0_fk_common_address_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contacts_contact
    ADD CONSTRAINT contacts_contact_address_id_0dbb18a0_fk_common_address_id FOREIGN KEY (address_id) REFERENCES public.common_address(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: contacts_contact_assigned_to contacts_contact_ass_contact_id_0269bc5d_fk_contacts_; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contacts_contact_assigned_to
    ADD CONSTRAINT contacts_contact_ass_contact_id_0269bc5d_fk_contacts_ FOREIGN KEY (contact_id) REFERENCES public.contacts_contact(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: contacts_contact_assigned_to contacts_contact_assigned_to_user_id_727306dd_fk_common_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contacts_contact_assigned_to
    ADD CONSTRAINT contacts_contact_assigned_to_user_id_727306dd_fk_common_user_id FOREIGN KEY (user_id) REFERENCES public.common_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: contacts_contact contacts_contact_created_by_id_57537352_fk_common_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contacts_contact
    ADD CONSTRAINT contacts_contact_created_by_id_57537352_fk_common_user_id FOREIGN KEY (created_by_id) REFERENCES public.common_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: contacts_contact_teams contacts_contact_tea_contact_id_76009c86_fk_contacts_; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contacts_contact_teams
    ADD CONSTRAINT contacts_contact_tea_contact_id_76009c86_fk_contacts_ FOREIGN KEY (contact_id) REFERENCES public.contacts_contact(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: contacts_contact_teams contacts_contact_teams_teams_id_b69a29e7_fk_teams_teams_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contacts_contact_teams
    ADD CONSTRAINT contacts_contact_teams_teams_id_b69a29e7_fk_teams_teams_id FOREIGN KEY (teams_id) REFERENCES public.teams_teams(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: customers_customer customers_customer_created_by_id_e3e9e010_fk_common_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.customers_customer
    ADD CONSTRAINT customers_customer_created_by_id_e3e9e010_fk_common_user_id FOREIGN KEY (created_by_id) REFERENCES public.common_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: customers_customer customers_customer_project_id_90b110dc_fk_projects_project_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.customers_customer
    ADD CONSTRAINT customers_customer_project_id_90b110dc_fk_projects_project_id FOREIGN KEY (project_id) REFERENCES public.projects_project(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk_common_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_common_user_id FOREIGN KEY (user_id) REFERENCES public.common_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: events_event_assigned_to events_event_assigned_to_event_id_211aebd2_fk_events_event_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.events_event_assigned_to
    ADD CONSTRAINT events_event_assigned_to_event_id_211aebd2_fk_events_event_id FOREIGN KEY (event_id) REFERENCES public.events_event(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: events_event_assigned_to events_event_assigned_to_user_id_88f9a1f0_fk_common_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.events_event_assigned_to
    ADD CONSTRAINT events_event_assigned_to_user_id_88f9a1f0_fk_common_user_id FOREIGN KEY (user_id) REFERENCES public.common_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: events_event_contacts events_event_contact_contact_id_de30d576_fk_contacts_; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.events_event_contacts
    ADD CONSTRAINT events_event_contact_contact_id_de30d576_fk_contacts_ FOREIGN KEY (contact_id) REFERENCES public.contacts_contact(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: events_event_contacts events_event_contacts_event_id_3da8569b_fk_events_event_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.events_event_contacts
    ADD CONSTRAINT events_event_contacts_event_id_3da8569b_fk_events_event_id FOREIGN KEY (event_id) REFERENCES public.events_event(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: events_event events_event_created_by_id_2c28ea90_fk_common_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.events_event
    ADD CONSTRAINT events_event_created_by_id_2c28ea90_fk_common_user_id FOREIGN KEY (created_by_id) REFERENCES public.common_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: events_event_teams events_event_teams_event_id_ebaa210d_fk_events_event_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.events_event_teams
    ADD CONSTRAINT events_event_teams_event_id_ebaa210d_fk_events_event_id FOREIGN KEY (event_id) REFERENCES public.events_event(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: events_event_teams events_event_teams_teams_id_8c21a9a0_fk_teams_teams_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.events_event_teams
    ADD CONSTRAINT events_event_teams_teams_id_8c21a9a0_fk_teams_teams_id FOREIGN KEY (teams_id) REFERENCES public.teams_teams(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: function_items_functionitem function_items_funct_approved_by_id_02875902_fk_common_us; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.function_items_functionitem
    ADD CONSTRAINT function_items_funct_approved_by_id_02875902_fk_common_us FOREIGN KEY (approved_by_id) REFERENCES public.common_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: function_items_functionitem function_items_funct_created_by_id_5f94ff8b_fk_common_us; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.function_items_functionitem
    ADD CONSTRAINT function_items_funct_created_by_id_5f94ff8b_fk_common_us FOREIGN KEY (created_by_id) REFERENCES public.common_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: function_items_functionitemhistory function_items_funct_function_item_id_2e6850d2_fk_function_; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.function_items_functionitemhistory
    ADD CONSTRAINT function_items_funct_function_item_id_2e6850d2_fk_function_ FOREIGN KEY (function_item_id) REFERENCES public.function_items_functionitem(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: function_items_functionitem function_items_funct_last_updated_by_id_6ba5a432_fk_common_us; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.function_items_functionitem
    ADD CONSTRAINT function_items_funct_last_updated_by_id_6ba5a432_fk_common_us FOREIGN KEY (last_updated_by_id) REFERENCES public.common_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: function_items_functionitemhistory function_items_funct_updated_by_id_3afbe02a_fk_common_us; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.function_items_functionitemhistory
    ADD CONSTRAINT function_items_funct_updated_by_id_3afbe02a_fk_common_us FOREIGN KEY (updated_by_id) REFERENCES public.common_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: function_items_subfunctionitem function_items_subfu_approved_by_id_c2f3ab62_fk_common_us; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.function_items_subfunctionitem
    ADD CONSTRAINT function_items_subfu_approved_by_id_c2f3ab62_fk_common_us FOREIGN KEY (approved_by_id) REFERENCES public.common_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: function_items_subfunctionitem function_items_subfu_created_by_id_a5121cb9_fk_common_us; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.function_items_subfunctionitem
    ADD CONSTRAINT function_items_subfu_created_by_id_a5121cb9_fk_common_us FOREIGN KEY (created_by_id) REFERENCES public.common_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: function_items_subfunctionitem function_items_subfu_last_updated_by_id_01e35040_fk_common_us; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.function_items_subfunctionitem
    ADD CONSTRAINT function_items_subfu_last_updated_by_id_01e35040_fk_common_us FOREIGN KEY (last_updated_by_id) REFERENCES public.common_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: function_items_subfunctionitem function_items_subfu_related_function_ite_8f2bd2de_fk_function_; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.function_items_subfunctionitem
    ADD CONSTRAINT function_items_subfu_related_function_ite_8f2bd2de_fk_function_ FOREIGN KEY (related_function_item_id) REFERENCES public.function_items_functionitem(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: function_items_subfunctionitemhistory function_items_subfu_sub_function_item_id_b176cb95_fk_function_; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.function_items_subfunctionitemhistory
    ADD CONSTRAINT function_items_subfu_sub_function_item_id_b176cb95_fk_function_ FOREIGN KEY (sub_function_item_id) REFERENCES public.function_items_subfunctionitem(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: function_items_subfunctionitemhistory function_items_subfu_updated_by_id_c4614a1f_fk_common_us; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.function_items_subfunctionitemhistory
    ADD CONSTRAINT function_items_subfu_updated_by_id_c4614a1f_fk_common_us FOREIGN KEY (updated_by_id) REFERENCES public.common_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: invoices_invoice_assigned_to invoices_invoice_ass_invoice_id_8b0ff865_fk_invoices_; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.invoices_invoice_assigned_to
    ADD CONSTRAINT invoices_invoice_ass_invoice_id_8b0ff865_fk_invoices_ FOREIGN KEY (invoice_id) REFERENCES public.invoices_invoice(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: invoices_invoice_assigned_to invoices_invoice_assigned_to_user_id_0aa3df96_fk_common_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.invoices_invoice_assigned_to
    ADD CONSTRAINT invoices_invoice_assigned_to_user_id_0aa3df96_fk_common_user_id FOREIGN KEY (user_id) REFERENCES public.common_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: invoices_invoice_companies invoices_invoice_com_company_id_ab7d6e05_fk_companies; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.invoices_invoice_companies
    ADD CONSTRAINT invoices_invoice_com_company_id_ab7d6e05_fk_companies FOREIGN KEY (company_id) REFERENCES public.companies_company(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: invoices_invoice_companies invoices_invoice_com_invoice_id_2a580af9_fk_invoices_; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.invoices_invoice_companies
    ADD CONSTRAINT invoices_invoice_com_invoice_id_2a580af9_fk_invoices_ FOREIGN KEY (invoice_id) REFERENCES public.invoices_invoice(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: invoices_invoice invoices_invoice_created_by_id_9b878bcd_fk_common_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.invoices_invoice
    ADD CONSTRAINT invoices_invoice_created_by_id_9b878bcd_fk_common_user_id FOREIGN KEY (created_by_id) REFERENCES public.common_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: invoices_invoice invoices_invoice_from_address_id_c42db748_fk_common_address_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.invoices_invoice
    ADD CONSTRAINT invoices_invoice_from_address_id_c42db748_fk_common_address_id FOREIGN KEY (from_address_id) REFERENCES public.common_address(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: invoices_invoice_teams invoices_invoice_tea_invoice_id_a15c151f_fk_invoices_; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.invoices_invoice_teams
    ADD CONSTRAINT invoices_invoice_tea_invoice_id_a15c151f_fk_invoices_ FOREIGN KEY (invoice_id) REFERENCES public.invoices_invoice(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: invoices_invoice_teams invoices_invoice_teams_teams_id_b51618e6_fk_teams_teams_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.invoices_invoice_teams
    ADD CONSTRAINT invoices_invoice_teams_teams_id_b51618e6_fk_teams_teams_id FOREIGN KEY (teams_id) REFERENCES public.teams_teams(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: invoices_invoice invoices_invoice_to_address_id_d9360206_fk_common_address_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.invoices_invoice
    ADD CONSTRAINT invoices_invoice_to_address_id_d9360206_fk_common_address_id FOREIGN KEY (to_address_id) REFERENCES public.common_address(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: invoices_invoicehistory invoices_invoicehist_from_address_id_cffac1b5_fk_common_ad; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.invoices_invoicehistory
    ADD CONSTRAINT invoices_invoicehist_from_address_id_cffac1b5_fk_common_ad FOREIGN KEY (from_address_id) REFERENCES public.common_address(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: invoices_invoicehistory invoices_invoicehist_invoice_id_05ee6eb8_fk_invoices_; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.invoices_invoicehistory
    ADD CONSTRAINT invoices_invoicehist_invoice_id_05ee6eb8_fk_invoices_ FOREIGN KEY (invoice_id) REFERENCES public.invoices_invoice(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: invoices_invoicehistory_assigned_to invoices_invoicehist_invoicehistory_id_02417412_fk_invoices_; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.invoices_invoicehistory_assigned_to
    ADD CONSTRAINT invoices_invoicehist_invoicehistory_id_02417412_fk_invoices_ FOREIGN KEY (invoicehistory_id) REFERENCES public.invoices_invoicehistory(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: invoices_invoicehistory invoices_invoicehist_to_address_id_492fbb02_fk_common_ad; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.invoices_invoicehistory
    ADD CONSTRAINT invoices_invoicehist_to_address_id_492fbb02_fk_common_ad FOREIGN KEY (to_address_id) REFERENCES public.common_address(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: invoices_invoicehistory invoices_invoicehist_updated_by_id_2ccd68d8_fk_common_us; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.invoices_invoicehistory
    ADD CONSTRAINT invoices_invoicehist_updated_by_id_2ccd68d8_fk_common_us FOREIGN KEY (updated_by_id) REFERENCES public.common_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: invoices_invoicehistory_assigned_to invoices_invoicehist_user_id_7b1e7786_fk_common_us; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.invoices_invoicehistory_assigned_to
    ADD CONSTRAINT invoices_invoicehist_user_id_7b1e7786_fk_common_us FOREIGN KEY (user_id) REFERENCES public.common_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: leads_lead_assigned_to leads_lead_assigned_to_lead_id_b43e64b4_fk_leads_lead_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.leads_lead_assigned_to
    ADD CONSTRAINT leads_lead_assigned_to_lead_id_b43e64b4_fk_leads_lead_id FOREIGN KEY (lead_id) REFERENCES public.leads_lead(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: leads_lead_assigned_to leads_lead_assigned_to_user_id_e9de5cbf_fk_common_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.leads_lead_assigned_to
    ADD CONSTRAINT leads_lead_assigned_to_user_id_e9de5cbf_fk_common_user_id FOREIGN KEY (user_id) REFERENCES public.common_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: leads_lead_contacts leads_lead_contacts_contact_id_643d700d_fk_contacts_contact_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.leads_lead_contacts
    ADD CONSTRAINT leads_lead_contacts_contact_id_643d700d_fk_contacts_contact_id FOREIGN KEY (contact_id) REFERENCES public.contacts_contact(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: leads_lead_contacts leads_lead_contacts_lead_id_e9cd308e_fk_leads_lead_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.leads_lead_contacts
    ADD CONSTRAINT leads_lead_contacts_lead_id_e9cd308e_fk_leads_lead_id FOREIGN KEY (lead_id) REFERENCES public.leads_lead(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: leads_lead leads_lead_created_by_id_bd2e8097_fk_common_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.leads_lead
    ADD CONSTRAINT leads_lead_created_by_id_bd2e8097_fk_common_user_id FOREIGN KEY (created_by_id) REFERENCES public.common_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: leads_lead_teams leads_lead_teams_lead_id_fb912735_fk_leads_lead_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.leads_lead_teams
    ADD CONSTRAINT leads_lead_teams_lead_id_fb912735_fk_leads_lead_id FOREIGN KEY (lead_id) REFERENCES public.leads_lead(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: leads_lead_teams leads_lead_teams_teams_id_9753bcb3_fk_teams_teams_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.leads_lead_teams
    ADD CONSTRAINT leads_lead_teams_teams_id_9753bcb3_fk_teams_teams_id FOREIGN KEY (teams_id) REFERENCES public.teams_teams(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: marketing_blockeddomain marketing_blockeddom_created_by_id_a4cbe960_fk_common_us; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_blockeddomain
    ADD CONSTRAINT marketing_blockeddom_created_by_id_a4cbe960_fk_common_us FOREIGN KEY (created_by_id) REFERENCES public.common_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: marketing_blockedemail marketing_blockedemail_created_by_id_7f859478_fk_common_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_blockedemail
    ADD CONSTRAINT marketing_blockedemail_created_by_id_7f859478_fk_common_user_id FOREIGN KEY (created_by_id) REFERENCES public.common_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: marketing_campaign_contact_lists marketing_campaign_c_campaign_id_47b7ad3f_fk_marketing; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_campaign_contact_lists
    ADD CONSTRAINT marketing_campaign_c_campaign_id_47b7ad3f_fk_marketing FOREIGN KEY (campaign_id) REFERENCES public.marketing_campaign(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: marketing_campaign_contact_lists marketing_campaign_c_contactlist_id_f870c4d0_fk_marketing; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_campaign_contact_lists
    ADD CONSTRAINT marketing_campaign_c_contactlist_id_f870c4d0_fk_marketing FOREIGN KEY (contactlist_id) REFERENCES public.marketing_contactlist(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: marketing_campaign marketing_campaign_created_by_id_c4d2ec89_fk_common_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_campaign
    ADD CONSTRAINT marketing_campaign_created_by_id_c4d2ec89_fk_common_user_id FOREIGN KEY (created_by_id) REFERENCES public.common_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: marketing_campaign marketing_campaign_email_template_id_16ed1ee5_fk_marketing; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_campaign
    ADD CONSTRAINT marketing_campaign_email_template_id_16ed1ee5_fk_marketing FOREIGN KEY (email_template_id) REFERENCES public.marketing_emailtemplate(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: marketing_campaign_tags marketing_campaign_t_campaign_id_4a5b98e2_fk_marketing; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_campaign_tags
    ADD CONSTRAINT marketing_campaign_t_campaign_id_4a5b98e2_fk_marketing FOREIGN KEY (campaign_id) REFERENCES public.marketing_campaign(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: marketing_campaign_tags marketing_campaign_tags_tag_id_973530fe_fk_marketing_tag_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_campaign_tags
    ADD CONSTRAINT marketing_campaign_tags_tag_id_973530fe_fk_marketing_tag_id FOREIGN KEY (tag_id) REFERENCES public.marketing_tag(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: marketing_campaigncompleted marketing_campaignco_campaign_id_8722a42c_fk_marketing; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_campaigncompleted
    ADD CONSTRAINT marketing_campaignco_campaign_id_8722a42c_fk_marketing FOREIGN KEY (campaign_id) REFERENCES public.marketing_campaign(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: marketing_campaignlinkclick marketing_campaignli_campaign_id_bad5722a_fk_marketing; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_campaignlinkclick
    ADD CONSTRAINT marketing_campaignli_campaign_id_bad5722a_fk_marketing FOREIGN KEY (campaign_id) REFERENCES public.marketing_campaign(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: marketing_campaignlinkclick marketing_campaignli_contact_id_a20f4980_fk_marketing; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_campaignlinkclick
    ADD CONSTRAINT marketing_campaignli_contact_id_a20f4980_fk_marketing FOREIGN KEY (contact_id) REFERENCES public.marketing_contact(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: marketing_campaignlinkclick marketing_campaignli_link_id_df848b66_fk_marketing; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_campaignlinkclick
    ADD CONSTRAINT marketing_campaignli_link_id_df848b66_fk_marketing FOREIGN KEY (link_id) REFERENCES public.marketing_link(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: marketing_campaignlog marketing_campaignlo_campaign_id_0a5d9b5a_fk_marketing; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_campaignlog
    ADD CONSTRAINT marketing_campaignlo_campaign_id_0a5d9b5a_fk_marketing FOREIGN KEY (campaign_id) REFERENCES public.marketing_campaign(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: marketing_campaignlog marketing_campaignlo_contact_id_757a80df_fk_marketing; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_campaignlog
    ADD CONSTRAINT marketing_campaignlo_contact_id_757a80df_fk_marketing FOREIGN KEY (contact_id) REFERENCES public.marketing_contact(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: marketing_campaignopen marketing_campaignop_campaign_id_18fc81d4_fk_marketing; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_campaignopen
    ADD CONSTRAINT marketing_campaignop_campaign_id_18fc81d4_fk_marketing FOREIGN KEY (campaign_id) REFERENCES public.marketing_campaign(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: marketing_campaignopen marketing_campaignop_contact_id_f1813fb0_fk_marketing; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_campaignopen
    ADD CONSTRAINT marketing_campaignop_contact_id_f1813fb0_fk_marketing FOREIGN KEY (contact_id) REFERENCES public.marketing_contact(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: marketing_contact_contact_list marketing_contact_co_contact_id_23181bed_fk_marketing; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_contact_contact_list
    ADD CONSTRAINT marketing_contact_co_contact_id_23181bed_fk_marketing FOREIGN KEY (contact_id) REFERENCES public.marketing_contact(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: marketing_contact_contact_list marketing_contact_co_contactlist_id_51f313b1_fk_marketing; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_contact_contact_list
    ADD CONSTRAINT marketing_contact_co_contactlist_id_51f313b1_fk_marketing FOREIGN KEY (contactlist_id) REFERENCES public.marketing_contactlist(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: marketing_contact marketing_contact_created_by_id_c5fc4040_fk_common_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_contact
    ADD CONSTRAINT marketing_contact_created_by_id_c5fc4040_fk_common_user_id FOREIGN KEY (created_by_id) REFERENCES public.common_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: marketing_contactemailcampaign marketing_contactema_created_by_id_49bdc16d_fk_common_us; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_contactemailcampaign
    ADD CONSTRAINT marketing_contactema_created_by_id_49bdc16d_fk_common_us FOREIGN KEY (created_by_id) REFERENCES public.common_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: marketing_contactlist_visible_to marketing_contactlis_contactlist_id_239ee189_fk_marketing; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_contactlist_visible_to
    ADD CONSTRAINT marketing_contactlis_contactlist_id_239ee189_fk_marketing FOREIGN KEY (contactlist_id) REFERENCES public.marketing_contactlist(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: marketing_contactlist_tags marketing_contactlis_contactlist_id_d5b1120c_fk_marketing; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_contactlist_tags
    ADD CONSTRAINT marketing_contactlis_contactlist_id_d5b1120c_fk_marketing FOREIGN KEY (contactlist_id) REFERENCES public.marketing_contactlist(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: marketing_contactlist_visible_to marketing_contactlis_user_id_55499a9a_fk_common_us; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_contactlist_visible_to
    ADD CONSTRAINT marketing_contactlis_user_id_55499a9a_fk_common_us FOREIGN KEY (user_id) REFERENCES public.common_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: marketing_contactlist marketing_contactlist_created_by_id_ca6d9a00_fk_common_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_contactlist
    ADD CONSTRAINT marketing_contactlist_created_by_id_ca6d9a00_fk_common_user_id FOREIGN KEY (created_by_id) REFERENCES public.common_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: marketing_contactlist_tags marketing_contactlist_tags_tag_id_d2d98941_fk_marketing_tag_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_contactlist_tags
    ADD CONSTRAINT marketing_contactlist_tags_tag_id_d2d98941_fk_marketing_tag_id FOREIGN KEY (tag_id) REFERENCES public.marketing_tag(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: marketing_contactunsubscribedcampaign marketing_contactuns_campaigns_id_631325bd_fk_marketing; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_contactunsubscribedcampaign
    ADD CONSTRAINT marketing_contactuns_campaigns_id_631325bd_fk_marketing FOREIGN KEY (campaigns_id) REFERENCES public.marketing_campaign(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: marketing_contactunsubscribedcampaign marketing_contactuns_contacts_id_0a7bbbe4_fk_marketing; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_contactunsubscribedcampaign
    ADD CONSTRAINT marketing_contactuns_contacts_id_0a7bbbe4_fk_marketing FOREIGN KEY (contacts_id) REFERENCES public.marketing_contact(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: marketing_duplicatecontacts marketing_duplicatec_contact_list_id_eb57a05e_fk_marketing; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_duplicatecontacts
    ADD CONSTRAINT marketing_duplicatec_contact_list_id_eb57a05e_fk_marketing FOREIGN KEY (contact_list_id) REFERENCES public.marketing_contactlist(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: marketing_duplicatecontacts marketing_duplicatec_contacts_id_0cd30367_fk_marketing; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_duplicatecontacts
    ADD CONSTRAINT marketing_duplicatec_contacts_id_0cd30367_fk_marketing FOREIGN KEY (contacts_id) REFERENCES public.marketing_contact(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: marketing_emailtemplate marketing_emailtempl_created_by_id_6641e947_fk_common_us; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_emailtemplate
    ADD CONSTRAINT marketing_emailtempl_created_by_id_6641e947_fk_common_us FOREIGN KEY (created_by_id) REFERENCES public.common_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: marketing_failedcontact_contact_list marketing_failedcont_contactlist_id_0774af5c_fk_marketing; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_failedcontact_contact_list
    ADD CONSTRAINT marketing_failedcont_contactlist_id_0774af5c_fk_marketing FOREIGN KEY (contactlist_id) REFERENCES public.marketing_contactlist(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: marketing_failedcontact marketing_failedcont_created_by_id_69df0cfc_fk_common_us; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_failedcontact
    ADD CONSTRAINT marketing_failedcont_created_by_id_69df0cfc_fk_common_us FOREIGN KEY (created_by_id) REFERENCES public.common_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: marketing_failedcontact_contact_list marketing_failedcont_failedcontact_id_2ec42ab1_fk_marketing; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_failedcontact_contact_list
    ADD CONSTRAINT marketing_failedcont_failedcontact_id_2ec42ab1_fk_marketing FOREIGN KEY (failedcontact_id) REFERENCES public.marketing_failedcontact(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: marketing_link marketing_link_campaign_id_87874449_fk_marketing_campaign_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_link
    ADD CONSTRAINT marketing_link_campaign_id_87874449_fk_marketing_campaign_id FOREIGN KEY (campaign_id) REFERENCES public.marketing_campaign(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: marketing_tag marketing_tag_created_by_id_e0e8f0cb_fk_common_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marketing_tag
    ADD CONSTRAINT marketing_tag_created_by_id_e0e8f0cb_fk_common_user_id FOREIGN KEY (created_by_id) REFERENCES public.common_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: opportunity_opportunity opportunity_opportun_company_id_dde6fcb8_fk_companies; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.opportunity_opportunity
    ADD CONSTRAINT opportunity_opportun_company_id_dde6fcb8_fk_companies FOREIGN KEY (company_id) REFERENCES public.companies_company(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: opportunity_opportunity_contacts opportunity_opportun_contact_id_64ee0712_fk_contacts_; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.opportunity_opportunity_contacts
    ADD CONSTRAINT opportunity_opportun_contact_id_64ee0712_fk_contacts_ FOREIGN KEY (contact_id) REFERENCES public.contacts_contact(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: opportunity_opportunity opportunity_opportun_created_by_id_89d5f804_fk_common_us; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.opportunity_opportunity
    ADD CONSTRAINT opportunity_opportun_created_by_id_89d5f804_fk_common_us FOREIGN KEY (created_by_id) REFERENCES public.common_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: opportunity_opportunity_contacts opportunity_opportun_opportunity_id_01fbf845_fk_opportuni; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.opportunity_opportunity_contacts
    ADD CONSTRAINT opportunity_opportun_opportunity_id_01fbf845_fk_opportuni FOREIGN KEY (opportunity_id) REFERENCES public.opportunity_opportunity(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: opportunity_opportunity_assigned_to opportunity_opportun_opportunity_id_1c8df51a_fk_opportuni; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.opportunity_opportunity_assigned_to
    ADD CONSTRAINT opportunity_opportun_opportunity_id_1c8df51a_fk_opportuni FOREIGN KEY (opportunity_id) REFERENCES public.opportunity_opportunity(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: opportunity_opportunity_teams opportunity_opportun_opportunity_id_81eab463_fk_opportuni; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.opportunity_opportunity_teams
    ADD CONSTRAINT opportunity_opportun_opportunity_id_81eab463_fk_opportuni FOREIGN KEY (opportunity_id) REFERENCES public.opportunity_opportunity(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: opportunity_opportunity_tags opportunity_opportun_opportunity_id_98683361_fk_opportuni; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.opportunity_opportunity_tags
    ADD CONSTRAINT opportunity_opportun_opportunity_id_98683361_fk_opportuni FOREIGN KEY (opportunity_id) REFERENCES public.opportunity_opportunity(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: opportunity_opportunity_tags opportunity_opportun_tags_id_89b307a4_fk_companies; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.opportunity_opportunity_tags
    ADD CONSTRAINT opportunity_opportun_tags_id_89b307a4_fk_companies FOREIGN KEY (tags_id) REFERENCES public.companies_tags(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: opportunity_opportunity_teams opportunity_opportun_teams_id_4f8d4a54_fk_teams_tea; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.opportunity_opportunity_teams
    ADD CONSTRAINT opportunity_opportun_teams_id_4f8d4a54_fk_teams_tea FOREIGN KEY (teams_id) REFERENCES public.teams_teams(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: opportunity_opportunity_assigned_to opportunity_opportun_user_id_ce65565d_fk_common_us; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.opportunity_opportunity_assigned_to
    ADD CONSTRAINT opportunity_opportun_user_id_ce65565d_fk_common_us FOREIGN KEY (user_id) REFERENCES public.common_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: opportunity_opportunity opportunity_opportunity_closed_by_id_7399917f_fk_common_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.opportunity_opportunity
    ADD CONSTRAINT opportunity_opportunity_closed_by_id_7399917f_fk_common_user_id FOREIGN KEY (closed_by_id) REFERENCES public.common_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: planner_event_assigned_to planner_event_assigned_to_event_id_467b0d2b_fk_planner_event_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.planner_event_assigned_to
    ADD CONSTRAINT planner_event_assigned_to_event_id_467b0d2b_fk_planner_event_id FOREIGN KEY (event_id) REFERENCES public.planner_event(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: planner_event_assigned_to planner_event_assigned_to_user_id_3d65f14a_fk_common_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.planner_event_assigned_to
    ADD CONSTRAINT planner_event_assigned_to_user_id_3d65f14a_fk_common_user_id FOREIGN KEY (user_id) REFERENCES public.common_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: planner_event_attendees_contacts planner_event_attend_contact_id_2c29dbd4_fk_contacts_; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.planner_event_attendees_contacts
    ADD CONSTRAINT planner_event_attend_contact_id_2c29dbd4_fk_contacts_ FOREIGN KEY (contact_id) REFERENCES public.contacts_contact(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: planner_event_attendees_leads planner_event_attend_event_id_05e9c4f9_fk_planner_e; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.planner_event_attendees_leads
    ADD CONSTRAINT planner_event_attend_event_id_05e9c4f9_fk_planner_e FOREIGN KEY (event_id) REFERENCES public.planner_event(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: planner_event_attendees_contacts planner_event_attend_event_id_7a6e26bc_fk_planner_e; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.planner_event_attendees_contacts
    ADD CONSTRAINT planner_event_attend_event_id_7a6e26bc_fk_planner_e FOREIGN KEY (event_id) REFERENCES public.planner_event(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: planner_event_attendees_user planner_event_attend_event_id_f806e2a6_fk_planner_e; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.planner_event_attendees_user
    ADD CONSTRAINT planner_event_attend_event_id_f806e2a6_fk_planner_e FOREIGN KEY (event_id) REFERENCES public.planner_event(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: planner_event_attendees_leads planner_event_attendees_leads_lead_id_b543353a_fk_leads_lead_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.planner_event_attendees_leads
    ADD CONSTRAINT planner_event_attendees_leads_lead_id_b543353a_fk_leads_lead_id FOREIGN KEY (lead_id) REFERENCES public.leads_lead(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: planner_event_attendees_user planner_event_attendees_user_user_id_d6b53a5e_fk_common_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.planner_event_attendees_user
    ADD CONSTRAINT planner_event_attendees_user_user_id_d6b53a5e_fk_common_user_id FOREIGN KEY (user_id) REFERENCES public.common_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: planner_event planner_event_content_type_id_e1697281_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.planner_event
    ADD CONSTRAINT planner_event_content_type_id_e1697281_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: planner_event planner_event_created_by_id_ff507edf_fk_common_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.planner_event
    ADD CONSTRAINT planner_event_created_by_id_ff507edf_fk_common_user_id FOREIGN KEY (created_by_id) REFERENCES public.common_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: planner_event_reminders planner_event_remind_reminder_id_a980f736_fk_planner_r; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.planner_event_reminders
    ADD CONSTRAINT planner_event_remind_reminder_id_a980f736_fk_planner_r FOREIGN KEY (reminder_id) REFERENCES public.planner_reminder(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: planner_event_reminders planner_event_reminders_event_id_9c33650c_fk_planner_event_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.planner_event_reminders
    ADD CONSTRAINT planner_event_reminders_event_id_9c33650c_fk_planner_event_id FOREIGN KEY (event_id) REFERENCES public.planner_event(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: planner_event planner_event_updated_by_id_1a3b400a_fk_common_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.planner_event
    ADD CONSTRAINT planner_event_updated_by_id_1a3b400a_fk_common_user_id FOREIGN KEY (updated_by_id) REFERENCES public.common_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: project_expenses_projectexpense project_expenses_pro_expense_type_id_055551ef_fk_project_e; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.project_expenses_projectexpense
    ADD CONSTRAINT project_expenses_pro_expense_type_id_055551ef_fk_project_e FOREIGN KEY (expense_type_id) REFERENCES public.project_expenses_expensetype(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: project_expenses_projectexpense project_expenses_pro_project_id_64d3d992_fk_projects_; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.project_expenses_projectexpense
    ADD CONSTRAINT project_expenses_pro_project_id_64d3d992_fk_projects_ FOREIGN KEY (project_id) REFERENCES public.projects_project(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: project_items_item_item_properties project_items_item_i_item_id_94cb7d40_fk_project_i; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.project_items_item_item_properties
    ADD CONSTRAINT project_items_item_i_item_id_94cb7d40_fk_project_i FOREIGN KEY (item_id) REFERENCES public.project_items_item(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: project_items_item_item_properties project_items_item_i_itemproperty_id_ce36b063_fk_project_i; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.project_items_item_item_properties
    ADD CONSTRAINT project_items_item_i_itemproperty_id_ce36b063_fk_project_i FOREIGN KEY (itemproperty_id) REFERENCES public.project_items_itemproperty(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: project_items_item project_items_item_item_type_id_547d8eba_fk_project_i; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.project_items_item
    ADD CONSTRAINT project_items_item_item_type_id_547d8eba_fk_project_i FOREIGN KEY (item_type_id) REFERENCES public.project_items_itemtype(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: project_items_itemformula project_items_itemfo_item_id_c9ba87fc_fk_project_i; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.project_items_itemformula
    ADD CONSTRAINT project_items_itemfo_item_id_c9ba87fc_fk_project_i FOREIGN KEY (item_id) REFERENCES public.project_items_item(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: project_items_itemtypematerial project_items_itemty_item_type_id_e402a683_fk_project_i; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.project_items_itemtypematerial
    ADD CONSTRAINT project_items_itemty_item_type_id_e402a683_fk_project_i FOREIGN KEY (item_type_id) REFERENCES public.project_items_itemtype(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: project_misc_projectmisc project_misc_project_misc_id_64c4a54b_fk_project_m; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.project_misc_projectmisc
    ADD CONSTRAINT project_misc_project_misc_id_64c4a54b_fk_project_m FOREIGN KEY (misc_id) REFERENCES public.project_misc_misc(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: project_misc_projectmisc project_misc_project_project_id_2b8485b5_fk_projects_; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.project_misc_projectmisc
    ADD CONSTRAINT project_misc_project_project_id_2b8485b5_fk_projects_ FOREIGN KEY (project_id) REFERENCES public.projects_project(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: project_timetable_projectmilestone project_timetable_pr_project_id_319ea6aa_fk_projects_; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.project_timetable_projectmilestone
    ADD CONSTRAINT project_timetable_pr_project_id_319ea6aa_fk_projects_ FOREIGN KEY (project_id) REFERENCES public.projects_project(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: project_timetable_projectwork project_timetable_pr_project_id_7b7200d0_fk_projects_; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.project_timetable_projectwork
    ADD CONSTRAINT project_timetable_pr_project_id_7b7200d0_fk_projects_ FOREIGN KEY (project_id) REFERENCES public.projects_project(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: projects_companyprojectcomparison projects_companyproj_company_id_cfbc7a33_fk_companies; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects_companyprojectcomparison
    ADD CONSTRAINT projects_companyproj_company_id_cfbc7a33_fk_companies FOREIGN KEY (company_id) REFERENCES public.companies_company(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: projects_companyprojectcomparison_projects projects_companyproj_companyprojectcompar_73145583_fk_projects_; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects_companyprojectcomparison_projects
    ADD CONSTRAINT projects_companyproj_companyprojectcompar_73145583_fk_projects_ FOREIGN KEY (companyprojectcomparison_id) REFERENCES public.projects_companyprojectcomparison(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: projects_companyprojectcomparison_projects projects_companyproj_project_id_b6cfd7c7_fk_projects_; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects_companyprojectcomparison_projects
    ADD CONSTRAINT projects_companyproj_project_id_b6cfd7c7_fk_projects_ FOREIGN KEY (project_id) REFERENCES public.projects_project(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: projects_project projects_project_company_id_66b5c58b_fk_companies_company_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects_project
    ADD CONSTRAINT projects_project_company_id_66b5c58b_fk_companies_company_id FOREIGN KEY (company_id) REFERENCES public.companies_company(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: projects_project projects_project_created_by_id_c49d7b6d_fk_common_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects_project
    ADD CONSTRAINT projects_project_created_by_id_c49d7b6d_fk_common_user_id FOREIGN KEY (created_by_id) REFERENCES public.common_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: projects_projecthistory projects_projecthist_from_address_id_ae28216a_fk_common_ad; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects_projecthistory
    ADD CONSTRAINT projects_projecthist_from_address_id_ae28216a_fk_common_ad FOREIGN KEY (from_address_id) REFERENCES public.common_address(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: projects_projecthistory projects_projecthist_project_id_2bbe7236_fk_projects_; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects_projecthistory
    ADD CONSTRAINT projects_projecthist_project_id_2bbe7236_fk_projects_ FOREIGN KEY (project_id) REFERENCES public.projects_project(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: projects_projecthistory_assigned_to projects_projecthist_projecthistory_id_d6490520_fk_projects_; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects_projecthistory_assigned_to
    ADD CONSTRAINT projects_projecthist_projecthistory_id_d6490520_fk_projects_ FOREIGN KEY (projecthistory_id) REFERENCES public.projects_projecthistory(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: projects_projecthistory projects_projecthist_to_address_id_a3022acd_fk_common_ad; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects_projecthistory
    ADD CONSTRAINT projects_projecthist_to_address_id_a3022acd_fk_common_ad FOREIGN KEY (to_address_id) REFERENCES public.common_address(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: projects_projecthistory projects_projecthist_updated_by_id_3ca3d6b3_fk_common_us; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects_projecthistory
    ADD CONSTRAINT projects_projecthist_updated_by_id_3ca3d6b3_fk_common_us FOREIGN KEY (updated_by_id) REFERENCES public.common_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: projects_projecthistory_assigned_to projects_projecthist_user_id_6d816790_fk_common_us; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects_projecthistory_assigned_to
    ADD CONSTRAINT projects_projecthist_user_id_6d816790_fk_common_us FOREIGN KEY (user_id) REFERENCES public.common_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: projects_projectimageset projects_projectimag_project_milestone_id_d548a3e0_fk_project_t; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects_projectimageset
    ADD CONSTRAINT projects_projectimag_project_milestone_id_d548a3e0_fk_project_t FOREIGN KEY (project_milestone_id) REFERENCES public.project_timetable_projectmilestone(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: projects_projectimageset_imgs projects_projectimag_projectimage_id_b6ebbc55_fk_projects_; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects_projectimageset_imgs
    ADD CONSTRAINT projects_projectimag_projectimage_id_b6ebbc55_fk_projects_ FOREIGN KEY (projectimage_id) REFERENCES public.projects_projectimage(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: projects_projectimageset_imgs projects_projectimag_projectimageset_id_f87d1b7e_fk_projects_; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects_projectimageset_imgs
    ADD CONSTRAINT projects_projectimag_projectimageset_id_f87d1b7e_fk_projects_ FOREIGN KEY (projectimageset_id) REFERENCES public.projects_projectimageset(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: projects_projectimageset projects_projectimag_related_project_id_1e8f4d16_fk_projects_; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects_projectimageset
    ADD CONSTRAINT projects_projectimag_related_project_id_1e8f4d16_fk_projects_ FOREIGN KEY (related_project_id) REFERENCES public.projects_project(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: projects_projectimage projects_projectimag_related_project_id_d9c75c44_fk_projects_; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects_projectimage
    ADD CONSTRAINT projects_projectimag_related_project_id_d9c75c44_fk_projects_ FOREIGN KEY (related_project_id) REFERENCES public.projects_project(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: projects_projectinvoice projects_projectinvo_project_id_7ebf8b67_fk_projects_; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects_projectinvoice
    ADD CONSTRAINT projects_projectinvo_project_id_7ebf8b67_fk_projects_ FOREIGN KEY (project_id) REFERENCES public.projects_project(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: projects_projectreceipt projects_projectrece_project_id_437bb88a_fk_projects_; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects_projectreceipt
    ADD CONSTRAINT projects_projectrece_project_id_437bb88a_fk_projects_ FOREIGN KEY (project_id) REFERENCES public.projects_project(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: quotations_quotation quotations_quotation_approved_by_id_5c8a042e_fk_common_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.quotations_quotation
    ADD CONSTRAINT quotations_quotation_approved_by_id_5c8a042e_fk_common_user_id FOREIGN KEY (approved_by_id) REFERENCES public.common_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: quotations_quotation_companies quotations_quotation_company_id_0493e81f_fk_companies; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.quotations_quotation_companies
    ADD CONSTRAINT quotations_quotation_company_id_0493e81f_fk_companies FOREIGN KEY (company_id) REFERENCES public.companies_company(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: quotations_quotation quotations_quotation_created_by_id_f86a7566_fk_common_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.quotations_quotation
    ADD CONSTRAINT quotations_quotation_created_by_id_f86a7566_fk_common_user_id FOREIGN KEY (created_by_id) REFERENCES public.common_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: quotations_quotationhistory quotations_quotation_from_address_id_95f05125_fk_common_ad; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.quotations_quotationhistory
    ADD CONSTRAINT quotations_quotation_from_address_id_95f05125_fk_common_ad FOREIGN KEY (from_address_id) REFERENCES public.common_address(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: quotations_quotation quotations_quotation_from_address_id_c5ab9397_fk_common_ad; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.quotations_quotation
    ADD CONSTRAINT quotations_quotation_from_address_id_c5ab9397_fk_common_ad FOREIGN KEY (from_address_id) REFERENCES public.common_address(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: quotations_quotation quotations_quotation_last_updated_by_id_0ad36aaa_fk_common_us; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.quotations_quotation
    ADD CONSTRAINT quotations_quotation_last_updated_by_id_0ad36aaa_fk_common_us FOREIGN KEY (last_updated_by_id) REFERENCES public.common_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: quotations_quotation_teams quotations_quotation_quotation_id_40df249e_fk_quotation; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.quotations_quotation_teams
    ADD CONSTRAINT quotations_quotation_quotation_id_40df249e_fk_quotation FOREIGN KEY (quotation_id) REFERENCES public.quotations_quotation(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: quotations_quotation_assigned_to quotations_quotation_quotation_id_47354fdf_fk_quotation; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.quotations_quotation_assigned_to
    ADD CONSTRAINT quotations_quotation_quotation_id_47354fdf_fk_quotation FOREIGN KEY (quotation_id) REFERENCES public.quotations_quotation(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: quotations_quotation_companies quotations_quotation_quotation_id_57749bb7_fk_quotation; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.quotations_quotation_companies
    ADD CONSTRAINT quotations_quotation_quotation_id_57749bb7_fk_quotation FOREIGN KEY (quotation_id) REFERENCES public.quotations_quotation(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: quotations_quotationhistory quotations_quotation_quotation_id_da50d945_fk_quotation; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.quotations_quotationhistory
    ADD CONSTRAINT quotations_quotation_quotation_id_da50d945_fk_quotation FOREIGN KEY (quotation_id) REFERENCES public.quotations_quotation(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: quotations_quotationhistory_assigned_to quotations_quotation_quotationhistory_id_adf697b4_fk_quotation; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.quotations_quotationhistory_assigned_to
    ADD CONSTRAINT quotations_quotation_quotationhistory_id_adf697b4_fk_quotation FOREIGN KEY (quotationhistory_id) REFERENCES public.quotations_quotationhistory(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: quotations_quotation_teams quotations_quotation_teams_teams_id_1a13ccfe_fk_teams_teams_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.quotations_quotation_teams
    ADD CONSTRAINT quotations_quotation_teams_teams_id_1a13ccfe_fk_teams_teams_id FOREIGN KEY (teams_id) REFERENCES public.teams_teams(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: quotations_quotation quotations_quotation_to_address_id_5047eb68_fk_common_ad; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.quotations_quotation
    ADD CONSTRAINT quotations_quotation_to_address_id_5047eb68_fk_common_ad FOREIGN KEY (to_address_id) REFERENCES public.common_address(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: quotations_quotationhistory quotations_quotation_to_address_id_e224b1e3_fk_common_ad; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.quotations_quotationhistory
    ADD CONSTRAINT quotations_quotation_to_address_id_e224b1e3_fk_common_ad FOREIGN KEY (to_address_id) REFERENCES public.common_address(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: quotations_quotationhistory quotations_quotation_updated_by_id_d4b10b58_fk_common_us; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.quotations_quotationhistory
    ADD CONSTRAINT quotations_quotation_updated_by_id_d4b10b58_fk_common_us FOREIGN KEY (updated_by_id) REFERENCES public.common_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: quotations_quotationhistory_assigned_to quotations_quotation_user_id_05a80596_fk_common_us; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.quotations_quotationhistory_assigned_to
    ADD CONSTRAINT quotations_quotation_user_id_05a80596_fk_common_us FOREIGN KEY (user_id) REFERENCES public.common_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: quotations_quotation_assigned_to quotations_quotation_user_id_7af1c95f_fk_common_us; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.quotations_quotation_assigned_to
    ADD CONSTRAINT quotations_quotation_user_id_7af1c95f_fk_common_us FOREIGN KEY (user_id) REFERENCES public.common_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: rooms_room rooms_room_related_project_id_520c6c88_fk_projects_project_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rooms_room
    ADD CONSTRAINT rooms_room_related_project_id_520c6c88_fk_projects_project_id FOREIGN KEY (related_project_id) REFERENCES public.projects_project(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: rooms_room rooms_room_room_type_id_d6bd9615_fk_rooms_roomtype_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rooms_room
    ADD CONSTRAINT rooms_room_room_type_id_d6bd9615_fk_rooms_roomtype_id FOREIGN KEY (room_type_id) REFERENCES public.rooms_roomtype(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: rooms_roomitem rooms_roomitem_item_id_474eaabc_fk_project_items_item_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rooms_roomitem
    ADD CONSTRAINT rooms_roomitem_item_id_474eaabc_fk_project_items_item_id FOREIGN KEY (item_id) REFERENCES public.project_items_item(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: rooms_roomitem rooms_roomitem_room_id_184c0f52_fk_rooms_room_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rooms_roomitem
    ADD CONSTRAINT rooms_roomitem_room_id_184c0f52_fk_rooms_room_id FOREIGN KEY (room_id) REFERENCES public.rooms_room(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: rooms_roomtype_related_items rooms_roomtype_relat_item_id_b808a064_fk_project_i; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rooms_roomtype_related_items
    ADD CONSTRAINT rooms_roomtype_relat_item_id_b808a064_fk_project_i FOREIGN KEY (item_id) REFERENCES public.project_items_item(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: rooms_roomtype_related_items rooms_roomtype_relat_roomtype_id_79027218_fk_rooms_roo; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rooms_roomtype_related_items
    ADD CONSTRAINT rooms_roomtype_relat_roomtype_id_79027218_fk_rooms_roo FOREIGN KEY (roomtype_id) REFERENCES public.rooms_roomtype(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: rooms_roomtype_room_properties rooms_roomtype_room__roomproperty_id_34f8a1e2_fk_rooms_roo; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rooms_roomtype_room_properties
    ADD CONSTRAINT rooms_roomtype_room__roomproperty_id_34f8a1e2_fk_rooms_roo FOREIGN KEY (roomproperty_id) REFERENCES public.rooms_roomproperty(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: rooms_roomtype_room_properties rooms_roomtype_room__roomtype_id_e08c5f05_fk_rooms_roo; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rooms_roomtype_room_properties
    ADD CONSTRAINT rooms_roomtype_room__roomtype_id_e08c5f05_fk_rooms_roo FOREIGN KEY (roomtype_id) REFERENCES public.rooms_roomtype(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: rooms_roomtypeformula rooms_roomtypeformul_room_type_id_69b586c5_fk_rooms_roo; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rooms_roomtypeformula
    ADD CONSTRAINT rooms_roomtypeformul_room_type_id_69b586c5_fk_rooms_roo FOREIGN KEY (room_type_id) REFERENCES public.rooms_roomtype(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: subscription_plans_companysubscribedplan subscription_plans_c_company_id_d41fd89e_fk_companies; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subscription_plans_companysubscribedplan
    ADD CONSTRAINT subscription_plans_c_company_id_d41fd89e_fk_companies FOREIGN KEY (company_id) REFERENCES public.companies_company(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: subscription_plans_companysubscribedplan subscription_plans_c_plan_id_2c228c31_fk_subscript; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subscription_plans_companysubscribedplan
    ADD CONSTRAINT subscription_plans_c_plan_id_2c228c31_fk_subscript FOREIGN KEY (plan_id) REFERENCES public.subscription_plans_subscriptionplan(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tasks_task_assigned_to tasks_task_assigned_to_task_id_daf1a7ac_fk_tasks_task_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tasks_task_assigned_to
    ADD CONSTRAINT tasks_task_assigned_to_task_id_daf1a7ac_fk_tasks_task_id FOREIGN KEY (task_id) REFERENCES public.tasks_task(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tasks_task_assigned_to tasks_task_assigned_to_user_id_a003647a_fk_common_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tasks_task_assigned_to
    ADD CONSTRAINT tasks_task_assigned_to_user_id_a003647a_fk_common_user_id FOREIGN KEY (user_id) REFERENCES public.common_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tasks_task tasks_task_company_id_f699f141_fk_companies_company_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tasks_task
    ADD CONSTRAINT tasks_task_company_id_f699f141_fk_companies_company_id FOREIGN KEY (company_id) REFERENCES public.companies_company(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tasks_task_contacts tasks_task_contacts_contact_id_29ef4ac7_fk_contacts_contact_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tasks_task_contacts
    ADD CONSTRAINT tasks_task_contacts_contact_id_29ef4ac7_fk_contacts_contact_id FOREIGN KEY (contact_id) REFERENCES public.contacts_contact(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tasks_task_contacts tasks_task_contacts_task_id_90df7d53_fk_tasks_task_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tasks_task_contacts
    ADD CONSTRAINT tasks_task_contacts_task_id_90df7d53_fk_tasks_task_id FOREIGN KEY (task_id) REFERENCES public.tasks_task(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tasks_task tasks_task_created_by_id_1345568a_fk_common_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tasks_task
    ADD CONSTRAINT tasks_task_created_by_id_1345568a_fk_common_user_id FOREIGN KEY (created_by_id) REFERENCES public.common_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tasks_task_teams tasks_task_teams_task_id_d1e3d547_fk_tasks_task_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tasks_task_teams
    ADD CONSTRAINT tasks_task_teams_task_id_d1e3d547_fk_tasks_task_id FOREIGN KEY (task_id) REFERENCES public.tasks_task(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tasks_task_teams tasks_task_teams_teams_id_69d613d1_fk_teams_teams_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tasks_task_teams
    ADD CONSTRAINT tasks_task_teams_teams_id_69d613d1_fk_teams_teams_id FOREIGN KEY (teams_id) REFERENCES public.teams_teams(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: teams_teams teams_teams_created_by_id_c6e9aee3_fk_common_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.teams_teams
    ADD CONSTRAINT teams_teams_created_by_id_c6e9aee3_fk_common_user_id FOREIGN KEY (created_by_id) REFERENCES public.common_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: teams_teams_users teams_teams_users_teams_id_14b49914_fk_teams_teams_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.teams_teams_users
    ADD CONSTRAINT teams_teams_users_teams_id_14b49914_fk_teams_teams_id FOREIGN KEY (teams_id) REFERENCES public.teams_teams(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: teams_teams_users teams_teams_users_user_id_f834347a_fk_common_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.teams_teams_users
    ADD CONSTRAINT teams_teams_users_user_id_f834347a_fk_common_user_id FOREIGN KEY (user_id) REFERENCES public.common_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: token_blacklist_blacklistedtoken token_blacklist_blac_token_id_3cc7fe56_fk_token_bla; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.token_blacklist_blacklistedtoken
    ADD CONSTRAINT token_blacklist_blac_token_id_3cc7fe56_fk_token_bla FOREIGN KEY (token_id) REFERENCES public.token_blacklist_outstandingtoken(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: token_blacklist_outstandingtoken token_blacklist_outs_user_id_83bc629a_fk_common_us; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.token_blacklist_outstandingtoken
    ADD CONSTRAINT token_blacklist_outs_user_id_83bc629a_fk_common_us FOREIGN KEY (user_id) REFERENCES public.common_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

