class SuggestionEngine:

    def generate(self, message, mode):

        msg = message.lower()

        # ---------- STUDY ----------
        if mode == "STUDY":
            return [
                "Generate visual diagram",
                "Create revision notes",
                "Make practice questions"
            ]

        # ---------- BUSINESS ----------
        if mode == "BUSINESS":
            return [
                "Create execution roadmap",
                "Run SWOT analysis",
                "Estimate revenue model"
            ]

        # ---------- LIFE ----------
        if mode == "LIFE":
            return [
                "Create 30-day action plan",
                "Build decision matrix",
                "Define next priorities"
            ]

        # ---------- CREATIVE ----------
        if mode == "CREATIVE":
            return [
                "Convert into presentation",
                "Improve writing tone",
                "Create structured outline"
            ]

        # ---------- RESEARCH ----------
        if mode == "RESEARCH":
            return [
                "Generate comparison table",
                "Summarize key insights",
                "Create research framework"
            ]

        return []