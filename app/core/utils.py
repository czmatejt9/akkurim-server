def generate_sql_insert(
    table: str,
    data: dict,
) -> tuple[str, tuple]:
    columns = ", ".join(data.keys())
    placeholders = ", ".join([f"${i + 1}" for i in range(len(data))])
    return f"INSERT INTO {table} ({columns}) VALUES ({placeholders});", tuple(
        data.values()
    )


def generate_sql_insert_with_returning(
    table: str,
    data: dict,
    returning: list[str],
) -> tuple[str, tuple]:
    columns = ", ".join(data.keys())
    placeholders = ", ".join([f"${i + 1}" for i in range(len(data))])
    returning_str = ", ".join(returning)
    return (
        f"INSERT INTO {table} ({columns}) VALUES ({placeholders}) RETURNING {returning_str};",
        tuple(
            data.values(),
        ),
    )


def generate_sql_read(
    table: str,
    columns: list[str],
    conditions: dict = {},
) -> tuple[str, tuple]:
    columns = ", ".join(columns)
    conditions_str = " AND ".join(
        [f"{key} = ${i + 1}" for i, key in enumerate(conditions.keys())]
    )
    return f"SELECT {columns} FROM {table} WHERE {conditions_str};", tuple(
        conditions.values()
    )
