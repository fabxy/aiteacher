from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

# Define Pydantic schema for request validation
class SQLQuery(BaseModel):
    query: str

@router.post("/run/")
def run_query(sql_query: SQLQuery):
    try:
        import duckdb
        con = duckdb.connect(database=':memory:', read_only=False)
        result = con.execute(sql_query.query).fetchall()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}