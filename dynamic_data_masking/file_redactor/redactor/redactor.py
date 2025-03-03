from dynamic_data_masking.file_redactor.redactor.blackout_redaction import BlackoutRedaction

class RedactionStrategyFactory:
    @staticmethod
    def get_redaction_strategy(strategy_type="blackout"):
        strategies = {
            "blackout": BlackoutRedaction()
            # Future strategies: "blur": BlurRedaction(), "replace": ReplaceTextRedaction()
        }
        return strategies.get(strategy_type, BlackoutRedaction())