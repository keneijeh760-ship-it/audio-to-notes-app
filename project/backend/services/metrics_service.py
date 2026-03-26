from datetime import datetime
from project.backend.supabase_service import supabase

def get_metrics():
    res = supabase.table("metrics").select("*").limit(1).execute()
    return res.data[0]

def update_metrics(field, value):
    metrics = get_metrics()

    supabase.table("metrics").update({
        field: metrics[field] + value,
        "updated_at": datetime.utcnow().isoformat()
    }).eq("id", metrics["id"]).execute()