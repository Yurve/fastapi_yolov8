from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from serializers import Event
from ultralytics import YOLO
from PIL import Image

app = FastAPI() 

@app.post("/api/event/events")

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    error_response = jsonable_encoder({"detail": exc.detail})
    app.logger.error(error_response)
    return JSONResponse(content=error_response, status_code=exc.status_code)


async def create_event(event: Event):
    # try:
    #     event = Event(**request_body)
    #     if event.EventHeader is None:
    #          raise HTTPException(status_code=422, detail="EventHeader is required")
    # except ValidationError as e:
    #     raise HTTPException(status_code=422, detail=str(e))  
     
    if event.EventHeader is None:
        raise HTTPException(status_code=422, detail="EventHeader is required")
    
    model = YOLO("yolov8l.pt")

    try:
        userId = event.EventHeader.UserId
        cameraId = event.EventHeader.CameraId
        created = event.EventHeader.Created
        path = event.EventHeader.Path
        image = Image.open(path)

        results = model.predict(image)

        event_bodies = []
        for result in results:
            for bbox, cls in zip(result.boxes.xyxy, result.boxes.cls):
                left, top, right, bottom = bbox.tolist()
            event_bodies.append({
                'Label': cls.item(),
                'Left': left,
                'Top': top,
                'Right': right,
                'Bottom': bottom
            })

        _Event = {
            'EventHeader': {
                'UserId': userId,
                'CameraId': cameraId,
                'Created': created,
                'Path': path,
                'IsRequiredObjectDetection': False
            },
            'EventBodies': event_bodies,
        }

        image.close()
        event_dict = _Event.dict()
        return event_dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))






if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8888)