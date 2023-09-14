FROM postgres:14.1-alpine

# Original postgresql init script expects empty $PGDATA so we initially place
# certificates into the image to the intermediate directory
COPY /ssl/postgresql.crt /tmp.ssl/server.crt
COPY /ssl/postgresql.key /tmp.ssl/server.key
#COPY /ssl/ca/example.cossacklabs.com.crt /tmp.ssl/root.crt
COPY /ssl/ca/localhost.crt /tmp.ssl/root.crt

RUN chown -R postgres:postgres /tmp.ssl

COPY scripts/postgresql-ssl-configure.sh /docker-entrypoint-initdb.d/
