from datetime import datetime, date

from services.exceptions import ValidationError


def parse_date(value, nome_campo="data"):
    if value is None:
        raise ValidationError(f"O campo '{nome_campo}' é obrigatório.")
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        for formato in ("%Y-%m-%d", "%d/%m/%Y"):
            try:
                return datetime.strptime(value, formato).date()
            except ValueError:
                continue
    raise ValidationError(
        f"O campo '{nome_campo}' deve ser uma data válida (AAAA-MM-DD)."
    )


def to_float_or_none(value, nome_campo):
    if value is None:
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        raise ValidationError(f"O campo '{nome_campo}' deve ser numérico.")
    return number
