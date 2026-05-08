from datetime import date

def is_overdue(deadline: date) -> bool:
    """Check if a task is overdue"""
    if deadline:
        return deadline < date.today()
    return False
