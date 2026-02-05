/* {{ cookiecutter.project_name }}
 * {{ cookiecutter.description }}
 * Built with Cosmopolitan Libc
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
{% if cookiecutter.use_sqlite == "yes" %}
#include "db/database.h"
{% endif %}

int main(int argc, char *argv[]) {
    (void)argc; (void)argv;
{% if cookiecutter.use_sqlite == "yes" %}
    sqlite3 *db;
    if (mhi_db_open(&db, "{{ cookiecutter.project_slug }}.db") != 0) {
        fprintf(stderr, "Failed to open database\n");
        return 1;
    }
    mhi_db_init_schema(db);
    printf("{{ cookiecutter.project_name }} initialized (SQLite ready)\n");
    mhi_db_close(db);
{% else %}
    printf("{{ cookiecutter.project_name }} started\n");
{% endif %}
    return 0;
}
