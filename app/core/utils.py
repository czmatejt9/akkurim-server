def generate_sql_insert(
    table: str,
    data: dict,
) -> tuple[str, tuple]:
    columns = ", ".join(data.keys())
    placeholders = ", ".join(["%s" for _ in data.values()])
    return f"INSERT INTO {table} ({columns}) VALUES ({placeholders});", tuple(
        data.values()
    )


def generate_sql_read(
    table: str,
    columns: list[str],
    conditions: dict = {},
) -> tuple[str, tuple]:
    columns = ", ".join(columns)
    conditions = " AND ".join([f"{key} = %s" for key in conditions.keys()])
    return f"SELECT {columns} FROM {table} WHERE {conditions};", tuple(
        conditions.values()
    )
