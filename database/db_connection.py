# ============================================================
# database/db_connection.py
# Cybercrime Incident Management System (CIMS)
# ============================================================
# External database connectivity (MySQL/Aiven) has been removed.
# The system now runs exclusively using local CSV datasets in
# the `data/` directory.
# ============================================================

def is_database_enabled() -> bool:
    """Returns False since the application now uses CSV data store."""
    return False
