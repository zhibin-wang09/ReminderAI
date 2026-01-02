from engine import database
from config import query_engine
from model import Transcription, Query

from fastapi import FastAPI
from fastapi.responses import StreamingResponse, Response
from opentelemetry._logs import set_logger_provider
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
import logging

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

@app.post("/transcriptions")
def store_transcription(transcription: Transcription) -> Response:
    try:
        logging.info(f"Storing transcription initiated")
        database.save_transcribed_recording(transcription.transcription)
    except Exception as e:
        return Response(status_code=500, content=f"Error storing transcription: {str(e)}")
    return Response(status_code=200, content="Transcription stored successfully.")

@app.post("/chat")
async def chat_stream(query: Query) -> StreamingResponse:
    def response_streamer(query):
        streaming_response = query_engine.query(query)
        for token in streaming_response.response_gen:
            yield token.encode("utf-8")
    logging.info(f"Chatting initiated")
    return StreamingResponse(response_streamer(query.query), media_type="text/plain")
