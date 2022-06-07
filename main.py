from fastapi import FastAPI
from fastapi.responses import JSONResponse
from course.config.database import recreate_database
from course.routers import authentication, users, courses, purchase

recreate_database()
app = FastAPI()
app.include_router(authentication.router)
app.include_router(users.router)
app.include_router(courses.router)
app.include_router(purchase.router)


@app.exception_handler(Exception)
async def exception_handler(request, exc):
    json_resp = get_default_error_response()
    return json_resp


def get_default_error_response(status_code=500, message="Internal Server Error"):
    return JSONResponse(status_code=status_code, content={
        "status_code": status_code,
        "message": message
    })
