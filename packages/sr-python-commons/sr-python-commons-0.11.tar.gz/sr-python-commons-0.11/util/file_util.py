

def read_to_str(path: str, encoding='utf-8'):
    with open(path, 'r', encoding=encoding) as file:
        return file.read()


def write(path: str, content, encoding='utf-8'):
    with open(path, 'w', encoding=encoding) as file:
        return file.write(content)
