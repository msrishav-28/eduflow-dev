"""
Optional monitoring and metrics collection for EduFlow
Uncomment and configure based on your monitoring solution
"""
import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)


# ============================================
# SENTRY ERROR TRACKING (Recommended)
# ============================================
def setup_sentry() -> None:
    """
    Set up Sentry error tracking
    Install: pip install sentry-sdk[fastapi]
    """
    sentry_dsn = os.environ.get('SENTRY_DSN')
    if not sentry_dsn:
        logger.info("Sentry not configured (SENTRY_DSN not set)")
        return
    
    try:
        import sentry_sdk
        from sentry_sdk.integrations.fastapi import FastApiIntegration
        from sentry_sdk.integrations.logging import LoggingIntegration
        
        # Configure logging integration
        logging_integration = LoggingIntegration(
            level=logging.INFO,        # Capture info and above as breadcrumbs
            event_level=logging.ERROR  # Send errors as events
        )
        
        sentry_sdk.init(
            dsn=sentry_dsn,
            integrations=[
                FastApiIntegration(),
                logging_integration,
            ],
            # Performance monitoring
            traces_sample_rate=float(os.environ.get('SENTRY_TRACES_SAMPLE_RATE', 0.1)),
            # Error sampling
            sample_rate=1.0,
            # Environment
            environment=os.environ.get('ENV', 'development'),
            # Release tracking
            release=os.environ.get('RELEASE_VERSION', 'unknown'),
        )
        logger.info("Sentry error tracking initialized")
    except ImportError:
        logger.warning("Sentry SDK not installed. Install with: pip install sentry-sdk[fastapi]")
    except Exception as e:
        logger.error(f"Failed to initialize Sentry: {str(e)}")


# ============================================
# PROMETHEUS METRICS
# ============================================
def setup_prometheus(app) -> None:
    """
    Set up Prometheus metrics
    Install: pip install prometheus-fastapi-instrumentator
    """
    try:
        from prometheus_fastapi_instrumentator import Instrumentator
        
        Instrumentator().instrument(app).expose(app)
        logger.info("Prometheus metrics initialized at /metrics")
    except ImportError:
        logger.info("Prometheus not configured. Install with: pip install prometheus-fastapi-instrumentator")
    except Exception as e:
        logger.error(f"Failed to initialize Prometheus: {str(e)}")


# ============================================
# NEW RELIC APM
# ============================================
def setup_newrelic() -> None:
    """
    Set up New Relic APM
    Install: pip install newrelic
    """
    license_key = os.environ.get('NEW_RELIC_LICENSE_KEY')
    if not license_key:
        logger.info("New Relic not configured")
        return
    
    try:
        import newrelic.agent
        
        config_file = os.environ.get('NEW_RELIC_CONFIG_FILE', 'newrelic.ini')
        if os.path.exists(config_file):
            newrelic.agent.initialize(config_file)
            logger.info("New Relic APM initialized")
        else:
            logger.warning(f"New Relic config file not found: {config_file}")
    except ImportError:
        logger.warning("New Relic agent not installed. Install with: pip install newrelic")
    except Exception as e:
        logger.error(f"Failed to initialize New Relic: {str(e)}")


# ============================================
# DATADOG APM
# ============================================
def setup_datadog() -> None:
    """
    Set up Datadog APM
    Install: pip install ddtrace
    Run with: ddtrace-run python server.py
    """
    if os.environ.get('DD_SERVICE'):
        logger.info("Datadog APM configured (use ddtrace-run to start)")
    else:
        logger.info("Datadog not configured")


# ============================================
# CUSTOM METRICS (Example)
# ============================================
class MetricsCollector:
    """Simple in-memory metrics collector"""
    
    def __init__(self):
        self.request_count = 0
        self.error_count = 0
        self.llm_request_count = 0
        self.llm_error_count = 0
    
    def increment_request(self):
        self.request_count += 1
    
    def increment_error(self):
        self.error_count += 1
    
    def increment_llm_request(self):
        self.llm_request_count += 1
    
    def increment_llm_error(self):
        self.llm_error_count += 1
    
    def get_metrics(self) -> dict:
        return {
            "total_requests": self.request_count,
            "total_errors": self.error_count,
            "llm_requests": self.llm_request_count,
            "llm_errors": self.llm_error_count,
            "error_rate": self.error_count / max(self.request_count, 1),
            "llm_error_rate": self.llm_error_count / max(self.llm_request_count, 1),
        }


# Global metrics instance
metrics = MetricsCollector()


# ============================================
# SETUP ALL MONITORING
# ============================================
def setup_monitoring(app) -> None:
    """Initialize all configured monitoring solutions"""
    logger.info("Setting up monitoring...")
    
    # Error tracking
    setup_sentry()
    
    # APM solutions
    setup_newrelic()
    setup_datadog()
    
    # Metrics
    setup_prometheus(app)
    
    logger.info("Monitoring setup complete")


# ============================================
# HEALTH METRICS ENDPOINT
# ============================================
def get_health_metrics() -> dict:
    """Get application health metrics"""
    import psutil
    import time
    
    try:
        # System metrics
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        return {
            "timestamp": time.time(),
            "cpu": {
                "percent": cpu_percent,
                "count": psutil.cpu_count(),
            },
            "memory": {
                "total": memory.total,
                "available": memory.available,
                "percent": memory.percent,
                "used": memory.used,
            },
            "disk": {
                "total": disk.total,
                "used": disk.used,
                "free": disk.free,
                "percent": disk.percent,
            },
            "application": metrics.get_metrics(),
        }
    except ImportError:
        logger.warning("psutil not installed. Install with: pip install psutil")
        return {"application": metrics.get_metrics()}
    except Exception as e:
        logger.error(f"Failed to get health metrics: {str(e)}")
        return {"error": str(e)}
