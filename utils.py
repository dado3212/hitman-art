def hash_value_to_file(hash: int, resource_type: str) -> str:
    main = format(hash, 'x').upper()
    return main.rjust(16, '0') + '.' + resource_type