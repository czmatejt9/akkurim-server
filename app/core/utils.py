import uuid


def generate_sql_insert(
    tenant_id: str,
    table: str,
    data: dict,
) -> tuple[str, tuple]:
    columns = ", ".join(data.keys())
    placeholders = ", ".join([f"${i + 1}" for i in range(len(data))])
    return (
        f"INSERT INTO {tenant_id}.{table} ({columns}) VALUES ({placeholders});",
        tuple(data.values()),
    )


def generate_sql_insert_with_returning(
    tenant_id: str,
    table: str,
    data: dict,
    returning: list[str],
) -> tuple[str, tuple]:
    columns = ", ".join(data.keys())
    placeholders = ", ".join([f"${i + 1}" for i in range(len(data))])
    returning_str = ", ".join(returning)
    return (
        f"INSERT INTO {tenant_id}.{table} ({columns}) VALUES ({placeholders}) RETURNING {returning_str};",
        tuple(
            data.values(),
        ),
    )


def generate_sql_read(
    tenant_id: str,
    table: str,
    columns: list[str],
    conditions: dict = {},
) -> tuple[str, tuple]:
    columns = ", ".join(columns)
    conditions_str = " AND ".join(
        [f"{key} = ${i + 1}" for i, key in enumerate(conditions.keys())]
    )
    return f"SELECT {columns} FROM {tenant_id}.{table} WHERE {conditions_str};", tuple(
        conditions.values()
    )


def generate_sql_update(
    tenant_id: str,
    table: str,
    data: dict,
    conditions: dict,
) -> tuple[str, tuple]:
    columns = ", ".join([f"{key} = ${i + 1}" for i, key in enumerate(data.keys())])
    conditions_str = " AND ".join(
        [f"{key} = ${i + 1}" for i, key in enumerate(conditions.keys())]
    )
    return (
        f"UPDATE {tenant_id}.{table} SET {columns} WHERE {conditions_str};",
        tuple(
            [*data.values(), *conditions.values()],
        ),
    )


def generate_sql_update_with_returning(
    tenant_id: str,
    table: str,
    data: dict,
    conditions: dict,
    returning: list[str],
) -> tuple[str, tuple]:
    columns = ", ".join([f"{key} = ${i + 1}" for i, key in enumerate(data.keys())])
    conditions_str = " AND ".join(
        [f"{key} = ${i + 1 + len(data)}" for i, key in enumerate(conditions.keys())]
    )
    returning_str = ", ".join(returning)
    return (
        f"UPDATE {tenant_id}.{table} SET {columns} WHERE {conditions_str} RETURNING {returning_str};",
        tuple(
            [*data.values(), *conditions.values()],
        ),
    )


def generate_sql_delete_with_returning(
    tenant_id: str,
    table: str,
    conditions: dict,
) -> tuple[str, tuple]:
    conditions_str = " AND ".join(
        [f"{key} = ${i + 1}" for i, key in enumerate(conditions.keys())]
    )
    return (
        f"DELETE FROM {tenant_id}.{table} WHERE {conditions_str} RETURNING id;",
        tuple(conditions.values()),
    )


def convert_uuid_to_str(data: dict) -> dict:
    for key, value in data.items():
        if isinstance(value, uuid.UUID):
            data[key] = str(value)
    return data
