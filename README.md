# Hive Pulse - A django project for clustering and ranking of movies & seasons

### ReadMe version 0.0.1

./secrets.json

```
{
    "secret_key": "",
    "debug_mode": "",
    "db_pass": "db_password",
    "db_user": "db_user",
    "db_name": "db_name",
    "db_host": "db_host",
    "db_port": "db_port_as_string_even_if_it_is_a_number",
    "email_host": "",
    "email_user": "",
    "email_password": ""
}
```

project structure

hive-pulse {

    AuthApp,

    BlogApp,

    HivePulse,

    MoviesApp,

    aiven-ca.pem,

    manage.py,

    secrets.json,

    .env,

    requirements.txt

}


.env structure


SECRET_KEY=""

DEBUG=""

DB_NAME=""

DB_USER=""

DB_PASSWORD=""

DB_HOST=""

DB_PORT=""

EMAIL_HOST=""

EMAIL_HOST_USER=""

EMAIL_HOST_PASSWORD=""
