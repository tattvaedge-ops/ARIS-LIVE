try:
    planner_agent = None
except:
    planner_agent = None

def research_agent(x): return "Research module not available"
def creation_agent(x): return "Creation module not available"
def analyzer_agent(x): return "Analyzer module not available"
def executor_agent(x): return "Executor module not available"
def google_search(x): return "Search module not available"
def analyze_image(x): return "Image analysis not available"
def analyze_video(x): return "Video analysis not available"
def plan_task(x): return "DEFAULT"
def generate_scenes(x): return []
def build_video(x, y): return "Video module not available"

class ARISCoordinator:

    def __init__(self):
        print("ARIS Coordinator Initialized")

    def process_user_request(self, user_input):
        return self.coordinate_request(user_input)

    def coordinate_request(self, user_input, mode="general"):

        if not user_input or not user_input.strip():
            return "Please enter a valid request."

        print("Coordinator → Received request")

        text = user_input.lower()

        # -----------------------------
        # MULTIMODAL ANALYSIS
        # -----------------------------
        if "analyze image" in text:

            print("Coordinator → Multimodal Image Analysis")

            result = analyze_image(user_input)

            return result


        if "analyze video" in text:

            print("Coordinator → Multimodal Video Analysis")

            result = analyze_video(user_input)

            return result


        # -----------------------------
        # GOOGLE SEARCH
        # -----------------------------
        if "search" in text:

            print("Coordinator → Google Search")

            return google_search(user_input)


        # -----------------------------
        # AUTONOMOUS AGENT DECISION
        # -----------------------------
        task = plan_task(user_input)

        print("AGENT DECISION:", task)


        # -----------------------------
        # VIDEO CREATION PIPELINE
        # -----------------------------
        if task == "VIDEO_CREATION":

            print("\nCoordinator → Starting ARIS Video Pipeline\n")

            topic = user_input

            # 1️⃣ Generate scenes
            scenes = generate_scenes(topic)

            if not scenes:
                return "Scene generation failed."

            # 2️⃣ Extract image paths
            image_files = []

            for scene in scenes:

                img = scene.get("image_path")

                if img:
                    image_files.append(img)

            if not image_files:
                return "No scene images generated."

            # 3️⃣ Narration placeholder (future upgrade)
            narration_file = None

            # 4️⃣ Build video
            video_file = build_video(image_files, narration_file)

            return f"""
🎬 ARIS VIDEO CREATED

Topic:
{topic}

Scenes Generated:
{len(image_files)}

Video File:
{video_file}
"""


        # -----------------------------
        # IMAGE CREATION
        # -----------------------------
        elif task == "IMAGE_CREATION":

            print("Coordinator → Routing to Image Creation")

            return creation_agent(user_input)


        # -----------------------------
        # RESEARCH
        # -----------------------------
        elif task == "RESEARCH":

            print("Coordinator → Routing to Research Agent")

            result = research_agent(user_input)

            return f"""
⚙️ ARIS INTELLIGENCE ENGINE

Analyzing request...
Activating Research Agents...
Generating Intelligence Report...

{result}
"""


        # -----------------------------
        # ANALYSIS
        # -----------------------------
        elif task == "ANALYSIS":

            print("Coordinator → Routing to Analyzer Agent")

            return analyzer_agent(user_input)


        # -----------------------------
        # PLANNING
        # -----------------------------
        elif task == "PLANNER":
            return "Planner module temporarily disabled"


        # -----------------------------
        # DEFAULT EXECUTION
        # -----------------------------
        else:

            print("Coordinator → Routing to Executor")

            return executor_agent(user_input)


    # ---------------------------------------------------
    # LEGACY INTENT DETECTION (kept as fallback)
    # ---------------------------------------------------

    def detect_intent(self, user_input):

        from aris_brain import ask_ai

        prompt = f"""
Classify the user request into ONE category.

Categories:
planner
research
creator
analysis
chat

User request:
{user_input}

Respond with ONLY the category name.
"""

        try:

            intent = ask_ai(prompt).strip().lower()

            allowed = ["planner", "research", "creator", "analysis", "chat"]

            if intent in allowed:
                return intent

        except Exception:
            pass

        return "chat"