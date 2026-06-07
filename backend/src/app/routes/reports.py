from fastapi import APIRouter
from ..schemas import ReportCreate
from ..crud import reports as r

router = APIRouter()

# create a report
@router.post('/reports')
async def create_report(report: ReportCreate) -> dict:
  return r.create_report(report.post_id, report.reason)

# get reports
@router.get('/reports')
async def get_reports() -> list:
  return r.get_reports()