from aris_video_script import generate_video_script
from aris_image_engine import generate_image
from aris_voice_engine import generate_voice
from aris_video_builder import build_video
from aris_scene_planner import generate_scenes
from aris_visual_engine import enhance_visual_prompt
from aris_visual_mapper import map_visual_elements
from aris_concept_engine import generate_concept_structure
from aris_knowledge_graph import generate_knowledge_graph
from aris_overlay_engine import generate_overlays
from aris_self_improvement_engine import store_video_data, evaluate_video
from aris_cinematic_story_engine import generate_story_arc
from aris_visual_consistency_engine import select_visual_style, apply_visual_consistency
from aris_camera_engine import generate_camera_plan, apply_camera_style
from aris_scene_physics_engine import generate_physics_scene
from aris_world_simulation_engine import generate_world_context, apply_world_simulation
from aris_dynamic_animation_engine import apply_animation
from aris_scene_composition_engine import apply_scene_composition
from aris_motion_diffusion_engine import generate_motion_video

# NEW ENGINES
from aris_visual_tagging_engine import ARISVisualTaggingEngine
from aris_scene_timing_engine import ARISSceneTimingEngine
from aris_cinematic_editing_engine import ARISCinematicEditingEngine
from aris_clip_motion_engine import ARISClipMotionEngine
from aris_video_render_engine import ARISVideoRenderEngine


def clean_topic(user_input):

    text = user_input.lower()

    text = text.replace("create video about", "")
    text = text.replace("make video about", "")
    text = text.replace("generate video about", "")
    text = text.replace("video about", "")

    return text.strip()


def create_video(user_input):

    print("ARIS VIDEO ENGINE STARTED")

    topic = clean_topic(user_input)

    print("Detected topic:", topic)

    # -----------------------------
    # INITIALIZE NEW ENGINES
    # -----------------------------
    tagging_engine = ARISVisualTaggingEngine()
    timing_engine = ARISSceneTimingEngine()
    editing_engine = ARISCinematicEditingEngine()
    clip_engine = ARISClipMotionEngine()
    render_engine = ARISVideoRenderEngine()

    # -----------------------------
    # KNOWLEDGE GRAPH
    # -----------------------------
    knowledge_graph = generate_knowledge_graph(topic)
    print("KNOWLEDGE GRAPH GENERATED")

    # -----------------------------
    # CONCEPT STRUCTURE
    # -----------------------------
    concept = generate_concept_structure(topic)
    print("CONCEPT STRUCTURE GENERATED")

    # -----------------------------
    # CINEMATIC STORY ARC
    # -----------------------------
    story_arc = generate_story_arc(topic)
    print("CINEMATIC STORY ARC GENERATED")

    # -----------------------------
    # EDUCATIONAL OVERLAYS
    # -----------------------------
    overlays = generate_overlays(topic)
    print("EDUCATIONAL OVERLAYS GENERATED")

    # -----------------------------
    # VISUAL STYLE
    # -----------------------------
    visual_profile = select_visual_style()
    print("VISUAL STYLE LOCKED:", visual_profile)

    # -----------------------------
    # SCRIPT GENERATION
    # -----------------------------
    script = generate_video_script(concept)
    print("VIDEO SCRIPT GENERATED")

    # -----------------------------
    # SCENE PLANNING
    # -----------------------------
    scene_data = generate_scenes(topic)

    print("SCENE PLAN GENERATED")

    # -----------------------------
    # EXTRACT VISUAL PROMPTS
    # -----------------------------
    image_prompts = []

    for scene in scene_data:

        prompt = scene.get("visual_prompt")

        if prompt:
            image_prompts.append(prompt)

    if not image_prompts:

        image_prompts = [
            f"cinematic introduction of {topic}",
            f"visual explanation of {topic}",
            f"real world example of {topic}",
            f"close up demonstration of {topic}",
            f"advanced visualization of {topic}",
            f"cinematic ending scene about {topic}"
        ]

    # -----------------------------
    # SCENE STRUCTURE
    # -----------------------------
    scenes = []

    for prompt in image_prompts:

        scene = {
            "description": prompt,
            "narration": script
        }

        tags = tagging_engine.generate_tags(scene)

        scene["visual_tags"] = tags

        scenes.append(scene)

    # -----------------------------
    # TIMELINE GENERATION
    # -----------------------------
    timeline = timing_engine.generate_scene_timeline(scenes)

    # -----------------------------
    # CINEMATIC EDITING
    # -----------------------------
    edited_scenes = editing_engine.assign_transitions(timeline)

    # -----------------------------
    # WORLD SIMULATION
    # -----------------------------
    world = generate_world_context(topic)
    print("WORLD SIMULATION GENERATED")

    # -----------------------------
    # CAMERA PLAN
    # -----------------------------
    camera_plan = generate_camera_plan(len(edited_scenes))
    print("CAMERA PLAN GENERATED")

    scene_files = []

    USE_VIDEO_MODE = True

    # -----------------------------
    # GENERATION LOOP
    # -----------------------------
    for i, scene in enumerate(edited_scenes):

        base_prompt = scene["description"]

        mapped_prompt = map_visual_elements(topic, base_prompt)

        world_prompt = apply_world_simulation(mapped_prompt, world)

        physics_prompt = generate_physics_scene(topic, world_prompt)

        animated_prompt = apply_animation(physics_prompt, topic)

        composition_prompt = apply_scene_composition(animated_prompt, topic)

        enhanced_prompt = enhance_visual_prompt(topic, composition_prompt)

        consistent_prompt = apply_visual_consistency(enhanced_prompt, visual_profile)

        final_prompt = apply_camera_style(consistent_prompt, camera_plan[i])

        print("Generating scene:", final_prompt)

        # -----------------------------
        # VIDEO GENERATION
        # -----------------------------
        if USE_VIDEO_MODE:

            clip = generate_motion_video(final_prompt)

            if clip:
                scene_files.append(clip)
                continue

            print("Motion generation failed, fallback to image")

        # -----------------------------
        # IMAGE FALLBACK
        # -----------------------------
        img = generate_image(final_prompt)

        if img:

            duration = scene["duration"]

            clip = clip_engine.create_motion_clip(img, duration, i)

            scene_files.append(clip)

    # -----------------------------
    # SAFETY CHECK
    # -----------------------------
    if not scene_files:

        print("ERROR: No scenes generated")
        return "ARIS ERROR: Scene generation failed."

    # -----------------------------
    # VOICE GENERATION
    # -----------------------------
    narration = generate_voice(script)

    print("Voice narration generated")

    # -----------------------------
    # FINAL RENDER
    # -----------------------------
    print("Rendering cinematic video")

    video_file = render_engine.render_final_video(scene_files)

    # -----------------------------
    # SELF IMPROVEMENT
    # -----------------------------
    store_video_data(topic, image_prompts, video_file)

    review = evaluate_video(topic, image_prompts)

    print("ARIS SELF REVIEW")
    print(review)

    return f"""
ARIS CINEMATIC VIDEO GENERATED

Topic: {topic}

Scenes Created: {len(scene_files)}

Final Video File:
{video_file}
"""