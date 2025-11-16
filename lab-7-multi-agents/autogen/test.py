# test_available_agents.py
import autogen_agentchat
import pkgutil

print("Searching for available Agent classes...")

for importer, modname, ispkg in pkgutil.walk_packages(autogen_agentchat.__path__, prefix='autogen_agentchat.'):
    try:
        module = __import__(modname, fromlist=[''])
        for item in dir(module):
            if 'Agent' in item and not item.startswith('_'):
                print(f"Found: {item} in {modname}")
                # Check if it has llm_config parameter
                try:
                    import inspect
                    sig = inspect.signature(getattr(module, item).__init__)
                    params = list(sig.parameters.keys())
                    if 'llm_config' in params:
                        print(f"  ✓ Has llm_config: {params}")
                    else:
                        print(f"  ✗ No llm_config: {params}")
                except:
                    pass
    except:
        pass