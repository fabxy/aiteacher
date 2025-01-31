from fastapi import APIRouter
from app.schemas import SQLQuery

router = APIRouter()

@router.post("/run/")
def run_query(sql_query: SQLQuery):
    try:
        import duckdb
        con = duckdb.connect(database=':memory:', read_only=False)
        result = con.execute(sql_query.query).fetchall()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}