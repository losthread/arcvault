from ..database import conn
from ..schemas import SectionResponse

# return all the sections
def get_sections():
  # create a cursor to execute SQL
  cursor = conn.cursor()
  cursor.execute("SELECT section_id, name, description, slug, created_at FROM sections")

  # fetch query result as a list of tuples
  sections = cursor.fetchall()

  # convert list to SectionResponse pydantic object 
  response = list()
  for row in sections:
    section = SectionResponse(
      section_id = row[0],
      name = row[1],
      description = row[2],
      slug = row[3],
      created_at = row[4]
    )
    response.append(section)
  
  # close cursor
  cursor.close()

  # return json
  return response