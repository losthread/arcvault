from ..db import conn
from ..schemas import ReportResponse
from .error_handler import handle_error

# create report
def create_report(post_id, reason):
  cursor = conn.cursor()
  try:
    cursor.execute(
      """
        INSERT INTO reports(post_id, user_id, reason, created_at)
        VALUES(%s, %s, %s, NOW())
        RETURNING report_id
      """,
      (post_id, 1, reason)
    )
    row = cursor.fetchone()
    conn.commit()
    cursor.close()
    return {"report_id": row[0]}
  
  except Exception as e:
    handle_error(e, cursor)

# get reports
def get_reports():
  cursor = conn.cursor()
  cursor.execute(
    """
      SELECT report_id, post_id, reason, created_at 
      FROM reports 
      WHERE user_id = %s
    """, 
    (1,)
  )
  reports = cursor.fetchall()
  cursor.close()
  
  response = list()
  for row in reports:
    report = ReportResponse(report_id=row[0],post_id=row[1], reason=row[2], created_at=row[3])

    response.append(report)
  
  return response