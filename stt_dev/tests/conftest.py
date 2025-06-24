import sys, types

# Provide stub modules for missing dependencies
sys.modules.setdefault('dotenv', types.SimpleNamespace(load_dotenv=lambda *a, **k: None))
sys.modules.setdefault('requests', types.ModuleType('requests'))
if not hasattr(sys.modules['requests'], 'post'):
    def _dummy_post(*a, **k):
        raise RuntimeError('requests.post not stubbed')
    sys.modules['requests'].post = _dummy_post
