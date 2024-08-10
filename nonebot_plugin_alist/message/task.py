def take_info_msg(task):
    task_id = task["id"]
    task_name = task["name"]
    task_status = f"{status}" if (status := task["status"]) else "无"
    task_progress = f"{int(task['progress'])}%"
    return (
        f"任务ID: {task_id}\n"
        f"任务信息: {task_name}\n"
        f"任务状态: {task_status}\n"
        f"任务进度: {task_progress}\n"
    )


def task_list_msg(tasks):
    return "\n".join(map(take_info_msg, tasks))
