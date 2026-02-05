/* {{ cookiecutter.project_name }} — Tests */
#include <stdio.h>
#include <string.h>
{% if cookiecutter.use_sqlite == "yes" %}
#include <sqlite3.h>
#include "db/database.h"
{% endif %}

static int tests_run = 0, tests_passed = 0, tests_failed = 0;

#define TEST(name) static void name(void)
#define RUN(name) do { \
    printf("  %-50s ", #name); \
    tests_run++; \
    name(); \
    tests_passed++; \
    printf("PASS\n"); \
} while(0)
#define ASSERT(cond) do { if (!(cond)) { \
    printf("FAIL\n    ASSERT FAILED: %s [%s:%d]\n", #cond, __FILE__, __LINE__); \
    tests_failed++; tests_passed--; return; \
}} while(0)
#define ASSERT_EQ(a, b) ASSERT((a) == (b))
#define ASSERT_STR(a, b) ASSERT(strcmp((a), (b)) == 0)

{% if cookiecutter.use_sqlite == "yes" %}
TEST(test_schema_init) {
    sqlite3 *db;
    ASSERT_EQ(mhi_db_open(&db, ":memory:"), 0);
    ASSERT_EQ(mhi_db_init_schema(db), 0);
    mhi_db_close(db);
}
{% endif %}

TEST(test_basic) {
    ASSERT(1 + 1 == 2);
}

int main(void) {
    printf("\n{{ cookiecutter.project_name }} Tests\n\n");

    RUN(test_basic);
{% if cookiecutter.use_sqlite == "yes" %}
    RUN(test_schema_init);
{% endif %}

    printf("\n  TOTAL: %d  |  PASSED: %d  |  FAILED: %d\n\n",
           tests_run, tests_passed, tests_failed);
    return tests_failed > 0 ? 1 : 0;
}
