from unittest.mock import patch

from netcorex_modelswitch.cli.run import main


@patch("sys.argv", ["run", "--message", "Oi", "--json"])
def test_cli_json_output(capsys):
    with patch("netcorex_modelswitch.cli.run.ExecutionRunner.execute_message") as execute_message:
        from netcorex_modelswitch.contracts.models import (
            Complexity,
            ExecutionPlan,
            IntentAssessment,
            ModelExecutionResult,
            RiskLevel,
            RoutingDecision,
        )

        plan = ExecutionPlan(
            coordinator="coordinator",
            specialists=[],
            routing=RoutingDecision(provider="local", model="ollama-local-default", reason="test"),
            assessment=IntentAssessment(domain="general", complexity=Complexity.LOW, risk=RiskLevel.LOW),
        )
        result = ModelExecutionResult(content="ok", provider="ollama", model="qwen2.5:14b")
        execute_message.return_value = (plan, result)

        main()
        output = capsys.readouterr().out
        assert '"provider": "local"' in output
        assert '"content": "ok"' in output
