def ConvertRecordToList(record: list):
    """Конвертирует список из asyncpg.Record к Python типам"""
    return [
        (
            el['row'][0],
            el['row'][1],
            el['row'][2]
        )
        for el in record
    ]
