FROM postgres:9.6.5

ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=123
ENV POSTGRES_DB=is

COPY schema.sql /docker-entrypoint-initdb.d/

EXPOSE 5470