link = type('pardinalink', (), {})()
run = lambda f: f(link.backend) if hasattr(link, 'backend') else None
