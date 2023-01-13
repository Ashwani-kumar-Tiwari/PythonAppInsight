import logging

from opencensus.ext.azure.log_exporter import AzureLogHandler
from opencensus.ext.azure.trace_exporter import AzureExporter
from opencensus.trace import config_integration
from opencensus.trace.samplers import ProbabilitySampler
from opencensus.trace.tracer import Tracer

config_integration.trace_integrations(['logging'])

logger = logging.getLogger(__name__)

handler = AzureLogHandler(connection_string='InstrumentationKey=4497e9b3-381f-4070-9cb6-7dd666ca6ec4;IngestionEndpoint=https://centralus-0.in.applicationinsights.azure.com/;LiveEndpoint=https://centralus.livediagnostics.monitor.azure.com/')
handler.setFormatter(logging.Formatter('%(asctime)s %(traceId)s %(spanId)s %(message)s'))
logger.addHandler(handler)

tracer = Tracer(
    exporter=AzureExporter(connection_string='InstrumentationKey=4497e9b3-381f-4070-9cb6-7dd666ca6ec4;IngestionEndpoint=https://centralus-0.in.applicationinsights.azure.com/;LiveEndpoint=https://centralus.livediagnostics.monitor.azure.com/'),
    sampler=ProbabilitySampler(1.0)
)

logger.warning('Before the span')
with tracer.span(name='Hello'):
    logger.warning('In the span')
logger.warning('After the span')