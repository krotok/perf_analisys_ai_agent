class SlackReporter:

    def __init__(self, settings):
        self.webhook = settings.slack_webhook

    def send(self, service, analysis, fixes):
        message = f"""
        🔴 *Latency degradation detected*
        Service: {service}

        Root causes:
        {analysis}

        Suggested fixes:
        {fixes}
        """
        # POST to Slack webhook
