from netcorex_modelswitch.channels.telegram.adapter import TelegramAdapter
from netcorex_modelswitch.orchestrator.planner import ExecutionPlanner


def test_execution_planner_assigns_specialist_for_strategy():
    planner = ExecutionPlanner()
    adapter = TelegramAdapter()
    plan = planner.plan(adapter.normalize(user_id="u1", text="Preciso de uma estratégia de arquitetura para o MVP"))
    assert plan.specialists
    assert plan.routing.provider == "chatgpt"
