from datetime import datetime
from textwrap import dedent

import pytest

from juniorguru.web import template_filters


def test_email_link():
    markup = str(template_filters.email_link('xyz@example.com'))
    assert markup == '<a href="mailto:xyz&#64;example.com">xyz&#64;<!---->example.com</a>'


def test_md():
    markup = str(template_filters.md('call me **maybe**  \ncall me Honza'))
    assert markup == '<p>call me <strong>maybe</strong><br>\ncall me Honza</p>'


def test_md_heading_level_base():
    markup = str(template_filters.md(dedent('''
        # Heading 1
        ## Heading 2
        Paragraph text
    '''), heading_level_base=4)).strip()
    assert markup == dedent('''
        <h4 id="heading-1">Heading 1</h4>
        <h5 id="heading-2">Heading 2</h5>
        <p>Paragraph text</p>
    ''').strip()


@pytest.mark.parametrize('requirement,expected', [
    ('mainstream programming language', 'základy programování'),
    ('databases', 'databáze'),
    ('data analysis', 'datová analýza'),
    ('servers and operations', 'správa serverů'),
    ('web backend', 'webový backend'),
    ('web frontend', 'webový frontend'),
    ('mobile apps development', 'mobilní aplikace'),
    ('mobile apps', 'mobilní aplikace'),
    ('gargamel', 'gargamel'),
])
def test_job_requirement(requirement, expected):
    assert template_filters.job_requirement(requirement) == expected


@pytest.mark.parametrize('type_,expected', [
    ('full-time', 'plný úvazek'),
    ('part-time', 'částečný úvazek'),
    ('contract', 'kontrakt'),
    ('internship', 'stáž'),
    ('paid internship', 'placená stáž'),
    ('unpaid internship', 'neplacená stáž'),
    ('volunteering', 'dobrovolnictví'),
    ('gargamel', 'gargamel'),
])
def test_employment_type(type_, expected):
    assert template_filters.employment_type(type_) == expected


@pytest.mark.parametrize('types,expected', [
    (['part-time'], 'částečný úvazek'),
    (['part-time', 'gargamel', 'volunteering'], 'částečný úvazek, gargamel, dobrovolnictví'),
])
def test_employment_types(types, expected):
    assert template_filters.employment_types(types) == expected


def test_employment_types_empty():
    with pytest.raises(ValueError):
        template_filters.employment_types([])


@pytest.mark.parametrize('types,sep,expected', [
    (['part-time'], '/', 'částečný úvazek'),
    (['part-time', 'gargamel'], '/', 'částečný úvazek/gargamel'),
])
def test_employment_types_custom_separator(types, sep, expected):
    assert template_filters.employment_types(types, sep) == expected


@pytest.mark.parametrize('dt_str,expected', [
    ('2020-04-21 12:01:48', datetime(2020, 4, 21, 12, 1, 48)),
    ('2020-04-21T12:01:48', datetime(2020, 4, 21, 12, 1, 48)),
])
def test_to_datetime(dt_str, expected):
    assert template_filters.to_datetime(dt_str) == expected


@pytest.mark.parametrize('dt,expected', [
    (datetime(2019, 12, 10, 16, 20, 42), 'dnes'),
    (datetime(2019, 12, 9, 16, 20, 42), 'včera'),
    (datetime(2019, 12, 8, 16, 20, 42), 'předevčírem'),
    (datetime(2019, 12, 7, 16, 20, 42), 'před 3 dny'),
    (datetime(2019, 11, 30, 16, 20, 42), 'před 10 dny'),
    (datetime(2019, 10, 31, 16, 20, 42), 'před 40 dny'),
])
def test_ago(dt, expected):
    now = datetime(2019, 12, 10, 16, 20, 42)
    assert template_filters.ago(dt, now=now) == expected
