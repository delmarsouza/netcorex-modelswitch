from netcorex_modelswitch.channels.telegram.adapter import TelegramAdapter
from netcorex_modelswitch.contracts.models import Complexity
from netcorex_modelswitch.intent.analyzer import IntentAnalyzer


def test_intent_marks_short_message_as_low_complexity():
    adapter = TelegramAdapter()
    analyzer = IntentAnalyzer()
    msg = adapter.normalize(user_id="u1", text="Oi")
    assessment = analyzer.assess(msg)
    assert assessment.complexity == Complexity.LOW
