from engine import database
from config import query_engine, transcription_collection
from model import Reminder, Query

from fastapi import FastAPI
from fastapi.responses import StreamingResponse, Response
from opentelemetry._logs import set_logger_provider
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
import logging
import uuid

resource = Resource.create({"service.name": "reminder-ai-service"})
logger_provider = LoggerProvider(resource=resource)
set_logger_provider(logger_provider)

exporter = OTLPLogExporter(endpoint="http://localhost:4317", insecure=True)
logger_provider.add_log_record_processor(BatchLogRecordProcessor(exporter))

otel_handler = LoggingHandler(level=logging.INFO, logger_provider=logger_provider)
logging.getLogger().addHandler(otel_handler)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

app = FastAPI()
FastAPIInstrumentor.instrument_app(app)

@app.post("/reminder")
def store_reminder(reminder: Reminder) -> Response:
    try:
        doc_id: str = str(uuid.uuid4())
        logging.info(f"Storing reminder initiated for id: {doc_id}")
        database.save_transcribed_recording(doc_id, reminder.transcription)
    except Exception as e:
        return Response(status_code=500, content=f"Error storing reminder: {str(e)}")
    return Response(status_code=200, content=f"Reminder stored successfully for id: {doc_id}")

@app.post("/chat")
async def chat_stream(query: Query) -> StreamingResponse:
    def response_streamer(query):
        streaming_response = query_engine.query(query)
        for token in streaming_response.response_gen:
            yield token.encode("utf-8")
    logging.info(f"Chatting initiated")
    return StreamingResponse(response_streamer(query.query), media_type="text/plain")

@app.delete("/reminder/{doc_id}")
def delete_reminder(doc_id: str) -> Response:
    try:
        logging.info(f"Deletion initiated for id: {doc_id}")
        database.delete_transcribed_recording_by_id(doc_id)
    except Exception as e:
        return Response(status_code=500, content=f"Error deleting reminder: {str(e)}")
    return Response(status_code=200, content=f"Reminder deleted successfully for id: {doc_id}")

@app.delete("/reminders")
def clear_reminders() -> Response:
    try:
        logging.info(f"Clearing reminders collection")
        transcription_collection.delete(ids=transcription_collection.get()["ids"])
    except Exception as e:
        return Response(status_code=500, content=f"Error clearing ChromaDB: {str(e)}")
    return Response(status_code=200, content=f"ChromaDB cleared successfully")