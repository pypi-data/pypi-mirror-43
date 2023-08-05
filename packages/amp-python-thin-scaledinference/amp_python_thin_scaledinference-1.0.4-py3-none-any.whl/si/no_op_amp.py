import logging

from si import session


class NoOpAmp(object):
    def __init__(self, logger):
        self._logger = logger or logging.getLogger('amp').addHandler(logging.NullHandler())

    def __str__(self):
        return "<NoOp Amp>"

    @property
    def logger(self):
        return self._logger

    @logger.setter
    def logger(self, val):
        self._logger = val

    def session(self, **options):
        return NoOpSession(amp=self, **options)


class NoOpSession(object):
    def __init__(self, amp, **options):
        self._logger = options.get('logger', amp.logger)

    def __str__(self):
        return "<NoOpSession>"

    @property
    def logger(self):
        return self._logger

    @logger.setter
    def logger(self, val):
        self._logger = val

    def observe(self, name, properties, **options):
        logger = options.get('logger', self.logger)  # type: logging._loggerClass
        logger.warning('NoOp observe %s', name)
        return dict()

    def decide(self, decision_name, candidates, **options):
        logger = options.get('logger', self.logger)  # type: logging._loggerClass
        logger.warning('NoOp decide %s', decision_name)
        return {session.Session.DECISION_KEY: session.get_default_candidate(candidates),
                session.Session.FALLBACK_KEY: True, session.Session.REASON_KEY: "NoOp Session"}

    def decide_with_context(self, context_name, candidates, decision_name, properties, **options):
        logger = options.get('logger', self.logger)  # type: logging._loggerClass
        logger.warning('NoOp decide_with_context %s %s', context_name, decision_name)
        return {session.Session.DECISION_KEY: session.get_default_candidate(candidates),
                session.Session.FALLBACK_KEY: True, session.Session.REASON_KEY: "NoOp Session"}
