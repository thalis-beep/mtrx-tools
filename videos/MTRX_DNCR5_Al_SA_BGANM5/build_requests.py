"""Builds Veo 3.1 Lite batch requests (with eyeline direction) for the main video: Hook 1 + script body."""
import json, sys

MOM_V = "Voice: a warm, slightly raspy 62-year-old American woman, natural conversational General American accent"
DAU_V = "Voice: a 32-year-old American woman, natural conversational General American accent"
DRAMA = ("Naturalistic, understated film acting, like a scene from a dramatic feature film, not a commercial. "
         "Nobody ever looks at the camera or speaks to the camera.")
END = "Lips perfectly synced to the words. No music, no subtitles."

# (shot, start_frame_job_id, duration, prompt)
SHOTS = [
 ("01", "1ce821d5-90d2-439a-b268-849b11f566df", 6,
  "Evening, warm sconce light. The older woman climbs the carpeted stairs carrying the laundry basket, away from camera. Two steps later her foot catches the edge of a step and slips; she lurches and grabs the wooden handrail hard to catch herself, and the laundry basket falls from her hip and tumbles down the stairs toward camera, towels spilling out. She freezes, clinging to the rail. Static low angle, subtle handheld shake on impact. Audio: footsteps on carpet, a sharp gasp, the loud clatter of the plastic basket bouncing down the stairs, room tone. No dialogue, no music, no subtitles."),
 ("02", "36000151-7536-4249-813f-3f2c3cf33c7e", 4,
  f"Evening. The shaken older woman clutches the handrail, catches her breath, her eyes fixed down on the spilled laundry on the steps, and mutters under her breath to herself, not to anyone: \"These stairs are getting harder lately...\" {MOM_V}, soft, low, tired. Slow subtle push-in. Shaky breath, room tone. {DRAMA} {END}"),
 ("03", "6ebe387e-c1fd-491d-8b6a-f8083c94d9ee", 4,
  f"Evening. The young woman with the dish towel on her shoulder hurries out of the kitchen toward the stairs, her eyes locked up on her mother on the staircase off-frame to the right, and calls out: \"Mom! Are you okay?\" {DAU_V}, urgent and scared. Handheld follow. Quick footsteps on hardwood. {DRAMA} {END}"),
 ("04", "54746672-8672-4671-bff7-0f0b1e1a7a9d", 4,
  f"Evening, over the daughter's shoulder. The older woman on the stairs looks down at her daughter in the foreground, waves her hand dismissively with a forced, embarrassed smile and says to her: \"I'm fine, I'm fine. Just lost my footing.\" {MOM_V}, light and dismissive. Her eyeline stays on her daughter's face in the foreground. The daughter stays still, back to camera. Static, subtle handheld. {DRAMA} {END}"),
 ("05", "fcc3e1a0-aee5-481f-95e3-dc981812cafa", 4,
  f"Evening, framed through the stair balusters. The young woman keeps looking up at her mother off-frame above, unconvinced; a beat, her brows tighten, and she asks her softly: \"...Are you sure?\" {DAU_V}, quiet and worried. Her eyeline stays up toward her mother, off-frame. Very slow push-in. {DRAMA} {END}"),
 ("11", "87d8806b-fa3c-4a09-bbc7-21676b17ffa1", 6,
  f"Living room, late afternoon. The daughter, her hand on her mother's knee, leans in toward her mother and looks into her mother's eyes, gentle but serious: \"Mom, I need you to be honest with me. What's going on with you lately?\" {DAU_V}. The mother keeps her eyes lowered, avoiding her daughter's gaze. The two women only look at each other. Slow push-in. Quiet room tone. {DRAMA} {END}"),
 ("12", "b406c71f-2e9f-4207-89ba-c27a77f8da75", 6,
  f"The mother on the sofa keeps her eyes down on her clasped hands, then glances briefly toward her daughter sitting off-frame to the right, searching for words, and admits: \"I don't know how to explain it. I just feel weak. And my mind isn't sharp like it used to be.\" {MOM_V}, vulnerable, hesitant pauses. Static, subtle handheld. {DRAMA} {END}"),
 ("13", "fbab2f9a-456a-4e07-a3cc-3b96149cccac", 8,
  f"Close-up. The mother touches her temple, eyes glassy, gazing off to the side toward her daughter off-frame, lost and foggy: \"I feel foggy, slow, like I'm half a step behind everything. It's like I'm not really myself anymore.\" {MOM_V}, voice cracking slightly. Very slow push-in. {DRAMA} {END}"),
 ("14", "c97918d6-9108-4e31-b066-74a54d334e45", 4,
  f"The daughter on the sofa looks at her mother sitting off-frame to the left, worried and a little hurt, eyes wet: \"Why didn't you tell me?\" {DAU_V}, soft, hurt. Her eyeline stays on her mother, off-frame left. Static. {DRAMA} {END}"),
 ("15", "1501ba36-9528-43eb-b755-a9e351727def", 6,
  f"Tight close-up, a tear on the mother's cheek, chin trembling. She looks at her daughter off-frame to the right, with pride and fear: \"I didn't want you to worry. I didn't want to be the mom you have to take care of.\" {MOM_V}, emotional, near tears. Very slow push-in. {DRAMA} {END}"),
 ("16", "2023ca45-ffa5-470e-82db-bacd9f16578d", 6,
  f"The daughter looks at her mother, whose shoulder is in the foreground on the right, and softens into a warm, reassuring small smile, reaching for her hand: \"Mom, please. If you'd told me sooner, you could've been feeling so much better by now.\" {DAU_V}, gentle, mood lifting. Her eyes stay on her mother. Static. {DRAMA} {END}"),
 ("17", "7390c16f-fd92-4ec4-a847-7b9287615865", 4,
  f"The mother wipes a tear and lifts her eyes to her daughter off-frame to the right, a flicker of hope: \"What do you mean?\" {MOM_V}, curious, hopeful. Static. {DRAMA} {END}"),
 ("18", "973fed88-8207-4e74-815f-f43c207d8ab6", 8,
  f"Two-shot on the sofa. The daughter turns to her mother, looks at her, and hands her the Nectar stick pack, label to camera, steady and readable: \"Try this. It's Nectar Creatine. You're going to take one of these every morning with a glass of water.\" {DAU_V}, warm, matter-of-fact. The mother takes it and looks at it. The two women only look at each other and the packet. Static. The packet design never changes. {DRAMA} {END}"),
 ("19", "40294d73-0e35-4475-860c-6336aa78eb68", 4,
  f"The mother peers at the stick pack in her hand, label to camera, then glances up at her daughter off-frame to the right with a skeptical frown: \"Creatine? Why on earth would I take creatine?\" {MOM_V}, skeptical, half-amused. Static. The packet design never changes. {DRAMA} {END}"),
 ("20a", "c980b415-679b-4fee-bd2a-61935e82e3d3", 8,
  f"The daughter faces her mother, whose shoulder is in the foreground on the right, and explains patiently to her, gesturing gently: \"Because after forty, your body runs low on it, and creatine is what your cells use to make ATP.\" {DAU_V}, clear, caring. Her eyes stay on her mother. Static. {DRAMA} {END}"),
 ("20b", "c980b415-679b-4fee-bd2a-61935e82e3d3", 8,
  f"The daughter keeps explaining earnestly to her mother, whose shoulder is in the foreground on the right: \"It's literally the fuel your muscles and your brain run on. Women barely have any to begin with, so you need to get your levels back up.\" {DAU_V}. Her eyes stay on her mother. Static. {DRAMA} {END}"),
 ("21", "c7c37fc3-df4a-4cbb-9f94-77650a2ed0e6", 8,
  f"The mother leans back on the sofa, arms crossed, looking at her daughter off-frame to the right, doubtful: \"I don't know, honey. Every mom I know has told me creatine's done nothing for them. They just get bloated and give up after a week.\" {MOM_V}, skeptical, grounded. Static. {DRAMA} {END}"),
 ("22a", "f34e0635-4ea4-4206-9f6d-ce9cc32f6bcc", 8,
  f"The daughter, holding up the silver Nectar pouch steady with the label toward camera, keeps her head and eyes turned toward her mother sitting off-frame to the right and smiles reassuringly at her: \"Because they're not taking good quality stuff, Mom. Most creatine is packed with artificial fillers your body can't absorb.\" {DAU_V}, warm, confident. She talks to her mother, never to the lens. The pouch design never changes. {DRAMA} {END}"),
 ("22b", "f34e0635-4ea4-4206-9f6d-ce9cc32f6bcc", 8,
  f"The daughter, holding up the silver Nectar pouch with the label toward camera, keeps her eyes on her mother off-frame to the right, upbeat and sure: \"Nectar is clean. Zero sugar, zero calories, non-GMO, plant-based, and keto and paleo friendly.\" {DAU_V}. She talks to her mother, never to the lens. The pouch design never changes. {DRAMA} {END}"),
 ("23", "e26ce6fe-fb55-41eb-aa25-7fbf8d8c67e4", 4,
  "Product hero shot: very slow push-in on the Nectar pouch and stick packs on the coffee table, soft lamp light. The products stay perfectly still and unchanged. Audio: soft room tone only. No dialogue, no music, no subtitles."),
 ("24", "508025ce-3e52-403c-a2b4-6088ab15b952", 4,
  f"The mother looks at her daughter, whose shoulder is in the foreground on the left, and gives a small, unsure nod with a faint smile: \"...Alright. I'll give it a shot.\" {MOM_V}, hesitant, willing. Her eyes stay on her daughter. Static. {DRAMA} {END}"),
 ("25", "25f6422b-d129-4be1-8a86-a176f08c40ec", 8,
  f"Golden-hour mountain trail. The mother strides confidently uphill, glowing, and turns her head back over her shoulder to talk to her daughter walking behind her: \"I feel like I got twenty years back, honey. I'm stronger, my head is clear, I wake up actually ready for the day.\" {MOM_V}, bright, energetic, a little breathless. The daughter smiles at her. Handheld tracking backward. Birds, wind, footsteps on gravel. {DRAMA} {END}"),
 ("26", "8c19c0a5-0651-4319-8651-d3b41f47f96d", 4,
  f"The daughter watches her mother off-frame to the right, happy and relieved, eyes shining: \"I can see it. You're you again.\" {DAU_V}, warm, emotional. Her eyes stay on her mother. Gentle breeze. {DRAMA} {END}"),
 ("27", "d5667c46-3bd5-4507-9e3e-5fcf8cd64614", 8,
  f"At the summit, the mother faces her daughter, whose shoulder is in the foreground on the right, grateful tears, trembling smile: \"I can't thank you enough for not letting me just give up. I almost accepted that this was the rest of my life.\" {MOM_V}, heartfelt, emotional. Her eyes stay on her daughter. Slow push-in. Wind. {DRAMA} {END}"),
 ("28", "b3b01404-7eb2-452c-9e50-cda9a00af438", 6,
  "The mother and daughter hug tightly at the summit; the camera slowly pulls back and rises to reveal the vast golden valley and mountain ridgelines. Audio: wind, distant birds. No dialogue, no music, no subtitles."),
]

def request(i, shot, img, dur, prompt):
    return {"index": i, "params": {
        "model": "veo3_1_lite", "generate_audio": True, "aspect_ratio": "9:16", "duration": dur,
        "declined_preset_id": "24bae836-2c4a-48e0-89b6-49fcc0b21612",
        "medias": [{"role": "start_image", "value": img}],
        "prompt": "Photorealistic cinematic drama. " + prompt}}

if __name__ == "__main__":
    want = set(sys.argv[1:])
    reqs = [request(i, *s) for i, s in enumerate(SHOTS) if not want or s[0] in want]
    print(json.dumps(reqs))
    print(f"# clips={len(reqs)} seconds={sum(r['params']['duration'] for r in reqs)}", file=sys.stderr)
