# gunicorn-healthz-filter

Filter /healthz endpoint access from your gunicorn logs.

## Usage

```
gunicorn --logger-class "gunicorn_healthz_filter.Logger" --access-logfile - app
```
