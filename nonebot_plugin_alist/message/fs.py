def file_list_msg(file_list: list) -> str:
    def bytes_format(value):
        units = ["B", "KB", "MB", "GB", "TB", "PB"]
        size = 1024.0
        for unit in units:
            if value < size:
                return f"{value:.2f}{unit}"
            value /= size

    def file_msg(file):
        name = file["name"]
        is_dir = file["is_dir"]
        size = bytes_format(file["size"])
        if is_dir:
            name = name + "/"
            return f"-{name}"
        return f"-{name}    {size}"

    file_list = [file_msg(file) for file in file_list]
    return "\n".join(file_list)
