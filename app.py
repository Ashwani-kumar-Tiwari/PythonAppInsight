from flask import Flask
app = Flask(__name__)
import logging

from opencensus.ext.azure.log_exporter import AzureLogHandler
from opencensus.ext.azure.trace_exporter import AzureExporter
from opencensus.trace import config_integration
from opencensus.trace.samplers import ProbabilitySampler
from opencensus.trace.tracer import Tracer

config_integration.trace_integrations(['logging'])
logger = logging.getLogger(__name__)

@app.route("/")
def home():
    handler = AzureLogHandler(connection_string='InstrumentationKey=580014a9-da36-4a6e-b9fd-b6e2744333fe;IngestionEndpoint=https://northeurope-2.in.applicationinsights.azure.com/;LiveEndpoint=https://northeurope.livediagnostics.monitor.azure.com/')
    handler.setFormatter(logging.Formatter('%(asctime)s %(traceId)s %(spanId)s %(message)s'))
    logger.addHandler(handler)

    tracer = Tracer(
        exporter=AzureExporter(connection_string='InstrumentationKey=580014a9-da36-4a6e-b9fd-b6e2744333fe;IngestionEndpoint=https://northeurope-2.in.applicationinsights.azure.com/;LiveEndpoint=https://northeurope.livediagnostics.monitor.azure.com/'),
        sampler=ProbabilitySampler(1.0)
    )

    logger.warning('Before the span')
    with tracer.span(name='Hello'):
        logger.warning('In the span')
    logger.warning('After the span')
    return "Hello, this is a sample Python Web App running on Flask Framework!!!"

if __name__ == "__main__":
    app.run()