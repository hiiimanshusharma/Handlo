import uvicorn
import traceback
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.semconv.resource import ResourceAttributes
from context_ret import ContextRetriever
from caption import Caption
from hashtag_rag.query import HashtagRetriever


resource = Resource(attributes={
    ResourceAttributes.SERVICE_NAME: "fastapi-users"
})

jaeger_exporter = JaegerExporter(
    agent_host_name="localhost",
    agent_port=6831,
)

provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(jaeger_exporter)
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

tracer = trace.get_tracer(__name__)

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


FastAPIInstrumentor.instrument_app(app)

@app.post("/get-context")
async def get_context(response: dict = Body(...)):
    with tracer.start_as_current_span("get_context"):
        try:
            img_bytes = response['img_bytes']
            context_retriever = ContextRetriever()
            context = context_retriever.get_context(img_bytes)
            return {"context": context}
        except Exception as e:
            print(traceback.format_exc())
            return {"error": str(e)}
        
@app.post("/get-caption")
async def get_caption(response: dict = Body(...)):
    with tracer.start_as_current_span("get_caption"):
        try:
            context = response['context']
            mood = response['mood']
            caption = Caption(context, mood)
            captions = caption.generate_captions()
            return {"captions": captions}
        except Exception as e:
            print(traceback.format_exc())
            return {"error": str(e)}
        

@app.post("/get-hashtags")
async def get_hashtags(response: dict = Body(...)):
    with tracer.start_as_current_span("get_hashtags"):
        try:
            sentence = response['sentence']
            hashtag_retriever = HashtagRetriever()
            hashtags = hashtag_retriever.get_hashtags(sentence)
            return {"hashtags": hashtags}
        except Exception as e:
            print(traceback.format_exc())
            return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

